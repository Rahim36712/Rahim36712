"""Build self-contained profile artwork. Run from any working directory.

Biographical content comes only from the supplied Data Engineer Intern CV.
Portrait geometry comes from the user-supplied avatar's generated line-art study.
Rebuilds use the bundled Comfortaa font and fontTools; rendered SVGs do not
load fonts, scripts, or third-party resources.
"""

from pathlib import Path
import json
import re
from font_outlines import outlined_text, measure, wrap

OUT = Path(__file__).resolve().parents[1] / "assets"
INK, PAPER, TEAL, COPPER = "#FFFFFF", "#34402B", "#5B6D32", "#7F9058"
VIOLET, CORAL, MINT = "#657735", "#697C40", "#74874F"
MUTED, LINE, SOFT = "#68735E", "#DFE5D2", "#F3F6EB"
SANS = MONO = SERIF = "Comfortaa"
EASE = 'calcMode="spline" keyTimes="0;0.5;1" keySplines="0.42 0 0.58 1;0.42 0 0.58 1"'


def text(x, y, value, size=16, color=PAPER, family=SANS, **attrs):
    weight = int(attrs.pop("font_weight",500))
    spacing = float(attrs.pop("letter_spacing",0))
    anchor = attrs.pop("text_anchor","start")
    return outlined_text(x,y,value,size,color,weight,spacing,anchor,**attrs)


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
        strokes.append(f'''<path d="{path['d']}" pathLength="1" fill="none" stroke="{colors[(i//9)%len(colors)]}" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="1" stroke-dashoffset="1">
          <animate attributeName="stroke-dashoffset" values="1;1;0;0" keyTimes="0;{start/32:.5f};{end/32:.5f};1" dur="32s" repeatCount="indefinite" calcMode="spline" keySplines="0.42 0 0.58 1;0.42 0 0.58 1;0.42 0 0.58 1"/>
        </path>''')
    return f'''<g id="portrait" transform="translate({x} {y}) scale({scale})" opacity="1">
      <animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.06;0.86;0.96;1" dur="32s" repeatCount="indefinite" calcMode="spline" keySplines="0.42 0 0.58 1;0.42 0 0.58 1;0.42 0 0.58 1;0.42 0 0.58 1"/>
      {''.join(strokes)}
    </g>'''


def typing(x, y, width, size=20):
    width = round(measure('&gt; draw(profile)',size)+5,2)
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
    <radialGradient id="glow"><stop stop-color="#D9E2C7" stop-opacity="0.35"/><stop offset="1" stop-color="{INK}" stop-opacity="0"/></radialGradient>
    <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">
      <path d="M32 0H0V32" fill="none" stroke="{PAPER}" stroke-opacity="0.035"/>
    </pattern>
  </defs>
  <rect width="{width}" height="{height}" rx="28" fill="{INK}"/>
  <ellipse cx="{width*0.72}" cy="{height*0.4}" rx="{width*0.45}" ry="{height*0.75}" fill="url(#glow)"/>
  <rect x="0.5" y="0.5" width="{width-1}" height="{height-1}" rx="28" fill="none" stroke="{LINE}"/>
  {content}
</svg>
'''


def header(mobile=False):
    if mobile:
        w, h = 480, 772
        parts = [
            text(28, 42, "DATA / FIELDNOTES", 12, TEAL, MONO, letter_spacing=2),
            text(28, 89, "MUHAMMAD", 18, MUTED, SANS, letter_spacing=4),
            text(24, 156, "Rahim Jamil", 50, TEAL, SERIF,font_weight=700),
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
            text(36, 160, "Rahim Jamil", 58, TEAL, SERIF,font_weight=700),
            '<rect x="40" y="187" width="464" height="2" fill="url(#accent)"/>',
            text(40, 229, "Python data pipelines, web scraping,", 19),
            text(40, 261, "SQL databases, and healthcare/genomic", 19),
            text(40, 293, "data applications.", 19),
            f'<path d="M546 32V440" stroke="{LINE}" fill="none"/>',
            text(582,43,"PORTRAIT / DRAWING DESK",11,MUTED,MONO,letter_spacing=1),
            portrait(564,65,0.5),
            typing(40,360,216,21),
            text(40,425,"EXTRACT / STRUCTURE / EXPLAIN",12,MUTED,MONO,letter_spacing=1),
            f'<rect x="40" y="384" width="464" height="2" fill="{LINE}"/>',
            '<rect x="40" y="384" width="464" height="2" fill="url(#accent)"><animate attributeName="width" values="0;0;464;464;0;0" keyTimes="0;0.06;0.73;0.86;0.96;1" dur="32s" repeatCount="indefinite" calcMode="spline" keySplines="0.42 0 0.58 1;0.42 0 0.58 1;0.42 0 0.58 1;0.42 0 0.58 1;0.42 0 0.58 1"/></rect>',
        ]
    return canvas(w, h, "Muhammad Rahim Jamil", "Python data pipelines, web scraping, SQL databases, and healthcare/genomic data applications. A prompt types while an olive line-art interpretation of the supplied avatar draws, holds, fades, and repeats every 32 seconds.", "\n  ".join(parts))


def skills(mobile=False):
    w, h = (480, 348) if mobile else (960, 220)
    margin = 28 if mobile else 40
    parts = [text(margin, 40, "WORKING TOOLKIT", 12, TEAL, MONO, letter_spacing=2)]
    labels = ["Python", "SQL", "JavaScript", "C++"]
    if mobile:
        xs, ys, bw = [28, 252, 28, 252], [68, 68, 120, 120], 200
    else:
        xs, ys, bw = [40, 264, 488, 712], [66]*4, 208
    for x, y, label in zip(xs,ys,labels):
        parts += [
            f'<rect x="{x}" y="{y}" width="{bw}" height="40" rx="20" fill="{SOFT}" stroke="{LINE}"/>',
            text(x+16, y+27, label, 17, TEAL, MONO,font_weight=600),
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


def icon(kind,x,y):
    shape = ('<path d="M21 10l9 9-5 5-9-9z M16 15l-4 4 M23 25v4 M15 37h22 M27 25c11 0 12 11 3 12 M16 31h10"/>'
             if kind=="research" else
             '<rect x="14" y="14" width="20" height="20" rx="5"/><path d="M19 8v6 M29 8v6 M19 34v6 M29 34v6 M8 19h6 M8 29h6 M34 19h6 M34 29h6"/>')
    return f'<g transform="translate({x} {y})" data-experience-icon="{kind}"><circle cx="24" cy="24" r="24" fill="{SOFT}"/><g fill="none" stroke="{TEAL}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{shape}</g></g>'


def experience(kind,mobile=False):
    research = kind=="research"
    role = "Research Software Engineering Intern" if research else "Embedded Software Intern"
    employer = "Biomedical Image and Signal Processing Lab (BIOMISA)" if research else "RISETech Pvt. Ltd"
    meta = "Jun 2026 – Jul 2026 · Rawalpindi, Pakistan" if research else "Jun 2025 – Aug 2025 · Islamabad, Pakistan"
    bullets = (["4 custom genomic tracks · 10+ React components","Cancer-genomic data: CNVs, SVs, SNVs, and gene annotations","Wakhan Genome Browser · HiGlass · PIXI.js"] if research else
               ["5+ Python data-processing pipelines","Real-time sensor telemetry · Pandas · NumPy","UART/SPI collection, decoding, and validation"])
    w = 480 if mobile else 960
    parts = [icon(kind,28 if mobile else 36,26)]
    y = 54
    for line in wrap(role,360 if mobile else 810,21 if mobile else 24,700):
        parts.append(text(92 if mobile else 106,y,line,21 if mobile else 24,TEAL,font_weight=700))
        y+=31
    y+=16 if mobile else 8
    for line in wrap(employer,424 if mobile else 810,16 if mobile else 18,600):
        parts.append(text(28 if mobile else 106,y,line,16 if mobile else 18,PAPER,font_weight=600))
        y+=27
    y+=4
    for line in wrap(meta,424 if mobile else 810,14):
        parts.append(text(28 if mobile else 106,y,line,14,MUTED))
        y+=25
    divider_y=y-3
    parts.append(f'<path d="M{28 if mobile else 106} {divider_y}H{w-32}" fill="none" stroke="{LINE}"/>')
    y+=24
    for bullet in bullets:
        parts.append(f'<circle cx="{34 if mobile else 112}" cy="{y-5}" r="2.5" fill="{TEAL}"/>')
        for line in wrap(bullet,398 if mobile else 770,15 if mobile else 17):
            parts.append(text(48 if mobile else 128,y,line,15 if mobile else 17))
            y+=25 if mobile else 29
        y+=7
    return canvas(w,y+14,role,employer+". "+meta+". "+". ".join(bullets),"\n".join(parts))


def contact(label):
    w=round(measure(label,14,600)+44)
    title=label+" contact link"
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="40" viewBox="0 0 {w} 40" role="img" aria-label="{title}"><title>{title}</title><rect x="0.5" y="0.5" width="{w-1}" height="39" rx="19.5" fill="{TEAL}"/>{text(w/2,25,label,14,"#FFFFFF",font_weight=600,text_anchor="middle")}</svg>\n'


def static_svg(animated):
    # Motion points have no base coordinates; omit them in static artwork.
    static = re.sub(r'<circle\b[^>]*>\s*<animateMotion\b[^>]*/>(?:\s*<animate\b[^>]*/>)*\s*</circle>', "", animated)
    static = re.sub(r"<animate(?:Motion|Transform)?\b[^>]*/>", "", static)
    static = static.replace('stroke-dashoffset="1"','stroke-dashoffset="0"')
    return "\n".join(line.rstrip() for line in static.splitlines()) + "\n"


def main():
    OUT.mkdir(exist_ok=True)
    for name, builder in [("data-header", header), ("data-skills", skills)]:
        for mobile in [False, True]:
            stem = name + ("-mobile" if mobile else "")
            animated = builder(mobile)
            (OUT / f"{stem}.svg").write_text(animated, encoding="utf-8")
            static = static_svg(animated)
            (OUT / f"{stem}-static.svg").write_text(static, encoding="utf-8")
    for kind in ["research","embedded"]:
        for mobile in [False,True]:
            suffix="-mobile" if mobile else ""
            (OUT/f"experience-{kind}{suffix}.svg").write_text(static_svg(experience(kind,mobile)),encoding="utf-8")
    for label in ["Portfolio","LinkedIn","GitHub","Email"]:
        (OUT/f"contact-{label.lower()}.svg").write_text(contact(label),encoding="utf-8")
    print("Built 16 SVG assets with outlined Comfortaa typography.")


if __name__ == "__main__":
    main()
