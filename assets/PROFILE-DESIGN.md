# Data Fieldnotes profile artwork

Biographical content comes only from the supplied Data Engineer Intern CV.
Contact destinations are the CV's embedded hyperlinks. No project repository
URLs were supplied, so project titles have no guessed links. The portrait is
a line-art interpretation of the avatar the user supplied in this conversation;
it is decorative and is not represented as a photograph of the profile owner.

## Colour and motion

White `#FFFFFF`, olive `#5B6D32`, dark olive text `#34402B`, soft olive surfaces
`#F3F6EB`, and pale borders `#DFE5D2`. Cards have 28px corners, skill pills have
20px corners, and contact links use fully rounded white/olive badges.

All custom artwork uses actual Comfortaa. The unmodified variable font and SIL
Open Font License live in `assets/fonts/`. `scripts/font_outlines.py` converts
its glyphs to SVG paths, so rendering does not depend on an installed font or a
font-loading request. Ordinary Markdown uses GitHub's fixed typography.

The two experience cards use the same typography and generous spacing, with
one small microscope/chip icon per role. They have separate mobile layouts.
Original experience text is preserved in the expandable Experience details.

The header replays every 32 seconds: the prompt types, 1,097 portrait centerlines
draw progressively in olive, the completed drawing holds, and it fades before restarting.
The name and CV summary remain visible throughout. These animations use SVG
SMIL, not JavaScript. SVGs have no external fonts, images or foreignObject.

The picture sources select dedicated mobile artwork below 600px and fully
drawn static artwork for reduced motion. The toolkit keeps its 30-second flow
and a 28-second gradient cycle, with no proficiency scores or invented metrics.

## Contribution snake

`.github/workflows/snake.yml` uses Platane/snk to read the actual contribution
calendar daily at 00:00 UTC. It also runs when the workflow or styling script is
updated, and can be manually dispatched. Actions are pinned to inspected commits.
Only its publishing job gets contents-write permission. The generated SVGs are
committed to the existing `output` branch; the source on `main` is preserved.

`scripts/style_snake.py` slows every synchronized track to at least 60 seconds
and makes static variants. Four output images cover light/dark and
animated/static preferences. The calendar includes GitHub contributions beyond
commits, so the section is labelled "Contribution trail".

## Rebuild

Run `python scripts/build_profile_assets.py` for all sixteen SVG assets: eight
header/toolkit variants, four experience cards, and four contact badges.
This uses fontTools, the bundled font, and checked-in `portrait-paths.json`.
If replacing the raster master, run `python scripts/trace_portrait.py` first;
that optional trace step requires OpenCV, NumPy and scikit-image. It traces
centerlines without changing the raster source.

Host the sixteen generated SVGs on `main` in `Rahim36712/Rahim36712`. The README
contains full raw URLs. Snake output is hosted on the `output` branch. Both
snake themes use a rounded white surface and the same olive palette. All
displayed images are repository-hosted; there are no badge/font services to load.

## Ideas researched

- [readme-typing-svg](https://github.com/DenverCoder1/readme-typing-svg): looping
  typing banners. We built a local version to synchronize typing and drawing.
- [Platane/snk](https://github.com/Platane/snk): generated contribution snakes,
  custom colours and light/dark palettes. This supplies the actual calendar.
- [lowlighter/metrics](https://github.com/lowlighter/metrics): broader account
  infographics. Additional metric panels were unnecessary for this layout.
- [GitHub markup pipeline](https://github.com/github/markup): page scripts and
  inline styles are stripped. GSAP cannot execute inside a GitHub README; the
  displayed assets instead run native SVG animation. Native link title tooltips
  provide the badge hover behaviour.

## Portrait master and generation prompt

The built-in imagegen tool generated `assets/portrait-line-art.png` from the
original avatar as an edit reference. `assets/portrait-paths.json` contains the
deterministically traced geometry. The original GitHub avatar was retained
outside tracked assets and was not replaced.

Final prompt:

> Use case: style-transfer. Asset type: line-art master for a stroke-by-stroke animated SVG in a GitHub profile README. Edit target: the referenced GitHub avatar. Convert ONLY its photographic rendering into clean, expressive black ink contour line art on a pure white background. Preserve the exact subject, visible dark mask/face, draped embroidered robe and head covering, raised open hand on the viewer's left, seated pose, book in the lower center, arm and fingers holding it. Keep the same composition and bottom crop. This should be instantly recognizable as the supplied avatar. Use thin black contour lines and a few stronger silhouette lines, with moderate details on the folds and embroidery. Avoid large solid black regions, halftone, hatching, grey shading, colour, gradients, lettering, borders, UI, watermarks, and new props. All lines should be crisp and separated enough for deterministic contour-to-SVG tracing. The only output is the square portrait illustration on white.
