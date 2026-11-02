# SVGStereo: stereo pairs and depth in SVG

SVGStereo marks an authored stereo pair, or a single-view procedural drawing to be drawn with depth.
The stereo mark means two complete views side by side, left eye first, each at any resolution.
Colour stays with CSS, as everywhere else in SVG; SVGStereo adds no colour attributes.

Status: proposal, version 0.4, 2 November 2026.
Editor: Daniel Ramos, for [Sparky Stereo OS](https://github.com/Sparky-OS/sparky-stereo-os).
This is an independent proposal, not an adopted W3C specification.
It is open for incubation at [WICG/proposals#316](https://github.com/WICG/proposals/issues/316).
Comments and objections are welcome there and in this repository's issues.

## The namespace

The namespace is `https://github.com/Sparky-OS/svgstereo`.
The prefix `svgstereo` is a convention; readers match the namespace URI and local attribute name.
The attribute below belongs on the document's root `svg` element in the SVG namespace.
It has no meaning on descendants or in another namespace.
For `.svgz`, read the decompressed document.
The attribute is optional and is not animatable.
The separate [procedural depth attributes](DEPTH.md) may also occur on graphics elements and groups; depth can animate.

| Attribute | Meaning |
|---|---|
| `svgstereo:layout` | The stereo layout |

The [source clauses](SOURCES.md) distinguish this proposal's rules from the existing standards.

## Side by side only

The only stereo value is `sideBySideLeftFirst`.
Without `layout`, the drawing is one picture unless its root explicitly opts into the [procedural depth path](DEPTH.md).
Any other layout value means one picture shown as authored.
The authored side by side path remains available alongside procedural doubling.
A reader never guesses a pair from the drawing's shape, proportions or colours.
There is no separate mono value and no alternate eye order value in version 0.4.

```xml
<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:svgstereo="https://github.com/Sparky-OS/svgstereo"
     svgstereo:layout="sideBySideLeftFirst"
     viewBox="0 0 200 100">
  <rect x="0" y="0" width="100" height="100" fill="red"/>
  <rect x="100" y="0" width="100" height="100" fill="blue"/>
</svg>
```

A marked pair requires a valid `viewBox="x y width height"` with positive width and height.
It describes the complete packed drawing.
The left view occupies `(x, y, width/2, height)` and the right view occupies `(x + width/2, y, width/2, height)`.
The split is in the root user coordinate system, before the root viewport transform.
Each view keeps the aspect ratio of that rectangle for presentation.
Missing or invalid geometry makes the stereo declaration unusable; show one picture without guessing a boundary.
A stereo reader clips each view to its own rectangle, including strokes and filter effects.
An ordinary 2D reader shows the complete authored drawing.

Full side by side names the layout, not a size.
Rasterisation can use any resolution per view, including half-width or half-height source samples.
When unpacking an existing raster, copy each view's samples without stretching or squeezing them.
The presentation layer receives the views and their intended display geometry; it scales them for the output.
A transport that requires equal storage rectangles needs a common rasterisation size or padding and explicit crop information, not an undeclared resize.
SVGStereo itself declares neither a pixel count nor a display's packing.
Its left-first arrangement corresponds to `StereoMode` 1 in [RFC 9559 §5.1.4.1.28.3](https://www.rfc-editor.org/rfc/rfc9559.html#section-5.1.4.1.28.3).
Separately, the [IANA Matroska registry](https://www.iana.org/assignments/matroska) assigned StereoMode 15 through 20 for packed picture-and-depth raster layouts on 26 October 2026, after Track Plane Types 3 through 5 for separate depth tracks on 20 October.
Those container registrations reference [stereo-layer v1.9.0](https://github.com/Sparky-OS/stereo-layer/blob/v1.9.0/docs/depth-marks.md); they neither register an SVG attribute nor change this proposal's single side-by-side layout.

A reader may offer a per-file eye swap as a correction for the person viewing a pair.
Keep that choice in the reader's own per-file state, beside the resume position where applicable.
Do not change the file or its extended attributes automatically.
Offer to save the correction to the file only as an explicit user action.
Saving must exchange the authored views while retaining the left-first mark, then clear the stored correction so it is not applied twice.
A display's own eye swap remains an output setting.

## Procedural depth

A single-view drawing can opt in with `svgstereo:depth="screen"` on its root.
The reader draws its procedures once per eye, using Union's `sunk | screen | popped | <percentage> | <number>` vocabulary, the user's limits and one shared animation state.
[Procedural depth](DEPTH.md) defines the coordinates, shadow rules, nesting, exceptions and fallback.
The output remains full side by side, left eye first, at any resolution per view.
The authored pair is never doubled again.

## Colour

SVGStereo defines no colour attributes.
SVG takes its colours from CSS: [CSS Color 4](https://www.w3.org/TR/2026/CRD-css-color-4-20261101/) and [CSS Color 5](https://www.w3.org/TR/2026/WD-css-color-5-20261029/) for SDR, wide gamut included, and [CSS Color HDR](https://www.w3.org/TR/2026/WD-css-color-hdr-1-20261026/) for HDR.
Each element's colour names its own colour space, and CSS sets the minimum precision with which each space's values round-trip: 10 bits for `srgb` and `display-p3`, 12 for `rec2020` and 16 for `xyz` ([CSS Color 4 §16.5](https://www.w3.org/TR/2026/CRD-css-color-4-20261101/#serializing-color-function-values)), and 10 bits for `rec2100-pq` and `rec2100-hlg` and 16 for `rec2100-linear` ([CSS Color HDR §10.1](https://www.w3.org/TR/2026/WD-css-color-hdr-1-20261026/#serializing-color-function-values)).
Deep colour SDR and HDR in a drawing are therefore written in CSS, for a pair as for one picture.
Both views of a pair use the same colour processing, so each eye sees the same colours for the same element.

This pair is wide-gamut SDR; with `color(rec2100-pq 0.58 0.58 0.58)` in both views, the same pair is HDR.

```xml
<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:svgstereo="https://github.com/Sparky-OS/svgstereo"
     svgstereo:layout="sideBySideLeftFirst"
     viewBox="0 0 200 100">
  <rect width="100" height="100" fill="color(rec2020 0.4 0.3 0.2)"/>
  <rect x="100" width="100" height="100" fill="color(rec2020 0.4 0.3 0.2)"/>
</svg>
```

Version 0.3 proposed four more root attributes copying PNG Third Edition's `cICP`, `sBIT`, `mDCV` and `cLLI`.
Version 0.4 withdraws them, following Chris Lilley's review in [WICG/proposals#316](https://github.com/WICG/proposals/issues/316).
In a raster image every pixel uses the same colour model, while in CSS each element can use a different one, and the `cLLI` calculation counts pixels, not elements.

## Animated drawings

SVG animation uses the document timeline, including the animation elements described in [SVG 1.1 Second Edition, chapter 19](https://www.w3.org/TR/SVG11/animate.html).

1. Evaluate both views at the same document time and from the same state.
2. Keep the layout fixed throughout playback, including playback controlled by script.
   Readers ignore animation of the layout attribute and retain its initial value for that playback.
3. Keep each view inside its half at every frame, including filter output and motion paths.
4. Draw moving depth through changing horizontal disparity between the views; the mark itself carries no depth.
5. A reader that cannot animate shows the initial drawing before animation runs, using the same split.

These rules retain version 0.2's shared timeline, stable packing, boundary, drawn depth and still fallback requirements for the single supported layout.
They do not require every reader to implement an animation engine.

## Readers that do not support the marks

[SVG 1.1 Second Edition §23.1](https://www.w3.org/TR/SVG11/extend.html#ForeignNamespaces) permits foreign attributes and specifies that unknown attributes are ignored.
Thus the attributes alone do not change ordinary SVG rendering.
This says nothing about preservation by every editor, or a sanitiser's policy.

## Implementations and next work

Version 0.2 named [stereo-layer](https://github.com/Sparky-OS/stereo-layer) as a reader of its stereo mark in `.svg` and `.svgz` files.
That mark is unchanged in version 0.4.
The [reference reader](reference/README.md) checks the procedural depth path.

## Changes from 0.3

Version 0.3, dated 26 October 2026, remains in [repository history](https://github.com/Sparky-OS/svgstereo/blob/298f08e/README.md).
Version 0.4 withdraws its colour attributes `cICP`, `sBIT`, `mDCV` and `cLLI`, for the reasons under [Colour](#colour); colour in SVG stays with CSS.
A version 0.4 reader ignores those attributes in older files, as it ignores any unknown attribute.
The stereo layout, animation rules, per-file correction and procedural depth are unchanged.

## Changes from 0.2

Version 0.2, dated 14 October 2026, remains in [repository history](https://github.com/Sparky-OS/svgstereo/blob/a616813a888f9c3e28a58cab55033bc56c2ae04a/README.md).
Version 0.3 keeps only `sideBySideLeftFirst`, with complete views at any resolution.
It added independent colour and precision marks for deep colour SDR and HDR, plus optional mastering and content light levels; version 0.4 withdraws them.
It retains and adapts the animation rules and makes per-file eye correction a reader action.
It adds procedural doubling with Union's three depth levels, graded shadows and a bounded reference reader.
Older layout values are not version 0.3 or 0.4 values; a reader claiming older-version support may still handle them under that older specification.
The namespace stays the same and carries no version discriminator, so old readers can retain their older layout behaviour.
The existing left-first value keeps its meaning.

## Licence

This text is dedicated to the public domain under [CC0 1.0](LICENSE): anyone may implement, copy or adapt it.
Quoted standards passages in [SOURCES.md](SOURCES.md) retain their source attribution and licences.
