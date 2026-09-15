import os
import sys
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

SCOPES = ['https://www.googleapis.com/auth/blogger']
BLOG_ID = '866286363471382851'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLIENT_SECRETS_FILE = os.path.join(BASE_DIR, 'client_secrets.json')
TOKEN_FILE = os.path.join(BASE_DIR, 'token.json')

def main():
    print("STEP 1: Starting OAuth local server...", flush=True)
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    
    creds = flow.run_local_server(
        port=0,
        open_browser=True,
        authorization_prompt_message='AUTH_URL: {url}'
    )
    
    print("STEP 2: Authentication received! Saving token.json...", flush=True)
    with open(TOKEN_FILE, 'w', encoding='utf-8') as token:
        token.write(creds.to_json())
    print("STEP 3: token.json saved successfully!", flush=True)
    
    print("STEP 4: Connecting to Blogger API...", flush=True)
    service = build('blogger', 'v3', credentials=creds)
    
    print("STEP 5: Creating test draft post...", flush=True)
    body = {
        "title": "AI & Video Editing: The Future of Creator Workflows in 2026 | Editzaar",
        "content": """
        <h2>Why AI is Revolutionizing Video Editing</h2>
        <p>In 2026, creators are leveraging AI tools to cut hours of tedious work down to minutes.</p>
        <h3>Key Advantages:</h3>
        <ul>
            <li><strong>Smart Trimming & Silence Removal:</strong> Jump cuts and rough cuts generated automatically.</li>
            <li><strong>Automated B-Roll & Captions:</strong> Instant animated subtitles and contextual footage.</li>
            <li><strong>Color Grading Matching:</strong> Transfer cinema looks across shots with 1 click.</li>
        </ul>
        <p><em>Stay tuned to Editzaar for the latest editing breakdowns, workflows, and tutorials!</em></p>
        """,
        "labels": ["video editing", "Growth Tips"]
    }
    result = service.posts().insert(blogId=BLOG_ID, body=body, isDraft=True).execute()
    print("==================================================", flush=True)
    print("SUCCESS: DRAFT POST CREATED ON BLOGGER!", flush=True)
    print(f"Title: {result.get('title')}", flush=True)
    print(f"Post ID: {result.get('id')}", flush=True)
    print(f"Edit Link: https://www.blogger.com/blog/post/edit/{BLOG_ID}/{result.get('id')}", flush=True)
    print("==================================================", flush=True)

if __name__ == "__main__":
    main()
