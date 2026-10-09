"""Build self-contained profile artwork. Run from any working directory.

Biographical content comes only from the supplied Data Engineer Intern CV.
Portrait geometry comes from the user-supplied avatar's generated line-art study.
No network access, fonts, scripts, or third-party SVG dependencies are required.
"""

from pathlib import Path
import json
import re

OUT = Path(__file__).resolve().parents[1] / "assets"
INK, PAPER, TEAL, COPPER = "#101E32", "#FFF5E9", "#61D8EF", "#FFD582"
VIOLET, CORAL, MINT = "#C09AFF", "#FFA5A9", "#73E2BE"
MUTED, LINE = "#B4C6DF", "#344C6B"
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


def portrait(x, y, scale):
    data = json.loads((OUT / "portrait-paths.json").read_text(encoding="utf-8"))
    colors = [TEAL, VIOLET, MINT, COPPER, CORAL]
    strokes = []
    for i, path in enumerate(data["paths"]):
        start = 3 + 17 * i / max(1,len(data["paths"])-1)
        duration = min(3.5, max(0.8, path["length"] / 145))
        end = start + duration
        strokes.append(f'''<path d="{path['d']}" pathLength="1" fill="none" stroke="{colors[(i//9)%len(colors)]}" stroke-width="1.65" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="1" stroke-dashoffset="1">
          <animate attributeName="stroke-dashoffset" values="1;1;0;0" keyTimes="0;{start/32:.5f};{end/32:.5f};1" dur="32s" repeatCount="indefinite" calcMode="spline" keySplines="0.42 0 0.58 1;0.42 0 0.58 1;0.42 0 0.58 1"/>
        </path>''')
    return f'''<g id="portrait" transform="translate({x} {y}) scale({scale})" opacity="1">
      <animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.06;0.86;0.96;1" dur="32s" repeatCount="indefinite" calcMode="spline" keySplines="0.42 0 0.58 1;0.42 0 0.58 1;0.42 0 0.58 1;0.42 0 0.58 1"/>
      {''.join(strokes)}
    </g>'''


def typing(x, y, width, size=20):
    return f'''<g>
      <defs><clipPath id="typing-clip"><rect x="{x}" y="{y-size}" width="{width}" height="{size+10}">
        <animate attributeName="width" values="0;0;{width};{width};0;0" keyTimes="0;0.015;0.22;0.86;0.96;1" dur="32s" repeatCount="indefinite"/>
      </rect></clipPath></defs>
      {text(x,y,'&gt; draw(profile)',size,VIOLET,MONO,clip_path='url(#typing-clip)')}
      <rect x="{x+width}" y="{y-size+3}" width="2" height="{size}" fill="{TEAL}" opacity="0">
        <animate attributeName="x" values="{x};{x};{x+width};{x+width};{x};{x}" keyTimes="0;0.015;0.22;0.86;0.96;1" dur="32s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="0;0.9;0.3;0.9;0" keyTimes="0;0.1;0.5;0.86;1" dur="32s" repeatCount="indefinite"/>
      </rect>
    </g>'''


def canvas(width, height, title, description, content):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">{title}</title>
  <desc id="desc">{description}</desc>
  <defs>
    <linearGradient id="accent" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{width}" y2="0">
      <stop offset="0" stop-color="{TEAL}">
        <animate attributeName="stop-color" values="{TEAL};{COPPER};{TEAL}" dur="28s" repeatCount="indefinite" {EASE}/>
      </stop>
      <stop offset="0.5" stop-color="{VIOLET}"/>
      <stop offset="1" stop-color="{COPPER}">
        <animate attributeName="stop-color" values="{COPPER};{TEAL};{COPPER}" dur="28s" repeatCount="indefinite" {EASE}/>
      </stop>
    </linearGradient>
    <radialGradient id="glow"><stop stop-color="{VIOLET}" stop-opacity="0.2"/><stop offset="1" stop-color="{INK}" stop-opacity="0"/></radialGradient>
    <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">
      <path d="M32 0H0V32" fill="none" stroke="{PAPER}" stroke-opacity="0.035"/>
    </pattern>
  </defs>
  <rect width="{width}" height="{height}" rx="20" fill="{INK}"/>
  <ellipse cx="{width*0.72}" cy="{height*0.4}" rx="{width*0.45}" ry="{height*0.75}" fill="url(#glow)"/>
  <rect width="{width}" height="{height}" rx="20" fill="url(#grid)"/>
  <rect x="0.5" y="0.5" width="{width-1}" height="{height-1}" rx="20" fill="none" stroke="{LINE}"/>
  {content}
</svg>
'''


def header(mobile=False):
    if mobile:
        w, h = 480, 772
        parts = [
            text(28, 42, "DATA / FIELDNOTES", 12, TEAL, MONO, letter_spacing=2),
            text(28, 89, "MUHAMMAD", 18, MUTED, SANS, letter_spacing=4),
            text(24, 156, "Rahim Jamil", 62, "url(#accent)", SERIF),
            '<rect x="28" y="182" width="424" height="2" fill="url(#accent)"/>',
            text(28, 223, "Python data pipelines,", 22),
            text(28, 255, "web scraping, SQL databases,", 22),
            text(28, 287, "and healthcare/genomic", 22),
            text(28, 319, "data applications.", 22),
            typing(28,361,224,22),
            portrait(72,394,0.47),
            text(28,747,"EXTRACT / STRUCTURE / EXPLAIN",12,MUTED,MONO,letter_spacing=1),
        ]
    else:
        w, h = 960, 472
        parts = [
            text(40, 43, "DATA / FIELDNOTES", 13, TEAL, MONO, letter_spacing=2),
            text(40, 92, "MUHAMMAD", 18, MUTED, SANS, letter_spacing=4),
            text(36, 160, "Rahim Jamil", 72, "url(#accent)", SERIF),
            '<rect x="40" y="187" width="464" height="2" fill="url(#accent)"/>',
            text(40, 229, "Python data pipelines, web scraping,", 21),
            text(40, 261, "SQL databases, and healthcare/genomic", 21),
            text(40, 293, "data applications.", 21),
            '<path d="M546 32V440" stroke="#344C6B" fill="none"/>',
            text(582,43,"PORTRAIT / DRAWING DESK",11,MUTED,MONO,letter_spacing=1),
            portrait(564,65,0.5),
            typing(40,360,216,21),
            text(40,425,"EXTRACT / STRUCTURE / EXPLAIN",12,MUTED,MONO,letter_spacing=1),
            '<rect x="40" y="384" width="464" height="2" fill="#344C6B"/>',
            '<rect x="40" y="384" width="464" height="2" fill="url(#accent)"><animate attributeName="width" values="0;0;464;464;0;0" keyTimes="0;0.06;0.73;0.86;0.96;1" dur="32s" repeatCount="indefinite" calcMode="spline" keySplines="0.42 0 0.58 1;0.42 0 0.58 1;0.42 0 0.58 1;0.42 0 0.58 1;0.42 0 0.58 1"/></rect>',
        ]
    return canvas(w, h, "Muhammad Rahim Jamil", "Python data pipelines, web scraping, SQL databases, and healthcare/genomic data applications. A prompt types while a colourful line-art interpretation of the supplied avatar draws, holds, fades, and repeats every 32 seconds.", "\n  ".join(parts))


def skills(mobile=False):
    w, h = (480, 348) if mobile else (960, 220)
    margin = 28 if mobile else 40
    parts = [text(margin, 40, "WORKING TOOLKIT", 12, TEAL, MONO, letter_spacing=2)]
    labels = ["Python", "SQL", "JavaScript", "C++"]
    if mobile:
        xs, ys, bw = [28, 252, 28, 252], [68, 68, 120, 120], 200
    else:
        xs, ys, bw = [40, 264, 488, 712], [66]*4, 208
    for x, y, label, color, bg in zip(xs,ys,labels,[COPPER,TEAL,VIOLET,CORAL],["#3B3028","#193B4C","#30294E","#3E293C"]):
        parts += [
            f'<rect x="{x}" y="{y}" width="{bw}" height="40" rx="8" fill="{bg}" stroke="{color}" stroke-opacity="0.4"/>',
            text(x+16, y+27, label, 18, color, MONO),
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
            static = static.replace('stroke-dashoffset="1"','stroke-dashoffset="0"')
            static = "\n".join(line.rstrip() for line in static.splitlines()) + "\n"
            (OUT / f"{stem}-static.svg").write_text(static, encoding="utf-8")
    print("Built 8 SVG assets (desktop/mobile, animated/static).")


if __name__ == "__main__":
    main()
