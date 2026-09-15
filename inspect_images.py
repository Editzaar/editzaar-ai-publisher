import urllib.request
import json
import re
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "AIzaSyCQXoTceO4fKpWH1EryoiFrBV0Psd6Seh0"
BLOG_ID = "866286363471382851"

def inspect_previous_images():
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts?key={API_KEY}&maxResults=15"
    req = urllib.request.urlopen(url)
    data = json.loads(req.read().decode('utf-8'))

    print("==================================================")
    print("ANALYZING PREVIOUS POST THUMBNAILS & IMAGES:")
    print("==================================================")
    for idx, p in enumerate(data.get("items", []), 1):
        title = p.get("title", "")
        content = p.get("content", "")
        imgs = re.findall(r'<img [^>]*src=["\']([^"\']+)["\']', content)
        print(f"\n{idx}. {title}")
        if imgs:
            for img in imgs[:2]:
                print(f"   🖼️ {img}")
        else:
            print("   (No image found in content)")
    print("==================================================")

if __name__ == "__main__":
    inspect_previous_images()
