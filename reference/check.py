from pathlib import Path
from PIL import Image
import json
import subprocess
import sys
import xml.etree.ElementTree as ET

reference = Path(__file__).resolve().parent
evidence = Path(sys.argv[1]).resolve()
evidence.mkdir(parents=True, exist_ok=True)
sample = reference / 'sample.svg'
reader = reference / 'reader.py'
# Predictions from the source style and independent hand arithmetic, not reader output.
# Outer strengths .6*(8+4)=7.2 and .6*(2+2)=2.4 -> 1 and 1/3.
# Inset strongest -> -1; desktop stack has 3 equal steps -> 1/3,2/3,1.
colors = {'background': '#ffd100', 'card':'#ff00bb', 'weak-card':'#00e5ff',
          'field':'#aaff00', 'menu':'#ff6400', 'submenu':'#aa00ff', 'item':'#00ff88',
          'declared-screen':'#ffaaaa', 'edge':'#aaccff'}
cases = {'default': ([10,4,1], [-10,1,0,-1,1,3,4,0,0]),
         'internal12': ([10,4,12], [-10,12,4,-12,1,3,4,0,0]),
         'all12': ([12,12,12], [-12,12,4,-12,4,8,12,0,0]),
         'off': ([0,0,0], [0]*9)}

def marker(image, color):
    rgb = tuple(bytes.fromhex(color[1:]))
    coords = [(i % image.width, i // image.width) for i,p in enumerate(image.getdata()) if p[:3] == rgb and p[3] == 255]
    assert len(coords) == 576, (color, len(coords))
    return (sum(x for x,y in coords)/len(coords), sum(y for x,y in coords)/len(coords))

results = []
for name, (limits, expected) in cases.items():
    out = evidence / 'proof' / name
    subprocess.run([sys.executable, str(reader), str(sample), str(out), '--limits', *map(str, limits)], check=True)
    left, right, flat = [Image.open(out / f'{eye}.png').convert('RGBA') for eye in ('left','right','flat')]
    observed = []
    for (element, color), prediction in zip(colors.items(), expected):
        a,b = marker(left,color), marker(right,color)
        d = a[0] - b[0]
        assert d == prediction, (name,element,d,prediction)
        assert a[1] == b[1], (name,element,'vertical drift')
        observed.append(d)
    # Every eye retains procedural nodes, including the original seed.
    for eye in ('left', 'right'):
        eye_tree = ET.parse(out / f'{eye}.svg')
        assert all(n.get('seed') == '270' for n in eye_tree.iter('{http://www.w3.org/2000/svg}feTurbulence'))
    # Align only after two renders, to measure identity of the procedure carried with the card.
    card_d = expected[1]
    rs = -int(card_d/2); ls = card_d + rs
    a = left.crop((170+ls,240,350+ls,340))
    b = right.crop((170+rs,240,350+rs,340))
    unequal = sum(x != y for x,y in zip(a.getdata(),b.getdata()))
    assert unequal == 0, (name, 'noise swims', unequal)
    # Exclude a constant fill from satisfying the identity test accidentally.
    assert len(set(a.getdata())) > 1000
    baseline = out / 'baseline.png'
    subprocess.run(['rsvg-convert','--output',str(baseline),str(sample)],check=True)
    baseline = Image.open(baseline).convert('RGBA')
    assert flat.tobytes() == baseline.tobytes(), (name,'2D fallback changed')
    if name == 'off':
        assert left.tobytes() == baseline.tobytes() == right.tobytes()
    if name == 'all12':
        assert sum(v != 0 for v in expected) == 7
        assert any(marker(flat,c)[0]-marker(flat,c)[0] != p for c,p in zip(colors.values(),expected))
        # Wrong seed is a negative control for procedural identity, not merely for placement.
        tree = ET.parse(out / 'right.svg')
        for n in tree.iter('{http://www.w3.org/2000/svg}feTurbulence'):
            n.set('seed','271')
        tree.write(out/'wrong-seed.svg')
        subprocess.run(['rsvg-convert','--output',str(out/'wrong-seed.png'),str(out/'wrong-seed.svg')],check=True)
        wrong = Image.open(out/'wrong-seed.png').convert('RGBA').crop((170+rs,240,350+rs,340))
        changed = sum(x != y for x,y in zip(a.getdata(),wrong.getdata()))
        assert changed > 1000
        # Pair must carry the PNG parallel-view declaration and consist of independent views.
        pair = Image.open(out/'pair.png').convert('RGBA')
        assert pair.size == (3840,900)
        assert pair.crop((0,0,1920,900)).tobytes() == left.tobytes()
        assert pair.crop((1920,0,3840,900)).tobytes() == right.tobytes()
        results.append({'negative_control_wrong_seed_differing_pixels':changed})
    results.append({'case':name,'limits':limits,'expected':expected,'measured':observed,'vertical_disparity':0,'noise_differing_pixels':unequal,'2d_differing_pixels':0})
    print(f'PASS {name}: 9/9 disparities, zero vertical drift, identical aligned noise and unchanged 2D',flush=True)
(evidence/'depth-results.json').write_text(json.dumps(results,indent=2)+'\n')
print('PASS: flat rendering rejects seven nonzero predictions; changed turbulence seed rejects noise identity')

subprocess.run([sys.executable, str(reference / 'check-packing.py'), str(evidence)], check=True)
