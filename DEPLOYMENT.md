# Update the existing GitHub Pages site

Repository: https://github.com/MohdUjjain/world-history-dossier
Public website: https://mohdujjain.github.io/world-history-dossier/
Pages branch: `main` / `/(root)` — **already enabled**; do not change Pages settings.

## Option A — GitHub website (new assets only)

1. Download and extract `World_History_Dossier_Web_Upload.zip` (do **not** upload the ZIP itself).
2. Open https://github.com/MohdUjjain/world-history-dossier/upload/main.
3. The published repository already contains `og-image.jpg` and `20th-Century International History.pdf`; do not upload renamed duplicates. To make future changes, use Git CLI as described in Option B.
4. The website, modular source, PDF, and preview image are already present. Use Option B below when updating existing files rather than re-uploading the original package.

**Important:** The original ZIP is a historic release snapshot. Do not overwrite the live repository with it; pull the latest repository changes first.

## Option B — Git on your computer (recommended, one complete update)

Open a terminal in your existing local repository (or clone it if you have not yet done so), then run:

```bash
git pull --ff-only origin main
# Make your intended source or content edits
git add -A
git commit -m "Update dossier"
git push origin main
```

## Confirm publication

- Reader: https://mohdujjain.github.io/world-history-dossier/
- Preview image: https://mohdujjain.github.io/world-history-dossier/og-image.jpg
- PDF: https://mohdujjain.github.io/world-history-dossier/20th-Century%20International%20History.pdf
- Source: https://github.com/MohdUjjain/world-history-dossier/tree/main/src

Open the image URL directly to make sure it loads. Share the exact website root URL on WhatsApp to test its link preview. If WhatsApp shows a previously cached thumbnail, try appending `?v=2` temporarily.

The Open Graph title, description, image URL, image type, dimensions, and Twitter/X card data are in the literal HTML `<head>`; JavaScript is not required for crawlers to find them.

## Continued publishing

Update chapter files under `src/chapters/`, then run `python src/build.py -o index.html`. Update the pre-rendered PDF separately if chapter content changes. Commit both source and built HTML. If you change the shared CSS or JavaScript, keep `CSS_DOC.md` / `JS_DOC.md` current in the same commit.
