import os
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

SCOPES = ['https://www.googleapis.com/auth/blogger']
BLOG_ID = '866286363471382851'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(BASE_DIR, 'token.json')

def publish_sound_design_article():
    if not os.path.exists(TOKEN_FILE):
        print("Error: token.json not found.")
        return

    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    service = build('blogger', 'v3', credentials=creds)

    title = "5 Viral Sound Design Secrets That Boost Retention on Reels & Shorts | Editzaar"
    
    featured_banner_url = "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=1200&q=85"
    foley_image_url = "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?auto=format&fit=crop&w=1000&q=80"

    html_content = f"""
    <!-- Featured Cover Banner -->
    <div style="text-align: center; margin-bottom: 30px;">
        <img src="{featured_banner_url}" 
             alt="Sound Design Studio Setup for Video Editors" 
             style="width: 100%; max-height: 520px; object-fit: cover; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.15);" />
        <p style="font-size: 13px; color: #777; margin-top: 10px;"><em>Sound design is the invisible 50% of your video that dictates average view duration.</em></p>
    </div>

    <p style="font-size: 17px; line-height: 1.7; color: #222;">
        Most video editors spend 90% of their time color grading, masking, and adjusting speed ramps—yet viewers scroll away in the first 3 seconds because the <strong>audio feels lifeless</strong>.
    </p>
    <p style="font-size: 16px; line-height: 1.7; color: #333;">
        On short-form platforms like Instagram Reels, TikTok, and YouTube Shorts, sound design is what triggers subconscious physical attention. Here are the <strong>5 viral audio techniques</strong> used by top creator agencies to skyrocket retention.
    </p>

    <hr style="border: 0; height: 1px; background: #eee; margin: 30px 0;"/>

    <h2>1. The "Sub-Bass Drop" Hook Anchor</h2>
    <p>When switching from your opening hook sentence into your first point, insert a subtle <strong>sub-bass boom or low-frequency impact (40Hz–60Hz)</strong>. This adds physical weight to the transition and signals to the viewer's brain that high-value information is arriving.</p>

    <h2>2. The "Whoosh-Hit" Sync for Text & Overlays</h2>
    <p>Whenever animated text, stickers, or lower-thirds animate onto the screen, combine two distinct sounds:</p>
    <ul>
        <li><strong>A fast directional whoosh:</strong> plays right as the element slides into view.</li>
        <li><strong>A crisp pop, click, or thud:</strong> plays exactly on the frame the element stops moving.</li>
    </ul>
    <p>This audio-visual synchronicity makes visual animations feel tactile and satisfying to watch.</p>

    <div style="text-align: center; margin: 30px 0;">
        <img src="{foley_image_url}" 
             alt="Microphone Recording Foley Effects" 
             style="width: 100%; max-height: 400px; object-fit: cover; border-radius: 10px; box-shadow: 0 4px 16px rgba(0,0,0,0.12);" />
        <p style="font-size: 13px; color: #777; margin-top: 8px;"><em>Organic foley sounds (keyboard clicks, paper rips) make digital edits feel grounded.</em></p>
    </div>

    <h2>3. Micro-Ducking: Never Muffle Your Music</h2>
    <p>Standard auto-ducking often creates an unnatural "pumping" sound where the background music cuts out abruptly every time the speaker breathes. Instead, use an <strong>EQ notch filter</strong> at 1kHz–3.5kHz on your music track to carve out space specifically for human vocal clarity without reducing the music's punchy bass and energy.</p>

    <h2>4. Organic Foley Layering (The Paper & Click Method)</h2>
    <p>Digital motion graphics can easily feel sterile. Layering subtle organic foley sounds instantly breathes life into your timeline:</p>
    <ul>
        <li><em>Paper rustles & tape peels</em> for photos and split-screens.</li>
        <li><em>Mechanical keyboard clacks</em> for statistics and code snippets.</li>
        <li><em>Vintage camera shutter clicks</em> for screenshots and proof elements.</li>
    </ul>

    <h2>5. Stereo Panning for Dynamic B-Roll Flow</h2>
    <p>If a car drives from left to right across the screen, automate the sound pan from -40% Left to +40% Right. Stereo movement creates an immersive 3D space that prevents ear fatigue during longer videos.</p>

    <hr style="border: 0; height: 1px; background: #eee; margin: 30px 0;"/>

    <!-- Branded CTA Box -->
    <div style="background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); color: #fff; padding: 25px; border-radius: 12px; margin: 35px 0; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.2);">
        <h3 style="margin-top: 0; font-size: 22px; color: #00e5ff;">Take Your Video Retention to the Next Level</h3>
        <p style="font-size: 15px; line-height: 1.6; max-width: 600px; margin: 10px auto 20px auto; color: #eceff1;">
            Want professional, retention-optimized video editing and sound design for your content? Explore tutorials, presets, and editing breakdowns on <strong>Editzaar</strong>.
        </p>
        <a href="https://blog.editzaar.in/" style="background-color: #00e5ff; color: #111; padding: 12px 28px; text-decoration: none; font-weight: bold; border-radius: 30px; display: inline-block; box-shadow: 0 4px 12px rgba(0,229,255,0.4);">
            Read More on Editzaar Blogs →
        </a>
    </div>
    """

    labels = ["video editing", "Growth Tips", "Sound Design"]

    body = {
        "title": title,
        "content": html_content,
        "labels": labels
    }

    result = service.posts().insert(blogId=BLOG_ID, body=body, isDraft=True).execute()

    print("==================================================")
    print("NEW SOUND DESIGN ARTICLE CREATED AS DRAFT!")
    print(f"Title: {result.get('title')}")
    print(f"Post ID: {result.get('id')}")
    print(f"Status: {result.get('status')}")
    print(f"Blogger Edit Link: https://www.blogger.com/blog/post/edit/{BLOG_ID}/{result.get('id')}")
    print("==================================================")

if __name__ == "__main__":
    publish_sound_design_article()
