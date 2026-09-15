import urllib.request
import urllib.parse
import json
import re
import html

def live_web_search(query, max_results=6):
    try:
        url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            page_html = response.read().decode('utf-8', errors='ignore')

        # Extract result titles and snippets
        snippets = re.findall(r'<a[^>]*class="result__snippet[^>]*>(.*?)</a>', page_html, re.DOTALL)
        titles = re.findall(r'<a[^>]*class="result__url[^>]*>(.*?)</a>', page_html, re.DOTALL)
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
        print(f"Search error: {e}")
        return []

if __name__ == "__main__":
    res = live_web_search("Top 5 trending songs India youtube 2026")
    print(f"Results found: {len(res)}")
    for r in res:
        print("TITLE:", r["title"])
        print("SNIPPET:", r["snippet"])
        print("-" * 40)
