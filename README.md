# metalytics.co.uk

Static snapshots of the Metalytics website (www.metalytics.co.uk), captured from
the live Wix site and uploaded here as the starting point for moving the site to
Hostinger.

## What is in here

| Path | Contents |
| --- | --- |
| `index.html` | Homepage, as rendered by Wix (saveweb2zip capture, assets in the folders below) |
| `automation.html` | `/automation` page — "Metadata Driven Automation" (single-file capture, 25 Nov 2026) |
| `pharma.html` | `/pharma` page — "Increase Statistical Programming Efficiency" (single-file capture, 25 Nov 2026) |
| `images/` | Images referenced by the homepage |
| `fonts/` | Web fonts (Avenir, DIN Next, Helvetica, Proxima Nova, Open Sans) |
| `js/` | JavaScript bundles saved alongside the homepage |
| `media/file.mp4` | Background/promo video used on the homepage |

Note that the two captures differ in format from `index.html`: they are
single-file saves with their images inlined as `data:` URIs, so they have no
matching asset folders of their own.

## Page inventory

| Live page | Captured |
| --- | --- |
| `/` (home) | Yes — `index.html` |
| `/automation` | Yes — `automation.html` |
| `/pharma` | Yes — `pharma.html` |
| `/privacy-policy` | No |
| `/cookie-policy` | No |
| TLF Lifecycle guide PDF (`/_files/ugd/`) | No |

## Known limitations of these snapshots

These are captures of individual pages, not a working standalone site. Before
anything here can be hosted, three things need dealing with:

1. **Two pages and the PDF are still missing** — see the inventory above.
2. **Internal links are absolute** to `https://www.metalytics.co.uk/...`, so
   they point back at the live Wix site rather than at each other.
3. **Every page still loads scripts and stylesheets from Wix's CDN**
   (`static.parastorage.com`, `siteassets.parastorage.com`,
   `static.wixstatic.com`) — around 240 references per page. Those bundles are
   tied to the site's Wix `metaSiteId` and revision, so the layout depends on
   Wix continuing to serve them.

## Forms

All three pages carry a Wix-hosted form with the same fields (First Name, Last
Name, Email, Message, Company, Position):

- home — "Request a meeting"
- `/automation` — "Request a Review"
- `/pharma` — "Request a Demo"

These are handled by Wix and will stop working as soon as the site leaves Wix.
A replacement needs choosing as part of the move.
