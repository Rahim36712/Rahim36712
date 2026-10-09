# Profile artwork

The current README uses `data-header*.svg` and `data-skills*.svg`. The older
terminal artwork is retained for repository history and is not referenced.

Content comes only from the supplied Data Engineer Intern CV. Its embedded
hyperlinks supply the contact destinations. Project repository URLs were not
supplied in the CV, so project titles deliberately have no guessed links.

Palette: midnight ink `#142B32`, parchment `#F5F0E8`, sea-glass `#8BD5C5`, copper
`#D6A17B`. The name uses a system serif; supporting text uses system sans and
monospace fonts. SVGs contain no JavaScript, external resources, or foreignObject.

Motion: 16-second eased pulses, 24–32-second eased data flow, and a 28-second
gradient cycle. Flow points fade at the ends of each route for a smooth loop.
All essential text remains visible from the first frame.
The dots illustrate data processing; they are not proficiency scores or metrics.

The README's picture sources select dedicated mobile artwork below 600px and
static artwork when reduced motion is requested. The dark artwork is designed
to sit on both light and dark GitHub pages.

Rebuild with `python scripts/build_profile_assets.py`. Commit the README and all
eight `data-*.svg` files to the public `Rahim36712/Rahim36712` repository's `main`
branch. The full raw URLs in the README will then resolve. No workflow, token,
or SVG generation service is required; Shields.io supplies only contact badges.

GitHub renders links and their native title tooltips. Custom CSS hover effects
cannot be attached to the Markdown page.
