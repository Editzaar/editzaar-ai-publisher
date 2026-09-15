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

def publish_movie_breakdown():
    if not os.path.exists(TOKEN_FILE):
        print("Error: token.json not found.")
        return

    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    service = build('blogger', 'v3', credentials=creds)

    title = "Pushpa 2 & Mass Cinema Editing Secrets: How to Cut High-Impact Action & Slow-Mo Like Blockbusters | Editzaar"
    
    # High-impact cinematic banner images
    featured_banner_url = "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=1200&q=85"
    color_grade_url = "https://images.unsplash.com/photo-1536440136628-849c177e76a1?auto=format&fit=crop&w=1000&q=80"

    html_content = f"""
    <!-- Featured Cover Banner -->
    <div style="text-align: center; margin-bottom: 30px;">
        <img src="{featured_banner_url}" 
             alt="Cinematic Movie Editing and Film Production" 
             style="width: 100%; max-height: 520px; object-fit: cover; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.15);" />
        <p style="font-size: 13px; color: #777; margin-top: 10px;"><em>The visual psychology behind mass cinema editing and pacing.</em></p>
    </div>

    <p style="font-size: 17px; line-height: 1.7; color: #222;">
        When blockbuster movies like <strong>Pushpa 2: The Rule</strong> or <strong>KGF</strong> break box office records, the true hero isn't just the star power or the VFX—it is the <strong>ruthless, high-octane editing pacing</strong>.
    </p>
    <p style="font-size: 16px; line-height: 1.7; color: #333;">
        Mass cinema uses specific editing grammar to build unbearable tension, maximize heroic elevation, and keep millions on the edge of their seats. In this breakdown, we reveal the <strong>5 core movie editing techniques</strong> that you can steal for your YouTube videos, Reels, and commercials.
    </p>

    <hr style="border: 0; height: 1px; background: #eee; margin: 30px 0;"/>

    <h2>1. The Non-Linear Speed Ramp (Speed-Ramping Mastery)</h2>
    <p>Amateur speed ramps look robotic because they jump linearly from 100% to 500%. Cinematic editors use an <strong>exponential S-curve</strong>:</p>
    <ul>
        <li><strong>Lead-up (100% speed):</strong> The character begins an action (e.g. stepping out of a car or throwing a punch).</li>
        <li><strong>The Flash (300%–500% speed):</strong> 3 to 5 frames of hyper-speed to cover dead movement.</li>
        <li><strong>The Freeze Impact (20%–40% slow-mo):</strong> The exact peak moment of impact or eye contact is stretched out in 60fps/120fps slow motion.</li>
    </ul>

    <h2>2. Single-Frame Flash Inserts (The "Impact Frame" Trick)</h2>
    <p>On weapon strikes, explosions, or heavy bass drops, editors insert a <strong>1-frame white flash or inverted-color frame</strong>. This briefly overwhelms the viewer's optic nerve, giving the physical illusion that the cut hit harder than it actually did.</p>

    <div style="text-align: center; margin: 30px 0;">
        <img src="{color_grade_url}" 
             alt="Cinematic Color Grading & Dramatic Lighting" 
             style="width: 100%; max-height: 400px; object-fit: cover; border-radius: 10px; box-shadow: 0 4px 16px rgba(0,0,0,0.12);" />
        <p style="font-size: 13px; color: #777; margin-top: 8px;"><em>Warm earth tones vs deep cold shadows define modern mass-action aesthetics.</em></p>
    </div>

    <h2>3. The "Hero Elevation" Sound Build-up</h2>
    <p>Before a major cinematic entry or punchline:</p>
    <ol>
        <li><strong>The Sound Void:</strong> All background ambient noise and music are completely cut for 0.5 seconds of dead silence.</li>
        <li><strong>The Breath / Foley Cue:</strong> A single sharp sound (a cigar inhale, gun cock, or shoe stomp).</li>
        <li><strong>The Theme Drop:</strong> The high-energy brass/sub-bass theme hits precisely on the visual cut.</li>
    </ol>

    <h2>4. Low-Angle Match Dissolves and Tracking Flow</h2>
    <p>To establish sheer scale, editors cut between a low-angle tracking shot of the protagonist moving forward directly into an aerial wide drone shot moving backwards. This dual-axis motion contrast makes scenes feel massive and grand.</p>

    <h2>5. The Gritty "Earthy & Gold" Color Grade Profile</h2>
    <p>Mass blockbusters rely heavily on high-contrast color palettes: deep burnt oranges, rich forest greens, and crushed blacks. By pushing warm highlights into the subject's sweat and skin while preserving cool tones in the shadows, footage instantly looks raw, grounded, and expensive.</p>

    <hr style="border: 0; height: 1px; background: #eee; margin: 30px 0;"/>

    <!-- Branded CTA Box -->
    <div style="background: linear-gradient(135deg, #111 0%, #2e0808 100%); color: #fff; padding: 25px; border-radius: 12px; margin: 35px 0; text-align: center; border: 1px solid #ff4b2b; box-shadow: 0 10px 25px rgba(255,75,43,0.15);">
        <h3 style="margin-top: 0; font-size: 22px; color: #ff5722;">Want Cinematic Edits for Your Brand?</h3>
        <p style="font-size: 15px; line-height: 1.6; max-width: 600px; margin: 10px auto 20px auto; color: #ddd;">
            At <strong>Editzaar</strong>, we help creators, agencies, and brands produce high-octane, cinematic video content that stops scrolls and builds loyal audiences.
        </p>
        <a href="https://blog.editzaar.in/" style="background-color: #ff5722; color: #fff; padding: 12px 28px; text-decoration: none; font-weight: bold; border-radius: 30px; display: inline-block; box-shadow: 0 4px 12px rgba(255,87,34,0.4);">
            Explore More Editing Masterclasses on Editzaar →
        </a>
    </div>
    """

    labels = ["video editing", "Growth Tips", "Cinema Breakdown", "Pushpa 2"]

    search_description = "Uncover the secret movie editing techniques behind Pushpa 2 and mass cinema. Learn speed ramping S-curves, single-frame impact flashes, and cinematic color grading."

    body = {
        "title": title,
        "content": html_content,
        "labels": labels,
        "location": {
            "name": "India",
            "lat": 20.5937,
            "lng": 78.9629
        },
        "customMetaData": search_description
    }

    result = service.posts().insert(blogId=BLOG_ID, body=body, isDraft=True).execute()

    print("==================================================")
    print("NEW MOVIE BREAKDOWN ARTICLE CREATED AS DRAFT!")
    print(f"Title: {result.get('title')}")
    print(f"Post ID: {result.get('id')}")
    print(f"Status: {result.get('status')}")
    print(f"Location: {result.get('location', {}).get('name')}")
    print(f"Edit Link: https://www.blogger.com/blog/post/edit/{BLOG_ID}/{result.get('id')}")
    print("==================================================")

if __name__ == "__main__":
    publish_movie_breakdown()
