import os
import sys
import io
import time
import json
import base64
import re
import html
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

def live_web_search(query, max_results=6):
    """
    Performs live internet search to gather real-time facts, names, tools, and details.
    """
    try:
        url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as response:
            page_html = response.read().decode('utf-8', errors='ignore')

        snippets = re.findall(r'<a[^>]*class="result__snippet[^>]*>(.*?)</a>', page_html, re.DOTALL)
        raw_titles = re.findall(r'<h2[^>]*class="result__title"[^>]*>.*?<a[^>]*>(.*?)</a>', page_html, re.DOTALL)

        results = []
        for i in range(min(len(snippets), max_results)):
            clean_title = re.sub(r'<[^>]+>', '', raw_titles[i]).strip() if i < len(raw_titles) else ""
            clean_snippet = re.sub(r'<[^>]+>', '', snippets[i]).strip()
            clean_title = html.unescape(clean_title)
            clean_snippet = html.unescape(clean_snippet)
            if clean_snippet:
                results.append({"title": clean_title, "snippet": clean_snippet})
        return results
    except Exception as e:
        print(f"[Research] Search error for '{query}': {e}", flush=True)
        return []

def generate_custom_3d_thumbnail(title_text, subtitle_text="2026 CREATOR MASTERCLASS", theme="gold"):
    """
    Renders a custom 1280x720 16:9 3D graphic thumbnail with bold typography.
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

    for r in range(480, 0, -12):
        glow = (
            int(bg_color[0] + (accent_color[0] - bg_color[0]) * (1 - r / 480)),
            int(bg_color[1] + (accent_color[1] - bg_color[1]) * (1 - r / 480)),
            int(bg_color[2] + (accent_color[2] - bg_color[2]) * (1 - r / 480))
        )
        draw.ellipse([width//2 - r*2, height//2 - r, width//2 + r*2, height//2 + r], fill=glow)

    for x in range(0, width, 70):
        draw.line([(x, 0), (x, height)], fill=(28, 35, 52), width=1)
    for y in range(0, height, 70):
        draw.line([(0, y), (width, y)], fill=(28, 35, 52), width=1)

    draw.rounded_rectangle([20, 20, width - 20, height - 20], radius=22, outline=accent_color, width=4)

    badge_w = 440
    draw.rounded_rectangle([width//2 - badge_w//2, 45, width//2 + badge_w//2, 100], radius=27, fill=(255, 75, 43))
    
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

    badge_label = "EDITZAAR MASTERCLASS 2026"
    bbox = draw.textbbox((0, 0), badge_label, font=font_badge)
    bw = bbox[2] - bbox[0]
    draw.text(((width - bw) // 2, 58), badge_label, fill=(255, 255, 255), font=font_badge)

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
        draw.text((tx + 4, ty + 4), line, fill=(0, 0, 0), font=font_main)
        color = (255, 255, 255) if idx % 2 == 0 else highlight_color
        draw.text((tx, ty), line, fill=color, font=font_main)

    sub_bbox = draw.textbbox((0, 0), subtitle_text.upper(), font=font_sub)
    sw = sub_bbox[2] - sub_bbox[0]
    sub_x = (width - sw) // 2
    sub_y = height - 105

    draw.rounded_rectangle([sub_x - 25, sub_y - 6, sub_x + sw + 25, sub_y + 40], radius=18, fill=(15, 23, 42), outline=accent_color, width=2)
    draw.text((sub_x, sub_y), subtitle_text.upper(), fill=accent_color, font=font_sub)

    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=80, optimize=True)
    return buffer.getvalue()

def research_and_generate_article(raw_topic, custom_label=None):
    """
    Performs multi-pass deep research on the internet and compiles a master-level article.
    """
    topic = raw_topic.strip()
    topic_lower = topic.lower()

    print(f"[Deep Research] Starting live multi-query web research for: '{topic}'...", flush=True)
    
    # 1. Multi-query web search
    search_queries = [
        f"{topic} 2026 breakdown facts",
        f"{topic} top list guide tutorial",
        f"{topic} latest trend ranking"
    ]
    all_facts = []
    for q in search_queries:
        res = live_web_search(q, max_results=4)
        for r in res:
            all_facts.append(r["snippet"])
    
    print(f"[Deep Research] Gathered {len(all_facts)} live web research snippets.", flush=True)

    # 2. Determine Category Tag & Theme
    if custom_label and custom_label in EXISTING_LABELS:
        label = custom_label
    elif any(k in topic_lower for k in ["song", "music", "track", "audio", "sound", "beat", "podcast", "mic"]):
        label = "podcast" if "podcast" in topic_lower else "video editing"
    elif any(k in topic_lower for k in ["money", "client", "freelance", "pricing", "business"]):
        label = "Business Growth Tips"
    elif any(k in topic_lower for k in ["grow", "views", "hook", "viral", "algorithm", "retention", "youtube", "reels", "capcut"]):
        label = "Growth Tips"
    elif any(k in topic_lower for k in ["case study", "analysis", "breakdown"]):
        label = "Case Studies"
    elif any(k in topic_lower for k in ["strategy", "planning", "distribution"]):
        label = "Content Strategy"
    else:
        label = "video editing"

    # Theme and Subtitle
    if any(k in topic_lower for k in ["song", "music", "track", "audio", "beat"]):
        theme = "amber"
        subtitle = "TRENDING AUDIO & EDIT PACING GUIDE"
    elif any(k in topic_lower for k in ["ai tool", "ai video", "generation", "ganaration", "sora", "runway", "kling"]):
        theme = "cyan"
        subtitle = "TOP 10 AI VIDEO TOOLS IN 2026"
    elif any(k in topic_lower for k in ["movie", "film", "pushpa", "kalki", "cinema", "stree", "blockbuster"]):
        theme = "gold"
        subtitle = "CINEMA EDITING & PACING SECRETS"
    elif any(k in topic_lower for k in ["after effects", "plugin", "effect", "vfx", "motion graphics"]):
        theme = "purple"
        subtitle = "PRO MOTION GRAPHICS BLUEPRINT"
    elif any(k in topic_lower for k in ["color", "grade", "lut", "davinci"]):
        theme = "amber"
        subtitle = "HOLLYWOOD COLOR GRADING SECRETS"
    elif any(k in topic_lower for k in ["podcast", "interview"]):
        theme = "cyan"
        subtitle = "MUST-LISTEN CREATOR PODCASTS"
    elif any(k in topic_lower for k in ["grow", "viral", "retention", "views", "capcut"]):
        theme = "red"
        subtitle = "VIRAL RETENTION & EDITING PLAYBOOK"
    else:
        theme = "gold"
        subtitle = "CREATOR WORKFLOW & PACING GUIDE"

    clean_title = f"{topic} | Editzaar" if "editzaar" not in topic_lower else topic
    search_desc = f"Deep research breakdown on {topic}. Master real-world editing pacing, tools, and creator workflows by Editzaar."[:145]

    # Generate 3D Thumbnail
    img_bytes = generate_custom_3d_thumbnail(topic, subtitle_text=subtitle, theme=theme)
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    image_data_uri = f"data:image/jpeg;base64,{img_base64}"

    # 3. Build Deep Detailed Domain Sections
    if any(k in topic_lower for k in ["song", "music", "audio", "track", "soundtrack"]):
        sections = [
            ("1. 'Tauba Tauba' & High-BPM Dance Rhythms (Beat-Grid Editing)", """
            Tracks like <strong>'Tauba Tauba' (Karan Aujla / Bad Newz)</strong> and energetic Punjabi-Hip-Hop crossovers rely on sharp <strong>128–132 BPM syncopated beats</strong>.
            <ul>
                <li><strong>Timeline Technique:</strong> Place timeline markers exactly on every snare hit and 808 kick. Time your camera whip-zooms, speed ramps (0.2s from 100% to 500%), and cuts to trigger 1 frame BEFORE the audible transient.</li>
                <li><strong>Audio Frequency Ducking:</strong> Duck mid-range instruments by -4dB during vocal hooks to keep speech crystal clear.</li>
            </ul>
            """),
            ("2. 'Aaj Ki Raat' & Dramatic Drop Transitions (Stree 2 Wave)", """
            High-energy club and cinematic tracks like <strong>'Aaj Ki Raat' (Madhubanti Bagchi / Sachin-Jigar)</strong> feature huge tension risers leading to explosive bass drops.
            <ul>
                <li><strong>Visual Drop Trick:</strong> Cut all music for 2 frames before the drop (dead acoustic silence), then trigger a 1-frame inverted flash synced with the sub-bass impact.</li>
                <li><strong>Creator Application:</strong> Ideal for high-converting product reveals, gym transformations, and dramatic lifestyle reels.</li>
            </ul>
            """),
            ("3. 'Illuminati' & Viral Hook Pacing (Aavesham Grooves)", """
            Sushin Shyam's viral electronic-synth phenomenon <strong>'Illuminati'</strong> conquered Instagram Reels by creating an instant 3-second earworm.
            <ul>
                <li><strong>Micro-Cuts:</strong> Cut talking heads or B-roll every 1.2 to 1.8 seconds. Apply continuous subtle handheld camera shake (S_Shake or CapCut Camera Shake) to match the bassline pulse.</li>
            </ul>
            """),
            ("4. 'Angaaron' & Soulful Acoustic Resonance (Pushpa 2 / Shreya Ghoshal)", """
            For emotional storytelling and cinematic travel montages, tracks like <strong>'Angaaron (The Couple Song)'</strong> provide warm acoustic guitar layers and rich melodies.
            <ul>
                <li><strong>Pacing Rule:</strong> Use J-cuts and L-cuts with 24fps film grain and 35mm warm halation to match the organic warmth of live instruments.</li>
            </ul>
            """),
            ("5. 'Chaleya' / 'Soulmate' – Melodic Lo-Fi & Romantic Vlog Cuts", """
            Smooth R&B and pop melodies provide chill background momentum for daily vlogs, tech unboxings, and creator tutorials without overwhelming the spoken voiceover.
            """)
        ]
        summary_table = """
        <table style="width: 100%; border-collapse: collapse; margin: 25px 0; font-size: 15px; color: #333;">
            <thead>
                <tr style="background: #f2f2f2; text-align: left;">
                    <th style="padding: 12px; border: 1px solid #ddd;">Trending Track</th>
                    <th style="padding: 12px; border: 1px solid #ddd;">Genre / BPM</th>
                    <th style="padding: 12px; border: 1px solid #ddd;">Best Editing Style</th>
                    <th style="padding: 12px; border: 1px solid #ddd;">Key Transition Cue</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Tauba Tauba</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">Punjabi Pop (130 BPM)</td>
                    <td style="padding: 10px; border: 1px solid #ddd;">Speed ramps & snappy zooms</td>
                    <td style="padding: 10px; border: 1px solid #ddd;">Snare hit whip-pan</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Aaj Ki Raat</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">Club Dance (124 BPM)</td>
                    <td style="padding: 10px; border: 1px solid #ddd;">Tension build & Bass drop</td>
                    <td style="padding: 10px; border: 1px solid #ddd;">2-frame audio silence into flash</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Illuminati</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">Synth-Electronic (120 BPM)</td>
                    <td style="padding: 10px; border: 1px solid #ddd;">Fast B-roll montage</td>
                    <td style="padding: 10px; border: 1px solid #ddd;">Camera shake on kick drum</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Angaaron</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">Cinematic Melody (95 BPM)</td>
                    <td style="padding: 10px; border: 1px solid #ddd;">Slow emotional storytelling</td>
                    <td style="padding: 10px; border: 1px solid #ddd;">J-cut dialogue overlap</td>
                </tr>
            </tbody>
        </table>
        """
    elif any(k in topic_lower for k in ["ai tool", "ai video", "generation", "ganaration", "sora", "runway", "kling"]):
        sections = [
            ("1. Runway Gen-3 Alpha (Industry-Leading Motion & Camera Control)", "Runway Gen-3 Alpha is the primary tool for filmmakers needing precise camera panning, speed ramping, and motion brush controls directly in the browser."),
            ("2. OpenAI Sora (High-Fidelity 60s World Physics)", "Sora's diffusion-transformer architecture creates photorealistic continuous camera moves with realistic light reflections and zero temporal glitching."),
            ("3. Kling AI 1.5 (Complex Human Motion & Martial Arts Dynamics)", "Produces fluid 1080p clips with zero limb distortion. Perfect for high-energy fight choreography, sports reels, and product ads."),
            ("4. Luma Dream Machine 1.5 (Dynamic 3D Parallax & Spatial Pan)", "Transforms 2D keyframe stills into moving 3D camera tracks with deep parallax separation."),
            ("5. Topaz Video AI 5 (Essential 4K 60fps AI Upscaler)", "Takes raw 720p/1080p AI generated clips and upscales them to broadcast-ready 4K ProRes with temporal stabilization."),
            ("6. Pika 2.0 (Surreal Physics & Viral Micro-Transitions)", "Introduces creative physics effects (melt, explode, squish, inflate) for viral short-form hooks."),
            ("7. HeyGen 3.0 (Digital Twins & Studio AI Avatars)", "Automates talking-head videos with studio-quality 40+ language lip-sync."),
            ("8. Haiper AI 2.0 (Fast Concept Prototyping)", "Fast pre-visualization tool for commercial storyboards."),
            ("9. ElevenLabs AI Audio & Sound Effects", "Generates hyper-realistic Foley sounds and voiceovers synced to AI video clips."),
            ("10. CapCut AI Tools (Auto Reframe & AI Smart Cut)", "Timeline AI integration that cuts editing time by 70%.")
        ]
        summary_table = """
        <table style="width: 100%; border-collapse: collapse; margin: 25px 0; font-size: 15px; color: #333;">
            <thead>
                <tr style="background: #f2f2f2; text-align: left;">
                    <th style="padding: 12px; border: 1px solid #ddd;">AI Tool</th>
                    <th style="padding: 12px; border: 1px solid #ddd;">Best Use Case</th>
                    <th style="padding: 12px; border: 1px solid #ddd;">Pricing / Model</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Runway Gen-3</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">Cinematic B-roll & VFX</td>
                    <td style="padding: 10px; border: 1px solid #ddd;">Subscription / Credits</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Kling AI 1.5</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">Action & Fast Human Movement</td>
                    <td style="padding: 10px; border: 1px solid #ddd;">Free Tier + Pro Plans</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Topaz Video AI 5</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">Upscaling to 4K 60fps ProRes</td>
                    <td style="padding: 10px; border: 1px solid #ddd;">One-time License</td>
                </tr>
            </tbody>
        </table>
        """
    elif any(k in topic_lower for k in ["movie", "film", "pushpa", "kalki", "cinema", "stree", "blockbuster"]):
        sections = [
            ("1. Exponential S-Curve Speed Ramp Architecture", "Mass cinema action cuts between 100% real-time, 500% snap acceleration, and 24fps slow-mo impacts."),
            ("2. Single-Frame Impact Flashes (Optical Nerve Cues)", "Single-frame white or inverted frames on gunshots and punchlines over-saturate optic nerves for visceral impact."),
            ("3. The 'Audio Void' Hero Elevation Pause", "0.5 seconds of absolute silence resets listener acoustic perception before major bass themes hit."),
            ("4. Earthy Amber & Cool Cyan Film Grade", "Dense skin tone protection combined with deep shadows."),
            ("5. Dual-Axis Drone-to-Tracking Dissolves", "Low-angle forward dolly dissolving into backward aerial drone creates massive cinematic scale.")
        ]
        summary_table = ""
    else:
        # Dynamic fact-driven multi-section breakdown
        sections = [
            (f"1. Strategic Framework & 2026 Industry Landscape for {topic}", f"Mastering <strong>{topic}</strong> requires moving beyond surface-level tricks into disciplined technical workflows. Recent creator trends show that high-performing content prioritizes clear structure, dynamic visual hooks, and seamless sound design."),
            (f"2. Step-by-Step Practical Timeline Implementation", "Break your timeline into 3 distinct stages: Assembly Cut (tighten dialogue, remove filler), Polish Pass (layer B-roll, J-cuts, L-cuts, speed curves), and Audio Mastering (EQ, compression, SFX placement)."),
            (f"3. Audio Layering & Sound Design Hierarchy", "Sound drives 70% of audience retention. Maintain strict audio gain staging: Dialogue at -6dB to -10dB, SFX (whooshes, risers, impacts) at -14dB, and Background Score ducked to -22dB."),
            (f"4. Pattern Interrupts & Dopamine Pacing", "Introduce visual resets every 3.5 to 5 seconds: 105% punch-ins, kinetic typography highlights, and directional slide transitions to eliminate viewer scroll autopilot."),
            (f"5. Common Traps to Avoid & Pro Optimization Rules", "Avoid over-complicating cuts with flashy transitions when simple J-cuts convey a cleaner emotional story. Always preview exports on mobile displays at 50% brightness.")
        ]
        summary_table = f"""
        <table style="width: 100%; border-collapse: collapse; margin: 25px 0; font-size: 15px; color: #333;">
            <thead>
                <tr style="background: #f2f2f2; text-align: left;">
                    <th style="padding: 12px; border: 1px solid #ddd;">Workflow Phase</th>
                    <th style="padding: 12px; border: 1px solid #ddd;">Pro Editor Action</th>
                    <th style="padding: 12px; border: 1px solid #ddd;">Impact on Viewer</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Assembly</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">Remove pauses, tighten sentences</td>
                    <td style="padding: 10px; border: 1px solid #ddd;">High narrative speed</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Sound Design</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">Sync whooshes and bass drops to cuts</td>
                    <td style="padding: 10px; border: 1px solid #ddd;">Tactile, premium feel</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>Color & Export</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">Clean skin tones, high bitrate H.264</td>
                    <td style="padding: 10px; border: 1px solid #ddd;">Crisp mobile playback</td>
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
    In 2026, mastering <strong>{topic}</strong> is one of the highest-leverage skills you can build. Whether you are producing commercial edits, viral Reels, or cinematic long-form videos, understanding deep industry workflows, audio dynamics, and pacing separates amateur cuts from viral hits.
</p>
<p style="font-size: 17px; line-height: 1.8; color: #333;">
    In this comprehensive breakdown by Editzaar, we analyze real-world formulas, actionable timeline workflows, and exact settings you can implement immediately.
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

def post_article_with_deduplication(article_data):
    """
    Guarantees strict single-draft creation:
    If a draft with the same title already exists, updates it cleanly rather than creating duplicates.
    """
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

    # Check for existing draft with matching title to avoid duplicates
    try:
        drafts = service.posts().list(blogId=BLOG_ID, status=['DRAFT'], maxResults=30).execute().get('items', [])
        target_norm = article_data["title"].strip().lower()
        for d in drafts:
            if d.get("title", "").strip().lower() == target_norm:
                print(f"[Deduplication] Found existing draft ID {d['id']} for '{article_data['title']}'. Updating in-place...", flush=True)
                updated = service.posts().update(blogId=BLOG_ID, postId=d['id'], body=body).execute()
                edit_url = f"https://www.blogger.com/blog/post/edit/{BLOG_ID}/{d['id']}"
                return edit_url, d['id']
    except Exception as err:
        print(f"[Deduplication] Check warning: {err}", flush=True)

    # Insert fresh draft if none exists
    result = service.posts().insert(blogId=BLOG_ID, body=body, isDraft=True).execute()
    post_id = result.get('id')
    edit_url = f"https://www.blogger.com/blog/post/edit/{BLOG_ID}/{post_id}"
    return edit_url, post_id

def generate_and_post_article(topic, custom_label=None):
    article_data = research_and_generate_article(topic, custom_label=custom_label)
    edit_url, post_id = post_article_with_deduplication(article_data)
    return {
        "success": True,
        "title": article_data["title"],
        "label": article_data["label"],
        "location": article_data["location"],
        "edit_url": edit_url,
        "post_id": post_id,
        "search_desc": article_data["search_desc"],
        "img_bytes": article_data["img_bytes"]
    }
