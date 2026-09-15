import os
import sys
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

SCOPES = ['https://www.googleapis.com/auth/blogger']
BLOG_ID = '866286363471382851'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLIENT_SECRETS_FILE = os.path.join(BASE_DIR, 'client_secrets.json')
TOKEN_FILE = os.path.join(BASE_DIR, 'token.json')

def get_blogger_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(
                port=8080,
                prompt='consent',
                authorization_prompt_message='Open the following URL in your browser to sign in: {url}'
            )
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return build('blogger', 'v3', credentials=creds)

def create_draft_post(title, html_content, labels=None):
    service = get_blogger_service()
    if labels is None:
        labels = ["video editing"]

    body = {
        "title": title,
        "content": html_content,
        "labels": labels
    }
    
    posts = service.posts()
    result = posts.insert(blogId=BLOG_ID, body=body, isDraft=True).execute()
    
    print("\n" + "="*60)
    print(" DRAFT POST CREATED SUCCESSFULLY!")
    print(f" Title: {result.get('title')}")
    print(f" Post ID: {result.get('id')}")
    print(f" Status: {result.get('status')}")
    print(f" Live Edit URL: https://www.blogger.com/blog/post/edit/{BLOG_ID}/{result.get('id')}")
    print("="*60 + "\n")
    return result

if __name__ == "__main__":
    print("Starting authentication server...")
    test_title = "AI & Video Editing: The Future of Creator Workflows in 2026 | Editzaar"
    test_content = """
    <h2>Why AI is Revolutionizing Video Editing</h2>
    <p>Video editing is moving faster than ever. In 2026, creators are leveraging AI tools to cut hours of tedious work down to minutes.</p>
    <h3>Key Advantages:</h3>
    <ul>
        <li><strong>Smart Trimming & Silence Removal:</strong> Jump cuts and rough cuts generated automatically.</li>
        <li><strong>Automated B-Roll & Captions:</strong> Instant animated subtitles and contextual footage.</li>
        <li><strong>Color Grading Matching:</strong> Transfer cinema looks across shots with 1 click.</li>
    </ul>
    <p><em>Stay tuned to Editzaar for the latest editing breakdowns, workflows, and tutorials!</em></p>
    """
    create_draft_post(test_title, test_content, labels=["video editing", "Growth Tips"])
