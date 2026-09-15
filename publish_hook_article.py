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

def publish_hook_article():
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    service = build('blogger', 'v3', credentials=creds)

    title = "The 5-Second Retention Hook: How to Stop the Scroll on Reels & Shorts | Editzaar"
    search_desc = "Master the 5-second retention hook formula for Reels and Shorts. Learn visual patterns, audio cues, and pacing tricks to skyrocket watch time."
    banner_url = "https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?auto=format&fit=crop&w=1200&q=85"
    primary_label = "Growth Tips"  # Exact single tag from blog.editzaar.in

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
<!-- SEO & OpenGraph Structured Metadata for Google & Meta -->
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
         alt="{title}" 
         style="width: 100%; max-height: 520px; object-fit: cover; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.15);" />
    <p style="font-size: 13px; color: #777; margin-top: 10px;"><em>The first 5 seconds dictate 80% of your video's algorithm reach.</em></p>
</div>

<p style="font-size: 17px; line-height: 1.7; color: #222;">
    On Instagram Reels, YouTube Shorts, and TikTok, your video is competing against an infinite stream of dopamine. If you do not capture a viewer's attention in the <strong>first 3 to 5 seconds</strong>, they will swipe away—tanking your Average Percentage Viewed (APV) and killing the video's reach.
</p>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    The good news? Retention is not luck. It is an engineering formula. Here is the <strong>Editzaar 5-Second Hook Framework</strong> that top creators use to maintain 100%+ retention rates.
</p>

<hr style="border: 0; height: 1px; background: #eee; margin: 30px 0;"/>

<h2>1. The Visual "Pattern Interrupt"</h2>
<p>The human brain scrolls on autopilot until something looks unexpected. A pattern interrupt breaks that rhythm instantly:</p>
<ul>
    <li><strong>Fast Motion on Frame 1:</strong> Start mid-movement (a fast camera whip, dropping an object, or walking briskly into frame) rather than standing still.</li>
    <li><strong>Extreme Close-Up to Wide:</strong> Start tight on an intriguing detail for 1 second, then snap zoom to the full scene.</li>
    <li><strong>Negative Space Framing:</strong> Unusual camera angles that make the viewer pause to decode what they are seeing.</li>
</ul>

<h2>2. The "Curiosity Gap" Script Formula</h2>
<p>Never start with <em>"Hey guys, today I am going to show you..."</em>. Instead, use psychological curiosity loops:</p>
<ol>
    <li><strong>The Contrarian Hook:</strong> <em>"Everything you’ve been told about editing Reels is wrong."</em></li>
    <li><strong>The Stakes Hook:</strong> <em>"This 1 mistake is costing you 90% of your watch time."</em></li>
    <li><strong>The Transformation Hook:</strong> <em>"Here is how we turned a 200-view video into a 2M-view viral Reel."</em></li>
</ol>

<h2>3. Audio Velocity & Sound Design Anchors</h2>
<p>Pair every opening visual with synchronized sound design. A subtle <strong>whoosh + bass impact</strong> in the first 0.8 seconds wakes up the audio cortex and primes the viewer to listen attentively.</p>

<h2>4. Rapid Visual Pacing in the First 5 Seconds</h2>
<p>While the rest of the video can breathe with 3–4 second cuts, the intro must move fast:</p>
<ul>
    <li><strong>Cut 1 (0.0s - 1.5s):</strong> Talking head + bold keyword subtitle.</li>
    <li><strong>Cut 2 (1.5s - 3.0s):</strong> High-energy B-roll or dynamic screenshot proof.</li>
    <li><strong>Cut 3 (3.0s - 5.0s):</strong> Push-in zoom on subject delivering the value promise.</li>
</ul>

<h2>5. The Seamless Seamless Loop (The 100%+ Retention Hack)</h2>
<p>Connect your final sentence seamlessly into your opening hook. When the video ends, the viewer loops back to the start without realizing it, boosting your retention stats past 100% and signaling the algorithm to push your video to millions.</p>

<hr style="border: 0; height: 1px; background: #eee; margin: 30px 0;"/>

<!-- Branded Editzaar CTA Box -->
<div style="background: linear-gradient(135deg, #1f1c2c 0%, #928dab 100%); color: #fff; padding: 25px; border-radius: 12px; margin: 35px 0; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.2);">
    <h3 style="margin-top: 0; font-size: 22px; color: #ffeb3b;">Want Viral Edits Crafted for Your Channel?</h3>
    <p style="font-size: 15px; line-height: 1.6; max-width: 600px; margin: 10px auto 20px auto; color: #f0f0f0;">
        At <strong>Editzaar</strong>, we specialize in high-retention video editing, viral hooks, and creative growth strategies for creators and brands worldwide.
    </p>
    <a href="https://blog.editzaar.in/" style="background-color: #ff4b2b; color: #fff; padding: 12px 28px; text-decoration: none; font-weight: bold; border-radius: 30px; display: inline-block; box-shadow: 0 4px 12px rgba(255,75,43,0.4);">
        Discover More Growth Guides on Editzaar →
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
    print("SUCCESS: 5-SECOND RETENTION HOOK ARTICLE DRAFTED!")
    print(f"Title: {result.get('title')}")
    print(f"Single Label: {result.get('labels')}")
    print(f"Location: {result.get('location', {}).get('name')}")
    print(f"Post ID: {result.get('id')}")
    print(f"Edit Link: https://www.blogger.com/blog/post/edit/{BLOG_ID}/{result.get('id')}")
    print("==================================================")

if __name__ == "__main__":
    publish_hook_article()
