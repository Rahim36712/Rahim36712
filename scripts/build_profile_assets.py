"""Build self-contained profile artwork. Run from any working directory.

Content is drawn only from Muhammad_Rahim_Jamil_Data_Engineer_Intern_CV.pdf.
No network access, fonts, scripts, or third-party SVG dependencies are required.
"""

from pathlib import Path
import re

OUT = Path(__file__).resolve().parents[1] / "assets"
INK, PAPER, TEAL, COPPER = "#142B32", "#F5F0E8", "#8BD5C5", "#D6A17B"
MUTED, LINE = "#A9BEBC", "#345057"
SANS = "Segoe UI, Arial, sans-serif"
MONO = "Consolas, Liberation Mono, monospace"
SERIF = "Georgia, Times New Roman, serif"
EASE = 'calcMode="spline" keyTimes="0;0.5;1" keySplines="0.42 0 0.58 1;0.42 0 0.58 1"'


def text(x, y, value, size=16, color=PAPER, family=SANS, **attrs):
    extra = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    return f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" fill="{color}" {extra}>{value}</text>'


def pulse():
    return f'<animate attributeName="opacity" values="0.3;0.8;0.3" dur="16s" repeatCount="indefinite" {EASE}/>'


def travel(path, duration="24s", phase="0s", color=TEAL):
    return f'''<circle r="4" fill="{color}" opacity="0.85">
      <animateMotion path="{path}" dur="{duration}" begin="{phase}" repeatCount="indefinite"
        calcMode="spline" keyTimes="0;1" keyPoints="0;1" keySplines="0.42 0 0.58 1"/>
      <animate attributeName="opacity" values="0;0.85;0.85;0" dur="{duration}" begin="{phase}" repeatCount="indefinite"
        calcMode="spline" keyTimes="0;0.12;0.88;1" keySplines="0.42 0 0.58 1;0.42 0 0.58 1;0.42 0 0.58 1"/>
    </circle>'''


def canvas(width, height, title, description, content):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">{title}</title>
  <desc id="desc">{description}</desc>
  <defs>
    <linearGradient id="accent" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{width}" y2="0">
      <stop offset="0" stop-color="{TEAL}">
        <animate attributeName="stop-color" values="{TEAL};{COPPER};{TEAL}" dur="28s" repeatCount="indefinite" {EASE}/>
      </stop>
      <stop offset="1" stop-color="{COPPER}">
        <animate attributeName="stop-color" values="{COPPER};{TEAL};{COPPER}" dur="28s" repeatCount="indefinite" {EASE}/>
      </stop>
    </linearGradient>
    <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">
      <path d="M32 0H0V32" fill="none" stroke="{PAPER}" stroke-opacity="0.035"/>
    </pattern>
  </defs>
  <rect width="{width}" height="{height}" rx="20" fill="{INK}"/>
  <rect width="{width}" height="{height}" rx="20" fill="url(#grid)"/>
  <rect x="0.5" y="0.5" width="{width-1}" height="{height-1}" rx="20" fill="none" stroke="{LINE}"/>
  {content}
</svg>
'''


def header(mobile=False):
    if mobile:
        w, h = 480, 468
        parts = [
            text(28, 42, "DATA / FIELDNOTES", 12, TEAL, MONO, letter_spacing=2),
            text(28, 89, "MUHAMMAD", 18, MUTED, SANS, letter_spacing=4),
            text(24, 156, "Rahim Jamil", 62, PAPER, SERIF),
            '<rect x="28" y="182" width="424" height="2" fill="url(#accent)"/>',
            text(28, 223, "Python data pipelines,", 22),
            text(28, 255, "web scraping, SQL databases,", 22),
            text(28, 287, "and healthcare/genomic", 22),
            text(28, 319, "data applications.", 22),
            '<path d="M40 373H216C236 373 236 408 256 408H440" fill="none" stroke="url(#accent)" stroke-width="2"/>',
            '<circle cx="40" cy="373" r="6" fill="#142B32" stroke="#8BD5C5" stroke-width="2"/>',
            '<circle cx="440" cy="408" r="6" fill="#142B32" stroke="#D6A17B" stroke-width="2"/>',
            travel("M40 373H216C236 373 236 408 256 408H440"),
            text(28, 438, "EXTRACT / STRUCTURE / EXPLAIN", 12, MUTED, MONO, letter_spacing=1),
        ]
    else:
        w, h = 960, 360
        parts = [
            text(40, 43, "DATA / FIELDNOTES", 13, TEAL, MONO, letter_spacing=2),
            text(40, 92, "MUHAMMAD", 18, MUTED, SANS, letter_spacing=4),
            text(36, 160, "Rahim Jamil", 72, PAPER, SERIF),
            '<rect x="40" y="187" width="504" height="2" fill="url(#accent)"/>',
            text(40, 229, "Python data pipelines, web scraping,", 21),
            text(40, 261, "SQL databases, and healthcare/genomic", 21),
            text(40, 293, "data applications.", 21),
            '<path d="M600 32V328" stroke="#345057" fill="none"/>',
            text(638, 43, "DATA PIPELINES", 12, MUTED, MONO, letter_spacing=2),
            '<path d="M660 100H715C748 100 748 169 782 169H900 M660 180H700C744 180 744 169 782 169 M660 260H715C748 260 748 169 782 169" fill="none" stroke="#345057" stroke-width="1.5"/>',
            travel("M660 100H715C748 100 748 169 782 169H900", "24s", "-4s"),
            travel("M660 180H700C744 180 744 169 782 169H900", "28s", "-12s", COPPER),
            travel("M660 260H715C748 260 748 169 782 169H900", "32s", "-19s"),
            '<rect x="637" y="86" width="64" height="28" rx="7" fill="#142B32" stroke="#345057"/>',
            '<rect x="637" y="166" width="80" height="28" rx="7" fill="#142B32" stroke="#345057"/>',
            '<rect x="637" y="246" width="96" height="28" rx="7" fill="#142B32" stroke="#345057"/>',
            text(651, 105, "WEB", 13, MUTED, MONO),
            text(651, 185, "SENSOR", 13, MUTED, MONO),
            text(651, 265, "GENOMIC", 13, MUTED, MONO),
            '<rect x="798" y="126" width="95" height="88" rx="12" fill="#142B32" stroke="#8BD5C5" stroke-opacity="0.55"/>',
            '<path d="M813 150H877 M813 169H854 M813 188H865" stroke="#8BD5C5" stroke-width="2" stroke-linecap="round"/>',
            f'<circle cx="886" cy="134" r="16" fill="none" stroke="{TEAL}" opacity="0.3">{pulse()}</circle>',
            text(815, 242, "STRUCTURE", 12, COPPER, MONO),
            text(638, 311, "EXTRACT / STRUCTURE / EXPLAIN", 11, MUTED, MONO),
        ]
    return canvas(w, h, "Muhammad Rahim Jamil", "Python data pipelines, web scraping, SQL databases, and healthcare/genomic data applications. Slow moving points illustrate data flow.", "\n  ".join(parts))


def skills(mobile=False):
    w, h = (480, 348) if mobile else (960, 220)
    margin = 28 if mobile else 40
    parts = [text(margin, 40, "WORKING TOOLKIT", 12, TEAL, MONO, letter_spacing=2)]
    labels = ["Python", "SQL", "JavaScript", "C++"]
    if mobile:
        xs, ys, bw = [28, 252, 28, 252], [68, 68, 120, 120], 200
    else:
        xs, ys, bw = [40, 264, 488, 712], [66]*4, 208
    for x, y, label in zip(xs, ys, labels):
        parts += [
            f'<rect x="{x}" y="{y}" width="{bw}" height="40" rx="8" fill="#1B363D" stroke="{LINE}"/>',
            text(x+16, y+27, label, 18, PAPER, MONO),
        ]
    if mobile:
        path = "M44 209H436C456 209 456 279 436 279H44"
        parts.append(f'<path d="{path}" fill="none" stroke="url(#accent)" stroke-width="1.5"/>')
        steps = [(44, 209, "EXTRACT"), (276, 209, "CLEAN"), (276, 279, "VALIDATE"), (44, 279, "TRANSFORM")]
    else:
        path = "M54 158H904"
        parts.append(f'<path d="{path}" fill="none" stroke="url(#accent)" stroke-width="1.5"/>')
        steps = [(54, 158, "EXTRACT"), (324, 158, "CLEAN"), (594, 158, "VALIDATE"), (864, 158, "TRANSFORM")]
    parts.append(travel(path, "30s"))
    for x, y, label in steps:
        label_x = x-16 if mobile else x
        anchor = "start" if mobile else ("end" if label == "TRANSFORM" else "start")
        parts += [
            f'<circle cx="{x}" cy="{y}" r="5" fill="{INK}" stroke="{TEAL}" stroke-width="1.5"/>',
            text(label_x, y+29, label, 12, MUTED, MONO, text_anchor=anchor, letter_spacing=1),
        ]
    return canvas(w, h, "Working toolkit", "Python, SQL, JavaScript, and C++. Data extraction, cleaning, validation, and transformation. The animation is decorative and does not represent proficiency or performance.", "\n  ".join(parts))


def main():
    OUT.mkdir(exist_ok=True)
    for name, builder in [("data-header", header), ("data-skills", skills)]:
        for mobile in [False, True]:
            stem = name + ("-mobile" if mobile else "")
            animated = builder(mobile)
            (OUT / f"{stem}.svg").write_text(animated, encoding="utf-8")
            # Motion points have no base coordinates; omit them in static artwork.
            static = re.sub(r'<circle\b[^>]*>\s*<animateMotion\b[^>]*/>(?:\s*<animate\b[^>]*/>)*\s*</circle>', "", animated)
            static = re.sub(r"<animate(?:Motion|Transform)?\b[^>]*/>", "", static)
            static = "\n".join(line.rstrip() for line in static.splitlines()) + "\n"
            (OUT / f"{stem}-static.svg").write_text(static, encoding="utf-8")
    print("Built 8 SVG assets (desktop/mobile, animated/static).")


if __name__ == "__main__":
    main()
