# metalytics.co.uk

The Metalytics website, rebuilt as a plain static site for Hostinger. It replaces
the Wix build and has no dependency on Wix, its CDN or its runtime.

## Pages

| URL | File | Notes |
| --- | --- | --- |
| `/` | `index.html` | Home |
| `/automation` | `automation.html` | Metadata Driven Automation |
| `/pharma` | `pharma.html` | Statistical programming / PharmaBot |
| `/privacy-policy` | `privacy-policy.html` | Policy text unchanged, last updated 20 May 2018 |
| `/cookie-policy` | `cookie-policy.html` | Policy text unchanged |
| `/thank-you` | `thank-you.html` | Shown after a form POST without JavaScript |
| — | `404.html` | Served by `ErrorDocument` |

Extensionless URLs are handled by `.htaccess`, which also redirects `/page.html`
to `/page` so each page has one canonical address.

## Layout

| Path | Contents |
| --- | --- |
| `assets/css/site.css` | All styling — one file, no framework |
| `assets/js/site.js` | Mobile navigation and in-place form submission |
| `assets/img/` | Logo, hero, illustrations and the Pharma feature panels |
| `assets/docs/` | The TLF lifecycle guide offered on the homepage |
| `contact.php` | Enquiry form handler (all three forms) |
| `_build/build.py` | Regenerates the HTML pages from shared header, footer and form |
| `_snapshot/` | The original Wix captures, kept for reference. Blocked from the public site |

Both `_build/` and `_snapshot/` are denied in `.htaccess`, so they stay in the
repository without being served.

## Editing

The five pages share one header, footer and form. Edit `_build/build.py` and run:

```sh
python3 _build/build.py
```

That rewrites the HTML files. Editing a built `.html` file directly works too,
but the change is lost the next time the builder runs.

## Forms

The three forms (Request a meeting / Request a Review / Request a Demo) all post
to `contact.php`, which validates the input, blocks header injection, carries a
honeypot field against bots, and emails the enquiry.

**Before go-live, set the destination inbox** at the top of `contact.php`:

```php
const MAIL_TO   = 'info@metalytics.co.uk';   // where enquiries land
const MAIL_FROM = 'no-reply@metalytics.co.uk';  // must stay on this domain
```

`MAIL_FROM` has to be an address on the site's own domain or Hostinger will
refuse to send. Create both mailboxes in hPanel first.

## Still outstanding

1. **Fonts.** The Wix build used Avenir, DIN Next, Helvetica and Proxima Nova,
   which are licensed to Wix and were not carried over. The site uses the
   system font stack instead. Licensing a webfont is a separate decision.
2. **Analytics.** The cookie policy mentions Google Analytics; no analytics tag
   is installed on this build.

## History

The first two commits hold the saveweb2zip and single-file captures of the Wix
site. They are kept in `_snapshot/` as the record of what the site looked like
before the move.
