import urllib.request
import json
import sys
from collections import Counter

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "AIzaSyCQXoTceO4fKpWH1EryoiFrBV0Psd6Seh0"
BLOG_ID = "866286363471382851"

def scan_labels():
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts?key={API_KEY}&maxResults=50"
    req = urllib.request.urlopen(url)
    data = json.loads(req.read().decode('utf-8'))

    labels = []
    for post in data.get("items", []):
        for l in post.get("labels", []):
            labels.append(l)

    counts = Counter(labels)
    print("\n==========================================")
    print("ALL EXISTING LABELS ON BLOG.EDITZAAR.IN:")
    print("==========================================")
    for label, count in counts.most_common():
        print(f" • '{label}' ({count} articles)")
    print("==========================================\n")

if __name__ == "__main__":
    scan_labels()
