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
| [§3.1, dynamic-range-limit](https://www.w3.org/TR/2026/WD-css-color-hdr-1-20261008/#dynamic-range-limit) | “all elements” | CSS headroom control remains effective |
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
