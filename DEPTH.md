# Procedural depth in SVGStereo 0.3

This is the single-view path of the proposal, alongside an authored side by side pair.
A stereo reader draws the same procedures twice, one view per eye, with a horizontal translation for each element's depth.
There are no cameras, perspective projections or added scale cues.
The reader must not rasterise the drawing once and shift pieces of that bitmap to manufacture the other eye.
Normal raster intermediates used inside a filter are allowed independently in each eye.
Deep colour SDR and HDR retain the colour rules in [README.md](README.md).
The [source clauses](SOURCES.md#procedural-depth-clauses) quote the coordinate, filter and Union rules used here.

## Choosing the path

A valid `svgstereo:layout="sideBySideLeftFirst"` selects the authored pair and takes precedence over depth marks.
Depth marks do not add disparity to that existing pair.
With no `layout`, `svgstereo:depth="screen"` on the root opts a single-view drawing into procedural doubling.
Without that root opt-in, the drawing is one picture, even if its shapes have shadows or some descendants carry depth.
An invalid or unknown layout does not trigger depth guessing.
A reader offers ordinary 2D viewing as well as stereo viewing; the file's explicit path is the default when stereo is enabled.
Converting an authored pair into a procedural drawing is not implied.

## Syntax and Union's vocabulary

The chosen syntax is the namespaced XML attribute `svgstereo:depth` on an SVG graphics element or a group.
It uses the same values as Union's `depth` property:

| Value | Local level |
|---|---|
| `sunk` | -1, the sunk limit |
| `screen` | 0, the plane of what the element lies on |
| `popped` | 1, the popped limit |
| `<percentage>` | A fraction of the limit on its side, from -100% to 100% |
| `<number>` | A fraction of the limit on its side, from -1 to 1 |

An invalid or out-of-range value is ignored as a declaration.
The root opt-in must be `screen` or its numeric equivalent of zero.
An undeclared child adds no declared step; it does not inherit and reapply the parent's step.
Its surface, paints, text and ordinary descendants move with it.
A descendant with its own depth adds a relative step on what it lies on.
An explicit depth, including `screen`, always wins over shadow inference.
Depth changes presentation, never document layout, text flow or the original hit-test geometry.

This proposal does not register a new CSS property.
Namespaced XML avoids presenting Union's toolkit property as a CSS property already accepted by browsers.
Readers supporting SMIL may animate the foreign attribute using `attributeName="svgstereo:depth"` and `attributeType="XML"`, with the prefix bound to this namespace.
Resolve keywords to -1, 0 and 1, percentages to fractions, and interpolate the resulting numbers before fitting the stack.
Both eyes use the same sampled value.
CSS transitions do not directly animate this XML attribute; a future CSS binding would need its own property definition and cascade rules.
Script may update the attribute in the shared document state before the two rendering passes.

## Limits and nested surfaces

The reader and user own the limits, never the file.
On the desktop these are Stereo KWin's `SunkLimit`, `PoppedLimit` and `ElementLimit`, measured as disparity in pixels of a view 1920 wide.
The edition's documented defaults are 10, 4 and 1 respectively.
12 pixels is a useful measuring scale, not a proposed default.

`svgstereo:depth-range="desktop"` selects a separate surface with Union's popup role default, as used for menus, popups, tooltips and dialogs.
With no valid declared depth, its relative step is `popped`, even when it has no shadow.
This selector does not classify a drawing by its name, appearance or SVG element type.
To use this range for a background, declare `svgstereo:depth="sunk"` for a background behind its parent or `svgstereo:depth="screen"` for one on its parent's plane.
A plain surface in this range also needs explicit `screen` to override the popup default.
`svgstereo:depth-range="element"`, the default, identifies an element within a surface.
With no valid declared depth, this range uses shadow inference and adds zero when no shadow is recognised.
Explicit `screen` adds zero in either range, before the existing stack fitting and edge rules; it is relative to the parent, not an instruction to reset an entire nested stack.
This is a proposed SVG selector for Union's existing two ranges, not another depth vocabulary or a file-specified comfort limit.
An embedding toolkit may supply equivalent surface roles from its own model.
The attribute does not inherit; a button inside a desktop menu normally uses the element range.
Unknown range values use the element range.

Within each range, add the relative steps along the parent chain.
For each surface and each sign separately, divide by the farthest accumulated magnitude if it exceeds one.
Do not enlarge a stack whose accumulated magnitude is already below one.
Three equal popped steps therefore occupy one third, two thirds and the whole popped range.
Fit desktop surfaces together; fit internal elements independently on each surface.
A desktop child stays at or in front of the surface that opened it.
An element's final reference disparity is its desktop level times that side's desktop limit, plus its internal level times `ElementLimit`.
Thus an internal button on a menu can be one internal step nearer than the menu; the two ranges retain their distinct budgets.

For view width W, multiply reference disparity by W/1920.
For a vector renderer, Union's continuous split uses `right = -trunc(disparity/2)` and `left = disparity + right`.
A renderer using integer pixel placement first rounds disparity to the nearest integer, with half values away from zero, then uses the same split.
Positive disparity moves the left view rightwards relative to the right view.
Document the chosen rounding; do not silently mix the two policies within a pair.
The bounded reference script uses integer placement, as Union's Widgets path does.

## Shadows and the current Union rule

The current rule is in Union's `s1-0009` patch, which supersedes the early half-popped-limit rule in `s1-0001` and `s1-0002`.
Its strength is `opacity * (hypot(dx, dy) + blurRadius/2 + max(spread, 0))`.
For an isotropic SVG Gaussian, `blurRadius/2` is `stdDeviation`; the SVG blur must not be halved again.
For anisotropic blur this binding uses the larger standard deviation as the reach term.
Convert lengths to a common surface coordinate system before comparing strengths.
An outer shadow has positive strength; an inset shadow has negative strength.
Normalise against the strongest undeclared shadow on the same side of the same surface, then fit nested levels.
A declared depth is excluded from that shadow normalisation and always wins.
These shadow inference rules apply to the element range only; no shadow there adds no step.
The desktop range uses its declared depth or the popup default above, independently of shadows.

`feDropShadow` is an outer shadow.
An identifiable blur and offset of SourceAlpha composited under SourceGraphic is also an outer shadow.
An identifiable offset and blurred alpha subtracted from SourceAlpha, coloured, clipped inside it and composited over SourceGraphic is an inset shadow.
SVG has no `inset` keyword for `feDropShadow`.
The reference fixture contains that explicit inset graph.
Do not infer a shadow from arbitrary dark paint, lighting or a displacement filter.
For an ambiguous filter graph in the element range, use its declared depth or no inferred step; do not guess intent from the picture.
If multiple identifiable shadows compete, this binding uses the greatest absolute strength, with the last in filter order breaking a tie.
This graph recognition and tie rule are new SVG binding choices, not existing SVG shadow semantics.

Union's `s1-0012` patch also preserves a cast shadow on its receiving surface while the element moves.
This is an exception inside the translated element: adjust only the shadow branch's horizontal offset by receiverShift minus elementShift in that eye.
The filter region and other procedural coordinates still follow the element.
Expand a generated filter region if the receiver correction would otherwise clip a shadow that was visible in 2D.
Inset shading remains attached to the inset element and is clipped by its surface.
The reference fixture has enough filter-region margin for both tested shifts.

## Translate the procedure with the element

At each frame, advance script, events and animation once to obtain a shared document state.
Then evaluate its rendering procedures independently for each view at that same time.
Do not run a script's random-number generator, network action or mutation twice to obtain two different states.
Each view uses the same resources, parameters and `feTurbulence` seed.

Apply the per-eye translation outside the element's existing transform, in the view's horizontal coordinate system.
Do not add the shift to a rotated element's local x coordinate.
If M maps the element's parent coordinates to the view, the inserted local transform is `inverse(M) * translate(delta, 0) * M`.
Here delta is the child's absolute eye shift minus its parent's absolute eye shift, avoiding a second move of descendants.
A singular M makes that branch's extra depth unusable for that frame; retain its inherited plane and report the unsupported transform.
The original authored transforms remain intact.

| Procedure | Per-eye rule and source |
|---|---|
| Gradients | Keep gradient coordinates, `gradientUnits` and `gradientTransform` in the element's translated coordinate chain; do not rewrite shared definitions globally. SVG 2 §14.2, including §14.2.2 and §14.2.3. |
| Patterns | Keep `patternUnits`, `patternContentUnits`, `patternTransform` and any pattern viewBox intact, instantiated in the translated reference element's space. `userSpaceOnUse` does not by itself mean fixed to the screen. SVG 2 §14.3. |
| `use` and `symbol` | Translate each instance with its own reference context, including the symbol viewport, without modifying the shared definition for every instance. SVG 2 §5.4 and §5.5. |
| Filter region | Carry `filterUnits` and the filter's x, y, width and height with the referencing element; preserve clipping in that coordinate chain. Filter Effects 1 §7 and §8. |
| Primitive subregions | Carry primitive x, y, width and height with `primitiveUnits`; `objectBoundingBox` stays tied to the untranslated geometry's box before the outer shift. Filter Effects 1 §9.4. |
| `feTurbulence` | Evaluate the noise in the same primitive coordinates and with the same seed in each view, then translate with the element. Filter Effects 1 §9.21. |
| `feOffset`, `feGaussianBlur`, `feDropShadow` | Preserve offsets and blur scale in the moving primitive space; only a recognised cast-shadow receiver correction changes the shadow branch's dx. Filter Effects 1 §9.18, §9.14 and §9.12. |
| `feDiffuseLighting`, `feSpecularLighting` | Light positions move in the same primitive coordinate space as the surface; distant-light directions do not change under translation. Filter Effects 1 §9.10, §9.19 and §11. |
| `feDisplacementMap` | Evaluate both inputs in the same eye's translated filter context; preserve scale and selected channels. Filter Effects 1 §9.11. |
| Text | Translate the completed glyph layout with its element, retaining shaping, text paths and selection geometry. SVG 2 §11 and §8.5. |
| SMIL, CSS animation and scripted content | Share the sampled time and state, including generated descendants; evaluate each view's paints and filters independently. SVG animation remains the animation model. |

Viewport-relative percentages and CSS viewport units retain their original reference viewport dimensions; the eye translation must not change those dimensions.
A nested SVG viewport, its clip and its contents move together when that viewport is the translated element.
Ancestor clips and the drawing's outer clip remain on their own planes.
A deliberately canvas-fixed pattern or external backdrop remains in canvas space and is resampled for each eye; its texels need not match after aligning a moving foreground.
Such fixed paint must be explicit in the authoring or embedding model, never inferred from `userSpaceOnUse` alone.
`BackgroundImage`, `BackgroundAlpha`, blending and backdrop-dependent effects read the corresponding eye's already composed backdrop at the proper receiving coordinates.
They must not reuse the other eye's backdrop or a cached mono composite.
Filters on an ancestor operate on that eye's composed descendants; they are not distributable across children in general.
External images and `feImage` remain their own image or document resources, not newly projected geometry.
Non-scaling strokes and other vector effects keep their SVG viewport rules while the added translation changes position only.
`foreignObject`, embedded canvases, videos and external documents require their host's paired-state support; otherwise keep the unsupported branch on its inherited plane and report that fallback.

## The stereo window

A popped element cut by or touching the drawing's outer edge stays at the screen plane for that frame.
Check its visible extent in either eye, including stroke, filter reach and the proposed translation, rather than only its unshifted fill box.
Apply the edge constraint after fitting and propagate it through dependent popped descendants so a child cannot escape the same cut.
The edge rule wins over a request for positive depth.
A sunk element is seen through its own rectangle at the parent's plane, so its shifted content does not leak outside that frame.
Clip each completed view to its own output rectangle, then pack the two complete views side by side, left first.
Declare that output once; do not retain a procedural root opt-in on the packed result as a request to double it again.

## Themes in union

[Plasma's desktoptheme assets and icons](https://develop.kde.org/docs/plasma/theme/theme-details/#theme-location-structure-and-definition) include SVG drawings.
A theme's SVG can therefore carry depth using the same sunk, screen and popped words that Union and Stereo KWin read.
That is a statement of fit and a proposed shared vocabulary, not a claim that KDE has adopted these SVG attributes.
An ordinary 2D reader ignores them and draws the original SVG unchanged.

## Reference proof and limits

[reference/reader.py](reference/reader.py) renders [reference/sample.svg](reference/sample.svg) with librsvg once per eye.
It is a static rectangular-layer reference, not a complete SVG engine or a production renderer.
It implements the fixture's declared depth, two ranges, shadow strengths, nesting, integer eye shifts, simple edge clamp and inset rectangle clips.
It recognises the fixture's direct `feDropShadow` and canonical inset graph; general shadow graphs require the fuller reader described above.
It supports the fixture's ordinary gradient, pattern, `use` and turbulence through librsvg, preserving the SVG procedures in the generated per-eye documents.
It rejects authored transforms, script, CSS stylesheets and live animation rather than claiming to evaluate them.
Its simple rectangular edge check does not establish the general painted-extent edge rule.
The specification's lighting, displacement, arbitrary transform, backdrop, dynamic-state and colour paths need additional implementation proof.
The measurements made by `reference/check.py` are scoped to this fixture and reader.
