import re
from pathlib import Path

CSV_PATH = Path(r"C:\Users\baps\.gemini\antigravity-ide\brain\bd07581c-f9a8-4b1f-bce2-5a586ca969d5\.system_generated\steps\19\content.md")

with open(CSV_PATH, 'r', encoding='utf-8') as f:
    text = f.read()

for kw in ["line", "bead", "string", "8mm", "pcs", "piece", "kg"]:
    matches = [line for line in text.splitlines() if kw in line.lower()]
    print(f"Keyword: '{kw}' | Matches: {len(matches)}")
    for m in matches[:5]:
        print(f"  - {m}")
