"""Give Platane/snk SVG output a calm replay and static reduced-motion variant."""

from pathlib import Path
import argparse
import re
import xml.etree.ElementTree as ET


def style(directory):
    for filename in ["github-contribution-grid-snake.svg", "github-contribution-grid-snake-dark.svg"]:
        path = directory / filename
        content = path.read_text(encoding="utf-8")
        ET.fromstring(content)
        # snk's emitted CSS uses ms durations. Keep all tracks synchronized.
        durations = re.findall(r"animation:[^;}]*?(\d+(?:\.\d+)?)ms", content)
        if not durations:
            raise ValueError(f"No snake timeline found in {filename}")
        factor = max(1, 60000 / min(float(value) for value in durations))
        content = re.sub(r'(animation:[^;}]*?)(\d+(?:\.\d+)?)ms', lambda match: match[1] + str(round(float(match[2])*factor)) + 'ms', content)
        # Embedded CSS executes as image styling, without page scripts.
        content = content.replace('</style>', '@media(prefers-reduced-motion:reduce){.s,.c,.u{animation:none!important}}</style>')
        path.write_text(content+'\n', encoding="utf-8")
        static = re.sub(r'@keyframes\s+[^{}]+\{(?:[^{}]|\{[^{}]*\})*\}', '', content)
        static = re.sub(r'animation(?:-[a-z-]+)?\s*:[^;{}]*(?:;|(?=\}))', '', static)
        static = re.sub(r'@media\(prefers-reduced-motion:reduce\)\{[^{}]*\{[^{}]*\}\}', '', static)
        ET.fromstring(static)
        path.with_name(path.stem+'-static.svg').write_text(static+'\n',encoding="utf-8")
        print(f"Styled {filename}; loop >=60s; static fallback saved.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory",type=Path,required=True)
    style(parser.parse_args().directory)
