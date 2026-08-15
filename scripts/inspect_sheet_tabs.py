import re
from pathlib import Path

HTML_PATH = Path(r"C:\Users\baps\.gemini\antigravity-ide\brain\bd07581c-f9a8-4b1f-bce2-5a586ca969d5\.system_generated\steps\68\content.md")

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

# Look for sheet names or tab names in the HTML
# Google Sheets stores sheet names in JavaScript objects or arrays, often like:
# {"1": "SheetName"} or similar, or we can look for keywords like "bead", "string", "anklet", "tumble"
print("Searching for sheet metadata...")
matches = re.findall(r'"name"\s*:\s*"([^"]+)"', html)
if matches:
    print("Found sheet names in JSON:")
    for m in set(matches):
        print(f"  - {m}")

# Search for any sheet/tab title occurrences
title_matches = re.findall(r'aria-label="([^"]+)"', html)
print("\nFound aria-labels:")
for m in set(title_matches):
    if "sheet" in m.lower() or "tab" in m.lower() or "page" in m.lower():
        print(f"  - {m}")
        
# Search for raw keywords in HTML
for kw in ["bead line", "bead lines", "beads string", "string 8mm", "8mm string", "beads string 8mm"]:
    cnt = html.lower().count(kw)
    print(f"Keyword: '{kw}' | Occurrences: {cnt}")
