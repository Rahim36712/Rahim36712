"""Render actual Comfortaa glyphs as SVG paths, without browser font loading."""

from functools import lru_cache
from html import unescape
from pathlib import Path
from xml.sax.saxutils import quoteattr

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

FONT_PATH = Path(__file__).resolve().parents[1] / "assets/fonts/Comfortaa.ttf"


@lru_cache(maxsize=4)
def font(weight):
    return instantiateVariableFont(TTFont(FONT_PATH), {"wght": weight}, inplace=True)


def measure(value, size=16, weight=500, spacing=0):
    value = unescape(value)
    face = font(weight)
    cmap = face.getBestCmap()
    scale = size / face["head"].unitsPerEm
    return sum(face["hmtx"].metrics[cmap[ord(char)]][0] * scale for char in value) + max(0, len(value)-1)*spacing


def outlined_text(x, y, value, size=16, color="#34402B", weight=500, spacing=0, anchor="start", **attrs):
    value = unescape(value)
    face = font(weight)
    cmap = face.getBestCmap()
    glyphs = face.getGlyphSet()
    scale = size / face["head"].unitsPerEm
    width = measure(value,size,weight,spacing)
    cursor = x - (width if anchor=="end" else width/2 if anchor=="middle" else 0)
    pen = SVGPathPen(glyphs, ntos=lambda n: f"{n:.2f}".rstrip("0").rstrip(".") or "0")
    for char in value:
        name = cmap[ord(char)]
        glyphs[name].draw(TransformPen(pen,(scale,0,0,-scale,cursor,y)))
        cursor += face["hmtx"].metrics[name][0]*scale + spacing
    extra = " ".join(f'{key.replace("_","-")}={quoteattr(str(v))}' for key,v in attrs.items())
    return f'<g data-font="Comfortaa" data-weight="{weight}" data-text={quoteattr(value)} fill={quoteattr(color)} {extra}><path d="{pen.getCommands()}"/></g>'


def wrap(value, width, size=16, weight=500):
    lines, line = [], ""
    for word in value.split():
        candidate = (line + " " + word).strip()
        if line and measure(candidate,size,weight) > width:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    return lines
