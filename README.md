# SVGStereo: side by side SVG, with deep colour SDR and HDR

SVGStereo marks an authored stereo pair or a single-view procedural drawing with depth, and describes its intended colour rendering.
The stereo mark means two complete views side by side, left eye first, each at any resolution.
The optional colour marks cover deep colour SDR and HDR, independently of stereo.
They reuse PNG's colour fields and ITU-T H.273 code points.
CSS continues to define the colours within the drawing.

Status: proposal, version 0.3, 26 October 2026.
Editor: Daniel Ramos, for [Sparky Stereo OS](https://github.com/Sparky-OS/sparky-stereo-os).
This is an independent proposal, not an adopted W3C specification.
Comments and objections are welcome in this repository's issues.

## The namespace

The namespace is `https://github.com/Sparky-OS/svgstereo`.
The prefix `svgstereo` is a convention; readers match the namespace URI and local attribute name.
The five attributes below belong on the document's root `svg` element in the SVG namespace.
They have no meaning on descendants or in another namespace.
For `.svgz`, read the decompressed document.
These five attributes are optional and are not animatable.
The separate [procedural depth attributes](DEPTH.md) may also occur on graphics elements and groups; depth can animate.

| Attribute | Meaning |
|---|---|
| `svgstereo:layout` | The stereo layout |
| `svgstereo:cICP` | Intended rendered colour encoding, using H.273 |
| `svgstereo:sBIT` | Intended significant precision of the rendered components |
| `svgstereo:mDCV` | Mastering display colour volume |
| `svgstereo:cLLI` | Content light levels |

The capitalisation `cICP`, `sBIT`, `mDCV` and `cLLI` follows the PNG Third Edition Recommendation.
These are XML attributes, not PNG chunks or new H.273 code points.
The tuple syntax, SVG scope and rendering rules below are this proposal's additions.
The [source clauses](SOURCES.md) distinguish those additions from the existing standards.

## Side by side only

The only stereo value is `sideBySideLeftFirst`.
Without `layout`, the drawing is one picture unless its root explicitly opts into the [procedural depth path](DEPTH.md).
Any other layout value means one picture shown as authored.
The authored side by side path remains available alongside procedural doubling.
A reader never guesses a pair from the drawing's shape, proportions or colours.
There is no separate mono value and no alternate eye order value in version 0.3.

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

## Deep colour SDR and HDR

Colour metadata does not imply stereo, and stereo does not imply any colour encoding or precision.
The root colour description applies to the intended rendered picture and to both views of a pair.
It is static across the document's animation.

A renderer first interprets every paint, gradient, filter and embedded image according to SVG, CSS and that image's own colour description.
It must not reinterpret `#ffffff`, an `rgb()` value or an embedded sRGB image as PQ merely because the root says PQ.
A reader that supports this proposal converts the rendered result to the declared encoding, or uses a working representation that retains the same colour information.
It passes the actual representation's description to the next layer.
It must not attach the requested CICP values to pixels encoded another way.
The root metadata does not override CSS colour interpolation, compositing or `dynamic-range-limit`.

[CSS Color 4 §10.1 and §10.8](https://www.w3.org/TR/2026/CRD-css-color-4-20261022/#predefined) define `color()` and the `rec2020` colour space.
For example, `color(rec2020 0.4 0.3 0.2)` expresses wide-gamut colour without asserting PQ or HLG.
[CSS Color HDR Level 1 §7 and §8](https://www.w3.org/TR/2026/WD-css-color-hdr-1-20261008/#color-function) adds `rec2100-pq`, `rec2100-hlg` and `rec2100-linear`.
Its §3.1 defines `dynamic-range-limit`, which controls displayed headroom.
Those CSS documents are drafts, dated 22 October 2026 and 8 October 2026 respectively.
A colour syntax being specified does not establish support in a particular SVG renderer.

The proposed marks add intended component precision and applicable mastering and light-level metadata to this colour content.
They do not define another colour function, a tone mapping algorithm or a screen capability.
In Sparky Stereo OS, the application preserves this information and the compositor adapts it per output, following the [house formats](https://github.com/Sparky-OS/sparky-stereo-os/blob/main/docs/house-formats.md).
A reader that cannot preserve a requested encoding or precision should report that limitation and use its normal colour-managed fallback.
Absence of the marks does not authorise reducing existing deep colour SDR and HDR content to eight bits.

### Numeric syntax

Each colour attribute is a complete tuple of unsigned base-10 integers separated by XML whitespace.
Leading and trailing XML whitespace is allowed.
Signs, fractions, exponents, commas, missing fields and extra fields are invalid.
Leading zeroes are allowed and do not mean octal.
An invalid tuple is ignored as a whole, without affecting a valid stereo declaration or independent colour attributes.
An unknown attribute is ignored.
Readers must not silently clamp an out-of-range metadata integer into a different declaration.

### cICP

`svgstereo:cICP="ColorPrimaries TransferFunction MatrixCoefficients VideoFullRangeFlag"`

The field order matches PNG §11.3.2.6, Table 18.
The first two integers are H.273 enumerations in the range 0 to 255.
The matrix coefficient is 0 for this RGB representation.
The range flag is 1 for full range or 0 for narrow range, with H.273's range scaling applied when encoding actual samples.
The range flag does not change CSS's numeric syntax.
Reserved or unspecified primaries or transfer values do not identify a usable encoding here.
A reader that does not understand a code point ignores the CICP tuple and its dependent metadata, rather than inventing a transfer function.
Authors must use assigned code points appropriate to their content.

| Decimal tuple | Intended RGB encoding |
|---|---|
| `1 13 0 1` | sRGB primaries and sRGB transfer, SDR |
| `1 1 0 1` | BT.709 primaries and transfer, SDR |
| `9 1 0 1` | BT.2020 primaries with BT.709 transfer, wide-gamut SDR |
| `9 16 0 1` | BT.2020 primaries with PQ transfer |
| `9 18 0 1` | BT.2020 primaries with HLG transfer |

These examples use H.273 §8.1, §8.2 and §8.3, Tables 2 to 4.
Primaries alone do not distinguish SDR from HDR; transfer characteristics carry that distinction for these examples.
The encoding examples do not restrict the allowed precision values below.
The `9 1 0 1` tuple is not an assertion that CSS `rec2020` coordinates can be copied without colour conversion.

### sBIT

`svgstereo:sBIT="Red Green Blue"` or `svgstereo:sBIT="Red Green Blue Alpha"`

Each component is one of `8`, `10`, `12` or `16` significant bits.
The order follows the RGB and RGBA forms of PNG §11.3.2.4, Table 14.
In SVG this records the author's intended minimum significant precision on rasterisation, because vector drawing commands have no single original sample depth.
It does not assert that the source contains that many measured significant bits.
When alpha precision is omitted, it is unspecified, not zero and not a demand to discard transparency.
An absent `sBIT` leaves precision unspecified.
The attribute is useful for deep colour SDR and HDR alike, with or without `cICP`.

A supporting renderer chooses buffers and intermediate processing that retain at least the requested precision over the represented range.
A 16-bit floating-point storage label alone does not establish 16 significant bits per component.
Do not quantise a 10-, 12- or 16-bit request through an eight-bit intermediate and then expand it.
A reader should report an unmet precision request.
When exporting PNG, set its real sample depth and any `sBIT` from the resulting samples under PNG's rules; do not copy this intention as a claim about original raster precision.
For RGB PNG, 10 or 12 significant bits require a 16-bit sample container.

### mDCV

`svgstereo:mDCV="Rx Ry Gx Gy Bx By Wx Wy MaxLuminance MinLuminance"`

The field order and scales follow PNG §11.3.2.7, Table 19.

| Fields | Stored integer range | Physical value |
|---|---|---|
| `Rx Ry Gx Gy Bx By Wx Wy` | 0 to 65535 | Integer × 0.00002, CIE 1931 x or y |
| `MaxLuminance MinLuminance` | 0 to 2147483647 | Integer × 0.0001 cd/m² |

The chromaticity pairs describe the mastering display's red, green, blue and white point.
They describe the mastering display, which can have different primaries from the content encoding in `cICP`.
Use physically valid chromaticities and a maximum luminance greater than the minimum.
The four-byte integer ceiling follows PNG §7.1.

This attribute is optional and requires usable `cICP`, as in PNG.
It can describe a known SDR mastering display as well as PQ or HLG mastering.
Do not manufacture mastering measurements when they are unknown.
PNG notes that SDR adaptation from default viewing conditions to those signalled by mastering metadata lacks a standardised method.
This proposal does not supply one.

### cLLI

`svgstereo:cLLI="MaxCLL MaxFALL"`

Both integers range from 0 to 2147483647 and represent units of 0.0001 cd/m², as in PNG §11.3.2.8, Table 20 and §7.1.
Zero means unknown for that field.
For example, `10000000 2500000` means 1000 cd/m² and 250 cd/m².

The attribute is optional.
This SVG binding requires usable `cICP` so the luminance description has an identified encoding.
PNG defines these fields for HDR content; ordinary SDR content should omit `cLLI`, even when it uses deep colour or wide gamut.
SDR mastering information belongs in `mDCV` when it is known.

MaxCLL describes the maximum content light level across the rendered sequence.
MaxFALL describes the maximum frame average light level across that sequence.
For a still drawing the sequence contains one frame.
For a pair, a frame is the complete packed drawing, matching a PNG export of that drawing; MaxFALL is not a separate maximum for each eye.
A consumer must not label it as a measured per-eye value.
The same output adaptation policy should apply to both eyes.

Only supply nonzero values valid for all supported animation states and rendering conditions of the document.
If scripts, external resources, resolution-dependent effects, CSS headroom or an unknown background prevent that determination, omit the attribute or use zero for each unknown field.
Do not copy a single raster preview's statistics as a claim about every possible vector rendering.
Changed content requires recalculation or removal of stale light-level metadata.

## Examples of deep colour SDR and HDR

This one-picture example asks for 12 significant bits with wide-gamut SDR output.
Its CSS fill retains its CSS colour meaning and is converted to the requested output encoding.

```xml
<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:svgstereo="https://github.com/Sparky-OS/svgstereo"
     svgstereo:cICP="9 1 0 1" svgstereo:sBIT="12 12 12"
     viewBox="0 0 100 100">
  <rect width="100" height="100" fill="color(rec2020 0.4 0.3 0.2)"/>
</svg>
```

This pair asks for PQ output with 16 significant bits per colour component.
The example mastering display uses BT.2020 primaries, D65, a 4000 cd/m² maximum and a 0.0005 cd/m² minimum.
Those numbers are an illustrative declaration, not measurements of this drawing or proof of a reader's output.
Content light levels remain unknown.

```xml
<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:svgstereo="https://github.com/Sparky-OS/svgstereo"
     svgstereo:layout="sideBySideLeftFirst"
     svgstereo:cICP="9 16 0 1" svgstereo:sBIT="16 16 16 16"
     svgstereo:mDCV="35400 14600 8500 39850 6550 2300 15635 16450 40000000 5"
     svgstereo:cLLI="0 0"
     viewBox="0 0 200 100">
  <rect width="100" height="100" fill="color(rec2100-pq 0.58 0.58 0.58)"/>
  <rect x="100" width="100" height="100" fill="color(rec2100-pq 0.58 0.58 0.58)"/>
</svg>
```

The examples require support for their CSS colour functions to render as intended.
They are syntax examples, not visual or physical-display validation.

## Animated drawings

SVG animation uses the document timeline, including the animation elements described in [SVG 1.1 Second Edition, chapter 19](https://www.w3.org/TR/SVG11/animate.html).

1. Evaluate both views at the same document time and from the same state.
2. Keep the layout and root colour metadata fixed throughout playback, including playback controlled by script.
   Readers ignore animation of these attributes and retain their initial values for that playback.
3. Keep each view inside its half at every frame, including filter output and motion paths.
4. Draw moving depth through changing horizontal disparity between the views; the mark itself carries no depth.
5. A reader that cannot animate shows the initial drawing before animation runs, using the same split.

These rules retain version 0.2's shared timeline, stable packing, boundary, drawn depth and still fallback requirements for the single supported layout.
They do not require every reader to implement an animation engine.

## Readers that do not support the marks

[SVG 1.1 Second Edition §23.1](https://www.w3.org/TR/SVG11/extend.html#ForeignNamespaces) permits foreign attributes and specifies that unknown attributes are ignored.
Thus the attributes alone do not change ordinary SVG rendering.
This says nothing about support for a particular CSS colour function, preservation by every editor, or a sanitiser's policy.
A reader may support the stereo attribute while ignoring the colour attributes, or the reverse.
Ignoring colour metadata must not relabel unchanged samples as if the conversion had happened.

## Implementations and next work

Version 0.2 named [stereo-layer](https://github.com/Sparky-OS/stereo-layer) as a reader of its stereo mark in `.svg` and `.svgz` files.
That historical statement is not a claim of version 0.3 colour support.
Version 0.3 needs parser, precision, colour conversion and metadata propagation tests in readers.
Before writers emit the new attributes, register them in stereo-layer and the shared standards and house-format documentation.
No deep colour SDR and HDR rendering or physical-display conformance is claimed by this proposal.

## Changes from 0.2

Version 0.2, dated 14 October 2026, remains in [repository history](https://github.com/Sparky-OS/svgstereo/blob/a616813a888f9c3e28a58cab55033bc56c2ae04a/README.md).
Version 0.3 keeps only `sideBySideLeftFirst`, with complete views at any resolution.
It adds independent colour and precision marks for deep colour SDR and HDR, plus optional mastering and content light levels.
It retains and adapts the animation rules and makes per-file eye correction a reader action.
It adds procedural doubling with Union's three depth levels, graded shadows and a bounded reference reader.
Older layout values are not version 0.3 values; a reader claiming older-version support may still handle them under that older specification.
The namespace stays the same and carries no version discriminator, so old readers can retain their older layout behaviour.
The existing left-first value keeps its meaning.

## Licence

This text is dedicated to the public domain under [CC0 1.0](LICENSE): anyone may implement, copy or adapt it.
Quoted standards passages in [SOURCES.md](SOURCES.md) retain their source attribution and licences.
