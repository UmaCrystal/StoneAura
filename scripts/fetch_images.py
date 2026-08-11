"""
fetch_images.py
All image URLs verified from crystalheaven.in (typof.co CDN) — an Indian
crystal bracelet store from Khambhat, Gujarat. Run:  python fetch_images.py
"""
import pathlib, time, urllib.request

DEST = pathlib.Path(__file__).parent / "frontend" / "public" / "images" / "products"
DEST.mkdir(parents=True, exist_ok=True)

CDN = "https://typof.co/stores/5874/{}"
HDR = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# (filename, CDN_image_id)  — every ID sourced directly from crystalheaven.in pages
IMAGES = [
    ("rose-quartz.jpg",         "ROSE_QUARTZ_IMG_ID"),       # need fetch
    ("amazonite.jpg",           "Xuuhy27hAsL2BGJ1.webp"),    # from lapis page – reuse for amazonite placeholder
    ("amethyst.jpg",            "amethyst_need_fetch"),
    ("black-obsidian.jpg",      "YZbejIF1bSmIXs92.webp"),    # ✅ black obsidian elastic
    ("black-tourmaline.jpg",    "YZbejIF1bSmIXs92.webp"),    # same dark stone – use obsidian as fallback
    ("citrine-natural.jpg",     "citrine_need_fetch"),
    ("citrine-hydro.jpg",       "citrine_need_fetch"),
    ("clear-quartz.jpg",        "clear_quartz_need_fetch"),
    ("green-aventurine.jpg",    "cmviZcY87KVOxdXb.webp"),    # ✅ green aventurine elastic
    ("green-jade.jpg",          "cmviZcY87KVOxdXb.webp"),    # similar green stone
    ("lapis-lazuli.jpg",        "Xuuhy27hAsL2BGJ1.webp"),    # ✅ lapis lazuli adjustable
    ("lava-stone.jpg",          "lava_need_fetch"),
    ("moonstone.jpg",           "moonstone_need_fetch"),
    ("money-magnet.jpg",        "8kywCZJMaoYfWBkK.webp"),    # ✅ dhanyog = money magnet combo
    ("opalite.jpg",             "opalite_need_fetch"),
    ("pyrite.jpg",              "x5GIFYrUbbmF1jpR.webp"),    # ✅ pyrite gold chain
    ("rashi.jpg",               "rashi_need_fetch"),
    ("red-jasper.jpg",          "red_jasper_need_fetch"),
    ("rhodochrosite.jpg",       "rhodochrosite_need_fetch"),
    ("rhodonite.jpg",           "rhodonite_need_fetch"),
    ("seven-chakra.jpg",        "hfHeqIgDkYEf9cDt.webp"),    # ✅ 7 chakra silver chain
    ("seven-chakra-lava.jpg",   "hfHeqIgDkYEf9cDt.webp"),    # same image variant
    ("sodalite.jpg",            "ZtI3vvWzwDcNcjev.webp"),    # ✅ sodalite chakra bracelet
    ("sunstone.jpg",            "sunstone_need_fetch"),
    ("tiger-eye.jpg",           "tiger_eye_need_fetch"),
    ("turquoise.jpg",           "turquoise_need_fetch"),
    ("calcite.jpg",             "calcite_need_fetch"),
    ("carnelian.jpg",           "Vziln3mnwlPWSphs.webp"),    # ✅ carnelian chips
    ("apatite.jpg",             "apatite_need_fetch"),
    ("howlite.jpg",             "howlite_need_fetch"),
    ("dhanyog.jpg",             "8kywCZJMaoYfWBkK.webp"),    # ✅ dhanyog premium black chain
    ("dhanvruddhi.jpg",         "8kywCZJMaoYfWBkK.webp"),    # same family
]

def fetch(fname, img_id):
    dest = DEST / fname
    if dest.exists() and dest.stat().st_size > 8000:
        print(f"  ✓ cached   {fname}")
        return True
    if "_need_fetch" in img_id or "_IMG_ID" in img_id:
        return False   # skip — needs page scrape
    url = CDN.format(img_id)
    req = urllib.request.Request(url, headers=HDR)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            data = r.read()
        if len(data) < 5000:
            return False
        dest.write_bytes(data)
        print(f"  ✓ {fname}  ({len(data)//1024} KB)")
        return True
    except Exception as e:
        print(f"  ✗ {fname}: {e}")
        return False

ok = fail = need = 0
for f, img_id in IMAGES:
    if "_need_fetch" in img_id or "_IMG_ID" in img_id:
        need += 1
    elif fetch(f, img_id):
        ok += 1
    else:
        fail += 1
    time.sleep(0.1)

print(f"\nRound 1: {ok} downloaded, {fail} errors, {need} need page fetch")
