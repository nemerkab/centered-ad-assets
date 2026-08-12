# Centered Software — Meta ad creative

Static ad images for Meta Ads, rendered from HTML/CSS via headless Chrome.
Brand tokens taken from centeredsoftware.com.

## Packs

| Folder | Destination | Notes |
|---|---|---|
| `start-apply/` | `/start/apply` | **Current** — 10 concepts, 1:1 + 4:5 PNGs, Meta copy in `CONCEPTS.md` |
| Root `build.py` + `images/` | Earlier exploratory set (4 concepts) | Superseded for the apply funnel |

### `start-apply/` (use this)

```bash
cd start-apply && python3 build.py
```

- `start-apply/images/` — PNGs ready to drop into Meta
- `start-apply/CONCEPTS.md` — primary text / headline / description per concept
- `start-apply/html/` — source pages for regeneration

Images can be hosted so Meta's uploader can fetch them by public URL.
Once uploaded, Meta stores its own copy by hash — URLs are only needed at upload time.
