"""
Interactive Script for Using InstaCapture

This script provides an interactive way to use the InstaCapture package for downloading
Instagram stories (using cookies) and posts, reels, or IGTV videos (without requiring cookies).

Features:
1. Download Instagram Stories: Requires user cookies and the username/profile URL.
2. Download Instagram Posts/Reels: Requires the post/reel URL or code.

Modules Used:
- InstaStory: For downloading stories using cookies.
- InstaPost: For downloading posts, reels, and IGTV videos without cookies.

Usage:
- Run the script and follow the prompts.
- Enter cookies when prompted for story downloads.
- Provide valid Instagram URLs or codes for posts/reels.

Author: Prathmesh Soni
"""

from instacapture import InstaStory, InstaPost


def get_cookies():
    """
        Prompts the user to input cookies line by line.
        Collects cookies until the user provides an empty line.
        
        Returns:
            str: A single string containing all the cookies.
    """
    print("Enter Cookies (press Enter on an empty line to finish):")
    cookies_lines = []
    while True:
        line = input()
        if line == "":
            break
        cookies_lines.append(line)
    return " ".join(cookies_lines)


def main_v2():
    """
        Provides an interactive menu for users to download Instagram stories or posts/reels.
        
        Options:
        1. Download Instagram Story: Requires cookies and a username/profile URL.
        2. Download Instagram Post/Reel: Requires a post/reel URL or code.
        3. Exit: Exits the script.
    """
    cookies = {}
    story_obj = InstaStory()
    post_obj = InstaPost()
    
    while True:
        # Display the main menu
        check_input = input("""
1. Download Instagram Story
2. Download Instagram Post/ Reel
3. Exit
Enter Number: """)
        
        if check_input == '1':
            # Handle story download
            story_obj.username = input("Enter Username or Profile URL: ")
            if not cookies:
                cookies = get_cookies()
                story_obj.cookies = cookies
            
            story_obj.story_download()
        
        elif check_input == '2':
            # Handle post/reel download
            post_obj.reel_id = input("Enter Post/Reel URL or code: ")
            post_obj.media_download()
        
        elif check_input == '3':
            # Exit the program
            print("Thank you for using InstaCapture. Goodbye!")
            return "Exiting..."
        
        else:
            # Handle invalid inputs
            print("Invalid input. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main_v2()
