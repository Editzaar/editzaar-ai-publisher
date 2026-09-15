import os
import sys
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

SCOPES = ['https://www.googleapis.com/auth/blogger']
BLOG_ID = '866286363471382851'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(BASE_DIR, 'token.json')

def publish_humanized_article():
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    service = build('blogger', 'v3', credentials=creds)

    title = "Why Your YouTube Videos Get Stuck at 200 Views (And How to Fix It) | Editzaar"
    search_desc = "Stuck in the 200-view jail on YouTube? Here are 4 simple editing and packaging fixes that actually help your videos get recommended."
    banner_url = "https://images.unsplash.com/photo-1533750349088-cd871a92f312?auto=format&fit=crop&w=1200&q=85"
    primary_label = "Growth Tips"  # Exact single tag from website

    json_ld_schema = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": title,
        "description": search_desc,
        "image": banner_url,
        "author": {
            "@type": "Organization",
            "name": "Editzaar",
            "url": "https://blog.editzaar.in/"
        },
        "publisher": {
            "@type": "Organization",
            "name": "Editzaar Blogs",
            "logo": {
                "@type": "ImageObject",
                "url": "https://blog.editzaar.in/favicon.ico"
            }
        },
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": "https://blog.editzaar.in/"
        }
    }

    html_content = f"""
<!-- SEO Schema for Search Engines -->
<script type="application/ld+json">
{json.dumps(json_ld_schema, indent=2)}
</script>
<meta name="description" content="{search_desc}" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{search_desc}" />
<meta property="og:image" content="{banner_url}" />
<meta property="og:type" content="article" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{title}" />
<meta name="twitter:description" content="{search_desc}" />
<meta name="twitter:image" content="{banner_url}" />

<!-- Featured Cover Banner -->
<div style="text-align: center; margin-bottom: 30px;">
    <img src="{banner_url}" 
         alt="Frustrated creator looking at analytics" 
         style="width: 100%; max-height: 520px; object-fit: cover; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.15);" />
</div>

<p style="font-size: 18px; line-height: 1.8; color: #222;">
    We have all been there. You spend 10 hours recording, editing, finding music, and tweaking colors. You hit upload, feel proud, and check back 5 hours later... only to see <strong>187 views</strong>.
</p>
<p style="font-size: 17px; line-height: 1.8; color: #333;">
    It hurts. But here is the truth: YouTube does not hate your channel, and the algorithm isn't broken. Usually, it comes down to just a few small mistakes that are easy to fix once you see them.
</p>
<p style="font-size: 17px; line-height: 1.8; color: #333;">
    Here are 4 simple reasons your videos get stuck—and what to do instead on your next upload.
</p>

<hr style="border: 0; height: 1px; background: #eee; margin: 30px 0;"/>

<h2 style="font-size: 22px; color: #111;">1. Your Intro Takes Too Long to Get to the Point</h2>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    When a new viewer clicks your video, they give you about 5 seconds to prove you won't waste their time. If you spend the first 30 seconds saying <em>"Welcome back to my channel, make sure to like and subscribe, today was a busy day..."</em>, half your audience has already clicked away.
</p>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    <strong>The Quick Fix:</strong> Cut straight to the action. Start your video right inside the main topic, and save your channel intro for the middle or end.
</p>

<h2 style="font-size: 22px; color: #111;">2. Too Much "Dead Space" in the Timeline</h2>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    When you edit your own video, pauses feel natural because you lived that moment. But to a stranger on the internet, even a 1-second silence feels slow.
</p>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    <strong>The Quick Fix:</strong> Zoom into your audio waveform. Trim out the silent gaps between sentences, deep breaths, and hesitation words. Your video will instantly feel tighter and more energetic.
</p>

<h2 style="font-size: 22px; color: #111;">3. The Thumbnail and Title Don't Tell a Story</h2>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    A great video with a boring thumbnail gets zero clicks. If your thumbnail just has your face and 8 lines of tiny text, nobody scrolling on a phone can read it.
</p>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    <strong>The Quick Fix:</strong> Keep it clean. Use 1 strong visual, a clear facial expression, and maximum 3 to 4 big bold words. Let the title create curiosity, and let the thumbnail show the emotion.
</p>

<h2 style="font-size: 22px; color: #111;">4. Forgetting to Change the Visual Every Few Seconds</h2>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    If a viewer stares at the exact same talking head angle for 2 minutes straight, their eyes get tired and their mind wanders off.
</p>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    <strong>The Quick Fix:</strong> Mix it up! Add simple punch-in zooms (crop in 10%), throw in some B-roll footage, highlight a keyword on screen, or use a sound effect to reset their focus.
</p>

<hr style="border: 0; height: 1px; background: #eee; margin: 30px 0;"/>

<h3 style="font-size: 20px; color: #111;">The Takeaway</h3>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    Growing a channel isn't about buying a $3,000 camera. It is about respecting the viewer's time and making every minute of your video engaging and fun to watch.
</p>

<!-- Branded Editzaar CTA Box -->
<div style="background-color: #f8f9fa; border: 2px solid #ff4b2b; padding: 25px; border-radius: 12px; margin: 35px 0; text-align: center;">
    <h3 style="margin-top: 0; font-size: 22px; color: #111;">Need Help Editing Your Videos?</h3>
    <p style="font-size: 15px; line-height: 1.6; max-width: 600px; margin: 10px auto 20px auto; color: #555;">
        At <strong>Editzaar</strong>, we help creators turn raw footage into crisp, engaging videos that keep people watching till the end. Check out our latest editing tips and tutorials!
    </p>
    <a href="https://blog.editzaar.in/" style="background-color: #ff4b2b; color: #fff; padding: 12px 28px; text-decoration: none; font-weight: bold; border-radius: 30px; display: inline-block;">
        Read More on Editzaar Blogs →
    </a>
</div>
"""

    body = {
        "title": title,
        "content": html_content,
        "labels": [primary_label],
        "location": {
            "name": "India",
            "lat": 20.5937,
            "lng": 78.9629
        },
        "customMetaData": search_desc
    }

    result = service.posts().insert(blogId=BLOG_ID, body=body, isDraft=True).execute()

    print("==================================================")
    print("SUCCESS: HUMANIZED ARTICLE DRAFTED ON EDITZAAR BLOGS!")
    print(f"Title: {result.get('title')}")
    print(f"Tag: {result.get('labels')}")
    print(f"Post ID: {result.get('id')}")
    print(f"Edit Link: https://www.blogger.com/blog/post/edit/{BLOG_ID}/{result.get('id')}")
    print("==================================================")

if __name__ == "__main__":
    publish_humanized_article()
