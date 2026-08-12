# Centered Software — Meta ad creative

Static ad images for Meta Ads, rendered from HTML/CSS via headless Chrome.
Brand tokens taken from centeredsoftware.com.

- `build.py` — regenerates all creative
- `images/` — rendered PNGs (1080x1080 and 1080x1350)

Images are hosted here so Meta's ad image uploader can fetch them by public URL.
Once uploaded, Meta stores its own copy and references it by hash — these URLs
are only needed at upload time.

Regenerate: `python3 build.py`
