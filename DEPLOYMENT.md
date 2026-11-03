# Update the existing GitHub Pages site

Repository: https://github.com/MohdUjjain/world-history-dossier
Public website: https://mohdujjain.github.io/world-history-dossier/
Pages branch: `main` / `/(root)` — **already enabled**; do not change Pages settings.

## Option A — GitHub website (new assets only)

1. Download and extract `World_History_Dossier_Web_Upload.zip` (do **not** upload the ZIP itself).
2. Open https://github.com/MohdUjjain/world-history-dossier/upload/main.
3. Upload **only the two files that do not already exist**: `og-image.jpg` and `World_History_Dossier.pdf`. Commit to `main`.
4. The existing `index.html` and `README.md` must also be replaced; GitHub's browser uploader may reject a file whose path already exists. For those updates, use the GitHub code editor (copy the full corrected files) or, preferably, **Option B** below. The source tree is also best added with Option B.

**Simplest complete method if you dislike the terminal:** Use **GitHub Desktop**. Clone `MohdUjjain/world-history-dossier`, copy the *contents* of the extracted complete-repo package into the local clone (overwriting `index.html` and `README.md`), then click **Commit to main** and **Push origin**.

## Option B — Git on your computer (recommended, one complete update)

Download and extract `World_History_Dossier_Complete_Repo.zip`. Open a terminal in the extracted directory and run:

```bash
git clone https://github.com/MohdUjjain/world-history-dossier.git current-repo
# Copy the EXTRACTED package contents — index.html, og-image.jpg, PDF, src/, README.md,
# DEPLOYMENT.md and .nojekyll — into current-repo/ (overwriting old files).
cd current-repo
git add -A
git commit -m "Publish full dossier source, PDF and social sharing preview"
git push origin main
```

Alternatively, from within the repository clone, copy in the package using:

**macOS / Linux** (with the extracted full package at `../World_History_Dossier_GitHub_Repo_Ready`):
```bash
cp -R ../World_History_Dossier_GitHub_Repo_Ready/. .
git add -A
git commit -m "Publish full dossier source, PDF and social sharing preview"
git push origin main
```

**Windows**: use File Explorer to copy the contents of `World_History_Dossier_GitHub_Repo_Ready` into your cloned `current-repo` folder, agreeing to replace `index.html` and `README.md`, then run the three `git` commands above.

## Confirm publication

- Reader: https://mohdujjain.github.io/world-history-dossier/
- Preview image: https://mohdujjain.github.io/world-history-dossier/og-image.jpg
- PDF: https://mohdujjain.github.io/world-history-dossier/World_History_Dossier.pdf
- Source: https://github.com/MohdUjjain/world-history-dossier/tree/main/src

Open the image URL directly to make sure it loads. Share the exact website root URL on WhatsApp to test its link preview. If WhatsApp shows a previously cached thumbnail, try appending `?v=2` temporarily.

The Open Graph title, description, image URL, image type, dimensions, and Twitter/X card data are in the literal HTML `<head>`; JavaScript is not required for crawlers to find them.

## Continued publishing

Update chapter files under `src/chapters/`, then run `python src/build.py -o index.html`. Update the pre-rendered PDF separately if chapter content changes. Commit both source and built HTML. If you change the shared CSS or JavaScript, keep `CSS_DOC.md` / `JS_DOC.md` current in the same commit.
