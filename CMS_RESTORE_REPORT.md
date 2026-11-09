# Legacy CMS restore report

## Source

- Prepared `ncn_backup/` from `ncn.zip` (read-only `db.sqlite3`, `media/`, `core/`).
- No separate `ncn_backup` archive existed on disk beforehand.

## Command

```bash
python manage.py restore_legacy_cms --dry-run
python manage.py restore_legacy_cms
```

Idempotent: second run created **0** records and skipped existing ones.

## Restored into `main`

| Legacy source | Destination | Result |
|---|---|---|
| HomeHero + HomeHeroSlide (4) | `HeroSlide` | Created / filled |
| GivePage | `PageCopy` (`give`) | M-Pesa + cheque HTML restored |
| Membership | `DynamicPage` `membership` | Created / filled |
| Volunteer | `DynamicPage` `volunteer` | Created / filled (campus name corrected to Ngong Hills) |
| EGroup (7) | `DynamicPage` `egroups` | Intro + ABCDEs stored in `content` |
| Plugin (8) | `DynamicPage` `prayer` | Plug-In objectives + how-to stored in `content` |
| Quest (4) | `DynamicPage` `quest` | Sections stored in `content` |
| ClubFusion (6) | `DynamicPage` `club-fusion` | Sections stored in `content` |
| ClubFusionResource (1) | `ClubFusionResource` | Created |
| Event (1) | `Event` | Created if missing |
| GalleryAlbum (2) + GalleryImage (36) | `GalleryAlbum` / `GalleryImage` | Created; images mapped to Cloudinary URLs |
| — | `DynamicPage` `gallery` | Engage-menu entry + `/gallery` pages |

## Could not map safely (legacy empty)

These tables had **0 rows** in the backup DB. Existing production records were **not** overwritten:

- `HomeAbout` → `FounderPurposeBlock`
- `OurServices` → `Service`
- `Pastorate` → `PastoralTeamSection`
- `Mens` → `mens-ministry`
- `Womens` → `womens-ministry`
- `BibleStudyContent` / `BibleStudyGuide` → bible-study page / `BibleStudyResource`

## Media notes

- Local backup `media/` files were copied into project `media/` where missing.
- Most gallery/hero paths in the legacy DB are Cloudinary public IDs (`media/gallery/...`). Restore maps them to `https://res.cloudinary.com/<cloud>/image/upload/...` using `CLOUDINARY_URL` / `CLOUDINARY_CLOUD_NAME`.
- ASSETS stems (`HOME1`, `HOME2`, …) are used only when a matching local file exists.

## Template notes

- eGroups / Plug-In / QUEST / Club Fusion dedicated partials remain visually unchanged (hardcoded markup already matched legacy copy). Restored HTML is available in CMS `DynamicPage.content` for admin editing.
- Give page body now renders with `|safe` so M-Pesa/cheque HTML displays correctly.
- New gallery list/detail templates serve restored albums.

## Tests

```bash
python manage.py check
python manage.py test main.tests
```

All restore + gallery tests passed; re-run creates no duplicates.
