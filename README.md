# SVGStereo: a stereo mark for SVG

SVG has no way to say that a drawing holds the two views of a stereo pair.
SVGStereo is one attribute that says it, so a program that understands stereo can show the drawing in 3D, and every other program draws it exactly as before.

Status: proposal, version 0.1, 14 October 2026.
Editor: Daniel Ramos, for [Sparky Stereo OS](https://github.com/Sparky-OS/sparky-stereo-os).
Comments and objections are welcome in this repository's issues.

## The mark

```xml
<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:svgstereo="https://github.com/Sparky-OS/svgstereo"
     svgstereo:layout="sideBySideLeftFirst"
     viewBox="0 0 200 100">
  <!-- the left view in x 0..100, the right view in x 100..200 -->
</svg>
```

- **Namespace:** `https://github.com/Sparky-OS/svgstereo` (this page). The prefix `svgstereo` is a convention; readers match the namespace, not the prefix.
- **Attribute:** `layout`, on the root `svg` element of the SVG namespace. It is read nowhere else.
- **Value:** one of the layouts below. The `viewBox` holds the whole packed picture, both views included, exactly as a stereo photograph's pixels hold them.
- **Eye order:** `LeftFirst` and `RightFirst` say which view comes first in the drawing (left half, top half, first column, first row, first checker), not how a viewer should fuse them.

## The layouts

The values are the stereo layouts the edition uses for every picture and video, so an SVG is marked with the same words as a JPEG, a PNG or a Matroska file.
Each is tied to the two standards that define stereo packing: Matroska's `StereoMode` ([RFC 9559](https://www.rfc-editor.org/rfc/rfc9559), section 5.1.4.1.28.3) and the frame packing arrangement of H.264 and H.265 (ITU-T H.264 and H.265, Annex D, Table D-8, `frame_packing_arrangement_type`).

| `layout` | Meaning | RFC 9559 StereoMode | H.264/H.265 Table D-8 |
|---|---|---|---|
| `mono` | One picture, not a pair | 0 | no frame packing |
| `sideBySideLeftFirst` | Left view in the left half | 1 | 3, side by side |
| `sideBySideRightFirst` | Right view in the left half | 11 | 3, side by side |
| `sideBySideQuincunxLeftFirst` | Side by side, quincunx sampled, left first | (none) | 3 with `quincunx_sampling_flag` |
| `sideBySideQuincunxRightFirst` | Side by side, quincunx sampled, right first | (none) | 3 with `quincunx_sampling_flag` |
| `topBottomLeftFirst` | Left view in the top half | 3 | 4, top and bottom |
| `topBottomRightFirst` | Right view in the top half | 2 | 4, top and bottom |
| `checkerboardLeftFirst` | Views alternate as a checkerboard, left first | 5 | 0, checkerboard |
| `checkerboardRightFirst` | Checkerboard, right first | 4 | 0, checkerboard |
| `rowInterleavedLeftFirst` | Views alternate by row, left first | 7 | 2, row interleaving |
| `rowInterleavedRightFirst` | Row interleaved, right first | 6 | 2, row interleaving |
| `columnInterleavedLeftFirst` | Views alternate by column, left first | 9 | 1, column interleaving |
| `columnInterleavedRightFirst` | Column interleaved, right first | 8 | 1, column interleaving |
| `anaglyphCyanRed` | One picture holding both views as a red/cyan anaglyph | 10 | (none) |
| `anaglyphGreenMagenta` | One picture holding both views as a green/magenta anaglyph | 12 | (none) |

Four values of the full set have no meaning inside one drawing and are not valid here: `frameSequentialLeftFirst` and `frameSequentialRightFirst` (views alternate in time, Table D-8 type 5) and `blockLacedLeftFirst` and `blockLacedRightFirst` (both views laced in one Matroska block, StereoMode 13 and 14).

## Rules for readers

1. Read the mark only from the root `svg` element, in this namespace. For a compressed `.svgz` file, read it from the decompressed document.
2. An unknown or invalid value means one picture: the drawing is shown as it is.
3. An SVG without the mark is a drawing, one picture. Never pair it by its shape or its colours.
4. A reader that shows the pair splits the `viewBox` by the layout, gives each eye its own view, and shows the drawing unchanged on a 2D screen.

## Why it is safe everywhere else

SVG lets any element carry attributes from other namespaces, and renderers ignore the ones they do not know: [SVG 1.1 Second Edition](https://www.w3.org/TR/SVG11/extend.html#ForeignNamespaces), section 23.1, "Foreign namespaces and private data".
So a marked file is still a valid SVG and draws the same in every browser, editor and viewer that does not read the mark.

## Implementations

- [stereo-layer](https://github.com/Sparky-OS/stereo-layer) (GPL-2.0), the shared stereo policy of Sparky Stereo OS: reads the mark, in `.svg` and `.svgz` files, for thumbnails, tooltips and previews in Dolphin and the other programs built on it.

## Licence

This text is dedicated to the public domain under [CC0 1.0](LICENSE): anyone may implement, copy or adapt it.
