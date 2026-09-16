import os
import sys
import json
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import urllib.parse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from gemini_engine import generate_and_post_article, EXISTING_LABELS

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Editzaar AI Blogger CMS</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }
        body { background: #0f1117; color: #e1e4ea; min-height: 100vh; display: flex; flex-direction: column; align-items: center; padding: 40px 20px; }
        .container { width: 100%; max-width: 680px; background: #181b24; border-radius: 16px; padding: 32px; border: 1px solid #282d3d; box-shadow: 0 12px 40px rgba(0,0,0,0.4); }
        .badge { display: inline-block; background: #ff4b2b; color: #fff; font-size: 12px; font-weight: 700; padding: 4px 10px; border-radius: 20px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 12px; }
        h1 { font-size: 26px; color: #fff; margin-bottom: 8px; }
        p.subtitle { color: #8c93a8; font-size: 14px; margin-bottom: 28px; }
        .form-group { margin-bottom: 20px; }
        label { display: block; font-size: 13px; font-weight: 600; color: #c4c9d8; margin-bottom: 8px; }
        input[type="text"], textarea, select { width: 100%; background: #0f1117; border: 1px solid #2e3447; border-radius: 8px; padding: 12px 14px; color: #fff; font-size: 15px; outline: none; transition: border-color 0.2s; }
        input[type="text"]:focus, textarea:focus, select:focus { border-color: #ff4b2b; }
        textarea { resize: vertical; min-height: 90px; }
        button { width: 100%; background: linear-gradient(135deg, #ff4b2b 0%, #ff416c 100%); color: #fff; border: none; padding: 14px; font-size: 16px; font-weight: 700; border-radius: 8px; cursor: pointer; transition: opacity 0.2s, transform 0.1s; margin-top: 10px; }
        button:hover { opacity: 0.95; }
        button:active { transform: scale(0.99); }
        button:disabled { opacity: 0.5; cursor: not-allowed; }
        #result { margin-top: 24px; padding: 20px; border-radius: 10px; display: none; }
        .success-box { background: #0d2818; border: 1px solid #1e5e3a; color: #52b788; }
        .error-box { background: #381315; border: 1px solid #782a2d; color: #f28482; }
        .post-link { display: inline-block; background: #2d6a4f; color: #fff; padding: 10px 18px; text-decoration: none; border-radius: 6px; font-weight: 600; margin-top: 12px; font-size: 14px; }
        .post-link:hover { background: #40916c; }
        .copy-box { background: #0b0c10; padding: 10px 12px; border-radius: 6px; border: 1px solid #222; font-family: monospace; font-size: 13px; color: #ffeb3b; margin-top: 8px; word-break: break-all; }
        .loading-spinner { display: inline-block; width: 18px; height: 18px; border: 2px solid rgba(255,255,255,0.3); border-radius: 50%; border-top-color: #fff; animation: spin 0.8s ease-in-out infinite; vertical-align: middle; margin-right: 8px; }
        @keyframes spin { to { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <div class="container">
        <span class="badge">Editzaar Automation</span>
        <h1>AI Blogger CMS & Auto-Publisher</h1>
        <p class="subtitle">Type any topic or brief. The system writes a humanized article, attaches a high-CTR banner, adds SEO schema, and drafts it to Blogger instantly.</p>

        <form id="cmsForm">
            <div class="form-group">
                <label for="topic">Article Topic / Video Title / Brief</label>
                <input type="text" id="topic" placeholder="e.g. 5 Secret CapCut Tricks to Edit Reels Like a Pro" required />
            </div>

            <div class="form-group">
                <label for="category">Select Website Category (Single Tag)</label>
                <select id="category">
                    <option value="video editing" selected>video editing</option>
                    <option value="Growth Tips">Growth Tips</option>
                    <option value="Content Strategy">Content Strategy</option>
                    <option value="podcast">podcast</option>
                    <option value="Business Growth Tips">Business Growth Tips</option>
                    <option value="Case Studies">Case Studies</option>
                </select>
            </div>

            <button type="submit" id="submitBtn">Generate & Draft to Blogger</button>
        </form>

        <div id="result"></div>
    </div>

    <script>
        const form = document.getElementById('cmsForm');
        const submitBtn = document.getElementById('submitBtn');
        const resultDiv = document.getElementById('result');

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const topic = document.getElementById('topic').value.trim();
            const category = document.getElementById('category').value;

            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="loading-spinner"></span> Generating Humanized Article & Publishing...';
            resultDiv.style.display = 'none';

            try {
                const response = await fetch('/api/publish', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ topic, category })
                });
                const data = await response.json();

                if (data.success) {
                    resultDiv.className = 'success-box';
                    resultDiv.innerHTML = `
                        <h3 style="color: #fff; margin-bottom: 8px;">🎉 Draft Created on Blogger!</h3>
                        <p style="color: #c4c9d8; margin-bottom: 6px;"><strong>Title:</strong> ${data.title}</p>
                        <p style="color: #c4c9d8; margin-bottom: 6px;"><strong>Tag:</strong> <code>${data.label}</code> | <strong>Location:</strong> ${data.location}</p>
                        <div style="margin-top: 10px;">
                            <strong style="color: #c4c9d8; font-size: 13px;">Search Description (0/150 for Blogger sidebar):</strong>
                            <div class="copy-box">${data.search_desc}</div>
                        </div>
                        <a href="${data.edit_url}" target="_blank" class="post-link">Open & Preview in Blogger Dashboard ↗</a>
                    `;
                } else {
                    resultDiv.className = 'error-box';
                    resultDiv.innerHTML = `<strong>Error:</strong> ${data.error || 'Failed to publish post'}`;
                }
            } catch (err) {
                resultDiv.className = 'error-box';
                resultDiv.innerHTML = `<strong>Network Error:</strong> ${err.message}`;
            } finally {
                resultDiv.style.display = 'block';
                submitBtn.disabled = false;
                submitBtn.innerHTML = 'Generate & Draft to Blogger';
            }
        });
    </script>
</body>
</html>
"""

class CMSHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200, content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self._set_headers(200)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_HEAD(self):
        self._set_headers(200, "text/html; charset=utf-8")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            body = HTML_PAGE.encode('utf-8')
            self._set_headers(200, "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/api/publish":
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                payload = json.loads(post_data.decode('utf-8'))
                topic = payload.get('topic', '').strip()
                category = payload.get('category', 'video editing')
                print(f"[CMS] Generating & drafting for: '{topic}' with label: '{category}'", flush=True)
                
                result = generate_and_post_article(topic, custom_label=category)
                print(f"[CMS] Success: {result['title']} -> {result['post_id']}", flush=True)
                
                resp_body = json.dumps(result).encode('utf-8')
                self._set_headers(200, "application/json")
                self.send_header("Content-Length", str(len(resp_body)))
                self.end_headers()
                self.wfile.write(resp_body)
            except Exception as e:
                print(f"[CMS] Error: {e}", flush=True)
                resp_body = json.dumps({"success": False, "error": str(e)}).encode('utf-8')
                self._set_headers(500, "application/json")
                self.send_header("Content-Length", str(len(resp_body)))
                self.end_headers()
                self.wfile.write(resp_body)
        else:
            self.send_response(404)
            self.end_headers()

def run_server(port=3000):
    server_address = ('127.0.0.1', port)
    httpd = ThreadingHTTPServer(server_address, CMSHandler)
    print(f"==================================================", flush=True)
    print(f"Editzaar AI Blogger CMS Dashboard is running!")
    print(f"Open in your browser: http://localhost:{port}")
    print(f"==================================================", flush=True)
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
