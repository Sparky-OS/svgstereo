# Source clauses for SVGStereo 0.3

Checked on 26 October 2026 for the side by side and deep colour SDR and HDR proposal.
Short quotations below identify the relied-on clauses; the linked sections contain the full requirements.
The standards do not define the proposed `svgstereo` colour attributes.

## PNG Third Edition

Source: [W3C Recommendation, 24 June 2025](https://www.w3.org/TR/2025/REC-png-3-20250624/).

| Section | Short quotation | Used for |
|---|---|---|
| [§7.1, Integers and byte order](https://www.w3.org/TR/2025/REC-png-3-20250624/#7Integers-and-byte-order) | “are limited to the range” | The PNG four-byte ceiling, 2147483647 |
| [§11.3.2.4, sBIT, Table 14](https://www.w3.org/TR/2025/REC-png-3-20250624/#11sBIT) | “original number of significant bits” | Component order and the distinction between significant bits and storage depth |
| [§11.3.2.6, cICP, Table 18](https://www.w3.org/TR/2025/REC-png-3-20250624/#cICP-chunk) | “four 1-byte unsigned integers” | Primaries, transfer, matrix and range fields; RGB matrix 0 |
| [§11.3.2.7, mDCV](https://www.w3.org/TR/2025/REC-png-3-20250624/#mDCV-chunk) | “supplemental static metadata” | Mastering description, CICP dependency, SDR applicability and the SDR adaptation caveat |
| [§11.3.2.7, Table 19](https://www.w3.org/TR/2025/REC-png-3-20250624/#mDCV-chunk-syntax) | “Divisor value” | RGB and white chromaticities in 0.00002 units; luminance in 0.0001 cd/m² |
| [§11.3.2.8, cLLI, Table 20](https://www.w3.org/TR/2025/REC-png-3-20250624/#cLLI-chunk) | “unknown or not currently calculable” | Zero sentinel, sequence statistics and 0.0001 cd/m² units |

PNG's `sBIT` is about existing raster samples.
The SVG precision intention is a new binding, and must not be copied blindly into PNG `sBIT` on export.
PNG does not define an SVG rasterisation, CSS precedence, a packed SVG frame or a default SVG sample depth.

## ITU-T H.273

Source: [Coding-independent code points for video signal type identification, version 4, July 2024](https://www.itu.int/rec/T-REC-H.273-202407-I/en).
The PDF is available from that page.
The section and table numbers here identify the edition checked; the code point names identify the reused definitions.

| Clause | Short quotation | Used for |
|---|---|---|
| §7.2 | “responsibility of the specification using the code point” | Defining an XML representation without redefining code point meanings |
| §8.1, Table 2 | “ColourPrimaries” | Primaries 1 for BT.709/sRGB and 9 for BT.2020 |
| §8.2, Table 3 | “TransferCharacteristics” | Transfers 1, 13, 16 and 18 for the SDR, sRGB, PQ and HLG examples |
| §8.3, Table 4 and range equations | “MatrixCoefficients” and “VideoFullRangeFlag” | RGB identity and full or narrow sample range |

The PNG field labelled Transfer Function maps to H.273 TransferCharacteristics.
The PNG field labelled Color Primaries maps to H.273 ColourPrimaries.
The code points themselves are unchanged.
Wide-gamut SDR and precision are independent of the PQ and HLG choices.

## CSS colour content

Source: [CSS Color 4, Candidate Recommendation Draft, 22 October 2026](https://www.w3.org/TR/2026/CRD-css-color-4-20261022/).

| Clause | Short quotation | Used for |
|---|---|---|
| [§4, Representing Colors](https://www.w3.org/TR/2026/CRD-css-color-4-20261022/#color-type) | “the sRGB hex color notation” | Existing paint syntax retains its meaning |
| [§10.1, color()](https://www.w3.org/TR/2026/CRD-css-color-4-20261022/#color-function) | “predefined color spaces” | Explicit colour spaces within SVG paints |
| [§10.8, rec2020](https://www.w3.org/TR/2026/CRD-css-color-4-20261022/#predefined-rec2020) | “accepts three numeric parameters” | Wide-gamut RGB coordinates, independent of precision |
| [§10.8, characteristics table](https://www.w3.org/TR/2026/CRD-css-color-4-20261022/#predefined-rec2020) | “gamma 2.40” | Do not equate a CSS keyword with a raw CICP sample encoding |

Source: [CSS Color HDR Module Level 1, Working Draft, 8 October 2026](https://www.w3.org/TR/2026/WD-css-color-hdr-1-20261008/).
Its official title is retained here; SVGStereo's colour scope is deep colour SDR and HDR.

| Clause | Short quotation | Used for |
|---|---|---|
| [§3.1, dynamic-range-limit](https://www.w3.org/TR/2026/WD-css-color-hdr-1-20261008/#propdef-dynamic-range-limit) | “all elements” | CSS headroom control remains effective |
| [§7, color()](https://www.w3.org/TR/2026/WD-css-color-hdr-1-20261008/#color-function) | “Its syntax is now as follows” | Extended colour-space syntax |
| [§8.1, rec2100-pq](https://www.w3.org/TR/2026/WD-css-color-hdr-1-20261008/#valdef-color-rec2100-pq) | “Perceptual Quantizer (PQ)” | PQ colour values |
| [§8.2, rec2100-hlg](https://www.w3.org/TR/2026/WD-css-color-hdr-1-20261008/#valdef-color-rec2100-hlg) | “Hybrid Log-Gamma (HLG)” | HLG colour values |
| [§8.3, rec2100-linear](https://www.w3.org/TR/2026/WD-css-color-hdr-1-20261008/#valdef-color-rec2100-linear) | “nominal range of [0, 1]” | Linear colour values |

These drafts specify colour expressions and presentation controls.
They do not establish implementation support or specify SVGStereo's precision and mastering attributes.

## SVG and stereo

| Source | Short quotation | Used for |
|---|---|---|
| [SVG 1.1 Second Edition §23.1, 16 August 2011](https://www.w3.org/TR/SVG11/extend.html#ForeignNamespaces) | “SVG allows inclusion of attributes from foreign namespaces on any SVG element.” | Namespaced extension attributes and unchanged rendering when ignored |
| [SVG 1.1 Second Edition §19.1](https://www.w3.org/TR/SVG11/animate.html#Introduction) | “SVG content can be animated” | Existing animation model; the shared pair timeline is SVGStereo's rule |
| [RFC 9559 §5.1.4.1.28.3, Table 5, October 2024](https://www.rfc-editor.org/rfc/rfc9559.html#section-5.1.4.1.28.3) | “side by side (left eye first)” | Established layout corresponding to StereoMode 1 |
| [SVGStereo 0.2, 14 October 2026](https://github.com/Sparky-OS/svgstereo/blob/a616813a888f9c3e28a58cab55033bc56c2ae04a/README.md#animated-drawings) | “Both views share one timeline” | Preserve all five animation rules while reducing the layout set |

## Edition contract

Source: [House formats, introductory table and rules](https://github.com/Sparky-OS/sparky-stereo-os/blob/main/docs/house-formats.md), retrieved 26 October 2026.
The video colour row says “never reduced in the middle”.
The rules say “Output adaptation belongs to the compositor.”
The reconstruction status says “not implemented or tested on HDR devices”.
These clauses support preserving source precision and descriptions without claiming physical-display proof.
The file's SDR and HDR design status is separate from this proposal's completion.

## What this proposal adds

The XML namespace binding, decimal tuple grammar, root-only scope, static metadata and independent stereo handling are SVGStereo rules.
So are the single permitted layout, viewBox split, any-resolution contract, per-file correction and compatibility policy.
For deep colour SDR and HDR, the new rules are the rendered-output scope, significant-precision intention, safe failure handling and preservation of CSS colour semantics.
The `cLLI` CICP dependency, whole-packed-frame scope and restrictions on unbounded animation are explicit SVG binding choices.
They are offered for upstream review, not attributed to PNG or CSS as already standardised SVG behaviour.

## Attribution

W3C quotations are attributed to their named specifications under the [W3C document licence](https://www.w3.org/copyright/document-license/).
ITU and IETF excerpts retain their respective source attribution.
The new specification text remains CC0 as described in [LICENSE](LICENSE).

## Procedural depth clauses

The linked passages define SVG's rendering coordinates and effects, not stereo depth.
The per-eye translation, shared state, depth inference and fallback rules are new SVGStereo requirements.

| Source clause | Short quotation | Application |
|---|---|---|
| [SVG 2 §8.5](https://www.w3.org/TR/SVG2/coords.html#TransformProperty) | “transform” | Preserve authored transforms and add the horizontal view translation outside them |
| [SVG 2 §8.9](https://www.w3.org/TR/SVG2/coords.html#Units) | “viewport” | Preserve the original percentage reference dimensions |
| [SVG 2 §8.11](https://www.w3.org/TR/SVG2/coords.html#ObjectBoundingBoxUnits) | “objectBoundingBox” | Geometry-relative coordinate units |
| [SVG 2 §8.13](https://www.w3.org/TR/SVG2/coords.html#VectorEffects) | “vector effects” | Keep the existing viewport rules for non-scaling strokes |
| [SVG 2 §14.2](https://www.w3.org/TR/SVG2/pservers.html#Gradients) | “part of its own geometry” | Gradients follow the referencing element's transform |
| [SVG 2 §14.3.1](https://www.w3.org/TR/SVG2/pservers.html#PatternElementAttributes) | “userSpaceOnUse” and “objectBoundingBox” | Pattern and content coordinates follow their reference context |
| [SVG 2 §5.4](https://www.w3.org/TR/SVG2/struct.html#SymbolElement) | “symbol” | Preserve instance viewport semantics |
| [SVG 2 §5.5](https://www.w3.org/TR/SVG2/struct.html#UseElement) | “use” | Translate instances without editing shared definitions |
| [SVG 2 §11](https://www.w3.org/TR/SVG2/text.html) | “Text” | Keep text layout intact inside the shifted element |
| [SVG 1.1 §19.2.6](https://www.w3.org/TR/SVG11/animate.html#Animation.nsexample) | “Animation with namespaces” | Bind SMIL's target to the foreign depth attribute |
| [Filter Effects 1 §7](https://www.w3.org/TR/filter-effects-1/#FilterElement) | “primitiveUnits” | Coordinate system of primitive lengths |
| [Filter Effects 1 §8](https://www.w3.org/TR/filter-effects-1/#FilterEffectsRegion) | “hard clipping region” | Filter region moves in its reference coordinate chain |
| [Filter Effects 1 §9.2](https://www.w3.org/TR/filter-effects-1/#CommonAttributes) | “BackgroundImage” | Eye-specific backdrop inputs are exceptions to identical aligned paint |
| [Filter Effects 1 §9.4](https://www.w3.org/TR/filter-effects-1/#FilterPrimitiveSubRegion) | “filter primitive subregion” | Keep primitive subregions in the same moving space |
| [Filter Effects 1 §9.10](https://www.w3.org/TR/filter-effects-1/#feDiffuseLightingElement) | “feDiffuseLighting” | Surface and light coordinate relation |
| [Filter Effects 1 §9.11](https://www.w3.org/TR/filter-effects-1/#feDisplacementMapElement) | “feDisplacementMap” | Evaluate both map inputs per eye |
| [Filter Effects 1 §9.12](https://www.w3.org/TR/filter-effects-1/#feDropShadowElement) | “feDropShadow” | Recognisable cast-shadow branch |
| [Filter Effects 1 §9.14](https://www.w3.org/TR/filter-effects-1/#feGaussianBlurElement) | “standard deviation” | SVG blur's relation to Union's CSS blur radius |
| [Filter Effects 1 §9.18](https://www.w3.org/TR/filter-effects-1/#feOffsetElement) | “feOffset” | Offset in primitive coordinates |
| [Filter Effects 1 §9.19](https://www.w3.org/TR/filter-effects-1/#feSpecularLightingElement) | “feSpecularLighting” | Specular light and surface evaluated together |
| [Filter Effects 1 §9.21](https://www.w3.org/TR/filter-effects-1/#feTurbulenceElement) | “seed” | Identical noise parameters in both rendering passes |
| [Filter Effects 1 §11](https://www.w3.org/TR/filter-effects-1/#LightSourceDefinitions) | “Light source elements” | Point and spot positions, distant-light directions |
| [CSS Backgrounds 3 §6.1](https://www.w3.org/TR/css-backgrounds-3/#box-shadow) | “lifted above the canvas” and “shifted behind it” | Outer and inset shadows' depth meaning |

The SVG 2 passages are from its 4 October 2018 Candidate Recommendation.
Filter Effects 1 is the 18 December 2018 Working Draft; CSS Backgrounds 3 is the 11 March 2024 Candidate Recommendation Draft.
Backdrops and fixed canvas paint are not promised identical after foreground alignment.

## Union source precedence

[Depth inside every window, The values](https://github.com/Sparky-OS/sparky-stereo-os/blob/main/docs/depth-inside-windows.md#the-values-and-what-each-one-is-for) says “A depth the theme declares always wins”.
Its defaults table gives 10/4/1, and its test explanation distinguishes the 12-pixel measuring scale.
[Depth on the desktop](https://github.com/Sparky-OS/sparky-stereo-os/blob/main/docs/depth-on-the-desktop.md) names “sunk, screen and popped”.

Union's initial [property commit 970436a](https://invent.kde.org/danielcamposramos/union/-/commit/970436aefed7268458cf2e25bd4e8a2a32cbeedd) defines the common vocabulary.
The later [depth-range commit 6a695e8](https://invent.kde.org/danielcamposramos/union/-/commit/6a695e8b5130a1a3ccb8645e80e266423cb8d8ed) replaces the fixed shadow step with strength and separate internal limits.
Its `Depth::shadowStrength` uses `opacity * (length(offset) + blur radius / 2 + max(spread distance, 0))`.
Its `Reach::fit`, `referenceDepth` and `exactEyeShift` define the fitting, reference-width scaling and eye split used here.
Its `DepthTree::update()` uses `node.placement.declared.value_or(Depth::Popped)` for desktop roles and `elementStep` for internal elements.
The accompanying comment names menu, popup, tooltip and dialog roles.
The proposed SVG desktop selector deliberately selects that popup default; a background must explicitly choose sunk or screen.
An undeclared shadowless internal element adds zero; explicit screen overrides inference in either range.
The later [Qt Quick integration commit 7c8ab92](https://invent.kde.org/danielcamposramos/union/-/commit/7c8ab92f0fd3b86d0e662ee740adf5f1ac882152) keeps “the shadow left where it falls”.
These commit identities were read from the edition's patch headers; the local patch series, including later patches, was inspected for superseding rules.
The procedure-preserving SVG reference is an implementation of the described rule, not copied Union code or proof of complete Union parity.

[KDE's Understanding Plasma Styles, Theme Location, Structure and Definition](https://develop.kde.org/docs/plasma/theme/theme-details/#theme-location-structure-and-definition) says “All SVG images are optional” and lists the desktoptheme `icons/` and `widgets/` assets.
This supports the statement of theme fit, without implying adoption of SVGStereo.
[PNG Extensions 1.4.0 §3.6](https://www.libpng.org/pub/png/spec/register/pngext-1.4.0-pdg.html#C.sTER) defines the `sTER` mark used in the proof PNGs, including mode 1 for parallel viewing.
