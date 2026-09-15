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
LOCAL_IMAGE = os.path.join(r"C:\Users\Lenovo\.gemini\antigravity\brain\eb4fd464-2aa1-422b-97e6-fc0b916786b7", "color_grading_3node_film_look_cover_1789413526812.jpg")

def optimize_and_encode_image(image_path, max_width=1000, quality=75):
    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    w_percent = (max_width / float(img.size[0]))
    h_size = int((float(img.size[1]) * float(w_percent)))
    img = img.resize((max_width, h_size), Image.Resampling.LANCZOS)
    
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=quality, optimize=True)
    size_kb = len(buffer.getvalue()) / 1024
    print(f"Optimized custom thumbnail size: {size_kb:.1f} KB")
    return f"data:image/jpeg;base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"

def publish_color_grading_post():
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    service = build('blogger', 'v3', credentials=creds)

    image_data_uri = optimize_and_encode_image(LOCAL_IMAGE)

    title = "The 3-Node Color Grading Secret: How to Get the Film Look in 2026 | Editzaar"
    search_desc = "Master the 3-node cinematic color grading formula for DaVinci Resolve and Premiere Pro. Learn exposure balancing, skin tones, and film contrast."
    primary_label = "video editing"

    html_content = f"""
<!-- SEO OpenGraph Meta -->
<meta name="description" content="{search_desc}" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{search_desc}" />
<meta property="og:type" content="article" />
<meta name="twitter:card" content="summary_large_image" />

<!-- Custom 3D Featured Cover Banner (Bebas Neue / Poppins Typography) -->
<div style="text-align: center; margin-bottom: 30px;">
    <img src="{image_data_uri}" 
         alt="3-Node Film Look Color Grading Secret - Editzaar" 
         style="width: 100%; max-height: 560px; object-fit: cover; border-radius: 14px; box-shadow: 0 10px 30px rgba(0,0,0,0.3);" />
</div>

<p style="font-size: 18px; line-height: 1.8; color: #222;">
    Have you ever slapped an expensive "Cinematic LUT" onto your video footage, only for your actor's face to turn bright orange and the shadows to look like muddy gray soup?
</p>
<p style="font-size: 17px; line-height: 1.8; color: #333;">
    LUTs aren't magic. Professional Hollywood colorists don't use 20 complicated adjustment layers—they use a clean, structured <strong>3-Node workflow</strong> that works on any camera (Sony, Canon, iPhone, or RED) in both <strong>DaVinci Resolve and Adobe Premiere Pro</strong>.
</p>
<p style="font-size: 17px; line-height: 1.8; color: #333;">
    Here is the exact 3-step color grading formula you can use today to make your videos look like they were shot on 35mm cinema film.
</p>

<hr style="border: 0; height: 1px; background: #eee; margin: 30px 0;"/>

<h2 style="font-size: 22px; color: #111;">Node 1: Exposure & White Balance (The Clean Base)</h2>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    Never apply a creative color look to raw, unbalanced footage. Your first node is strictly for technical correction:
</p>
<ul style="font-size: 16px; line-height: 1.8; color: #333;">
    <li><strong>Set Your Shadows (Lift):</strong> Pull down your blacks until they barely touch the 0 line on your Waveform monitor (don't crush them completely).</li>
    <li><strong>Set Your Highlights (Gain):</strong> Push your brights up to around 85–90 IRE so your scene feels alive and bright without blowing out skin highlights.</li>
    <li><strong>Neutralize White Balance:</strong> Pick a neutral gray or white object in the frame to remove unwanted green or magenta camera tints.</li>
</ul>

<h2 style="font-size: 22px; color: #111;">Node 2: The S-Curve & Color Separation</h2>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    Cinema cameras capture a very wide dynamic range that looks flat in Log. Node 2 brings back rich film contrast and color separation:
</p>
<ul style="font-size: 16px; line-height: 1.8; color: #333;">
    <li><strong>The Gentle S-Curve:</strong> Add a subtle S-curve in your RGB Curves tool. Slightly lift highlights and gently pin down shadows.</li>
    <li><strong>Color Boost vs. Saturation:</strong> Instead of cranking up normal Saturation (which makes skin look nuclear), use <em>Color Boost</em> (in DaVinci) or <em>Vibrance</em> (in Premiere). This only saturates dull colors while keeping human skin natural.</li>
</ul>

<h2 style="font-size: 22px; color: #111;">Node 3: The Creative Film Emulation (Teal & Orange Harmony)</h2>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    Now that your footage is balanced and contrasty, you apply the creative mood on Node 3:
</p>
<ol style="font-size: 16px; line-height: 1.8; color: #333;">
    <li><strong>Cool the Shadows:</strong> Push your <em>Lift / Shadows</em> wheel slightly towards cyan/teal (-5% to -10%).</li>
    <li><strong>Warm the Midtones & Skin:</strong> Push your <em>Gamma / Midtones</em> wheel towards warm golden amber.</li>
    <li><strong>Clean Highlights:</strong> Keep your highlights slightly warm or neutral so light bulbs and sky stay realistic.</li>
    <li><strong>Optional Film Grain:</strong> Add 35mm fine grain (around 20% opacity) to hide digital noise and give your digital sensor footage an organic texture.</li>
</ol>

<hr style="border: 0; height: 1px; background: #eee; margin: 30px 0;"/>

<h3 style="font-size: 20px; color: #111;">Why This 3-Node Method Works Every Time</h3>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    By separating <strong>Correction (Node 1)</strong>, <strong>Contrast (Node 2)</strong>, and <strong>Creative Look (Node 3)</strong>, you can grade 50 shots from different cameras in minutes just by copying Node 2 & 3 and tweaking Node 1 on each clip!
</p>

<!-- Branded Editzaar CTA Box -->
<div style="background-color: #f8f9fa; border: 2px solid #ff4b2b; padding: 25px; border-radius: 12px; margin: 35px 0; text-align: center;">
    <h3 style="margin-top: 0; font-size: 22px; color: #111;">Need Cinematic Edits & Color Grading for Your Brand?</h3>
    <p style="font-size: 15px; line-height: 1.6; max-width: 600px; margin: 10px auto 20px auto; color: #555;">
        At <strong>Editzaar</strong>, we handle full-cycle video production—from pacing and sound design to studio-grade cinematic color grading that elevates your content above the competition.
    </p>
    <a href="https://blog.editzaar.in/" style="background-color: #ff4b2b; color: #fff; padding: 12px 28px; text-decoration: none; font-weight: bold; border-radius: 30px; display: inline-block;">
        Explore More Masterclasses on Editzaar Blogs →
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
    print("SUCCESS: 3-NODE FILM LOOK ARTICLE DRAFTED ON BLOGGER!")
    print(f"Title: {result.get('title')}")
    print(f"Single Label: {result.get('labels')}")
    print(f"Location: {result.get('location', {}).get('name')}")
    print(f"Post ID: {result.get('id')}")
    print(f"Edit Link: https://www.blogger.com/blog/post/edit/{BLOG_ID}/{result.get('id')}")
    print("==================================================")

if __name__ == "__main__":
    publish_color_grading_post()
