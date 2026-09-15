import os
import sys
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

SCOPES = ['https://www.googleapis.com/auth/blogger']
BLOG_ID = '866286363471382851'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(BASE_DIR, 'token.json')

def publish_seo_optimized_post(title, summary, primary_label, banner_url, article_body_html):
    """
    Publishes an article adhering strictly to:
    1. Exactly ONE existing label from blog.editzaar.in (e.g. 'video editing' or 'Growth Tips')
    2. Embedded JSON-LD SEO Schema for Google Rich Snippets
    3. OpenGraph / Twitter Card Meta for Meta & social crawlers
    4. Blogger customMetaData (Search Description)
    5. Location targeting
    """
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    service = build('blogger', 'v3', credentials=creds)

    # Valid existing labels on blog.editzaar.in
    valid_labels = ["video editing", "Growth Tips", "Content Strategy", "podcast", "Business Growth Tips", "Case Studies"]
    if primary_label not in valid_labels:
        primary_label = "video editing" # fallback to primary category

    # JSON-LD Structured Data Schema for Google Search
    json_ld_schema = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": title,
        "description": summary,
        "image": banner_url,
        "author": {
            "@type": "Organization",
            "name": "Editzaar",
            "url": "https://blog.editzaar.in/"
        },
        "publisher": {
            "@type": "Organization",
            "name": "Editzaar Blogs",
            "logo": {
                "@type": "ImageObject",
                "url": "https://blog.editzaar.in/favicon.ico"
            }
        },
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": "https://blog.editzaar.in/"
        }
    }

    # Combine JSON-LD schema, OpenGraph tags, and article HTML
    full_html = f"""
<!-- SEO & OpenGraph Structured Metadata for Google & Meta -->
<script type="application/ld+json">
{json.dumps(json_ld_schema, indent=2)}
</script>
<meta name="description" content="{summary}" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{summary}" />
<meta property="og:image" content="{banner_url}" />
<meta property="og:type" content="article" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{title}" />
<meta name="twitter:description" content="{summary}" />
<meta name="twitter:image" content="{banner_url}" />

<!-- Featured Cover Banner (Auto-detected by Blogger & Social Crawlers) -->
<div style="text-align: center; margin-bottom: 30px;">
    <img src="{banner_url}" 
         alt="{title}" 
         style="width: 100%; max-height: 520px; object-fit: cover; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.15);" />
</div>

{article_body_html}

<!-- Branded Editzaar CTA Box -->
<div style="background: linear-gradient(135deg, #18191a 0%, #292a2d 100%); color: #fff; padding: 25px; border-radius: 12px; margin: 35px 0; text-align: center; border: 1px solid #ff4b2b; box-shadow: 0 10px 25px rgba(255,75,43,0.15);">
    <h3 style="margin-top: 0; font-size: 22px; color: #ff5722;">Ready to Level Up Your Content?</h3>
    <p style="font-size: 15px; line-height: 1.6; max-width: 600px; margin: 10px auto 20px auto; color: #ddd;">
        At <strong>Editzaar</strong>, we produce viral video edits, retention-optimized pacing, and high-impact storytelling for top creators.
    </p>
    <a href="https://blog.editzaar.in/" style="background-color: #ff5722; color: #fff; padding: 12px 28px; text-decoration: none; font-weight: bold; border-radius: 30px; display: inline-block; box-shadow: 0 4px 12px rgba(255,87,34,0.4);">
        Explore More Guides on Editzaar →
    </a>
</div>
"""

    body = {
        "title": title,
        "content": full_html,
        "labels": [primary_label],  # EXACTLY ONE LABEL FROM EXISTING WEBSITE
        "location": {
            "name": "India",
            "lat": 20.5937,
            "lng": 78.9629
        },
        "customMetaData": summary  # Blogger Search Description for Google SERP
    }

    result = service.posts().insert(blogId=BLOG_ID, body=body, isDraft=True).execute()

    print("==================================================")
    print("SUCCESS: POST PUBLISHED WITH 1 TAG & FULL SEO SCHEMA!")
    print(f"Title: {result.get('title')}")
    print(f"Single Label: {result.get('labels')}")
    print(f"Location: {result.get('location', {}).get('name')}")
    print(f"Post ID: {result.get('id')}")
    print(f"Edit Link: https://www.blogger.com/blog/post/edit/{BLOG_ID}/{result.get('id')}")
    print("==================================================")
    return result

if __name__ == "__main__":
    post_title = "DaVinci Resolve vs Premiere Pro 2026: The Ultimate Video Editing Showdown | Editzaar"
    post_summary = "Comparing DaVinci Resolve and Adobe Premiere Pro in 2026. Discover which video editing software offers better playback performance, AI tools, and color grading."
    banner = "https://images.unsplash.com/photo-1535016120720-40c646be5580?auto=format&fit=crop&w=1200&q=85"
    
    body_content = """
    <p style="font-size: 17px; line-height: 1.7; color: #222;">
        The battle between <strong>Adobe Premiere Pro</strong> and <strong>Blackmagic DaVinci Resolve</strong> has never been fiercer. In 2026, both platforms have integrated powerful generative AI, ultra-fast timeline caching, and cloud collaboration.
    </p>
    <p style="font-size: 16px; line-height: 1.7; color: #333;">
        If you are a YouTuber, agency editor, or commercial filmmaker, which one should you invest your time and money into? Let's break it down category by category.
    </p>

    <hr style="border: 0; height: 1px; background: #eee; margin: 30px 0;"/>

    <h2>1. Timeline Performance & GPU Playback</h2>
    <p>When scrubbing through 4K 10-bit 4:2:2 drone footage or 6K RAW files:</p>
    <ul>
        <li><strong>DaVinci Resolve Studio:</strong> Delivers superior GPU optimization and butter-smooth real-time playback without generating heavy proxy files.</li>
        <li><strong>Premiere Pro:</strong> Offers improved hardware decoding on Apple Silicon and modern RTX GPUs, though dynamic link caching can still slow down heavy timelines.</li>
    </ul>

    <h2>2. Color Grading & Finishing: The Clear King</h2>
    <p>There is no contest here: <strong>DaVinci Resolve remains the industry standard</strong> for color grading. Its node-based Color page, HDR color wheels, Magic Mask 2.0, and color-space transform tools blow Lumetri Color out of the water.</p>

    <h2>3. AI Tools & Text-Based Editing</h2>
    <p>Both software suites have pushed heavily into AI automation:</p>
    <ul>
        <li><strong>Premiere Pro:</strong> Leads in speech-to-text accuracy, generative extend (lengthening audio clips seamlessly), and auto-reframing.</li>
        <li><strong>DaVinci Resolve:</strong> Shines with Voice Isolation (studio-quality audio cleanup in 1 click), Scene Cut Detection, and Depth Map AI.</li>
    </ul>

    <h2>4. Pricing: Subscription vs. Lifetime License</h2>
    <p>One of the biggest deciding factors for creators:</p>
    <ul>
        <li><strong>Premiere Pro:</strong> Requires a continuous Creative Cloud monthly/annual subscription ($22.99–$59.99/mo).</li>
        <li><strong>DaVinci Resolve:</strong> Offers an incredibly capable <em>Free version</em>, with the full Studio version costing a one-time fee of $295 with lifetime free updates.</li>
    </ul>

    <h2>The Final Verdict for 2026</h2>
    <p>If you do heavy YouTube video editing, motion graphics, and need fast text-based cuts, <strong>Premiere Pro</strong> is seamless. But if you want unbeatable color, superior stability, zero monthly fees, and an all-in-one suite (editing, audio, VFX), <strong>DaVinci Resolve is the ultimate winner</strong>.</p>
    """

    publish_seo_optimized_post(
        title=post_title,
        summary=post_summary,
        primary_label="video editing",  # Single existing label on blog.editzaar.in
        banner_url=banner,
        article_body_html=body_content
    )
