import os
import sys
import io
import base64
import math
import random
from PIL import Image, ImageDraw, ImageFont

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def create_dynamic_3d_thumbnail(title_text, subtitle_text="2026 CREATOR MASTERCLASS", theme="cyan"):
    """
    Dynamically generates a unique, high-contrast 16:9 graphic thumbnail for ANY article topic.
    Includes glowing borders, gradient background, studio accents, and bold typography.
    """
    width, height = 1280, 720
    img = Image.new("RGB", (width, height), color=(12, 14, 20))
    draw = ImageDraw.Draw(img)

    # 1. Generate Cinematic Gradient Studio Background
    themes = {
        "cyan": ((15, 23, 42), (8, 145, 178), (255, 193, 7)),
        "amber": ((24, 15, 10), (217, 119, 6), (56, 189, 248)),
        "purple": ((20, 10, 30), (147, 51, 234), (250, 204, 21)),
        "red": ((25, 10, 15), (225, 29, 72), (251, 191, 36)),
        "green": ((10, 25, 18), (16, 185, 129), (245, 158, 11))
    }
    bg_color, accent_color, text_highlight = themes.get(theme, themes["cyan"])

    # Radial gradient glow in the center
    for r in range(400, 0, -10):
        alpha = int(35 * (1 - r / 400))
        glow_color = (
            int(bg_color[0] + (accent_color[0] - bg_color[0]) * (1 - r / 400)),
            int(bg_color[1] + (accent_color[1] - bg_color[1]) * (1 - r / 400)),
            int(bg_color[2] + (accent_color[2] - bg_color[2]) * (1 - r / 400))
        )
        draw.ellipse([width//2 - r*2, height//2 - r, width//2 + r*2, height//2 + r], fill=glow_color)

    # 2. Modern Studio Grid Lines
    grid_color = (30, 41, 59)
    for x in range(0, width, 80):
        draw.line([(x, 0), (x, height)], fill=grid_color, width=1)
    for y in range(0, height, 80):
        draw.line([(0, y), (width, y)], fill=grid_color, width=1)

    # 3. Outer Glowing Border
    draw.rounded_rectangle([20, 20, width - 20, height - 20], radius=24, outline=accent_color, width=4)

    # 4. Top Tag / Badge
    badge_bg = (255, 75, 43)
    draw.rounded_rectangle([width//2 - 200, 50, width//2 + 200, 100], radius=25, fill=badge_bg)
    
    # Fonts (Try loading Windows system fonts: Arial Black, Impact, Segoe UI Bold, or default)
    try:
        font_badge = ImageFont.truetype("impact.ttf", 26)
        font_main = ImageFont.truetype("impact.ttf", 64)
        font_sub = ImageFont.truetype("arialbd.ttf", 32)
    except:
        try:
            font_badge = ImageFont.truetype("arialbd.ttf", 24)
            font_main = ImageFont.truetype("arialbd.ttf", 54)
            font_sub = ImageFont.truetype("arial.ttf", 28)
        except:
            font_badge = ImageFont.load_default()
            font_main = ImageFont.load_default()
            font_sub = ImageFont.load_default()

    # Draw Badge Text
    badge_text = "EDITZAAR 2026 BREAKDOWN"
    bbox = draw.textbbox((0, 0), badge_text, font=font_badge)
    bw = bbox[2] - bbox[0]
    draw.text(((width - bw) // 2, 60), badge_text, fill=(255, 255, 255), font=font_badge)

    # 5. Format Main Title into 2 or 3 punchy lines
    words = title_text.upper().replace("| EDITZAAR", "").strip().split()
    lines = []
    curr_line = []
    for w in words:
        curr_line.append(w)
        if len(" ".join(curr_line)) > 24:
            lines.append(" ".join(curr_line))
            curr_line = []
    if curr_line:
        lines.append(" ".join(curr_line))

    lines = lines[:3]  # Max 3 lines
    total_text_height = len(lines) * 80
    start_y = (height - total_text_height) // 2 + 10

    for idx, line in enumerate(lines):
        line_bbox = draw.textbbox((0, 0), line, font=font_main)
        lw = line_bbox[2] - line_bbox[0]
        tx = (width - lw) // 2
        ty = start_y + idx * 80
        
        # 3D Drop Shadow
        draw.text((tx + 4, ty + 4), line, fill=(0, 0, 0), font=font_main)
        
        # Text color (Alternates between bright white and vibrant accent)
        t_color = (255, 255, 255) if idx % 2 == 0 else text_highlight
        draw.text((tx, ty), line, fill=t_color, font=font_main)

    # 6. Bottom Subtitle Ribbon
    sub_bbox = draw.textbbox((0, 0), subtitle_text.upper(), font=font_sub)
    sw = sub_bbox[2] - sub_bbox[0]
    sub_x = (width - sw) // 2
    sub_y = height - 110

    draw.rounded_rectangle([sub_x - 30, sub_y - 8, sub_x + sw + 30, sub_y + 42], radius=18, fill=(15, 23, 42), outline=accent_color, width=2)
    draw.text((sub_x, sub_y), subtitle_text.upper(), fill=accent_color, font=font_sub)

    # Save and optimize to Buffer
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=82, optimize=True)
    return buffer.getvalue()

if __name__ == "__main__":
    img_bytes = create_dynamic_3d_thumbnail("TOP 10 AFTER EFFECTS TRICKS", "PRO LEVEL MOTION GRAPHICS 2026", theme="purple")
    out_path = os.path.join(BASE_DIR, "test_thumbnail.jpg")
    with open(out_path, "wb") as f:
        f.write(img_bytes)
    print(f"Test dynamic thumbnail created at {out_path} (Size: {len(img_bytes)/1024:.1f} KB)")
