import os
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

SCOPES = ['https://www.googleapis.com/auth/blogger']
BLOG_ID = '866286363471382851'
POST_ID = '8936732062247744679'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(BASE_DIR, 'token.json')

def update_post_metadata():
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    service = build('blogger', 'v3', credentials=creds)

    # In Blogger API, viewing draft posts requires view='ADMIN'
    post = service.posts().get(blogId=BLOG_ID, postId=POST_ID, view='ADMIN').execute()

    # 1. Add Location
    post['location'] = {
        "name": "India",
        "lat": 20.5937,
        "lng": 78.9629
    }

    # 2. Add Search Description (Meta description for Google Search & SEO)
    post['customMetaData'] = "Discover 5 viral sound design secrets for Instagram Reels and YouTube Shorts. Learn how to use sub-bass drops, whoosh-hits, and foley to boost viewer retention."

    # Update post
    updated = service.posts().update(blogId=BLOG_ID, postId=POST_ID, body=post).execute()

    print("==================================================")
    print("SUCCESS: LOCATION AND SEARCH DESCRIPTION UPDATED!")
    print(f"Post ID: {updated.get('id')}")
    print(f"Location Name: {updated.get('location', {}).get('name')}")
    print(f"Search Description: {updated.get('customMetaData')}")
    print(f"Blogger Edit Link: https://www.blogger.com/blog/post/edit/{BLOG_ID}/{POST_ID}")
    print("==================================================")

if __name__ == "__main__":
    update_post_metadata()
