# metalytics.co.uk

Static snapshot of the Metalytics website (www.metalytics.co.uk), captured from
the live Wix site with saveweb2zip and uploaded here as the starting point for
moving the site to Hostinger.

## What is in here

| Path | Contents |
| --- | --- |
| `index.html` | The homepage, as rendered by Wix |
| `images/` | Images referenced by the homepage |
| `fonts/` | Web fonts (Avenir, DIN Next, Helvetica, Proxima Nova, Open Sans) |
| `js/` | JavaScript bundles saved alongside the page |
| `media/file.mp4` | Background/promo video used on the homepage |

## Known limitations of this snapshot

This is a capture of one page, not a working standalone site. Before it can be
hosted anywhere, three things need dealing with:

1. **Only the homepage was captured.** The navigation links to
   `/automation`, `/pharma`, `/privacy-policy` and `/cookie-policy`, and to a
   PDF under `/_files/ugd/`. None of those were saved.
2. **Internal links are absolute** to `https://www.metalytics.co.uk/...`, so
   they point back at the live Wix site rather than at local files.
3. **The page still loads 20 scripts and stylesheets from Wix's CDN**
   (`static.parastorage.com`, `siteassets.parastorage.com`). Those bundles are
   tied to the site's Wix `metaSiteId` and revision, so the layout depends on
   Wix continuing to serve them.
