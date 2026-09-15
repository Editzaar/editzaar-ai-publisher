import os
import sys
import io
import base64
import json
from PIL import Image
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

SCOPES = ['https://www.googleapis.com/auth/blogger']
BLOG_ID = '866286363471382851'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(BASE_DIR, 'token.json')
LOCAL_IMAGE = os.path.join(r"C:\Users\Lenovo\.gemini\antigravity\brain\eb4fd464-2aa1-422b-97e6-fc0b916786b7", "capcut_15min_viral_reels_cover_1789413182470.jpg")

def optimize_and_encode_image(image_path, max_width=1000, quality=75):
    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Resize proportionally
    w_percent = (max_width / float(img.size[0]))
    h_size = int((float(img.size[1]) * float(w_percent)))
    img = img.resize((max_width, h_size), Image.Resampling.LANCZOS)
    
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=quality, optimize=True)
    size_kb = len(buffer.getvalue()) / 1024
    print(f"Optimized custom thumbnail size: {size_kb:.1f} KB")
    return f"data:image/jpeg;base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"

def publish_capcut_post():
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    service = build('blogger', 'v3', credentials=creds)

    image_data_uri = optimize_and_encode_image(LOCAL_IMAGE)

    title = "The 15-Minute CapCut Viral Workflow: How to Edit Reels 5x Faster | Editzaar"
    search_desc = "Master the 15-minute CapCut PC and Mobile editing workflow for viral Instagram Reels. Learn auto-captions, speed curves, and keyframe transitions."
    primary_label = "video editing"

    html_content = f"""
<!-- SEO OpenGraph Meta -->
<meta name="description" content="{search_desc}" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{search_desc}" />
<meta property="og:type" content="article" />
<meta name="twitter:card" content="summary_large_image" />

<!-- Custom 3D Featured Cover Banner (Guaranteed 100% Load Reliability) -->
<div style="text-align: center; margin-bottom: 30px;">
    <img src="{image_data_uri}" 
         alt="CapCut 15-Minute Viral Video Editing Workflow" 
         style="width: 100%; max-height: 560px; object-fit: cover; border-radius: 14px; box-shadow: 0 10px 30px rgba(0,0,0,0.3);" />
</div>

<p style="font-size: 18px; line-height: 1.8; color: #222;">
    If you spend 3 hours editing a single 45-second Reel or Short, you are doing it wrong. In 2026, the algorithm rewards <strong>consistency and storytelling pace</strong> far more than overly complex 50-layer keyframe transitions.
</p>
<p style="font-size: 17px; line-height: 1.8; color: #333;">
    Whether you use CapCut on your iPhone, Android, or PC, here is the exact <strong>15-minute 4-step workflow</strong> used by full-time creators to pump out crisp, viral edits every single day without burning out.
</p>

<hr style="border: 0; height: 1px; background: #eee; margin: 30px 0;"/>

<h2 style="font-size: 22px; color: #111;">Step 1: The 3-Minute "Dead Space" Rough Cut</h2>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    Never edit effects while scrubbing through raw footage. Your first pass should be 100% focused on <strong>speech pacing</strong>:
</p>
<ul style="font-size: 16px; line-height: 1.8; color: #333;">
    <li><strong>Turn on Audio Waveforms:</strong> Look for flat lines between your spoken sentences.</li>
    <li><strong>Split & Ripple Delete:</strong> Cut out every breath, silence over 0.3 seconds, and repeated takes.</li>
    <li><strong>The Golden Rule:</strong> If a sentence doesn't deliver a punchline, proof, or helpful insight, delete it without mercy.</li>
</ul>

<h2 style="font-size: 22px; color: #111;">Step 2: Auto-Captions with the "Karaoke Highlight" Preset</h2>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    Don't type manual subtitles. In CapCut:
</p>
<ul style="font-size: 16px; line-height: 1.8; color: #333;">
    <li>Click <strong>Text → Auto Captions</strong> (takes 5 seconds).</li>
    <li>Choose a high-contrast font like <em>Montserrat Black</em> or <em>The Bold Font</em>.</li>
    <li>Enable the <strong>Word-by-Word Karaoke Animation</strong> with bright yellow or electric cyan text on key spoken words.</li>
    <li>Keep captions to 2–3 words per line so viewers read instantly without eye strain.</li>
</ul>

<h2 style="font-size: 22px; color: #111;">Step 3: The "Custom Speed Curve" for Visual Pop</h2>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    Linear speed ramps look cheap. Whenever you show B-roll (like opening a laptop, showing a product, or walking into a room):
</p>
<ol style="font-size: 16px; line-height: 1.8; color: #333;">
    <li>Go to <strong>Speed → Curve → Custom</strong>.</li>
    <li>Raise the first 2 points to <strong>3.0x speed</strong>, and drop the middle point down to <strong>0.8x speed</strong>.</li>
    <li>This creates a lightning-fast snap into your clip that instantly grabs viewer attention.</li>
</ol>

<h2 style="font-size: 22px; color: #111;">Step 4: The 3 Essential Sound Layer Cues</h2>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    In the final 3 minutes, add just 3 audio layers in your timeline:
</p>
<ul style="font-size: 16px; line-height: 1.8; color: #333;">
    <li><strong>Swoosh / Whoosh FX:</strong> On every major image, screenshot, or text slide-in.</li>
    <li><strong>Camera Click / Pop:</strong> On every stat, graphic, or proof sticker.</li>
    <li><strong>Background Lo-Fi / Phonk Music:</strong> Lower the volume to <strong>-22dB to -26dB</strong> so your voice cuts through crisp and clear.</li>
</ul>

<hr style="border: 0; height: 1px; background: #eee; margin: 30px 0;"/>

<h3 style="font-size: 20px; color: #111;">CapCut PC vs. Mobile: Which is Faster?</h3>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    If you edit short talking-head clips on the go, <strong>CapCut Mobile</strong> is unbeatable for speed. But if you work with heavy 4K footage and multi-track sound effects, the <strong>CapCut PC Desktop app</strong> allows you to use keyboard shortcuts (<code>Q</code> and <code>W</code> ripple edits) to finish edits twice as fast.
</p>

<!-- Branded Editzaar CTA Box -->
<div style="background-color: #f8f9fa; border: 2px solid #ff4b2b; padding: 25px; border-radius: 12px; margin: 35px 0; text-align: center;">
    <h3 style="margin-top: 0; font-size: 22px; color: #111;">Want Viral Video Edits Done for You?</h3>
    <p style="font-size: 15px; line-height: 1.6; max-width: 600px; margin: 10px auto 20px auto; color: #555;">
        At <strong>Editzaar</strong>, we produce retention-optimized YouTube videos, high-converting Reels, and creator growth assets that save you hours every week.
    </p>
    <a href="https://blog.editzaar.in/" style="background-color: #ff4b2b; color: #fff; padding: 12px 28px; text-decoration: none; font-weight: bold; border-radius: 30px; display: inline-block;">
        Explore More Workflows on Editzaar Blogs →
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
    print("SUCCESS: CAPCUT 15-MIN WORKFLOW DRAFTED ON BLOGGER!")
    print(f"Title: {result.get('title')}")
    print(f"Single Label: {result.get('labels')}")
    print(f"Location: {result.get('location', {}).get('name')}")
    print(f"Post ID: {result.get('id')}")
    print(f"Edit Link: https://www.blogger.com/blog/post/edit/{BLOG_ID}/{result.get('id')}")
    print("==================================================")

if __name__ == "__main__":
    publish_capcut_post()
