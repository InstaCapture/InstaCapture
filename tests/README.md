# InstaCapture Interactive Script

This script demonstrates an interactive way to use the **InstaCapture** package for downloading Instagram stories, posts, reels, and IGTV videos.

## Features
- **Download Instagram Stories**: Requires user cookies and the username or profile URL.
- **Download Instagram Posts/Reels/IGTV**: Requires the URL or code of the media.  
- Provides a user-friendly interface for interacting with the InstaCapture package.

---

## Requirements
- Python 3.6 or higher
- InstaCapture package installed

Install the InstaCapture package using:
```bash
pip install InstaCapture
```

---

## How to Use the Script

### 1. Run the Script
Run the script using:
```bash
python path/to/script.py
```

### 2. Main Menu
You will be prompted with the following options:
```plaintext
1. Download Instagram Story
2. Download Instagram Post/Reel
3. Exit
```

### 3. Downloading Instagram Stories
- Enter the **username** or **profile URL** of the target account.
- If cookies are not yet set, the script will prompt you to enter them.

#### **How to Get Cookies**
1. Open Chrome and go to Instagram.
2. Log in to your account.
3. Right-click anywhere and select **Inspect**.
4. Navigate to the **Network** tab.
5. Refresh the page.
6. Find a request to `instagram.com`.
7. Right-click the request and select **Copy as cURL**.
8. Use a [cURL to Python converter](https://curlconvert.vercel.app/) to extract cookies.
9. Paste the cookies in the script when prompted.

---

### 4. Downloading Instagram Posts/Reels
- Enter the **URL** or **code** of the post, reel, or IGTV video when prompted.
- The script will handle the download process automatically.

---

## Example Workflow

### Downloading Stories
```plaintext
1. Download Instagram Story
Enter Username or Profile Url: target_username
Enter Cookies (press Enter on an empty line to finish):
cookie_line_1
cookie_line_2
[Press Enter]
```

### Downloading Posts/Reels
```plaintext
2. Download Instagram Post/Reel
Enter Post/Reel URL or code: https://www.instagram.com/reel/example_code/
```

### Exiting
```plaintext
3. Exit
Thank you for using InstaCapture. Goodbye!
```

---

## Notes
- **Stories** require valid cookies for authentication.
- **Posts/Reels/IGTV videos** do not require cookies.
- Ensure you have the correct permissions to download content.

---

## License
This project is licensed under the [MIT License](LICENSE).

---

## Author
Created by **Prathmesh Soni**  
For more details, visit the [GitHub Repository](https://github.com/prathmeshsoni/InstaCapture).
```

Let me know if you need any changes or additions!