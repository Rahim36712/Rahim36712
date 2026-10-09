"""Trace the generated line-art master into centerline geometry for SVG replay.

Only needed when changing portrait-line-art.png. Normal asset rebuilds use the
checked-in JSON and Python's standard library. Tracing needs OpenCV, NumPy and
scikit-image; it never calls a service or changes the raster master.
"""

from pathlib import Path
import json
import math

import cv2
import numpy as np
from skimage.morphology import skeletonize

ROOT = Path(__file__).resolve().parents[1]


def main():
    image = cv2.imread(str(ROOT / "assets/portrait-line-art.png"), cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError("assets/portrait-line-art.png")
    image = cv2.resize(image, (720, 720), interpolation=cv2.INTER_AREA)
    skeleton = skeletonize(image < 155)
    coords = set(zip(*np.where(skeleton)))
    neighbors = {}
    for y, x in coords:
        nearby = []
        for dy, dx in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
            point = (y+dy, x+dx)
            if point not in coords:
                continue
            # Avoid extra branches caused by diagonal corner shortcuts.
            if dy and dx and ((y+dy, x) in coords or (y, x+dx) in coords):
                continue
            nearby.append(point)
        neighbors[(y,x)] = sorted(nearby)
    visited, chains = set(), []

    def edge(a, b):
        return tuple(sorted((a,b)))

    def walk(a, b):
        chain = [a, b]
        visited.add(edge(a,b))
        previous, current = a, b
        while len(neighbors[current]) == 2:
            following = next(p for p in neighbors[current] if p != previous)
            if edge(current,following) in visited:
                break
            visited.add(edge(current,following))
            chain.append(following)
            previous, current = current, following
        if len(chain) >= 6:
            chains.append(chain)

    for point in sorted(coords):
        if len(neighbors[point]) != 2:
            for following in neighbors[point]:
                if edge(point,following) not in visited:
                    walk(point,following)
    for point in sorted(coords):
        for following in neighbors[point]:
            if edge(point,following) not in visited:
                walk(point,following)

    paths = []
    for chain in chains:
        vertices = np.array([(x,y) for y,x in chain], dtype=np.float32)
        vertices = cv2.approxPolyDP(vertices, 0.65, False).reshape(-1,2)
        if len(vertices) < 2:
            continue
        length = sum(math.hypot(*(b-a)) for a,b in zip(vertices,vertices[1:]))
        if length < 7:
            continue
        d = "M" + " L".join(f"{x:g} {y:g}" for x,y in vertices)
        paths.append({"d":d,"length":round(length,2),"y":round(float(vertices[:,1].mean()),2)})
    # Major outlines first; then details arrive from top to bottom.
    major = sorted([p for p in paths if p['length'] > 110],key=lambda p:(p['y'],-p['length']))
    details = sorted([p for p in paths if p['length'] <= 110],key=lambda p:(p['y'],-p['length']))
    data = {"width":720,"height":720,"source":"portrait-line-art.png","paths":major+details}
    target = ROOT / "assets/portrait-paths.json"
    target.write_text(json.dumps(data,separators=(',',':'))+'\n',encoding='utf-8')
    print(f"Traced {len(paths)} centerline strokes to {target.name}.")


if __name__ == "__main__":
    main()
