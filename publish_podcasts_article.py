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
LOCAL_IMAGE = os.path.join(r"C:\Users\Lenovo\.gemini\antigravity\brain\eb4fd464-2aa1-422b-97e6-fc0b916786b7", "top_5_podcasts_video_editors_cover_1789416029734.jpg")

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

def publish_podcasts_post():
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    service = build('blogger', 'v3', credentials=creds)

    image_data_uri = optimize_and_encode_image(LOCAL_IMAGE)

    title = "Top 5 Podcasts Every Video Editor Must Listen to in 2026 | Editzaar"
    search_desc = "Discover the top 5 video editing podcasts in 2026: The Editing Podcast, The Rough Cut, Art of the Cut, Film Riot & Team Deakins. Level up your skills."
    primary_label = "podcast"  # Exact matching category on blog.editzaar.in

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
         alt="Top 5 Podcasts for Video Editors 2026" 
         style="width: 100%; max-height: 560px; object-fit: cover; border-radius: 14px; box-shadow: 0 10px 30px rgba(0,0,0,0.3);" />
</div>

<p style="font-size: 18px; line-height: 1.8; color: #222;">
    You can watch hundreds of 60-second software tutorials on YouTube, but real growth as an editor happens when you understand <strong>the psychology of storytelling, director-editor collaboration, and timeline pacing</strong>.
</p>
<p style="font-size: 17px; line-height: 1.8; color: #333;">
    The easiest way to absorb master-level advice from editors who cut for MrBeast, Marvel movies, and Oscar-winning directors is through long-form podcasts. Here are the <strong>Top 5 Podcasts Every Video Editor Should Listen to in 2026</strong>.
</p>

<hr style="border: 0; height: 1px; background: #eee; margin: 30px 0;"/>

<!-- Podcast 1 -->
<h2 style="font-size: 22px; color: #111;">1. The Editing Podcast — Hosted by Hayden Hillier-Smith & Jordan Orme</h2>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    If you edit for YouTube, Reels, or TikTok, this is the #1 podcast in the world for you. 
</p>
<ul style="font-size: 16px; line-height: 1.8; color: #333;">
    <li><strong>Who the Hosts Are:</strong> Hayden Hillier-Smith (editor for Logan Paul, MrBeast, and Creator of the Year winner) and Jordan Orme (music video editor for Justin Bieber, Roddy Ricch).</li>
    <li><strong>What You Learn:</strong> The psychology of the YouTube retention curve, why viewers swipe away on specific frames, how to charge premium rates as a freelance editor, and interviews with top YouTube creators.</li>
    <li><strong>Best Episode to Start:</strong> Any breakdown on the <em>"MrBeast Retention Myth vs Storytelling"</em>.</li>
</ul>

<!-- Podcast 2 -->
<h2 style="font-size: 22px; color: #111;">2. The Rough Cut — Hosted by Matt Feury</h2>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    Produced in partnership with Avid, <strong>The Rough Cut</strong> brings you direct conversations with the actual editors behind Hollywood blockbusters.
</p>
<ul style="font-size: 16px; line-height: 1.8; color: #333;">
    <li><strong>Who the Host Is:</strong> Matt Feury, a veteran interviewer who dives deep into feature film timelines.</li>
    <li><strong>What You Learn:</strong> How editors cut massive films like <em>Dune, Oppenheimer, Spider-Man, and Stranger Things</em>. You hear how they handle 500 hours of raw footage, communicate with directors like Christopher Nolan, and build emotional tension.</li>
    <li><strong>Best For:</strong> Filmmakers, narrative editors, and documentary creators.</li>
</ul>

<!-- Podcast 3 -->
<h2 style="font-size: 22px; color: #111;">3. Art of the Cut — Hosted by Steve Hullfish</h2>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    Steve Hullfish has interviewed hundreds of the greatest editors of all time, and his podcast is a goldmine of practical craft knowledge.
</p>
<ul style="font-size: 16px; line-height: 1.8; color: #333;">
    <li><strong>What You Learn:</strong> Timeline organization systems, bin structures, trimming dialogue, cutting music cues, and how to manage the emotional fatigue of long edit sessions.</li>
    <li><strong>Key Takeaway:</strong> Practical timeline tips you can implement in Premiere, DaVinci, or Avid immediately.</li>
</ul>

<!-- Podcast 4 -->
<h2 style="font-size: 22px; color: #111;">4. Film Riot Podcast — Hosted by Ryan Connolly</h2>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    Film Riot has educated a generation of indie creators. The podcast features candid conversations with directors, VFX artists, stunt coordinators, and editors.
</p>
<ul style="font-size: 16px; line-height: 1.8; color: #333;">
    <li><strong>What You Learn:</strong> How to achieve big-budget visual effects and sound design on zero budget, problem-solving on tight deadlines, and staying creative.</li>
    <li><strong>Best For:</strong> Solo creators who shoot, edit, and color grade their own projects.</li>
</ul>

<!-- Podcast 5 -->
<h2 style="font-size: 22px; color: #111;">5. Team Deakins — Hosted by Roger & James Deakins</h2>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    Legendary 2-time Oscar-winning cinematographer Roger Deakins (<em>Blade Runner 2049, 1917, The Shawshank Redemption</em>) and his collaborator James Deakins host deep discussions on the entire filmmaking pipeline.
</p>
<ul style="font-size: 16px; line-height: 1.8; color: #333;">
    <li><strong>What You Learn:</strong> Understanding visual lighting, camera angles, color grading, and how cinematography directly influences editing rhythm.</li>
    <li><strong>Why Editors Should Listen:</strong> An editor who understands lighting and camera lenses will always make better cut decisions than someone who only knows software shortcuts.</li>
</ul>

<hr style="border: 0; height: 1px; background: #eee; margin: 30px 0;"/>

<!-- Summary Table -->
<h2 style="font-size: 22px; color: #111;">Quick Podcast Guide for Editors</h2>
<table style="width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 15px; color: #333;">
    <thead>
        <tr style="background: #f2f2f2; text-align: left;">
            <th style="padding: 12px; border: 1px solid #ddd;">Podcast Name</th>
            <th style="padding: 12px; border: 1px solid #ddd;">Hosts</th>
            <th style="padding: 12px; border: 1px solid #ddd;">Main Focus</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;"><strong>The Editing Podcast</strong></td>
            <td style="padding: 10px; border: 1px solid #ddd;">Hayden Hillier-Smith & Jordan Orme</td>
            <td style="padding: 10px; border: 1px solid #ddd;">YouTube Pacing & Creator Retention</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;"><strong>The Rough Cut</strong></td>
            <td style="padding: 10px; border: 1px solid #ddd;">Matt Feury</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Hollywood Blockbusters & Feature Films</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;"><strong>Art of the Cut</strong></td>
            <td style="padding: 10px; border: 1px solid #ddd;">Steve Hullfish</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Master-level Timeline & Dialogue Trimming</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;"><strong>Film Riot</strong></td>
            <td style="padding: 10px; border: 1px solid #ddd;">Ryan Connolly</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Indie VFX & DIY Filmmaking Hacks</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;"><strong>Team Deakins</strong></td>
            <td style="padding: 10px; border: 1px solid #ddd;">Roger & James Deakins</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Cinematography, Lighting & Visual Story</td>
        </tr>
    </tbody>
</table>

<hr style="border: 0; height: 1px; background: #eee; margin: 30px 0;"/>

<!-- Branded Editzaar CTA Box -->
<div style="background-color: #f8f9fa; border: 2px solid #ff4b2b; padding: 25px; border-radius: 12px; margin: 35px 0; text-align: center;">
    <h3 style="margin-top: 0; font-size: 22px; color: #111;">Want High-Level Video Editing for Your Channel?</h3>
    <p style="font-size: 15px; line-height: 1.6; max-width: 600px; margin: 10px auto 20px auto; color: #555;">
        At <strong>Editzaar</strong>, we apply the pacing and storytelling principles used by top creator editors to deliver high-retention YouTube videos and viral Reels.
    </p>
    <a href="https://blog.editzaar.in/" style="background-color: #ff4b2b; color: #fff; padding: 12px 28px; text-decoration: none; font-weight: bold; border-radius: 30px; display: inline-block;">
        Explore More Guides on Editzaar Blogs →
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
    print("SUCCESS: TOP 5 PODCASTS ARTICLE DRAFTED ON BLOGGER!")
    print(f"Title: {result.get('title')}")
    print(f"Single Label: {result.get('labels')}")
    print(f"Location: {result.get('location', {}).get('name')}")
    print(f"Post ID: {result.get('id')}")
    print(f"Edit Link: https://www.blogger.com/blog/post/edit/{BLOG_ID}/{result.get('id')}")
    print("==================================================")

if __name__ == "__main__":
    publish_podcasts_post()
