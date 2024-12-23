import os
import json
import pytz
import requests

from lxml import html
from requests import Response
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional


class TimeConverter:
    """Utility class for handling timestamp conversions."""
    
    @staticmethod
    def convert_unix_timestamp(timestamp: int) -> tuple[str, str]:
        """
        Convert Unix timestamp to local time in Asia/Kolkata timezone.
        
        Args:
            timestamp (int): Unix timestamp
            
        Returns:
            tuple: (formatted_time, formatted_date)
                - formatted_time: string in format "dd Month YYYY HH:MM AM/PM Day"
                - formatted_date: string in format "YYYY-MM-DD"
        """
        dt_server = datetime.fromtimestamp(timestamp, tz=pytz.timezone('UTC'))
        dt_server -= timedelta(days=1)
        dt_local = dt_server.astimezone(pytz.timezone('Asia/Kolkata'))
        
        formatted_time = dt_local.strftime("%d %B %Y %I:%M %p %A")
        formatted_date = dt_local.strftime("%Y-%m-%d")
        
        return formatted_time, formatted_date


class InstaPost:
    """Class to handle Instagram post/reel downloading operations."""
    
    def __init__(self, media_id: Optional[str] = ''):
        """
            Initialize the InstaPost downloader.
            
            Args:
                media_id (Optional[str]): Instagram post or reel url/id to fetch stories from
        """
        self._reel_id = None
        self.reel_id = media_id
        self.cookies = {}
        
        self.username = 'demos'
        self.items = {}
        self.media_list = []
        
        self.session = requests.Session()
        self.folder_path = '.'
    
    @property
    def reel_id(self):
        """Get the reel_id."""
        return self._reel_id
    
    @reel_id.setter
    def reel_id(self, media_id):
        """
        Set the reel_id and call get_media_slug.
        
        Args:
            media_id (str): Instagram post or reel url/id to fetch stories from.
        """
        self._reel_id = self.get_media_slug(media_id)
    
    def get_media_slug(self, media_id: str) -> str:
        """
            Extract media slug from post/reel url.
            
            Args:
                media_id (str): Instagram post or reel url/id to fetch stories from
            
            Returns:
                str: Media slug extracted from url
        """
        
        return media_id.split('?')[0].strip('/').split('/')[-1].strip()
    
    def print(self, check: Optional[bool] = False) -> None:
        """
            Print the status of the post download operation.
            
            Args:
                check Optional[bool]: The check to print. If check is not empty, it indicates success; otherwise, failure.
        """
        if check:
            print(f'Post downloaded successfully at {self.folder_path}/post/{self.username}')
        else:
            print("Post not found or try again....")
    
    def media_download(self) -> Dict:
        """
            main function to download post or reel
            
            Returns:
                Dict: username with all info about post or reel
        """
        if not self.validate_inputs():
            print("post id is missing !!!")
            return {}
        
        response = self.make_initial_request()
        if not response:
            self.print()
            return {}
        
        json_data = self.make_second_request(response)
        if not json_data:
            self.print()
            return {}
        
        media_data = self.get_media(json_data)
        
        if not media_data['Media Data']:
            self.print()
            return {}
        
        with open(f'{self.folder_path}/post/{self.username}/{self.reel_id}.json', 'w') as f:
            json.dump({self.username: media_data}, f)
        
        self.print(True)
        return {self.username: media_data}
    
    def validate_inputs(self) -> bool:
        """
            Validate input data.
            
            Returns:
                bool: True if valid, False otherwise
        """
        return bool(self.reel_id)
    
    def make_initial_request(self) -> Response | bool:
        """
            Make initial request to get reel/post information.
            
            Returns:
                Response | bool: Response object if successful
        """
        try:
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'en-US,en;q=0.9',
                'priority': 'u=0, i',
                'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            }
            
            response = self.session.get(f'https://www.instagram.com/p/{self.reel_id}/', headers=headers)
            
            try:
                con = html.fromstring(response.text)
                pk = con.xpath('//meta[@property="instapp:owner_user_id"]/@content')[0]
            except:
                pk = ''
            
            return response if pk else None
        
        except:
            return None
    
    def make_second_request(self, response) -> Dict:
        """
            Make Second request to get reel/post json data.
            
            Args:
                response: Initial response containing necessary info
            
            Returns:
                Tuple[Dict]: Json object if successful
        """
        try:
            con = html.fromstring(response.text)
            try:
                self.username = f"""{con.xpath('//meta[@name="twitter:title"]/@content')[0]}""".split(')')[0].split('@')[1]
            except:
                pass
            
            headers, data = self.set_parameters(response)
            
            session = requests.Session()
            session.cookies.update(self.cookies)
            
            response = session.post('https://www.instagram.com/graphql/query', cookies=self.cookies, headers=headers, data=data)
            
            try:
                self.items = response.json()['data']['xdt_shortcode_media']
            except:
                pass
            try:
                self.media_list = [nodes['node'] for nodes in self.items['edge_sidecar_to_children']['edges']]
            except:
                self.media_list = [self.items] if self.items else []
            
            return response.json() if self.media_list else {}
        
        except:
            return {}
    
    def set_parameters(self, response) -> Tuple[Dict, Dict]:
        """
            Prepare headers and data for GraphQL request.
            
            Args:
                response: Initial response containing necessary tokens
            
            Returns:
                Tuple[Dict, Dict]: Headers and data for GraphQL request
        """
        try:
            csrf_token = response.text.split('csrf_token\\":\\"')[1].split('\\')[0]
        except:
            try:
                csrf_token = response.text.split('csrf_token":"')[1].split('"')[0]
            except:
                csrf_token = ''
        try:
            main_value = response.text.split('e2e_config')[0].split('country_code')[1]
        except:
            try:
                main_value = response.text.split('e2e_config')[0]
            except:
                main_value = ''
        try:
            val1 = main_value.split('machine_id')[1].split(':')[1].split(',')[0].replace('"', '')
        except:
            val1 = ''
        try:
            val2 = main_value.split('device_id')[1].split(':')[1].split(',')[0].replace('"', '')
        except:
            val2 = ''
        try:
            version = response.text.split('"versioningID"')[1].split(':')[1].split('}')[0].replace('"', '').strip()
        except:
            version = ''
        try:
            lsd = response.text.split('lsd"')[1].split(':')[1].split(',')[0].replace('"', '').strip()
        except:
            lsd = ''
        try:
            app = response.text.split('"app_id"')[1].split(':')[1].split(',')[0].replace('"', '').strip()
        except:
            app = ''
        try:
            __hsi = response.text.split('hsi"')[1].split(':')[1].split(',')[0].replace('"', '').strip()
        except:
            __hsi = ''
        try:
            __spin_r = response.text.split('__spin_r')[1].split(':')[1].split(',')[0].replace('"', '').strip()
        except:
            __spin_r = ''
        try:
            __spin_b = response.text.split('__spin_b')[1].split(':')[1].split(',')[0].replace('"', '').strip()
        except:
            __spin_b = ''
        try:
            __spin_t = response.text.split('__spin_t')[1].split(':')[1].split(',')[0].replace('"', '').strip()
        except:
            __spin_t = ''
        
        self.cookies = {
            'csrftoken': csrf_token,
            'datr': val1,
            'ig_did': val2,
            'ps_l': '1',
            'ps_n': '1',
            'wd': '1536x266',
            'dpr': '1.25',
            'mid': 'Z0JNPgALAAGTpsApPC50thMsjIWP',
            'ig_nrcb': '1',
        }
        
        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.instagram.com',
            'priority': 'u=1, i',
            'referer': f'https://www.instagram.com/p/{self.reel_id}/',
            'sec-ch-prefers-color-scheme': 'dark',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-full-version-list': '"Google Chrome";v="131.0.6778.86", "Chromium";v="131.0.6778.86", "Not_A Brand";v="24.0.0.0"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"10.0.0"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'x-asbd-id': '129477',
            'x-bloks-version-id': version,
            'x-csrftoken': f'{self.cookies["csrftoken"]}',
            'x-fb-friendly-name': 'PolarisPostActionLoadPostQueryQuery',
            'x-fb-lsd': lsd,
            'x-ig-app-id': app,
        }
        
        data = {
            'av': '0',
            '__d': 'www',
            '__user': '0',
            '__a': '1',
            '__req': 'c',
            '__hs': '20050.HYP:instagram_web_pkg.2.1..0.0',
            'dpr': '1',
            '__ccg': 'MODERATE',
            '__rev': '1018449779',
            '__s': '86hlha:c7l9r7:089wr2',
            '__hsi': __hsi,
            '__dyn': '7xeUjG1mxu1syUbFp41twpUnwgU7SbzEdF8aUco2qwJw5ux609vCwjE1EE2Cw8G11wBz81s8hwGxu786a3a1YwBgao6C0Mo2swtUd8-U2zxe2GewGw9a361qw8Xxm16wa-0nK3qazo7u3C2u2J0bS1LwTwKG1pg2fwxyo6O1FwlEcUed6goK2O4UrAwCAxW1oCz84u2G0CpWy9rDyo',
            '__csr': 'gsgZkQV9kAQjBUGRaKHpfD-WAm9iuBGAnC8XGa-JmbLAGXg-icGcy2aKil1p4AimpBchzFVQ4fyUyigES4FRmFk49Ey59qgOE-mpkuazoCAA8ii8QmEOnmt6yUCdhaoHhojwyDy8eoOdzEcd004-RwtK7bG0REakU1IU1n81dEe8460hO053o0NGO0d-0bUp9Qa4wn4A1BwEl2EfQqt0b508m682tl1W3FAgx0KZeu5wCawba2Kfwc216wk9no0xe8yF61kw3z97zU07mS09Sw2R8',
            '__comet_req': '7',
            'lsd': lsd,
            'jazoest': '2941',
            '__spin_r': __spin_r,
            '__spin_b': __spin_b,
            '__spin_t': __spin_t,
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'PolarisPostActionLoadPostQueryQuery',
            'variables': '{"shortcode":"' + self.reel_id + '","fetch_tagged_user_count":null,"hoisted_comment_id":null,"hoisted_reply_id":null}',
            'server_timestamps': 'true',
            'doc_id': '8845758582119845',
        }
        
        return headers, data
    
    def get_media(self, json_data) -> Dict:
        """
            Process media data and download content.
            
            Args:
                json_data: Second response containing necessary json data
            
            Returns:
                Dict: List of downloaded media data and many more about media items
        """
        try:
            items = self.items
            
            try:
                self.username = json_data['data']['xdt_shortcode_media']['owner']['username']
            except:
                pass
            
            if self.username == 'demos':
                try:
                    self.username = items[0]['owner']['username']
                except:
                    pass
            
            description = self.get_media_description()
            
            profile_pic = items['owner']['profile_pic_url']
            local_path = self.get_profile_path(profile_pic)
            
            post_time, _ = TimeConverter.convert_unix_timestamp(int(items['taken_at_timestamp']))
            
            processed_items = self.process_media_items()
            
            return {
                'url': f"https://www.instagram.com/p/{items['shortcode']}/",
                'description': description,
                'profile pic': local_path,
                'Time': post_time,
                'Media Data': processed_items
            }
        
        except:
            return {'Media Data': []}
    
    def process_media_items(self) -> List:
        """
            Download media content from extracted data.
            
            Returns:
                List: List of downloaded media items with metadata
        """
        try:
            processed_items = []
            
            for item in self.media_list:
                is_video = item['is_video']
                try:
                    video_links = item['video_url'] if is_video else item['display_url']
                except:
                    video_links = ''
                
                if not video_links:
                    continue
                
                tag_list = self.get_tagged_users(item)
                
                media_item = {
                    'Tag': tag_list,
                    'Link': video_links,
                }
                
                link = self.get_media_path(video_links, item['id'], is_video)
                if link:
                    media_item['Link'] = link
                
                processed_items.append(media_item)
            
            return processed_items
        
        except:
            return []
    
    def get_tagged_users(self, media_data: Dict) -> str:
        """
            Extract tagged users from media data.
            
            Args:
                media_data: Media data
            
            Returns:
                str: tagged users
        """
        tags = []
        try:
            for j in media_data['edge_media_to_tagged_user']['edges']:
                try:
                    tags.append(j['node']['user']['username'])
                except:
                    pass
        except:
            pass
        
        return ", ".join(tags)
    
    def get_media_path(self, link: str, media_id: str, is_video: bool) -> str:
        """
            Download media file and return local path.
            
            Args:
                link: post/reel url
                media_id: post/reel id
                is_video: is video or photo
            
            Returns:
                str: media local path
        """
        try:
            _path = f'{self.folder_path}/post/{self.username}'
            local_path = f"{_path}/{media_id}{'.mp4' if is_video else '.png'}"
            
            response = requests.get(link)
            if response.status_code == 200:
                with open(local_path, 'wb') as f:
                    f.write(response.content)
                
                return local_path
        except:
            pass
        
        return ''
    
    def get_profile_path(self, profile_pic_url) -> str:
        """
            Download profile pic and return local path.
            
            Args:
                profile_pic_url: profile pic url
            
            Returns:
                str: profile pic local path
        """
        try:
            _path = f'{self.folder_path}/post/{self.username}/profile'
            os.makedirs(_path, exist_ok=True)
            local_path = f'{_path}/profile.png'
            
            response = requests.get(profile_pic_url)
            if response.status_code == 200:
                with open(local_path, 'wb') as f:
                    f.write(response.content)
                
                return local_path
        except:
            pass
        
        return ''
    
    def get_media_description(self) -> str:
        """
            Extract media description from data.
            
            Returns:
                str: description
        """
        try:
            des = self.items['edge_media_to_caption']['edges'][0]['node']['text']
            return des if des else ''
        except:
            return ''
