import urllib.request
import json
import sys

# Ensure UTF-8 output on Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "AIzaSyCQXoTceO4fKpWH1EryoiFrBV0Psd6Seh0"
BLOG_ID = "866286363471382851"

def fetch_posts():
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts?key={API_KEY}&maxResults=10"
    req = urllib.request.urlopen(url)
    data = json.loads(req.read().decode('utf-8'))
    
    posts = data.get("items", [])
    print(f"Successfully fetched {len(posts)} recent posts from Editzaar Blogs:\n")
    for idx, post in enumerate(posts, 1):
        title = post.get("title", "No Title")
        published = post.get("published", "")[:10]
        labels = ", ".join(post.get("labels", ["No Tags"]))
        link = post.get("url", "")
        print(f"{idx}. [{published}] {title}")
        print(f"   Tags: {labels}")
        print(f"   Link: {link}\n")

if __name__ == "__main__":
    fetch_posts()
