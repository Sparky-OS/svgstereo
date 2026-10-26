#!/usr/bin/env python3
"""Static, rectangular-layer reference reader for the SVGStereo depth proposal."""
import argparse
import copy
import json
import math
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET

SVG = 'http://www.w3.org/2000/svg'
NS = 'https://github.com/Sparky-OS/svgstereo'
S = '{' + SVG + '}'
D = '{' + NS + '}'
ET.register_namespace('', SVG)
ET.register_namespace('svgstereo', NS)


def depth(value):
    if value is None:
        return None
    value = value.strip()
    if value in ('sunk', 'screen', 'popped'):
        return {'sunk': -1.0, 'screen': 0.0, 'popped': 1.0}[value]
    if not re.fullmatch(r'[+-]?(?:\d+(?:\.\d*)?|\.\d+)%?', value):
        return None
    number = float(value.rstrip('%')) / (100 if value.endswith('%') else 1)
    return number if -1 <= number <= 1 else None


def shadow(node, ids):
    """Recognise only the documented filter recipes, not arbitrary graph intent."""
    match = re.fullmatch(r'url\(#([^)]*)\)', node.get('filter', ''))
    if not match:
        return 0.0
    f = ids[match[1]]
    drop = f.find(S + 'feDropShadow')
    if drop is not None:
        dx, dy = float(drop.get('dx', '2')), float(drop.get('dy', '2'))
        sigma = float(drop.get('stdDeviation', '2'))
        return float(drop.get('flood-opacity', '1')) * (math.hypot(dx, dy) + sigma)
    tags = [n.tag.removeprefix(S) for n in f]
    # Inset: source alpha, blur, offset, source-minus-offset, coloured intersection, source then shade.
    if tags == ['feGaussianBlur', 'feOffset', 'feComposite', 'feFlood', 'feComposite', 'feMerge']:
        blur, offset, cut, flood, colour, merge = f
        if (blur.get('in') == 'SourceAlpha' and offset.get('in') == blur.get('result')
                and cut.get('in') == 'SourceAlpha' and cut.get('in2') == offset.get('result')
                and cut.get('operator') == 'out' and colour.get('operator') == 'in'
                and colour.get('in') == flood.get('result') and colour.get('in2') == cut.get('result')
                and [n.get('in') for n in merge] == ['SourceGraphic', colour.get('result')]):
            return -float(flood.get('flood-opacity', '1')) * (math.hypot(float(offset.get('dx', '0')), float(offset.get('dy', '0'))) + float(blur.get('stdDeviation', '0')))
    return 0.0


def round_away(value):
    return math.copysign(math.floor(abs(value) + 0.5), value)


def placements(root, limits, width):
    ids = {n.get('id'): n for n in root.iter() if n.get('id')}
    nodes = []

    def visit(element, parent=None):
        for child in element:
            if child.tag == S + 'defs':
                continue
            marked = child.tag == S + 'g' and (child.get(D + 'depth') is not None or child.get('filter') is not None or child.get(D + 'depth-range') is not None)
            current = parent
            if marked:
                if child.get('transform') or (parent and parent['element'].get('transform')):
                    raise ValueError('Reference profile requires untransformed rectangular layers')
                box = child.find(S + 'rect')
                if box is None:
                    raise ValueError('Reference layer needs its rectangular surface first')
                bounds = tuple(float(box.get(k, '0')) for k in ('x', 'y', 'width', 'height'))
                kind = child.get(D + 'depth-range', 'element')
                if kind not in ('element', 'desktop'):
                    kind = 'element'
                item = dict(element=child, id=child.get('id'), parent=parent, kind=kind,
                            declared=depth(child.get(D + 'depth')), shadow=shadow(child, ids), box=bounds)
                if not item['id']:
                    raise ValueError('Reference layers need IDs')
                item['surface'] = item if kind == 'desktop' else (parent['surface'] if parent else None)
                nodes.append(item)
                current = item
            visit(child, current)
    visit(root)
    strengths = {}
    for n in nodes:
        if n['kind'] == 'element' and n['declared'] is None:
            key = (n['surface']['id'] if n['surface'] else None, n['shadow'] > 0)
            strengths[key] = max(strengths.get(key, 0), abs(n['shadow']))
    for n in nodes:
        p = n['parent']
        if n['declared'] is not None:
            step = n['declared']
        elif n['kind'] == 'desktop':
            step = 1
        else:
            key = (n['surface']['id'] if n['surface'] else None, n['shadow'] > 0)
            step = n['shadow'] / strengths[key] if strengths.get(key, 0) else 0
        if n['kind'] == 'desktop':
            base = p['surface']['raw'] if p and p['surface'] else 0
        else:
            base = p['raw'] if p and p['kind'] == 'element' else 0
        n['raw'] = base + step
        x, y, w, h = n['box']
        _, _, vw, vh = map(float, root.get('viewBox').split())
        n['edge'] = x <= 0 or y <= 0 or x + w >= vw or y + h >= vh
        if n['edge'] and n['raw'] > 0:
            n['raw'] = 0
    reaches = {}
    for n in nodes:
        key = 'desktop' if n['kind'] == 'desktop' else ('element', n['surface']['id'] if n['surface'] else None)
        n['key'] = key
        low, high = reaches.get(key, (-1, 1))
        reaches[key] = min(low, n['raw']), max(high, n['raw'])
    for n in nodes:
        low, high = reaches[n['key']]
        n['fit'] = n['raw'] / (high if n['raw'] >= 0 else -low)
        p = n['parent']
        if n['kind'] == 'desktop' and p and p['surface'] and not n['edge']:
            n['fit'] = max(n['fit'], p['surface']['fit'])
    for n in nodes:
        surface = n['surface']
        desktop = surface['fit'] if surface else 0
        internal = n['fit'] if n['kind'] == 'element' else 0
        ref = desktop * (limits[1] if desktop >= 0 else limits[0]) + internal * limits[2]
        n['disparity'] = int(round_away(ref * width / 1920))
        if n['edge'] and n['disparity'] > 0:
            n['disparity'] = 0
    return nodes


def eye_shift(d, eye):
    right = -math.trunc(d / 2)
    return d + right if eye == 'left' else right


def make_eye(source, limits, width, eye, flat=False):
    root = copy.deepcopy(source)
    nodes = placements(root, limits, width)
    defs = root.find(S + 'defs')
    if defs is None:
        defs = ET.SubElement(root, S + 'defs')
    ids = {n.get('id'): n for n in root.iter() if n.get('id')}
    parents = {c: p for p in root.iter() for c in p}
    view_width = float(root.get('viewBox').split()[2])
    unit = view_width / width
    for n in nodes:
        el, p = n['element'], n['parent']
        own = 0 if flat else eye_shift(n['disparity'], eye)
        inherited = 0 if flat or not p else eye_shift(p['disparity'], eye)
        delta = (own - inherited) * unit
        container = parents[el]
        pos = list(container).index(el)
        container.remove(el)
        clip = ET.Element(S + 'g')
        translated = ET.SubElement(clip, S + 'g', {'transform': f'translate({delta:g} 0)'})
        translated.append(el)
        container.insert(pos, clip)
        # A sunk layer is a window onto content moving behind its own stationary rectangle.
        if n['disparity'] < (p['disparity'] if p else 0) and not flat:
            cid = f'cut-{n["id"]}-{eye}'
            cp = ET.SubElement(defs, S + 'clipPath', {'id': cid, 'clipPathUnits': 'userSpaceOnUse'})
            ET.SubElement(cp, S + 'rect', dict(zip(('x','y','width','height'), map(str, n['box']))))
            clip.set('clip-path', f'url(#{cid})')
        match = re.fullmatch(r'url\(#([^)]*)\)', el.get('filter', ''))
        if match:
            f = copy.deepcopy(ids[match[1]])
            drop = f.find(S + 'feDropShadow')
            if drop is not None:
                # Cast shadow stays on its receiver, as in Union s1-0012.
                drop.set('dx', str(float(drop.get('dx', '2')) - delta))
                fid = f'{match[1]}-{n["id"]}-{eye}'
                f.set('id', fid)
                defs.append(f)
                el.set('filter', f'url(#{fid})')
    return root, nodes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--limits', type=float, nargs=3, default=[10, 4, 1])
    parser.add_argument('--width', type=int, default=1920)
    args = parser.parse_args()
    source = ET.parse(args.input).getroot()
    geometry = list(map(float, source.get('viewBox', '').split()))
    if len(geometry) != 4 or geometry[:2] != [0, 0] or min(geometry[2:]) <= 0:
        raise ValueError('Reference profile requires a positive zero-origin viewBox')
    if args.width <= 0 or any(not math.isfinite(v) or v < 0 for v in args.limits):
        raise ValueError('Width must be positive and limits finite and nonnegative')
    if source.get(D + 'layout') is not None:
        raise ValueError('Reference script accepts procedural input only; authored pairs stay authored')
    if depth(source.get(D + 'depth')) != 0:
        raise ValueError('Reference profile opts in with root depth="screen"')
    forbidden = {'script', 'animate', 'animateMotion', 'animateTransform', 'set', 'style', 'foreignObject'}
    if any(n.tag.removeprefix(S) in forbidden for n in source.iter()):
        raise ValueError('Static reference profile needs an already evaluated document snapshot')
    if any(n.get('transform') for n in source.iter()):
        raise ValueError('Static reference profile does not support authored transforms')
    args.output.mkdir(parents=True, exist_ok=True)
    records = None
    for eye in ('left', 'right', 'flat'):
        root, nodes = make_eye(source, args.limits, args.width, eye, flat=eye == 'flat')
        path = args.output / f'{eye}.svg'
        ET.ElementTree(root).write(path, encoding='utf-8', xml_declaration=True)
        subprocess.run(['rsvg-convert', '--width', str(args.width), '--output', str(args.output / f'{eye}.png'), str(path)], check=True)
        records = [{k: n[k] for k in ('id','box','raw','fit','disparity','edge')} for n in nodes]
    (args.output / 'placement.json').write_text(json.dumps(records, indent=2) + '\n')
    # Raster packing occurs only after the two independent procedural render passes.
    from PIL import Image
    left = Image.open(args.output / 'left.png').convert('RGBA')
    right = Image.open(args.output / 'right.png').convert('RGBA')
    pack_pair(left, right, args.output / 'pair.png')


def pack_pair(left, right, path):
    from PIL import Image, PngImagePlugin
    if left.size != right.size:
        raise ValueError('PNG sTER requires equal-size views')
    padding = (-left.width) % 8
    pair = Image.new('RGBA', (left.width * 2 + padding, left.height))
    pair.paste(left, (0, 0))
    pair.paste(right, (left.width + padding, 0))
    info = PngImagePlugin.PngInfo()
    info.add(b'sTER', b'\x01')
    pair.save(path, pnginfo=info)

if __name__ == '__main__':
    main()
