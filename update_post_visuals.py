import os
import sys
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

SCOPES = ['https://www.googleapis.com/auth/blogger']
BLOG_ID = '866286363471382851'
POST_ID = '8100417000655486753'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(BASE_DIR, 'token.json')

def update_with_high_curiosity_visuals():
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    service = build('blogger', 'v3', credentials=creds)

    title = "Top 5 AI Video Generators in 2026: Tested & Ranked for Creators | Editzaar"
    search_desc = "We tested the top 5 AI video generators in 2026: Runway Gen-3, OpenAI Sora, Kling AI, Luma Dream Machine & Hailuo. See which is best for creators."
    
    # 100% reliable, direct high-contrast visual URLs
    featured_banner_url = "https://images.unsplash.com/photo-1536240478700-b869070f9279?auto=format&fit=crop&w=1200&q=85"
    runway_camera_url = "https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?auto=format&fit=crop&w=1000&q=85"
    sora_cinematic_url = "https://images.unsplash.com/photo-1485846234645-a62644f84728?auto=format&fit=crop&w=1000&q=85"
    
    primary_label = "video editing"

    json_ld_schema = {
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": title,
        "description": search_desc,
        "image": featured_banner_url,
        "author": {"@type": "Organization", "name": "Editzaar", "url": "https://blog.editzaar.in/"},
        "publisher": {
            "@type": "Organization",
            "name": "Editzaar Blogs",
            "logo": {"@type": "ImageObject", "url": "https://blog.editzaar.in/favicon.ico"}
        }
    }

    html_content = f"""
<!-- SEO & OpenGraph Structured Metadata -->
<script type="application/ld+json">
{json.dumps(json_ld_schema, indent=2)}
</script>
<meta name="description" content="{search_desc}" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{search_desc}" />
<meta property="og:image" content="{featured_banner_url}" />
<meta property="og:type" content="article" />
<meta name="twitter:card" content="summary_large_image" />

<!-- High-Curiosity Featured Cover Banner -->
<div style="text-align: center; margin-bottom: 30px; position: relative;">
    <img src="{featured_banner_url}" 
         alt="AI Video Generation Studio Testing 2026" 
         style="width: 100%; max-height: 520px; object-fit: cover; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.15);" />
    <div style="background: rgba(0,0,0,0.75); color: #00e5ff; padding: 8px 16px; border-radius: 20px; display: inline-block; font-size: 13px; font-weight: bold; margin-top: 10px;">
        ⚡ 2026 AI Video Shootout: Photorealism vs Control
    </div>
</div>

<p style="font-size: 18px; line-height: 1.8; color: #222;">
    Just two years ago, AI video was notorious for melting hands, warped faces, and blurry morphs. But in 2026, text-to-video tools have evolved into <strong>virtual cinema studios</strong> capable of rendering crisp 4K footage, accurate motion physics, and cinematic lighting on demand.
</p>
<p style="font-size: 17px; line-height: 1.8; color: #333;">
    If you are a video editor or content creator, which AI tool actually produces usable B-roll without looking fake? We put the <strong>top 5 AI video generators</strong> to the test.
</p>

<hr style="border: 0; height: 1px; background: #eee; margin: 30px 0;"/>

<!-- Tool 1 -->
<h2 style="font-size: 22px; color: #111;">1. Runway Gen-3 Alpha: The Professional Editor's Secret Weapon</h2>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    <strong>Runway Gen-3</strong> is designed specifically for timeline editors. Instead of random video clips, it gives you exact directorial controls:
</p>
<ul style="font-size: 16px; line-height: 1.8; color: #333;">
    <li><strong>Motion Brush 2.0:</strong> Paint over water, fire, or clouds to tell the AI exactly which part of your frame should move.</li>
    <li><strong>Precise Camera Angles:</strong> Lock camera pan, tilt speed, and zoom rate so clips seamlessly cut with your real footage.</li>
    <li><strong>Image-to-Video:</strong> Converts Midjourney, Flux, or Photoshop concept art into realistic 10-second cinematic shots.</li>
</ul>

<div style="text-align: center; margin: 30px 0;">
    <img src="{runway_camera_url}" 
         alt="Directing camera movement and lighting in AI timeline" 
         style="width: 100%; max-height: 420px; object-fit: cover; border-radius: 10px; box-shadow: 0 4px 16px rgba(0,0,0,0.12);" />
    <p style="font-size: 13px; color: #777; margin-top: 8px;"><em>Direct camera controls allow creators to match AI B-roll with live-action shots.</em></p>
</div>

<!-- Tool 2 -->
<h2 style="font-size: 22px; color: #111;">2. OpenAI Sora: The Photorealism & Physics Powerhouse</h2>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    When you need a 60-second uninterrupted scene where light accurately bounces off wet pavement and shadows track naturally, <strong>Sora</strong> remains unmatched.
</p>
<ul style="font-size: 16px; line-height: 1.8; color: #333;">
    <li><strong>World Simulation:</strong> Objects maintain their identity even when moving behind trees or cars.</li>
    <li><strong>No Weird Morphs:</strong> Characters and background crowds interact with convincing physical weight.</li>
</ul>

<div style="text-align: center; margin: 30px 0;">
    <img src="{sora_cinematic_url}" 
         alt="Cinematic lighting and photorealistic filmmaking" 
         style="width: 100%; max-height: 420px; object-fit: cover; border-radius: 10px; box-shadow: 0 4px 16px rgba(0,0,0,0.12);" />
    <p style="font-size: 13px; color: #777; margin-top: 8px;"><em>Realistic reflections and light physics create believable establishing shots.</em></p>
</div>

<!-- Tool 3 -->
<h2 style="font-size: 22px; color: #111;">3. Kling AI: The Undisputed King of Human Movement</h2>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    Most AI video models struggle with human hands and fast movement. <strong>Kling AI</strong> solved this with realistic skeletal tracking:
</p>
<ul style="font-size: 16px; line-height: 1.8; color: #333;">
    <li><strong>Natural Limbs & Faces:</strong> People running, talking, and gesturing look convincing on phone screens.</li>
    <li><strong>Smooth 60fps Output:</strong> Fast motion without weird digital ghosting.</li>
</ul>

<!-- Tool 4 -->
<h2 style="font-size: 22px; color: #111;">4. Luma Dream Machine: Sweeping 3D Drone & Camera Moves</h2>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    If you need high-speed action, FPV drone dives through mountains, or 360-degree orbital camera rotations, <strong>Luma Dream Machine</strong> renders spatial 3D perspective effortlessly.
</p>

<!-- Tool 5 -->
<h2 style="font-size: 22px; color: #111;">5. Minimax (Hailuo AI): Best Budget B-Roll Generator</h2>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    <strong>Hailuo AI</strong> follows complex descriptive prompts word for word. If you specify <em>"35mm anamorphic lens, golden hour rim light, cinematic dust particles"</em>, it outputs exactly that texture without needing 20 prompt attempts.
</p>

<hr style="border: 0; height: 1px; background: #eee; margin: 30px 0;"/>

<!-- Comparison Table -->
<h2 style="font-size: 22px; color: #111;">The Quick Creator Decision Guide</h2>
<table style="width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 15px; color: #333;">
    <thead>
        <tr style="background: #f2f2f2; text-align: left;">
            <th style="padding: 12px; border: 1px solid #ddd;">Tool</th>
            <th style="padding: 12px; border: 1px solid #ddd;">Best For</th>
            <th style="padding: 12px; border: 1px solid #ddd;">Key Superpower</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;"><strong>Runway Gen-3</strong></td>
            <td style="padding: 10px; border: 1px solid #ddd;">Video Editors & Agencies</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Brush Motion & Directional Controls</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;"><strong>OpenAI Sora</strong></td>
            <td style="padding: 10px; border: 1px solid #ddd;">Narrative & Commercials</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Flawless Physics & 60s Consistency</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;"><strong>Kling AI</strong></td>
            <td style="padding: 10px; border: 1px solid #ddd;">Reels & Human Characters</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Realistic Faces & Natural Motion</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;"><strong>Luma Dream Machine</strong></td>
            <td style="padding: 10px; border: 1px solid #ddd;">Action Trailers & Travel</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Dynamic 3D Camera Angles</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;"><strong>Minimax Hailuo</strong></td>
            <td style="padding: 10px; border: 1px solid #ddd;">Quick YouTube B-Roll</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Exact Prompt Adherence</td>
        </tr>
    </tbody>
</table>

<hr style="border: 0; height: 1px; background: #eee; margin: 30px 0;"/>

<!-- Branded Editzaar CTA Box -->
<div style="background-color: #f8f9fa; border: 2px solid #ff4b2b; padding: 25px; border-radius: 12px; margin: 35px 0; text-align: center;">
    <h3 style="margin-top: 0; font-size: 22px; color: #111;">Want to Level Up Your Video Editing?</h3>
    <p style="font-size: 15px; line-height: 1.6; max-width: 600px; margin: 10px auto 20px auto; color: #555;">
        At <strong>Editzaar</strong>, we craft high-retention video edits, viral storytelling cuts, and growth blueprints for creators and brands.
    </p>
    <a href="https://blog.editzaar.in/" style="background-color: #ff4b2b; color: #fff; padding: 12px 28px; text-decoration: none; font-weight: bold; border-radius: 30px; display: inline-block;">
        Explore More Guides on Editzaar Blogs →
    </a>
</div>
"""

    post = service.posts().get(blogId=BLOG_ID, postId=POST_ID, view='ADMIN').execute()
    post['title'] = title
    post['content'] = html_content
    post['labels'] = [primary_label]
    post['location'] = {
        "name": "India",
        "lat": 20.5937,
        "lng": 78.9629
    }
    post['customMetaData'] = search_desc

    updated = service.posts().update(blogId=BLOG_ID, postId=POST_ID, body=post).execute()

    print("==================================================")
    print("SUCCESS: ARTICLE UPDATED WITH 100% RELIABLE HIGH-CURIOSITY VISUALS!")
    print(f"Post ID: {updated.get('id')}")
    print(f"Edit Link: https://www.blogger.com/blog/post/edit/{BLOG_ID}/{POST_ID}")
    print("==================================================")

if __name__ == "__main__":
    update_with_high_curiosity_visuals()
