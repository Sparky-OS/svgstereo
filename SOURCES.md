# Source clauses for SVGStereo 0.4

Checked on 2 November 2026 for the side by side proposal and its procedural depth path.
Short quotations below identify the relied-on clauses; the linked sections contain the full requirements.
Version 0.3's PNG Third Edition and ITU-T H.273 clauses remain in [its source list](https://github.com/Sparky-OS/svgstereo/blob/298f08e/SOURCES.md), with the colour attributes version 0.4 withdrew.

## CSS colour

SVGStereo defines no colour; these clauses support the statement that SVG colour, its colour spaces and its precision are CSS's.

Source: [CSS Color 4, Candidate Recommendation Draft, 1 November 2026](https://www.w3.org/TR/2026/CRD-css-color-4-20261101/).

| Clause | Short quotation | Used for |
|---|---|---|
| [§5.1, rgb()](https://www.w3.org/TR/2026/CRD-css-color-4-20261101/#rgb-functions) | “honor the precision of the component as authored or calculated” | Authored precision is kept |
| [§10.1, color()](https://www.w3.org/TR/2026/CRD-css-color-4-20261101/#color-function) | “predefined color spaces” | Each element names its own colour space |
| [§16.5, serializing color()](https://www.w3.org/TR/2026/CRD-css-color-4-20261101/#serializing-color-function-values) | “minimum precision for round-tripping” | 10 bits for `srgb` and `display-p3`, 12 for `rec2020`, 16 for `xyz` |

Source: [CSS Color 5, Working Draft, 29 October 2026](https://www.w3.org/TR/2026/WD-css-color-5-20261029/).

| Clause | Short quotation | Used for |
|---|---|---|
| [§5, color()](https://www.w3.org/TR/2026/WD-css-color-5-20261029/#color-function) | “Predefined and Custom Color Spaces” | SDR colour spaces beyond the predefined ones |

Source: [CSS Color HDR Module Level 1, Working Draft, 26 October 2026](https://www.w3.org/TR/2026/WD-css-color-hdr-1-20261026/).

| Clause | Short quotation | Used for |
|---|---|---|
| [§3.1, dynamic-range-limit](https://www.w3.org/TR/2026/WD-css-color-hdr-1-20261026/#the-dynamic-range-limit-property) | “The dynamic-range-limit property” | Headroom control stays with CSS |
| [§8, HDR colour spaces](https://www.w3.org/TR/2026/WD-css-color-hdr-1-20261026/#predefined-HDR) | “Predefined color spaces for HDR” | `rec2100-pq`, `rec2100-hlg` and `rec2100-linear` |
| [§10.1, serializing color()](https://www.w3.org/TR/2026/WD-css-color-hdr-1-20261026/#serializing-color-function-values) | “minimum precision for round-tripping” | 10 bits for `rec2100-pq` and `rec2100-hlg`, 16 for `rec2100-linear` |

The review that withdrew the colour attributes is [Chris Lilley's comment on WICG/proposals#316](https://github.com/WICG/proposals/issues/316), 2 November 2026.

## SVG and stereo

| Source | Short quotation | Used for |
|---|---|---|
| [SVG 1.1 Second Edition §23.1, 16 August 2011](https://www.w3.org/TR/SVG11/extend.html#ForeignNamespaces) | “SVG allows inclusion of attributes from foreign namespaces on any SVG element.” | Namespaced extension attributes and unchanged rendering when ignored |
| [SVG 1.1 Second Edition §19.1](https://www.w3.org/TR/SVG11/animate.html#Introduction) | “SVG content can be animated” | Existing animation model; the shared pair timeline is SVGStereo's rule |
| [RFC 9559 §5.1.4.1.28.3, Table 5, October 2024](https://www.rfc-editor.org/rfc/rfc9559.html#section-5.1.4.1.28.3) | “side by side (left eye first)” | Established layout corresponding to StereoMode 1 |
| [SVGStereo 0.2, 14 October 2026](https://github.com/Sparky-OS/svgstereo/blob/a616813a888f9c3e28a58cab55033bc56c2ae04a/README.md#animated-drawings) | “Both views share one timeline” | Preserve all five animation rules while reducing the layout set |

## What this proposal adds

The XML namespace binding, root-only scope and static layout are SVGStereo rules.
So are the single permitted layout, viewBox split, any-resolution contract, per-file correction and compatibility policy.
For colour, SVGStereo adds only that both views of a pair use the same colour processing.
These rules are offered for review, not attributed to SVG or CSS as already standardised behaviour.

## Attribution

W3C quotations are attributed to their named specifications under the [W3C document licence](https://www.w3.org/copyright/document-license/).
IETF excerpts retain their source attribution.
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
