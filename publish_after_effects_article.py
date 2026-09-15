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
LOCAL_IMAGE = os.path.join(r"C:\Users\Lenovo\.gemini\antigravity\brain\eb4fd464-2aa1-422b-97e6-fc0b916786b7", "after_effects_top_10_effects_cover_1789416870509.jpg")

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

def publish_after_effects_post():
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    service = build('blogger', 'v3', credentials=creds)

    image_data_uri = optimize_and_encode_image(LOCAL_IMAGE)

    title = "Top 10 Most Useful After Effects Plugins & Effects Every Video Editor Needs | Editzaar"
    search_desc = "Discover the top 10 most useful After Effects effects and plugins in 2026: Deep Glow, RSMB, Turbulent Displace, S_Shake & more. Level up your edits."
    primary_label = "video editing"  # Exact single tag on blog.editzaar.in

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
         alt="Top 10 Most Useful After Effects Plugins & Effects - Editzaar" 
         style="width: 100%; max-height: 560px; object-fit: cover; border-radius: 14px; box-shadow: 0 10px 30px rgba(0,0,0,0.3);" />
</div>

<p style="font-size: 18px; line-height: 1.8; color: #222;">
    Adobe After Effects has over 300 built-in effects and thousands of third-party plugins. But the truth is, <strong>90% of viral YouTube edits, motion graphics, and music videos rely on the exact same 10 powerhouse tools</strong>.
</p>
<p style="font-size: 17px; line-height: 1.8; color: #333;">
    Whether you want to add organic camera shake, cinematic glowing text, or realistic motion blur, here is the curated list of the <strong>Top 10 Most Useful After Effects Effects & Plugins</strong> that every editor should have in their workflow.
</p>

<hr style="border: 0; height: 1px; background: #eee; margin: 30px 0;"/>

<!-- Effect 1 -->
<h2 style="font-size: 22px; color: #111;">1. Deep Glow (Plugin) — The Gold Standard for Cinematic Glow</h2>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    Standard native <em>Glow</em> in After Effects looks flat and harsh. <strong>Deep Glow</strong> uses a physically accurate inverse-square falloff with chromatic aberration and gamma correction. It turns simple vector shapes and text into soft, high-end neon light sources in 1 click.
</p>

<!-- Effect 2 -->
<h2 style="font-size: 22px; color: #111;">2. RSMB / ReelSmart Motion Blur (Plugin) — Natural Motion Physics</h2>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    Enabling native motion blur on 50 complex layers will freeze your computer during rendering. <strong>RSMB</strong> tracks pixel motion vectors and applies natural, optical motion blur to pre-rendered footage, 3D animations, and text pop-ups with lightning-fast render speeds.
</p>

<!-- Effect 3 -->
<h2 style="font-size: 22px; color: #111;">3. Turbulent Displace (Built-In) — Organic Liquid & Smoke Motion</h2>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    One of the most versatile native tools in After Effects. By keyframing the <em>Evolution</em> parameter, you can create:
</p>
<ul style="font-size: 16px; line-height: 1.8; color: #333;">
    <li>Wobbly hand-drawn cartoon outlines.</li>
    <li>Realistic water ripples and heatwave distortion.</li>
    <li>Organic fire and smoke displacement effects.</li>
</ul>

<!-- Effect 4 -->
<h2 style="font-size: 22px; color: #111;">4. Displacement Map (Built-In) — RGB Glitch & Glass Refraction</h2>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    Combined with a fractal noise layer, <strong>Displacement Map</strong> warps underlying pixels horizontally and vertically. It is the secret behind cyber glitch transitions, holographic HUD distortions, and magnifying glass refractions.
</p>

<!-- Effect 5 -->
<h2 style="font-size: 22px; color: #111;">5. Optics Compensation (Built-In) — The Fisheye Whip Zoom Hack</h2>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    Check <em>Reverse Lens Distortion</em> and crank up the <em>Field of View (FOV)</em> on an adjustment layer. Paired with a scale keyframe, this creates an aggressive fisheye warp-zoom transition that pulls viewers directly into your next scene.
</p>

<!-- Effect 6 -->
<h2 style="font-size: 22px; color: #111;">6. Sapphire S_Shake (Plugin) — Bass-Heavy Impact Camera Shakes</h2>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    Forget manual wiggle expressions. <strong>S_Shake</strong> allows you to dial in directional X/Y/Z camera shakes, tilt roll, motion blur, and RGB split. When timed to a gun shot, bass drop, or impact hit, it makes action scenes hit 10x harder.
</p>

<!-- Effect 7 -->
<h2 style="font-size: 22px; color: #111;">7. Posterize Time (Built-In) — The Anime & Stop-Motion Aesthetic</h2>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    Drop <strong>Posterize Time</strong> onto a 60fps layer and set the Frame Rate to <strong>12fps or 15fps</strong>. This instantly converts smooth digital footage into the stylized, hand-drawn frame rate made famous by <em>Spider-Man: Into the Spider-Verse</em>.
</p>

<!-- Effect 8 -->
<h2 style="font-size: 22px; color: #111;">8. BCC Fast Film Glow (Plugin) — Dreamy Halation & Highlights</h2>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    Boris FX’s <strong>Fast Film Glow</strong> targets only the brightest highlights in your footage, blooming them gently across the frame. It is the go-to tool for creating a 90s vintage film vibe or dreamy music video aesthetic.
</p>

<!-- Effect 9 -->
<h2 style="font-size: 22px; color: #111;">9. CC Particle World (Built-In) — 3D Dust, Sparks & Atmospheric Depth</h2>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    Flat graphic titles feel empty without depth. A subtle emitter of slow-moving floating dust motes or glowing embers created with <strong>CC Particle World</strong> instantly turns flat graphics into a 3D cinematic space.
</p>

<!-- Effect 10 -->
<h2 style="font-size: 22px; color: #111;">10. CC Radial Fast Blur (Built-In) — God Rays & Light Leaks</h2>
<p style="font-size: 16px; line-height: 1.7; color: #333;">
    Change the mode to <em>Brightest</em>, drag the center point towards your light source, and you will get volumetric sun rays shining through windows or around logos in real-time.
</p>

<hr style="border: 0; height: 1px; background: #eee; margin: 30px 0;"/>

<!-- Comparison Table -->
<h2 style="font-size: 22px; color: #111;">Quick Cheat-Sheet for After Effects Editors</h2>
<table style="width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 15px; color: #333;">
    <thead>
        <tr style="background: #f2f2f2; text-align: left;">
            <th style="padding: 12px; border: 1px solid #ddd;">Effect / Plugin</th>
            <th style="padding: 12px; border: 1px solid #ddd;">Type</th>
            <th style="padding: 12px; border: 1px solid #ddd;">Best Use Case</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;"><strong>Deep Glow</strong></td>
            <td style="padding: 10px; border: 1px solid #ddd;">Plugin</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Realistic neon titles & light falloff</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;"><strong>RSMB</strong></td>
            <td style="padding: 10px; border: 1px solid #ddd;">Plugin</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Fast optical motion blur on animations</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;"><strong>Turbulent Displace</strong></td>
            <td style="padding: 10px; border: 1px solid #ddd;">Built-in</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Liquid text reveals & organic heat distortion</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;"><strong>Displacement Map</strong></td>
            <td style="padding: 10px; border: 1px solid #ddd;">Built-in</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Glitch transitions & glass refractions</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;"><strong>Optics Compensation</strong></td>
            <td style="padding: 10px; border: 1px solid #ddd;">Built-in</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Fisheye whip zooms & warp transitions</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;"><strong>Sapphire S_Shake</strong></td>
            <td style="padding: 10px; border: 1px solid #ddd;">Plugin</td>
            <td style="padding: 10px; border: 1px solid #ddd;">High-impact bass-drop camera shakes</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;"><strong>Posterize Time</strong></td>
            <td style="padding: 10px; border: 1px solid #ddd;">Built-in</td>
            <td style="padding: 10px; border: 1px solid #ddd;">12fps Spider-Verse anime stylization</td>
        </tr>
    </tbody>
</table>

<hr style="border: 0; height: 1px; background: #eee; margin: 30px 0;"/>

<!-- Branded Editzaar CTA Box -->
<div style="background-color: #f8f9fa; border: 2px solid #ff4b2b; padding: 25px; border-radius: 12px; margin: 35px 0; text-align: center;">
    <h3 style="margin-top: 0; font-size: 22px; color: #111;">Want High-End Motion Graphics for Your Content?</h3>
    <p style="font-size: 15px; line-height: 1.6; max-width: 600px; margin: 10px auto 20px auto; color: #555;">
        At <strong>Editzaar</strong>, we craft custom After Effects animations, motion graphics, and viral storytelling cuts that make your brand stand out.
    </p>
    <a href="https://blog.editzaar.in/" style="background-color: #ff4b2b; color: #fff; padding: 12px 28px; text-decoration: none; font-weight: bold; border-radius: 30px; display: inline-block;">
        Explore More After Effects Masterclasses on Editzaar →
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
    print("SUCCESS: TOP 10 AFTER EFFECTS POST DRAFTED ON BLOGGER!")
    print(f"Title: {result.get('title')}")
    print(f"Single Label: {result.get('labels')}")
    print(f"Location: {result.get('location', {}).get('name')}")
    print(f"Post ID: {result.get('id')}")
    print(f"Edit Link: https://www.blogger.com/blog/post/edit/{BLOG_ID}/{result.get('id')}")
    print("==================================================")

if __name__ == "__main__":
    publish_after_effects_post()
