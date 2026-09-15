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

if sys.platform == win32:
    sys.stdout.reconfigure(encoding='utf-8')

GEMINI_API_KEY = os.environ.get(GEMINI_API_KEY, ")
GEMINI_MODELS = [gemini-3.5-flash, gemini-3.1-flash-lite-preview, gemini-3.6-flash, gemini-3.7-flash]

SCOPES = ['https://www.googleapis.com/auth/blogger']
BLOG_ID = os.environ.get(BLOGGER_BLOG_ID, 866286363471382851)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(BASE_DIR, 'token.json')

EXISTING_LABELS = [video editing, Growth Tips, Content Strategy, podcast, Business Growth Tips, Case Studies]

def get_blogger_credentials():
 if os.environ.get(BLOGGER_TOKEN_JSON):
 token_info = json.loads(os.environ[BLOGGER_TOKEN_JSON])
 return Credentials.from_authorized_user_info(token_info, SCOPES)
 if os.path.exists(TOKEN_FILE):
 return Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
 raise RuntimeError(No Blogger token found. Set BLOGGER_TOKEN_JSON environment variable or place token.json.)

def live_web_search(query, max_results=6):
 try:
 url = https://html.duckduckgo.com/html/?q= + urllib.parse.quote(query)
 headers = {
 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
 }
 req = urllib.request.Request(url, headers=headers)
 with urllib.request.urlopen(req, timeout=10) as response:
 page_html = response.read().decode('utf-8', errors='ignore')

 snippets = re.findall(r'<a[^>]*class=result__snippet[^>]*>(.*?)</a>', page_html, re.DOTALL)
        raw_titles = re.findall(r'<h2[^>]*class=result__title[^>]*>.*?<a[^>]*>(.*?)</a>', page_html, re.DOTALL)

        results = []
        for i in range(min(len(snippets), max_results)):
            clean_title = re.sub(r'<[^>]+>', '', raw_titles[i]).strip() if i < len(raw_titles) else "
 clean_snippet = re.sub(r'<[^>]+>', '', snippets[i]).strip()
 clean_title = html.unescape(clean_title)
 clean_snippet = html.unescape(clean_snippet)
 if clean_snippet:
 results.append(f- {clean_title}: {clean_snippet})
 return results
 except Exception as e:
 print(f[Research Search] Error for '{query}': {e}, flush=True)
 return []

def call_gemini_api(prompt, system_instruction=):
 api_key = os.environ.get(GEMINI_API_KEY, GEMINI_API_KEY)
 payload = {
 contents: [{parts: [{text: prompt}]}],
 generationConfig: {
 temperature: 0.7,
 maxOutputTokens: 4096
 }
 }
 if system_instruction:
 payload[systemInstruction] = {parts: [{text: system_instruction}]}

 data = json.dumps(payload).encode('utf-8')

 for model_name in GEMINI_MODELS:
 try:
 url = fhttps://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}
 req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
 with urllib.request.urlopen(req, timeout=40) as res:
 resp_json = json.loads(res.read().decode('utf-8'))
 candidates = resp_json.get(candidates, [])
 if candidates:
 return candidates[0][content][parts][0][text]
 except Exception as e:
 print(f[Gemini API] Failed on model {model_name}: {e}. Trying fallback..., flush=True)
 time.sleep(1)

 raise RuntimeError(All Gemini API models failed to generate content.)

def generate_custom_3d_thumbnail(title_text, subtitle_text=2026 CREATOR MASTERCLASS, theme=gold):
 width, height = 1280, 720
 img = Image.new(RGB, (width, height), color=(10, 12, 18))
 draw = ImageDraw.Draw(img)

 themes = {
 gold: ((24, 16, 10), (245, 158, 11), (255, 235, 59)),
 purple: ((18, 10, 32), (168, 85, 247), (250, 204, 21)),
 cyan: ((10, 22, 34), (6, 182, 212), (255, 255, 255)),
 red: ((28, 10, 14), (239, 68, 68), (252, 211, 77)),
 green: ((10, 24, 16), (34, 197, 94), (250, 204, 21)),
 amber: ((24, 14, 8), (245, 158, 11), (254, 240, 138))
 }
 bg_color, accent_color, highlight_color = themes.get(theme, themes[gold])

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
 font_badge = ImageFont.truetype(impact.ttf, 26)
 font_main = ImageFont.truetype(impact.ttf, 60)
 font_sub = ImageFont.truetype(arialbd.ttf, 28)
 except:
 try:
 font_badge = ImageFont.truetype(arialbd.ttf, 24)
 font_main = ImageFont.truetype(arialbd.ttf, 50)
 font_sub = ImageFont.truetype(arial.ttf, 26)
 except:
 font_badge = ImageFont.load_default()
 font_main = ImageFont.load_default()
 font_sub = ImageFont.load_default()

 badge_label = EDITZAAR MASTERCLASS 2026
 bbox = draw.textbbox((0, 0), badge_label, font=font_badge)
 bw = bbox[2] - bbox[0]
 draw.text(((width - bw) // 2, 58), badge_label, fill=(255, 255, 255), font=font_badge)

 clean_txt = title_text.upper().replace(| EDITZAAR, ).strip()
 words = clean_txt.split()
 lines = []
 curr = []
 for w in words:
 curr.append(w)
 if len( .join(curr)) > 20:
 lines.append( .join(curr))
 curr = []
 if curr:
 lines.append( .join(curr))
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
 img.save(buffer, format=JPEG, quality=80, optimize=True)
 return buffer.getvalue()

def generate_deep_article_with_gemini(raw_topic, custom_label=None):
 topic = raw_topic.strip()
 print(f[Gemini Deep Brain] Researching web & generating article for: '{topic}'..., flush=True)

 search_queries = [
 f{topic} 2026 facts breakdown,
 f{topic} tutorial guide tips
 ]
 web_snippets = []
 for q in search_queries:
 snippets = live_web_search(q, max_results=3)
 web_snippets.extend(snippets)
 research_context = \n.join(web_snippets) if web_snippets else No live snippets retrieved. Use deep domain expertise.

 system_prompt = "
You are the Lead Master Video Editor & Senior Content Strategist at Editzaar (blog.editzaar.in).
Your job is to write a comprehensive, deeply researched, master-level article in clean HTML format.

Strict Writing Rules:
1. Tone: 100% human, conversational, actionable, pro-editor advice. Zero robotic cliches or empty AI buzzwords (never use delve, game-changer, testament, revolutionize, tapestry).
2. Length & Depth: Thorough and detailed (1,200 to 1,800+ words). Break down real software (Premiere, DaVinci, After Effects, CapCut, Blender, Topaz), real movies, exact settings, dB levels, keyframe curves, and timecodes.
3. Strict Output Format: Respond with valid JSON only containing these keys:
 - title: Clean title ending with  | Editzaar
 - label: Strictly 1 existing category chosen from [video editing, Growth Tips, Content Strategy, podcast, Business Growth Tips, Case Studies]
 - theme: One color theme for 3D thumbnail chosen from [gold, purple, cyan, red, green, amber]
 - subtitle: 3 to 6 words uppercase subtitle for thumbnail (e.g. PRO PACING & TIMELINE SECRETS)
 - search_desc: Exact SEO description strictly under 145 characters (Blogger sidebar 0/150 limit)
 - html_body: The complete HTML content formatted with <h2>, <h3>, <p>, <ul>, <li>, a styled <table> comparison, and actionable pro tips. Do NOT include <html> or <body> tags.
"

 user_prompt = f"
Topic: {topic}
Selected Category Preference: {custom_label if custom_label else Auto-detect}

Live Web Research Context:
{research_context}

Write the full JSON object containing the complete, deeply structured masterclass article.
"

 raw_response = call_gemini_api(user_prompt, system_instruction=system_prompt)
 
 cleaned_json = re.sub(r'^`json\s*', '', raw_response.strip(), flags=re.MULTILINE)
 cleaned_json = re.sub(r'`$', '', cleaned_json.strip(), flags=re.MULTILINE)

 try:
 data = json.loads(cleaned_json)
 except Exception as e:
 print(f[Gemini Parsing] Fallback JSON parse: {e}, flush=True)
 title_m = re.search(r'title\s*:\s*(.*?)', raw_response)
 label_m = re.search(r'label\s*:\s*(.*?)', raw_response)
 theme_m = re.search(r'theme\s*:\s*(.*?)', raw_response)
 sub_m = re.search(r'subtitle\s*:\s*(.*?)', raw_response)
 desc_m = re.search(r'search_desc\s*:\s*(.*?)', raw_response)
 
 data = {
 title: title_m.group(1) if title_m else f{topic} | Editzaar,
 label: label_m.group(1) if label_m else (custom_label or video editing),
 theme: theme_m.group(1) if theme_m else gold,
 subtitle: sub_m.group(1) if sub_m else 2026 CREATOR MASTERCLASS,
 search_desc: desc_m.group(1) if desc_m else fMaster {topic}. Pro workflows by Editzaar.[:140],
 html_body: raw_response
 }

 selected_label = custom_label if (custom_label and custom_label in EXISTING_LABELS) else data.get(label, video editing)
 if selected_label not in EXISTING_LABELS:
 selected_label = video editing

 title = data.get(title, f{topic} | Editzaar)
 theme = data.get(theme, gold)
 subtitle = data.get(subtitle, 2026 CREATOR MASTERCLASS)
 search_desc = data.get(search_desc, fMaster {topic}. Pro workflows by Editzaar.)[:145]
 html_body = data.get(html_body, )

 img_bytes = generate_custom_3d_thumbnail(topic, subtitle_text=subtitle, theme=theme)
 img_base64 = base64.b64encode(img_bytes).decode('utf-8')
 image_data_uri = fdata:image/jpeg;base64,{img_base64}

 full_html = f"
<!-- SEO OpenGraph Meta -->
<meta name=description content={search_desc} />
<meta property=og:title content={title} />
<meta property=og:description content={search_desc} />
<meta property=og:type content=article />
<meta name=twitter:card content=summary_large_image />

<!-- Custom 3D Dynamic Cover Banner (100% Reliable, Zero Broken Links) -->
<div style=text-align: center; margin-bottom: 30px;>
 <img src={image_data_uri} 
 alt={title} 
 style=width: 100%; max-height: 560px; object-fit: cover; border-radius: 14px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); />
</div>

{html_body}

<hr style=border: 0; height: 1px; background: #eee; margin: 35px 0;/>

<!-- Branded Editzaar CTA Box -->
<div style=background-color: #f8f9fa; border: 2px solid #ff4b2b; padding: 25px; border-radius: 12px; margin: 35px 0; text-align: center;>
 <h3 style=margin-top: 0; font-size: 22px; color: #111;>Want Viral Video Edits for Your Brand?</h3>
 <p style=font-size: 15px; line-height: 1.6; max-width: 600px; margin: 10px auto 20px auto; color: #555;>
 At <strong>Editzaar</strong>, we craft high-retention video edits, viral storytelling cuts, and creator growth blueprints that save you hours every week.
 </p>
 <a href=https://blog.editzaar.in/ style=background-color: #ff4b2b; color: #fff; padding: 12px 28px; text-decoration: none; font-weight: bold; border-radius: 30px; display: inline-block;>
 Explore More Guides on Editzaar Blogs →
 </a>
</div>
"

 return {
 title: title,
 content: full_html,
 label: selected_label,
 location: India,
 search_desc: search_desc,
 img_bytes: img_bytes
 }

def post_article_with_deduplication(article_data):
 creds = get_blogger_credentials()
 service = build('blogger', 'v3', credentials=creds)

 body = {
 title: article_data[title],
 content: article_data[content],
 labels: [article_data[label]],
 location: {
 name: India,
 lat: 20.5937,
 lng: 78.9629
 },
 customMetaData: article_data[search_desc]
 }

 try:
 drafts = service.posts().list(blogId=BLOG_ID, status=['DRAFT'], maxResults=30).execute().get('items', [])
 target_norm = article_data[title].strip().lower()
 for d in drafts:
 if d.get(title, ).strip().lower() == target_norm:
 print(f[Deduplication] Updating existing draft ID {d['id']} for '{article_data['title']}'..., flush=True)
 service.posts().update(blogId=BLOG_ID, postId=d['id'], body=body).execute()
 edit_url = fhttps://www.blogger.com/blog/post/edit/{BLOG_ID}/{d['id']}
 return edit_url, d['id']
 except Exception as err:
 print(f[Deduplication] Check warning: {err}, flush=True)

 result = service.posts().insert(blogId=BLOG_ID, body=body, isDraft=True).execute()
 post_id = result.get('id')
 edit_url = fhttps://www.blogger.com/blog/post/edit/{BLOG_ID}/{post_id}
 return edit_url, post_id

def generate_and_post_article(topic, custom_label=None):
 article_data = generate_deep_article_with_gemini(topic, custom_label=custom_label)
 edit_url, post_id = post_article_with_deduplication(article_data)
 return {
 success: True,
 title: article_data[title],
 label: article_data[label],
 location: article_data[location],
 edit_url: edit_url,
 post_id: post_id,
 search_desc: article_data[search_desc],
 img_bytes: article_data[img_bytes]
 }
