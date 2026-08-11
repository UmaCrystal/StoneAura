# How to Add Google Drive Images to StoneAura

## Step 1 — Get the File ID from Google Drive

1. Open your shared **"AURA PRODUCTS IMAGES"** Google Drive folder.
2. Right-click on any image → **Get link**.
3. The shareable link looks like:
   ```
   https://drive.google.com/file/d/1aBcDeFgHiJkLmNoPqRsTuVwXyZ/view?usp=sharing
                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                    This is the FILE ID
   ```
4. Copy everything between `/d/` and `/view`.

## Step 2 — Paste IDs into seed_products.py

Open:
```
products/management/commands/seed_products.py
```

Find the entry for each bracelet and replace the placeholder like `AMETHYST_ID` with the real ID.

**Example — before:**
```python
{"name": "Amethyst Bracelet", ..., "img_id": "AMETHYST_ID"},
```

**After:**
```python
{"name": "Amethyst Bracelet", ..., "img_id": "1aBcDeFgHiJkLmNoPqRsTuVwXyZ"},
```

## Step 3 — Make images publicly accessible

Each image file in Google Drive must be set to **"Anyone with the link can view"**:
- Right-click → Share → Change access → Anyone with the link → Viewer.

Or select all images at once → Share → Anyone with the link.

## Step 4 — Run the seed command

```bash
python manage.py seed_products
```

The command will skip any bracelet whose `img_id` is still a placeholder and tell you exactly which ones need IDs.

## Image–Product Mapping Reference

| Product Name                  | Drive filename                              | Placeholder key           |
|-------------------------------|---------------------------------------------|---------------------------|
| Amazonite Bracelet            | amazomite.webp                              | AMAZONITE_ID              |
| Amazonite Healing Bracelet    | Benefits-Of-Amazonite-Bracelet.webp         | AMAZONITE_BENEFITS_ID     |
| Amethyst Bracelet             | AMETHYST.jpg                                | AMETHYST_ID               |
| Amethyst Oval Bracelet        | AMETHYST 2.jpg                              | AMETHYST2_ID              |
| Black Obsidian Bracelet       | black obsedian.webp                         | BLACK_OBSIDIAN_ID         |
| Black Obsidian Oval Bracelet  | black obsedian 1.webp                       | BLACK_OBSIDIAN2_ID        |
| Calcite Bracelet              | calcite.jpg                                 | CALCITE_ID                |
| Carnelian Bracelet            | carnelian92.webp                            | CARNELIAN_ID              |
| Citrine Bracelet              | CITRINE.webp                                | CITRINE_ID                |
| Citrine Oval Bracelet         | CITRINE 2.jpg                               | CITRINE2_ID               |
| Green Aventurine Bracelet     | GREEN_AVENTURINE_37360b00-...webp           | GREEN_AVENTURINE_ID       |
| Green Jade Bracelet           | Green-Jade-Bracelet-Final-1.webp            | GREEN_JADE_ID             |
| Howlite Bracelet              | howlite-bead-bracelet-1.jpg                 | HOWLITE_ID                |
| Howlite Oval Bracelet         | HOWLITE IMAGE 2                             | HOWLITE2_ID               |
| Lapis Lazuli Bracelet         | lapiz.webp                                  | LAPIS_ID                  |
| Lapis Lazuli Oval Bracelet    | lapiz 1.webp                                | LAPIS2_ID                 |
| Lava Stone Bracelet           | lava bracelet.webp                          | LAVA_ID                   |
| Money Magnet Bracelet         | money magnet.jpg                            | MONEY_MAGNET_ID           |
| Moonstone Bracelet            | moon stone.jpg                              | MOON_STONE_ID             |
| White Moonstone Bracelet      | WhiteMoonstone1.webp                        | WHITE_MOONSTONE_ID        |
| Opalite Bracelet              | OPALITE.webp                                | OPALITE_ID                |
| Opalite Oval Bracelet         | OPALITE 2.webp                              | OPALITE2_ID               |
| Peacock Ore Bracelet          | Peacock8651_copy.jpg                        | PEACOCK_ID                |
| Pyrite Bracelet               | NATURAL_PYRITE.webp                         | NATURAL_PYRITE_ID         |
| Pyrite Oval Bracelet          | PYRITE 2.webp                               | PYRITE2_ID                |
| Rashi Bracelet                | rashi bracelet.webp                         | RASHI_ID                  |
| Red Jasper Bracelet           | RED JASPER                                  | RED_JASPER_ID             |
| Rhodochrosite Bracelet        | RHODOCROSITE_00ac6fb4-...webp               | RHODOCHROSITE_ID          |
| Rhodochrosite Natural Bracelet| natural-rhodochrosite-bracelet-1.jpg        | RHODOCHROSITE2_ID         |
| Rhodonite Bracelet            | RHODONITE_001fd9ac-...webp                  | RHODONITE_ID              |
| Rhodonite Oval Bracelet       | RHODONITE 2.webp                            | RHODONITE2_ID             |
| Rose Quartz Bracelet          | ROSE QUATZ IM 1.jpg                         | ROSE_QUARTZ_ID            |
| Rose Quartz Oval Bracelet     | ROSE QUATZ 2.jpg                            | ROSE_QUARTZ2_ID           |
| Seven Chakra Bracelet         | seven chakra.png                            | SEVEN_CHAKRA_ID           |
| Seven Chakra Lava Bracelet    | seven chakra (2).png                        | SEVEN_CHAKRA2_ID          |
| Sodalite Bracelet             | sodalite-gemstones-bracelet-1.jpg           | SODALITE_ID               |
| Sodalite Bead Bracelet        | sodalite_bead_braceletl_view3.webp          | SODALITE2_ID              |
| Sunstone Bracelet             | sunstone.jpg                                | SUNSTONE_ID               |
| Tiger Eye Bracelet            | TIGER_EYE.webp                              | TIGER_EYE_ID              |
| Tiger Eye Oval Bracelet       | TIGER EYE 2.webp                            | TIGER_EYE2_ID             |
| Turquoise Bracelet            | TOURQOUIS.webp                              | TURQUOISE_ID              |
