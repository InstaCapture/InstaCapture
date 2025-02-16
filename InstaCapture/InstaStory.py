import os
import json
import pytz
import requests

from lxml import html
from requests import Response
from datetime import datetime, timedelta
from typing import Dict, List, Union, Optional


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


class InstaStory:
    """Class to handle Instagram story downloading operations."""
    
    def __init__(self, username: Optional[str] = '', cookies: Union[str, Dict] = '{}'):
        """
            Initialize the InstaStory downloader.
            
            Args:
                username (Optional[str]): Instagram username to fetch stories from.
                cookies (Optional[Union[str, Dict]]): Cookie data for authentication.
        """
        self._username = None
        self.username = username
        self._cookies = None
        self.cookies = cookies
        
        self.session = requests.Session()
        self.folder_path = '.'
    
    @property
    def username(self):
        """Get the username."""
        return self._username
    
    @username.setter
    def username(self, username_id):
        """
        Set the username and call get_profile_name.
        
        Args:
            username_id (str): Instagram username url to fetch stories from.
        """
        self._username = self.get_profile_name(username_id)
    
    @property
    def cookies(self):
        """Get the cookies."""
        return self._cookies
    
    @cookies.setter
    def cookies(self, cookies):
        """
            Set the cookies.
            
            Args:
                cookies (str): Instagram user cookies
        """
        try:
            self._cookies = json.loads(cookies)
        except:
            self._cookies = cookies
    
    def get_profile_name(self, username_id: str) -> str:
        """
            Extract profile name from profile url.
            
            Args:
                username_id (str): Instagram profile url/id to fetch stories
            
            Returns:
                str: profile name extracted from url
        """
        
        return username_id.split('?')[0].strip('/').split('/')[-1].strip()
    
    def print(self, check: Optional[bool] = False) -> None:
        """
            Print the status of the story download operation.
            
            Args:
                check Optional[bool]: The check to print. If check is not empty, it indicates success; otherwise, failure.
        """
        if check:
            print(f'Story downloaded successfully at {self.folder_path}/story/{self.username}')
        else:
            print("Story not found or try again....")
    
    def story_download(self) -> Dict:
        """
            Download stories from Instagram.
            
            Returns:
                Dict: Story data if found
        """
        if not self.validate_inputs():
            print("Cookies or Username is Missing !!!")
            return {}
        
        response = self.make_initial_request()
        if not response:
            self.print()
            return {}
        
        json_data = self.get_json_data(response)
        if not json_data:
            self.print()
            return {}
        
        story_data = self.get_story(json_data)
        if not story_data['Story Data']:
            self.print()
            return {}
        
        with open(f'{self.folder_path}/story/{self.username}/story.json', 'w') as f:
            json.dump({self.username: story_data}, f)
        
        with open(f'{self.folder_path}/story/{self.username}/story-main.json', 'w') as f:
            json.dump(json_data, f)
        
        self.print(True)
        return {self.username: story_data}
    
    def validate_inputs(self) -> bool:
        """
            Validate input data.
            
            Returns:
                bool: True if valid, False otherwise
        """
        return bool(self.username and self.cookies)
    
    def make_initial_request(self) -> Response | bool:
        """
            Make initial request to get story information.
            
            Returns:
                Response | bool: Response object if successful
        """
        try:
            response = self.session.get(
                f'https://www.instagram.com/stories/{self.username}/', params={'r': '1'},
                cookies=self.cookies, headers=self.headers()
            )
            return response if response.status_code == 200 else False
        
        except:
            return False
    
    def get_json_data(self, response: requests.Response) -> Dict:
        """
            Extract JSON data from response.
            
            Args:
                response (Response): Response object
            
            Returns:
                Dict: JSON data if found
        """
        try:
            con = html.fromstring(response.text)
            json_path = con.xpath("//script[@type='application/json' and contains(text(), 'items')]/text()")[0]
            
            return self.find_story_json(json.loads(json_path))
        
        except:
            return {}
    
    def find_story_json(self, data: Union[Dict, List]) -> Optional[Dict]:
        """
            Recursively search for story media in Instagram's JSON response.
            
            Args:
                data: JSON data to search through
                
            Returns:
                Optional[Dict]: Story media data if found, None otherwise
        """
        if isinstance(data, dict):
            if 'xdt_api__v1__feed__reels_media' in data:
                return data['xdt_api__v1__feed__reels_media']['reels_media'][0]
            for value in data.values():
                result = self.find_story_json(value)
                if result is not None:
                    return result
        
        elif isinstance(data, list):
            for item in data:
                result = self.find_story_json(item)
                if result is not None:
                    return result
    
    def get_story(self, json_data: Dict) -> Dict:
        """
            Extract story data from JSON data.
            
            Args:
                json_data (Dict): JSON data
                
            Returns:
                Dict: Story data if found
        """
        try:
            profile_pic = json_data['user']['profile_pic_url']
            local_path = self.get_profile_path(profile_pic)
            
            processed_items = self.process_story_items(json_data['items'])
            
            return {
                'url': f'https://www.instagram.com/stories/{self.username}/',
                'profile pic': local_path,
                'Story Data': processed_items
            }
        
        except:
            return {
                'url': f'https://www.instagram.com/stories/{self.username}/',
                'Story Data': []
            }
    
    def process_story_items(self, items) -> List:
        """
            Process story items and extract relevant data.
            
            Args:
                items: Story items data
            
            Returns:
                List: Processed story items data
        """
        processed_items = []
        try:
            for item in items:
                try:
                    is_video = True if item['video_versions'][0]['url'] else False
                except:
                    is_video = False
                try:
                    story_links = item['video_versions'][0]['url'] if is_video else item['image_versions2']['candidates'][0]['url']
                except:
                    story_links = ''
                
                if not story_links:
                    continue
                
                story_id = item['pk']
                
                story_time, _ = TimeConverter.convert_unix_timestamp(int(item['expiring_at']))
                tags = self.get_tagged_users(item)
                
                story_item = {
                    'url': f'https://www.instagram.com/stories/{self.username}/{story_id}/',
                    'Time': story_time,
                    'Tag': tags,
                    'Link': story_links,
                }
                
                link = self.get_story_path(story_links, story_id, is_video)
                if link:
                    story_item['Link'] = link
                
                processed_items.append(story_item)
        
        except:
            pass
        
        return processed_items
    
    def get_tagged_users(self, story_data: Dict) -> str:
        """
            Extract tagged users from story data.
            
            Args:
                story_data: Story data
            
            Returns:
                str: tagged users
        """
        tags = []
        try:
            for j in story_data['story_bloks_stickers']:
                try:
                    tags.append(j['bloks_sticker']['sticker_data']['ig_mention']['username'])
                except:
                    pass
        except:
            pass
        
        return ", ".join(tags)
    
    def get_story_path(self, link: str, story_id: str, is_video: bool) -> str:
        """
            Download story and return local path.
            
            Args:
                link: story url
                story_id: story id
                is_video: is video or photo
            
            Returns:
                str: story local path
        """
        try:
            _path = f'{self.folder_path}/story/{self.username}'
            local_path = f"{_path}/{story_id}{'.mp4' if is_video else '.png'}"
            
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
            _path = f'{self.folder_path}/story/{self.username}/profile'
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
    
    def headers(self) -> Dict:
        """
            Return headers for making requests.
        """
        return {
                'authority': 'www.instagram.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'en-US,en;q=0.9',
                'cache-control': 'no-cache',
                'dpr': '1.25',
                'pragma': 'no-cache',
                'sec-ch-prefers-color-scheme': 'dark',
                'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
                'sec-ch-ua-full-version-list': '"Chromium";v="122.0.6261.129", "Not(A:Brand";v="24.0.0.0", "Google Chrome";v="122.0.6261.129"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-model': '""',
                'sec-ch-ua-platform': '"Windows"',
                'sec-ch-ua-platform-version': '"10.0.0"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'viewport-width': '1536',
            }
