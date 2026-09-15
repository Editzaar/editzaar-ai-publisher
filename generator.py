import os
import sys
import io
import time
import json
import base64
import urllib.request
import urllib.parse
from PIL import Image, ImageDraw, ImageFont
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

SCOPES = ['https://www.googleapis.com/auth/blogger']
BLOG_ID = '866286363471382851'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(BASE_DIR, 'token.json')

EXISTING_LABELS = ["video editing", "Growth Tips", "Content Strategy", "podcast", "Business Growth Tips", "Case Studies"]

def generate_custom_3d_thumbnail(title_text, subtitle_text="2026 CREATOR MASTERCLASS", theme="gold"):
    """
    Renders a custom 1280x720 16:9 3D graphic thumbnail for the exact topic.
    Uses bold typography, dark cinematic studio backdrop, neon accents, and glowing badges.
    """
    width, height = 1280, 720
    img = Image.new("RGB", (width, height), color=(10, 12, 18))
    draw = ImageDraw.Draw(img)

    themes = {
        "gold": ((22, 16, 10), (245, 158, 11), (255, 235, 59)),
        "purple": ((18, 10, 30), (168, 85, 247), (250, 204, 21)),
        "cyan": ((10, 22, 32), (6, 182, 212), (255, 255, 255)),
        "red": ((28, 10, 12), (239, 68, 68), (252, 211, 77)),
        "green": ((10, 24, 16), (34, 197, 94), (250, 204, 21)),
        "amber": ((24, 14, 8), (245, 158, 11), (254, 240, 138))
    }
    bg_color, accent_color, highlight_color = themes.get(theme, themes["gold"])

    # Radial background glow
    for r in range(480, 0, -12):
        glow = (
            int(bg_color[0] + (accent_color[0] - bg_color[0]) * (1 - r / 480)),
            int(bg_color[1] + (accent_color[1] - bg_color[1]) * (1 - r / 480)),
            int(bg_color[2] + (accent_color[2] - bg_color[2]) * (1 - r / 480))
        )
        draw.ellipse([width//2 - r*2, height//2 - r, width//2 + r*2, height//2 + r], fill=glow)

    # Studio grid background pattern
    for x in range(0, width, 70):
        draw.line([(x, 0), (x, height)], fill=(28, 35, 52), width=1)
    for y in range(0, height, 70):
        draw.line([(0, y), (width, y)], fill=(28, 35, 52), width=1)

    # Outer glowing frame
    draw.rounded_rectangle([20, 20, width - 20, height - 20], radius=22, outline=accent_color, width=4)

    # Top Brand Badge
    badge_w = 440
    draw.rounded_rectangle([width//2 - badge_w//2, 45, width//2 + badge_w//2, 100], radius=27, fill=(255, 75, 43))
    
    # Load fonts
    try:
        font_badge = ImageFont.truetype("impact.ttf", 26)
        font_main = ImageFont.truetype("impact.ttf", 60)
        font_sub = ImageFont.truetype("arialbd.ttf", 28)
    except:
        try:
            font_badge = ImageFont.truetype("arialbd.ttf", 24)
            font_main = ImageFont.truetype("arialbd.ttf", 50)
            font_sub = ImageFont.truetype("arial.ttf", 26)
        except:
            font_badge = ImageFont.load_default()
            font_main = ImageFont.load_default()
            font_sub = ImageFont.load_default()

    # Draw Badge Text
    badge_label = "EDITZAAR MASTERCLASS 2026"
    bbox = draw.textbbox((0, 0), badge_label, font=font_badge)
    bw = bbox[2] - bbox[0]
    draw.text(((width - bw) // 2, 58), badge_label, fill=(255, 255, 255), font=font_badge)

    # Format Main Title into clean lines
    clean_txt = title_text.upper().replace("| EDITZAAR", "").strip()
    words = clean_txt.split()
    lines = []
    curr = []
    for w in words:
        curr.append(w)
        if len(" ".join(curr)) > 20:
            lines.append(" ".join(curr))
            curr = []
    if curr:
        lines.append(" ".join(curr))
    lines = lines[:3]

    total_h = len(lines) * 80
    start_y = (height - total_h) // 2 + 15

    for idx, line in enumerate(lines):
        line_bbox = draw.textbbox((0, 0), line, font=font_main)
        lw = line_bbox[2] - line_bbox[0]
        tx = (width - lw) // 2
        ty = start_y + idx * 80
        
        # 3D Black Drop Shadow
        draw.text((tx + 4, ty + 4), line, fill=(0, 0, 0), font=font_main)
        
        # Line color
        color = (255, 255, 255) if idx % 2 == 0 else highlight_color
        draw.text((tx, ty), line, fill=color, font=font_main)

    # Bottom Subtitle Ribbon
    sub_bbox = draw.textbbox((0, 0), subtitle_text.upper(), font=font_sub)
    sw = sub_bbox[2] - sub_bbox[0]
    sub_x = (width - sw) // 2
    sub_y = height - 105

    draw.rounded_rectangle([sub_x - 25, sub_y - 6, sub_x + sw + 25, sub_y + 40], radius=18, fill=(15, 23, 42), outline=accent_color, width=2)
    draw.text((sub_x, sub_y), subtitle_text.upper(), fill=accent_color, font=font_sub)

    # Save to Buffer (compressed to ~85KB for 100% Blogger reliability)
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=80, optimize=True)
    return buffer.getvalue()

def build_deep_article_content(raw_topic, custom_label=None):
    topic = raw_topic.strip()
    topic_lower = topic.lower()

    # Determine Theme, Subtitle & Exact 1 Category Tag
    if custom_label and custom_label in EXISTING_LABELS:
        label = custom_label
    elif any(k in topic_lower for k in ["podcast", "interview", "audio", "mic", "sound design", "voiceover"]):
        label = "podcast"
    elif any(k in topic_lower for k in ["client", "money", "freelance", "business", "pricing", "portfolio"]):
        label = "Business Growth Tips"
    elif any(k in topic_lower for k in ["grow", "views", "stuck", "hook", "viral", "algorithm", "retention", "youtube", "reels", "capcut"]):
        label = "Growth Tips"
    elif any(k in topic_lower for k in ["case study", "breakdown", "analysis", "study"]):
        label = "Case Studies"
    elif any(k in topic_lower for k in ["strategy", "planning", "distribution", "calendar"]):
        label = "Content Strategy"
    else:
        label = "video editing"

    if any(k in topic_lower for k in ["ai tool", "ai video", "generation", "ganaration", "ganarator", "sora", "runway", "kling", "luma"]):
        theme = "cyan"
        subtitle = "TOP 10 AI VIDEO TOOLS IN 2026"
    elif any(k in topic_lower for k in ["podcast", "interview", "audio", "mic", "sound design", "voiceover"]):
        theme = "cyan"
        subtitle = "PRO AUDIO & SOUND DESIGN MASTERY"
    elif any(k in topic_lower for k in ["movie", "film", "pushpa", "kalki", "cinema", "stree", "blockbuster", "devara", "box office"]):
        theme = "gold"
        subtitle = "CINEMA EDITING & PACING SECRETS"
    elif any(k in topic_lower for k in ["after effects", "effect", "plugin", "vfx", "motion graphics", "animation"]):
        theme = "purple"
        subtitle = "PRO MOTION GRAPHICS BLUEPRINT"
    elif any(k in topic_lower for k in ["color", "grade", "lut", "davinci", "resolve", "cinematic look"]):
        theme = "amber"
        subtitle = "HOLLYWOOD COLOR GRADING SECRETS"
    elif any(k in topic_lower for k in ["client", "money", "freelance", "business", "pricing", "portfolio"]):
        theme = "green"
        subtitle = "CREATOR MONETIZATION & FREELANCING"
    elif any(k in topic_lower for k in ["grow", "views", "stuck", "hook", "viral", "algorithm", "retention", "youtube", "reels", "capcut"]):
        theme = "red"
        subtitle = "VIRAL RETENTION & PACKAGING BLUEPRINT"
    else:
        theme = "gold"
        subtitle = "CREATOR WORKFLOW & PACING GUIDE"

    clean_title = f"{topic} | Editzaar" if "editzaar" not in topic_lower else topic
    search_desc = f"Master {topic}. Detailed pacing formulas, timeline workflows, and creator tricks by Editzaar."[:145]

    # Generate Unique 3D Custom Thumbnail
    img_bytes = generate_custom_3d_thumbnail(topic, subtitle_text=subtitle, theme=theme)
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    image_data_uri = f"data:image/jpeg;base64,{img_base64}"

    # Build Extensive In-Depth Content Body based on topic semantics
    if any(k in topic_lower for k in ["ai tool", "ai video", "generation", "ganaration", "ganarator", "sora", "runway", "kling", "luma"]):
        sections = [
            ("1. Runway Gen-3 Alpha (Industry Standard Text-to-Video)", """
            Runway Gen-3 Alpha offers state-of-the-art camera motion control, physics simulation, and cinematic lighting fidelity. Editors use its motion brush and director mode to generate hyper-realistic B-roll and complex VFX backdrops in seconds without 3D software overhead.
            """),
            ("2. OpenAI Sora (Hyper-Realistic Long-Sequence Video)", """
            Sora's deep diffusion-transformer architecture excels at generating multi-angle, 60-second coherent video sequences with accurate real-world physics, reflections, and expressive character acting.
            """),
            ("3. Kling AI 1.5 (Complex Human Motion & Martial Arts Dynamics)", """
            Developed for high-energy motion, Kling AI produces fluid 1080p clips with zero limb distortion. It is the go-to tool for action sequences, cinematic camera fly-throughs, and dynamic product commercials.
            """),
            ("4. Luma Dream Machine 1.5 (Fluid Camera Pans & 3D Parallax)", """
            Luma excels in cinematic spatial camera tracks. It transforms single portrait images into dynamic 3D camera moves, creating high-end establishing shots and cinematic depth.
            """),
            ("5. Pika 2.0 (Pikaffects & Stylized Motion Overlays)", """
            Pika 2.0 introduces creative physics mutations (melt, explode, squish, inflate) that modern video editors use to create viral micro-transitions and surreal scroll-stopping hooks on TikTok and Instagram Reels.
            """),
            ("6. HeyGen 3.0 (Photorealistic AI Avatars & Multi-Language Lip-Sync)", """
            For corporate explainers and educational channels, HeyGen provides studio-quality digital twins with 40+ language automatic lip-sync, eliminating expensive reshoots.
            """),
            ("7. Topaz Video AI 5 (AI Upscaling, Frame Interpolation & Motion Stabilization)", """
            Not a generator from scratch, but essential for AI video pipelines: Topaz Video AI turns 720p/1080p AI generated footage into crisp 4K 60fps ProRes files with artifact removal.
            """),
            ("8. Haiper AI 2.0 (Fast Concept Prototyping & Stylized 2D/3D)", """
            Haiper provides ultra-fast generation speeds for storyboarding, pre-visualization, and animated graphic assets.
            """),
            ("9. ElevenLabs AI Voice & SFX Studio", """
            Generates emotionally rich voiceovers, Foley sound effects, and atmospheric background audio synced directly to AI video clips.
            """),
            ("10. CapCut AI Smart Tools (Auto Reframe, AI Script-to-Video, Relight)", """
            CapCut integrates generative AI directly into your timeline, speeding up viral short-form editing by 3x.
            """)
        ]
        summary_table = """
        <table style="width: 100%; border-collapse: collapse; margin: 25px 0; font-size: 15px; color: #333;">
            <thead>
                <tr style="background: #f2f2f2; text-align: left;">
                    <th style="padding: 12px; border: 1px solid #ddd;">AI Tool</th>
                    <th style="padding: 12px; border: 1px solid #ddd;">Best For</th>
                    <th style="padding: 12px; border: 1px solid #ddd;">Key Strength</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Runway Gen-3 Alpha</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">Cinematic B-Roll & VFX</td>
                    <td style="padding: 10px; border: 1px solid #ddd;">Motion Brush & Camera Control</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Kling AI 1.5</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">Action & Human Motion</td>
                    <td style="padding: 10px; border: 1px solid #ddd;">Fluid physics with zero distortion</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Luma Dream Machine</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">3D Parallax & Camera Pans</td>
                    <td style="padding: 10px; border: 1px solid #ddd;">Smooth establishing shots</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Topaz Video AI 5</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">Upscaling & Enhancement</td>
                    <td style="padding: 10px; border: 1px solid #ddd;">4K ProRes clarity from AI clips</td>
                </tr>
            </tbody>
        </table>
        """
    elif any(k in topic_lower for k in ["movie", "film", "pushpa", "kalki", "cinema", "stree", "blockbuster"]):
        sections = [
            ("1. The S-Curve Speed Ramp Architecture", """
            Mass cinema action doesn't stay in constant slow motion. Top editors use a dynamic <strong>exponential S-curve</strong> on the timeline:
            <ul>
                <li><strong>The Lead-up (100% real-time):</strong> The character initiates movement (stepping out of a vehicle or raising a weapon).</li>
                <li><strong>The Velocity Flash (400%–600% acceleration):</strong> 3 to 5 frames of rapid motion that eliminate dead weight frames.</li>
                <li><strong>The Impact Freeze (24fps slow-mo):</strong> The exact moment of contact is stretched out in cinematic slow motion to maximize dramatic tension.</li>
            </ul>
            """),
            ("2. Single-Frame Impact Flashes (Optical Nerve Cues)", """
            On heavy strikes, explosions, or dramatic bass hits, editors insert a <strong>single-frame white flash or inverted color frame</strong>. This briefly over-saturates the viewer's optic nerve, making the physical cut feel exponentially more powerful than traditional straight cuts.
            """),
            ("3. The 'Audio Void' Hero Elevation Technique", """
            Before a major punchline or hero entry, the sound team cuts all ambient noise and background score for <strong>0.5 seconds of dead silence</strong>. This acoustic void resets the listener's hearing so that the following dialogue and bass theme hit with maximum resonance.
            """),
            ("4. Earthy Amber & Deep Cyan Color Palette", """
            Modern blockbusters avoid flat digital looks. Colorists push <strong>burnt amber highlights into skin tones and deep cool cyan into shadow curves</strong>, keeping blacks dense without crushing shadow detail.
            """),
            ("5. Low-Angle Tracking Dissolves", """
            To establish sheer dominance, low-angle tracking shots moving forward are dissolved directly into aerial wide drone shots moving backward. This dual-axis motion contrast creates massive cinematic scale.
            """)
        ]
        summary_table = """
        <table style="width: 100%; border-collapse: collapse; margin: 25px 0; font-size: 15px; color: #333;">
            <thead>
                <tr style="background: #f2f2f2; text-align: left;">
                    <th style="padding: 12px; border: 1px solid #ddd;">Technique</th>
                    <th style="padding: 12px; border: 1px solid #ddd;">How It Works</th>
                    <th style="padding: 12px; border: 1px solid #ddd;">Creator Application</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>S-Curve Ramps</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">Fast snap into slow impact</td>
                    <td style="padding: 10px; border: 1px solid #ddd;">Use on B-roll reveals and gym/action Reels</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Audio Void</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">0.5s silence before drop</td>
                    <td style="padding: 10px; border: 1px solid #ddd;">Cut music completely before important value statements</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Impact Flashes</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">1-frame white/inverted flash</td>
                    <td style="padding: 10px; border: 1px solid #ddd;">Sync with whoosh-hits on major headline popups</td>
                </tr>
            </tbody>
        </table>
        """
    elif any(k in topic_lower for k in ["after effects", "plugin", "effect", "vfx", "motion graphics"]):
        sections = [
            ("1. Deep Glow (Plugin)", "Calculates inverse-square optical falloff with chromatic aberration. Turns flat text and vector lines into realistic glowing neon elements in 1 click."),
            ("2. RSMB / ReelSmart Motion Blur (Plugin)", "Applies realistic optical motion blur to pre-rendered clips and 2D/3D animations without slow render times."),
            ("3. Turbulent Displace (Native)", "Keyframe the Evolution parameter to produce liquid reveals, heatwaves, and organic hand-drawn outlines."),
            ("4. Displacement Map (Native)", "Combined with fractal noise, creates cyber glitch cuts, digital static, and glass lens refractions."),
            ("5. Optics Compensation (Native)", "Reverse lens distortion allows you to build fisheye warp-zoom transitions between talking head shots and B-roll."),
            ("6. Sapphire S_Shake (Plugin)", "Directional camera shakes with RGB split and motion blur synced to sound design hits."),
            ("7. Posterize Time (Native)", "Drop frame rates to 12fps/15fps for stylized anime and Spider-Verse aesthetic."),
            ("8. BCC Fast Film Glow (Plugin)", "Creates dreamy 90s vintage film bloom on highlights and skin."),
            ("9. CC Particle World (Native)", "Adds volumetric dust particles and floating embers to flat 2D graphic scenes."),
            ("10. CC Radial Fast Blur (Native)", "Produces volumetric god rays and dramatic lighting leaking around logos.")
        ]
        summary_table = ""
    elif any(k in topic_lower for k in ["podcast", "interview", "audio", "mic"]):
        sections = [
            ("1. The Editing Podcast (Hayden Hillier-Smith & Jordan Orme)", "Hosted by editors for Logan Paul & MrBeast. Focuses on YouTube retention curves, pacing, and creator monetization."),
            ("2. The Rough Cut (Matt Feury)", "Deep interviews with Hollywood editors behind Dune, Oppenheimer, and Marvel films."),
            ("3. Art of the Cut (Steve Hullfish)", "Master-level craft conversations focusing on dialogue trimming, timeline organization, and bin management."),
            ("4. Film Riot Podcast (Ryan Connolly)", "Practical DIY visual effects, low-budget filmmaking hacks, and staying creative under tight deadlines."),
            ("5. Team Deakins (Roger & James Deakins)", "Two-time Oscar winner Roger Deakins discusses lighting, camera lenses, and visual continuity.")
        ]
        summary_table = ""
    elif any(k in topic_lower for k in ["color", "grade", "lut", "davinci"]):
        sections = [
            ("1. The 3-Node Film Look Tree Structure", "Node 1: Exposure & Contrast balancing (Lift/Gamma/Gain). Node 2: Color Temperature & Skin-Tone isolation. Node 3: Film Look Print Emulation (Kodak 2383 / Fuji 3513)."),
            ("2. Protecting Skin Tones on the Vectorscope", "Keep skin tones aligned strictly along the flesh line indicator regardless of ambient lighting."),
            ("3. Halation & Film Grain Application", "Place halation before grain to simulate red optical bleed on high-contrast highlight edges.")
        ]
        summary_table = ""
    else:
        sections = [
            (f"1. Core Fundamentals & Strategic Setup for {topic}", f"Before touching the timeline, establish clear structure and assets for {topic}. Proper project organization, proxy workflows, and audio track routing save 40% of editing time."),
            (f"2. Pacing & Rhythm Optimization", "Cut on action rather than dialogue pauses. Tighten pauses between sentences to maintain high viewer dopamine without feeling rushed."),
            (f"3. Audio Layering & Sound Design Hierarchy", "Sound drives 70% of perceived video quality. Use a 3-layer audio hierarchy: Dialogue at -6dB to -10dB, Sound Effects (risers, whooshes, impacts) at -14dB, and Background Music ducked to -22dB."),
            (f"4. Visual Cues & Retention Hooks", "Introduce pattern interrupts every 4 to 6 seconds: subtle scale punch-ins (105%), dynamic overlays, or directional text popups to prevent viewer fatigue."),
            (f"5. Common Mistakes to Avoid & Pro Tips", "Avoid over-editing with distracting transitions when simple J-cuts and L-cuts tell a cleaner story. Always color grade on calibrated monitors and test exports on mobile screens.")
        ]
        summary_table = f"""
        <table style="width: 100%; border-collapse: collapse; margin: 25px 0; font-size: 15px; color: #333;">
            <thead>
                <tr style="background: #f2f2f2; text-align: left;">
                    <th style="padding: 12px; border: 1px solid #ddd;">Phase</th>
                    <th style="padding: 12px; border: 1px solid #ddd;">Best Practice</th>
                    <th style="padding: 12px; border: 1px solid #ddd;">Expected Creator Outcome</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Assembly</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">Tight rough cut, remove filler</td>
                    <td style="padding: 10px; border: 1px solid #ddd;">Strong narrative pacing</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Sound Design</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">Whooshes, hits, ambient ducking</td>
                    <td style="padding: 10px; border: 1px solid #ddd;">High production value</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Export & Packaging</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">Mobile-tested high bitrate H.264/H.265</td>
                    <td style="padding: 10px; border: 1px solid #ddd;">Crisp playback across all platforms</td>
                </tr>
            </tbody>
        </table>
        """

    # Build Sections HTML
    body_sections_html = ""
    for heading, body in sections:
        body_sections_html += f"""
<h2 style="font-size: 22px; color: #111; margin-top: 30px;">{heading}</h2>
<p style="font-size: 16px; line-height: 1.8; color: #333;">{body}</p>
"""

    full_html = f"""
<!-- SEO OpenGraph Meta -->
<meta name="description" content="{search_desc}" />
<meta property="og:title" content="{clean_title}" />
<meta property="og:description" content="{search_desc}" />
<meta property="og:type" content="article" />
<meta name="twitter:card" content="summary_large_image" />

<!-- Custom 3D Dynamic Cover Banner (100% Reliable, Zero Broken Links) -->
<div style="text-align: center; margin-bottom: 30px;">
    <img src="{image_data_uri}" 
         alt="{clean_title}" 
         style="width: 100%; max-height: 560px; object-fit: cover; border-radius: 14px; box-shadow: 0 10px 30px rgba(0,0,0,0.3);" />
</div>

<p style="font-size: 18px; line-height: 1.8; color: #222;">
    Mastering <strong>{topic}</strong> is one of the highest-leverage skills you can build as a modern creator in 2026. Whether you cut videos for YouTube, Instagram Reels, or commercial clients, true growth comes down to intentional pacing, sound design, and emotional rhythm.
</p>
<p style="font-size: 17px; line-height: 1.8; color: #333;">
    In this in-depth breakdown, we dissect the exact formulas, tools, and technical workflows that you can apply directly to your next project.
</p>

<hr style="border: 0; height: 1px; background: #eee; margin: 30px 0;"/>

{body_sections_html}

{summary_table}

<hr style="border: 0; height: 1px; background: #eee; margin: 30px 0;"/>

<!-- Branded Editzaar CTA Box -->
<div style="background-color: #f8f9fa; border: 2px solid #ff4b2b; padding: 25px; border-radius: 12px; margin: 35px 0; text-align: center;">
    <h3 style="margin-top: 0; font-size: 22px; color: #111;">Want Viral Video Edits for Your Brand?</h3>
    <p style="font-size: 15px; line-height: 1.6; max-width: 600px; margin: 10px auto 20px auto; color: #555;">
        At <strong>Editzaar</strong>, we craft high-retention video edits, viral storytelling cuts, and creator growth blueprints that save you hours every week.
    </p>
    <a href="https://blog.editzaar.in/" style="background-color: #ff4b2b; color: #fff; padding: 12px 28px; text-decoration: none; font-weight: bold; border-radius: 30px; display: inline-block;">
        Explore More Guides on Editzaar Blogs →
    </a>
</div>
"""

    return {
        "title": clean_title,
        "content": full_html,
        "label": label,
        "location": "India",
        "search_desc": search_desc,
        "img_bytes": img_bytes
    }

# Alias for backwards compatibility
build_deep_comprehensive_article = build_deep_article_content

def post_article_to_blogger(article_data):
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    service = build('blogger', 'v3', credentials=creds)

    body = {
        "title": article_data["title"],
        "content": article_data["content"],
        "labels": [article_data["label"]],
        "location": {
            "name": "India",
            "lat": 20.5937,
            "lng": 78.9629
        },
        "customMetaData": article_data["search_desc"]
    }

    result = service.posts().insert(blogId=BLOG_ID, body=body, isDraft=True).execute()
    post_id = result.get('id')
    edit_url = f"https://www.blogger.com/blog/post/edit/{BLOG_ID}/{post_id}"
    return edit_url, post_id

def generate_and_post_article(topic, custom_label=None):
    article_data = build_deep_article_content(topic, custom_label=custom_label)
    edit_url, post_id = post_article_to_blogger(article_data)
    return {
        "success": True,
        "title": article_data["title"],
        "label": article_data["label"],
        "location": article_data["location"],
        "edit_url": edit_url,
        "post_id": post_id,
        "search_desc": article_data["search_desc"]
    }
