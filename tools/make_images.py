"""Makes the fixture images of connect-test.disclarion.com. Run once from the
repo root; the output is committed and nothing is built when the site is
served:

    python tools/make_images.py

Needs Pillow (made with 13.0.0). Plain colored cards with a caption, no
photos. Two of them carry IPTC XMP
Iptc4xmpExt:DigitalSourceType = trainedAlgorithmicMedia although no AI made
them: they are fixtures for Disclarion Connect's "AI evidence" path
(ai/ai-iptc.jpg and blog/img/cover-3.jpg).

c2pa/lighthouse-gothenburg.png is NOT made here: it is a byte copy of the
landing site's public/c2pa-sample/lighthouse-gothenburg.png (see README).
"""

import io
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
SIZE = (800, 450)
IPTC = "http://cv.iptc.org/newscodes/digitalsourcetype/"


def _xmp(source_type: str) -> bytes:
    return (
        '<x:xmpmeta xmlns:x="adobe:ns:meta/"><rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">'
        '<rdf:Description rdf:about="" xmlns:Iptc4xmpExt="http://iptc.org/std/Iptc4xmpExt/2008-02-29/" '
        f'Iptc4xmpExt:DigitalSourceType="{IPTC}{source_type}"/></rdf:RDF></x:xmpmeta>'
    ).encode()


def _card(color, caption: str) -> Image.Image:
    img = Image.new("RGB", SIZE, color)
    draw = ImageDraw.Draw(img)
    draw.rectangle((24, 24, SIZE[0] - 25, SIZE[1] - 25), outline=(255, 255, 255), width=4)
    draw.text((48, SIZE[1] - 72), caption, fill=(255, 255, 255), font_size=32)
    return img


def _save(rel: str, color, caption: str, xmp: bytes = None) -> None:
    out = io.BytesIO()
    kwargs = {"quality": 85}
    if xmp is not None:
        kwargs["xmp"] = xmp
    _card(color, caption).save(out, "JPEG", **kwargs)
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(out.getvalue())
    print(rel)


def main() -> None:
    # Blog: og:image covers (shown above each post's <article>) and a different
    # first-in-content image per post.
    _save("blog/img/cover-1.jpg", (32, 96, 160), "Cover 1 (og:image)")
    _save("blog/img/cover-2.jpg", (32, 140, 96), "Cover 2 (og:image)")
    _save("blog/img/cover-3.jpg", (150, 60, 120), "Cover 3 (og:image, IPTC AI fixture)",
          _xmp("trainedAlgorithmicMedia"))
    _save("blog/img/post-1-inline.jpg", (200, 120, 40), "Post 1, first in content")
    _save("blog/img/post-2-inline.jpg", (90, 90, 180), "Post 2, first in content")
    _save("blog/img/post-3-inline.jpg", (60, 130, 140), "Post 3, first in content")
    # Post 4 was added after a /blog/ rule existed (rules only decide new items).
    _save("blog/img/cover-4.jpg", (170, 130, 40), "Cover 4 (og:image)")
    _save("blog/img/post-4-inline.jpg", (120, 60, 160), "Post 4, first in content")
    # Gallery: plain images, no metadata.
    _save("gallery/img/plain-1.jpg", (110, 110, 110), "Gallery 1")
    _save("gallery/img/plain-2.jpg", (140, 80, 60), "Gallery 2")
    _save("gallery/img/plain-3.jpg", (60, 100, 70), "Gallery 3")
    # AI page: unsigned IPTC metadata only.
    _save("ai/ai-iptc.jpg", (180, 70, 50), "IPTC AI fixture (not made by AI)",
          _xmp("trainedAlgorithmicMedia"))


if __name__ == "__main__":
    main()
