# 📸 InstaCapture: Anonymously Download Instagram Stories, Posts, Reels, IGTV Videos, and Profile Pictures 🕵️‍♂️📥

<p id="top" align="right">
  <a href="https://github.com/PrathmeshSoni">
  <img src="https://badges.pufler.dev/visits/prathmeshsoni/InstaCapture?label=VISITOR&style=for-the-badge&logoColor=FFFFFF&color=purple&labelColor=640464&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIGZpbGw9IndoaXRlIiB2ZXJzaW9uPSIxLjEiIHdpZHRoPSIxNiIgaGVpZ2h0PSIxNiIgdmlld0JveD0iMCAwIDE2IDE2IiBjbGFzcz0ib2N0aWNvbiBvY3RpY29uLWV5ZSIgYXJpYS1oaWRkZW49InRydWUiPjxwYXRoIGQ9Ik04IDJjMS45ODEgMCAzLjY3MS45OTIgNC45MzMgMi4wNzggMS4yNyAxLjA5MSAyLjE4NyAyLjM0NSAyLjYzNyAzLjAyM2ExLjYyIDEuNjIgMCAwIDEgMCAxLjc5OGMtLjQ1LjY3OC0xLjM2NyAxLjkzMi0yLjYzNyAzLjAyM0MxMS42NyAxMy4wMDggOS45ODEgMTQgOCAxNGMtMS45ODEgMC0zLjY3MS0uOTkyLTQuOTMzLTIuMDc4QzEuNzk3IDEwLjgzLjg4IDkuNTc2LjQzIDguODk4YTEuNjIgMS42MiAwIDAgMSAwLTEuNzk4Yy40NS0uNjc3IDEuMzY3LTEuOTMxIDIuNjM3LTMuMDIyQzQuMzMgMi45OTIgNi4wMTkgMiA4IDJaTTEuNjc5IDcuOTMyYS4xMi4xMiAwIDAgMCAwIC4xMzZjLjQxMS42MjIgMS4yNDEgMS43NSAyLjM2NiAyLjcxN0M1LjE3NiAxMS43NTggNi41MjcgMTIuNSA4IDEyLjVjMS40NzMgMCAyLjgyNS0uNzQyIDMuOTU1LTEuNzE1IDEuMTI0LS45NjcgMS45NTQtMi4wOTYgMi4zNjYtMi43MTdhLjEyLjEyIDAgMCAwIDAtLjEzNmMtLjQxMi0uNjIxLTEuMjQyLTEuNzUtMi4zNjYtMi43MTdDMTAuODI0IDQuMjQyIDkuNDczIDMuNSA4IDMuNWMtMS40NzMgMC0yLjgyNS43NDItMy45NTUgMS43MTUtMS4xMjQuOTY3LTEuOTU0IDIuMDk2LTIuMzY2IDIuNzE3Wk04IDEwYTIgMiAwIDEgMS0uMDAxLTMuOTk5QTIgMiAwIDAgMSA4IDEwWiI+PC9wYXRoPjwvc3ZnPg==">
  </a> 
</p>

## Overview
**InstaCapture** is a Python package that allows you to anonymously download Instagram stories, posts, reels, IGTV videos, and profile pictures. It provides two main modules:

- `InstaStory` for downloading stories (requires user cookies)
- `InstaPost` for downloading reels, posts, IGTV videos, and profile pictures (no cookies required)

📌 **Project Page**: [InstaCapture on PyPI](https://pypi.org/project/instacapture/)

## Features
✅ Download Instagram stories using user cookies.  
✅ Download reels, posts, IGTV videos, and profile pictures **without cookies**.  
✅ Simple and easy-to-use Python API.

---

## Installation
Install the package using pip:

```bash
pip install instacapture
```

---

## Usage

### **Import the Modules**
```python
from instacapture import InstaStory, InstaPost
```

---

### **Download Instagram Stories (Requires Cookies)**

#### **Example Usage:**
```python
cookies = {}

story_obj = InstaStory()
story_obj.cookies = cookies

story_obj.username = 'Enter username or profile link'
story_obj.story_download()

story_obj.username = 'Enter username or profile link'
story_obj.story_download()
```

#### **How to Get Cookies**
1. Open Chrome and go to Instagram.
2. Log in to your account.
3. Right-click anywhere and select **Inspect**.
4. Go to the **Network** tab.
5. Refresh the page.
6. Find a request to `instagram.com`.
7. Click on the request.
8. Right-click on the request and select **Copy as cURL**.
9. Paste the copied cURL command into a tool like [cURL to Python Converter](https://curlconvert.vercel.app/).
10. Copy the cookies from the converted Python code.
11. Assign the cookies to the `cookies` variable in your script.

---

### **Download Reels, Posts, IGTV, and Profile Pictures (No Cookies Required)**

#### **Example Usage:**
```python
post_obj = InstaPost()

post_obj.reel_id = "Enter Post/Reel URL or code"
post_obj.media_download()

post_obj.reel_id = "Enter another Post/Reel URL or code"
post_obj.media_download()
```

---

## Notes
⚠️ **Ensure your cookies are up to date** when downloading stories.
📌 **For reels, posts, IGTV, and profile pictures, cookies are not required.**

---

## License
This project is licensed under the [MIT License](https://github.com/prathmeshsoni/InstaCapture?tab=MIT-1-ov-file).

---

## All Set :)

<p style="float:left;" align="left">
  <a href="#top">Back To Top</a>
</p>

<p style="text-align:right;" align="right">
  <a href="https://github.com/PrathmeshSoni/InstaCapture" target="_blank">Back To Repository</a>
</p>


---
**<a href="https://instacapture.mrsoni.me?ref=footer-github" target="_blank">InstaCapture</a>** - Provided by **<a href="https://soniprathmesh.com?ref=footer-github" target="_blank">Prathmesh Soni</a>**
