"""Independent rendered regression for the proposed role/range/default binding."""
import json
from pathlib import Path
import subprocess
import sys

from PIL import Image

reference = Path(__file__).resolve().parent
out = Path(sys.argv[1]).resolve() / 'defaults-proof'
out.mkdir(parents=True, exist_ok=True)
# Union s1-0009 DepthTree::update(), origin 6a695e8b5130a1a3ccb8645e80e266423cb8d8ed:
# desktop declared.value_or(Depth::Popped); elementStep returns zero without shadow.
# Independent expectations: one unnested surface at +PoppedLimit=4; plain elements
# and explicit screen at zero; explicit background at -SunkLimit=-10.
# No expected value is read from placements(), placement.json or generated SVG.
cases = [
    ('popup-omitted', 'd:depth-range="desktop"', '#ff0011', 4),
    ('element-omitted', 'd:depth-range="element"', '#00ee22', 0),
    ('desktop-screen', 'd:depth-range="desktop" d:depth="screen"', '#1133ff', 0),
    ('default-range-screen', 'd:depth="screen"', '#ee22dd', 0),
    ('background-sunk', 'd:depth-range="desktop" d:depth="sunk"', '#ffaa11', -10),
]
groups = []
for i, (name, attrs, colour, _) in enumerate(cases):
    y = 80 + i * 130
    groups.append(f'<g id="{name}" {attrs}><rect x="100" y="{y}" width="220" height="100" fill="#222222"/>'
                  f'<rect x="150" y="{y+30}" width="24" height="24" fill="{colour}"/></g>')
source = out / 'input.svg'
source.write_text('<svg xmlns="http://www.w3.org/2000/svg" '
                  'xmlns:d="https://github.com/Sparky-OS/svgstereo" '
                  'viewBox="0 0 1920 900" d:depth="screen">' + ''.join(groups) + '</svg>\n')
subprocess.run([sys.executable, str(reference / 'reader.py'), str(source), str(out),
                '--limits', '10', '4', '1'], check=True)
images = [Image.open(out / f'{eye}.png').convert('RGBA') for eye in ('left', 'right')]

def centre(image, colour):
    pixel = tuple(bytes.fromhex(colour[1:])) + (255,)
    points = [(i % image.width, i // image.width) for i, p in enumerate(image.getdata()) if p == pixel]
    assert len(points) == 576, (colour, len(points))
    return tuple(sum(p[axis] for p in points) / len(points) for axis in (0, 1))

results = []
for name, _, colour, expected in cases:
    left, right = [centre(image, colour) for image in images]
    measured = left[0] - right[0]
    assert measured == expected and left[1] == right[1], (name, measured, expected)
    results.append(dict(case=name, expected=expected, measured=measured, vertical=left[1]-right[1]))
    print(f'PASS {name}: expected {expected}, measured {measured}, vertical 0', flush=True)
# The former unqualified no-shadow reading predicts zero for the first case.
assert results[0]['measured'] != 0
(out / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
print('PASS former unqualified no-shadow expectation rejected for desktop popup')
