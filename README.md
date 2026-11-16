# connect-test

Source of <https://connect-test.disclarion.com>, a fixture site for testing
Disclarion Connect scans end to end (pages, images, text, evidence and rules).
It is not a real site: every page carries `<meta name="robots" content="noindex">`
and this banner at the top:

> Test site for Disclarion Connect. Images and texts here are fixtures,
> including AI metadata on images that were not made by AI.

Static HTML on GitHub Pages: no build step, no tracking, no cookies.

## Pages

| Page | What it tests |
|---|---|
| `/` | Home, links to every page |
| `/blog/` | Blog index |
| `/blog/post-1/`, `/blog/post-2/` | An `og:image` cover (only in the meta tag) and a different first image in the content |
| `/blog/post-3/` | Same, and the `og:image` cover carries IPTC AI metadata (`blog/img/cover-3.jpg`) |
| `/gallery/` | Three plain images, no metadata |
| `/c2pa/` | `lighthouse-gothenburg.png`: Content Credentials from a signer on the C2PA trust list, digital source type `trainedAlgorithmicMedia` |
| `/ai/` | `ai-iptc.jpg`: unsigned IPTC XMP `Iptc4xmpExt:DigitalSourceType = trainedAlgorithmicMedia` |
| `/articles/a-1/` … `/a-3/` | Text only, inside `<article>` |

`robots.txt` allows everything (the Connect scanner honors robots.txt) and
points at `sitemap.xml`, which lists every page. `CNAME` sets the custom
domain; `.nojekyll` serves the files as they are.

## Images

- Made once by `tools/make_images.py` (Pillow); the output is committed. Rerunning
  it gives the same bytes. Two of them say "made by AI" in IPTC metadata although
  no AI made them; that is the point of the fixture.
- `c2pa/lighthouse-gothenburg.png` is a byte copy of the landing site's
  `public/c2pa-sample/lighthouse-gothenburg.png`, sha256
  `128bf5ac0565c89effaf9bfbca4f143cce319c23dae1776ff931d3547e0b0d53`. Never
  re-encode or edit it: any change breaks its Content Credentials.

## Changing the site

Add a page: write its `index.html` with the noindex meta and the banner, link it
from `/`, and add it to `sitemap.xml`.
