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
LOCAL_IMAGE = os.path.join(r"C:\Users\Lenovo\.gemini\antigravity\brain\eb4fd464-2aa1-422b-97e6-fc0b916786b7", "top_5_trending_movies_cover_1789415108084.jpg")

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

def publish_trending_movies_post():
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    service = build('blogger', 'v3', credentials=creds)

    image_data_uri = optimize_and_encode_image(LOCAL_IMAGE)

    title = "Top 5 Trending Blockbuster Movies in 2026: Editing & Cinematography Breakdown | Editzaar"
    search_desc = "Top 5 trending blockbuster movies of 2026: Pushpa 2, Kalki 2898 AD, Stree 2 & more. Discover the cinematography, pacing, and video editing secrets."
    primary_label = "video editing"

    html_content = f"""
<!-- SEO OpenGraph Meta -->
<meta name="description" content="{search_desc}" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{search_desc}" />
<meta property="og:type" content="article" />
<meta name="twitter:card" content="summary_large_image" />

<!-- Custom 3D Featured Cover Banner (Bebas Neue Typography) -->
<div style="text-align: center; margin-bottom: 30px;">
    <img src="{image_data_uri}" 
         alt="Top 5 Trending Blockbuster Movies 2026 Editing Breakdown" 
         style="width: 100%; max-height: 560px; object-fit: cover; border-radius: 14px; box-shadow: 0 10px 30px rgba(0,0,0,0.3);" />
</div>

<p style="font-size: 18px; line-height: 1.8; color: #222;">
    2026 has been an extraordinary year for cinema. From ground-breaking Indian mytho-sci-fi epics to massive Hollywood crossovers, films aren't just breaking box office records—they are setting <strong>brand new benchmarks for cinematography, visual pacing, and sound design</strong>.
</p>
<p style="font-size: 17px; line-height: 1.8; color: #333;">
    Whether you are a filmmaker, YouTuber, or video editor looking to bring cinematic storytelling into your own videos, here is an in-depth breakdown of the <strong>Top 5 Trending Movies in 2026</strong> and the editing secrets behind their massive success.
</p>

<hr style="border: 0; height: 1px; background: #eee; margin: 30px 0;"/>

<!-- Movie 1 -->
<h2 style="font-size: 22px; color: #111;">1. Pushpa 2: The Rule — The Mass-Elevation Pacing Formula</h2>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    Allu Arjun and Sukumar’s <em>Pushpa 2: The Rule</em> is a masterclass in building relentless tension. 
</p>
<ul style="font-size: 16px; line-height: 1.8; color: #333;">
    <li><strong>S-Curve Speed Ramps:</strong> Action sequences don't stay in slow motion. The editor uses hyper-fast 400% speed snaps that suddenly freeze into 24fps slow-mo at the exact moment of physical impact.</li>
    <li><strong>The Gritty Color Palette:</strong> Deep burnt amber highlights, dusty crimson reds, and crushed forest shadows give every forest standoff a raw, tactile texture.</li>
    <li><strong>Audio Void Entry:</strong> Before Pushpa speaks a punchline, all ambient music completely cuts out for 0.5s of dead silence, making the following dialogue hit twice as hard.</li>
</ul>

<!-- Movie 2 -->
<h2 style="font-size: 22px; color: #111;">2. Kalki 2898 AD — Futuristic VFX & Complex Worldbuilding</h2>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    Nag Ashwin’s dystopian epic combines Indian mythology with high-tech futuristic warfare.
</p>
<ul style="font-size: 16px; line-height: 1.8; color: #333;">
    <li><strong>Seamless CGI-to-Live Action Blend:</strong> The editors maintain strict eye-line matching when transitioning from human close-ups (Prabhas / Amitabh Bachchan) into full-screen 3D vehicle battles.</li>
    <li><strong>Atmospheric Soundscapes:</strong> Multi-tiered sound design layering deep mechanical vehicle hums (-20dB) with crisp vocal dialogue.</li>
    <li><strong>Contrast Pacing:</strong> Fast-paced vehicular dogfights are balanced with grand, slow-dissolve wide shots of the dystopian Complex.</li>
</ul>

<!-- Movie 3 -->
<h2 style="font-size: 22px; color: #111;">3. Stree 2 — The Science of Horror-Comedy Timing</h2>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    Blending genuine jump scares with laugh-out-loud comedy is one of the hardest editing challenges in cinema.
</p>
<ul style="font-size: 16px; line-height: 1.8; color: #333;">
    <li><strong>The Extended Hold:</strong> The editor holds on awkward silence for 2 seconds longer than expected before cutting to Rajkummar Rao’s comedic reaction.</li>
    <li><strong>Micro-Jumpcuts for Scares:</strong> Disorienting 2-frame cuts during entity appearances trigger instant physical shock in audiences.</li>
</ul>

<!-- Movie 4 -->
<h2 style="font-size: 22px; color: #111;">4. Deadpool & Wolverine — Fourth-Wall Breaches & Match-Cuts</h2>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    The Marvel blockbuster relies heavily on rhythmic comedy and seamless multi-character combat.
</p>
<ul style="font-size: 16px; line-height: 1.8; color: #333;">
    <li><strong>Directional Motion Flow:</strong> If Wolverine slashes left-to-right, the camera immediately whips in the exact same direction into Deadpool’s counter-attack.</li>
    <li><strong>Pop-Music Contrast:</strong> Pairing brutal, fast-paced action choreography with upbeat 90s pop tracks creates high-energy entertainment.</li>
</ul>

<!-- Movie 5 -->
<h2 style="font-size: 22px; color: #111;">5. Devara: Part 1 — Water Physics & High-Octane Action</h2>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    Koratala Siva and Jr NTR deliver heavy sea-based action sequences that demand precise timeline speed control.
</p>
<ul style="font-size: 16px; line-height: 1.8; color: #333;">
    <li><strong>Slow-Motion Water Impacts:</strong> Blood mixing in dark stormy water rendered in high-contrast 120fps.</li>
    <li><strong>Low-Angle Tracking Dissolves:</strong> Low-angle camera sweeps make the protagonist appear larger than life against the stormy ocean horizon.</li>
</ul>

<hr style="border: 0; height: 1px; background: #eee; margin: 30px 0;"/>

<!-- Comparison Summary -->
<h2 style="font-size: 22px; color: #111;">Movie Editing Takeaways for Creators</h2>
<table style="width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 15px; color: #333;">
    <thead>
        <tr style="background: #f2f2f2; text-align: left;">
            <th style="padding: 12px; border: 1px solid #ddd;">Movie</th>
            <th style="padding: 12px; border: 1px solid #ddd;">Key Editing Technique</th>
            <th style="padding: 12px; border: 1px solid #ddd;">Creator Takeaway</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;"><strong>Pushpa 2</strong></td>
            <td style="padding: 10px; border: 1px solid #ddd;">S-Curve Speed Ramps</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Use fast speed snaps before slow-mo impacts in Reels</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;"><strong>Kalki 2898 AD</strong></td>
            <td style="padding: 10px; border: 1px solid #ddd;">Seamless Eye-line Matching</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Keep viewer's eyes in the same focal spot during B-roll cuts</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;"><strong>Stree 2</strong></td>
            <td style="padding: 10px; border: 1px solid #ddd;">Extended Reaction Pauses</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Let funny moments breathe without rushing</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;"><strong>Deadpool & Wolverine</strong></td>
            <td style="padding: 10px; border: 1px solid #ddd;">Directional Match Cuts</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Sync visual direction with high-energy music</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;"><strong>Devara: Part 1</strong></td>
            <td style="padding: 10px; border: 1px solid #ddd;">Low-Angle Scale Dissolves</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Shoot subjects from low angles to build authority</td>
        </tr>
    </tbody>
</table>

<hr style="border: 0; height: 1px; background: #eee; margin: 30px 0;"/>

<!-- Branded Editzaar CTA Box -->
<div style="background-color: #f8f9fa; border: 2px solid #ff4b2b; padding: 25px; border-radius: 12px; margin: 35px 0; text-align: center;">
    <h3 style="margin-top: 0; font-size: 22px; color: #111;">Want Cinematic Editing for Your Content?</h3>
    <p style="font-size: 15px; line-height: 1.6; max-width: 600px; margin: 10px auto 20px auto; color: #555;">
        At <strong>Editzaar</strong>, we bring big-screen filmmaking principles—pacing, sound design, and color grading—to YouTube channels, Reels, and creator brands.
    </p>
    <a href="https://blog.editzaar.in/" style="background-color: #ff4b2b; color: #fff; padding: 12px 28px; text-decoration: none; font-weight: bold; border-radius: 30px; display: inline-block;">
        Read More Film Masterclasses on Editzaar Blogs →
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
    print("SUCCESS: TOP 5 TRENDING MOVIES ARTICLE DRAFTED!")
    print(f"Title: {result.get('title')}")
    print(f"Single Label: {result.get('labels')}")
    print(f"Location: {result.get('location', {}).get('name')}")
    print(f"Post ID: {result.get('id')}")
    print(f"Edit Link: https://www.blogger.com/blog/post/edit/{BLOG_ID}/{result.get('id')}")
    print("==================================================")

if __name__ == "__main__":
    publish_trending_movies_post()
