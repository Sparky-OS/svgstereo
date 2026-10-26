# Run the procedural reference

This bounded reader demonstrates SVGStereo's procedural depth path.
It uses librsvg for a separate rendering pass per eye and Pillow only for checking and packing the rendered views.
The reader does not flatten the SVG first.
It does not implement deep colour SDR and HDR conversion.

From the repository root, build the image and run the checks with a writable output directory:

```sh
docker build --platform linux/amd64 -t svgstereo-proof reference
mkdir -p evidence
docker run --rm --platform linux/amd64 --cpus 4 --user "$(id -u):$(id -g)" \
  -v "$PWD:$PWD" -w "$PWD" svgstereo-proof \
  /usr/bin/python3 reference/check.py evidence
```

To render one set of limits:

```sh
docker run --rm --platform linux/amd64 --cpus 4 --user "$(id -u):$(id -g)" \
  -v "$PWD:$PWD" -w "$PWD" svgstereo-proof \
  /usr/bin/python3 reference/reader.py reference/sample.svg evidence/custom --limits 10 4 12
```

The arguments are `SunkLimit PoppedLimit ElementLimit` in disparity pixels at a view 1920 wide.
The four cases are 10/4/1, 10/4/12, 12/12/12 and 0/0/0.
Only 10/4/1 is the edition's documented default.
The hand predictions are in `check.py`, independently of the reader's placement output.
Each case checks nine elements, their vertical alignment, the aligned procedural noise and unchanged 2D rendering.
The changed-seed control must fail the noise-identity check, and flat rendering must fail all seven nonzero disparity predictions at 12/12/12.

The output includes each eye's SVG and PNG, an ordinary 2D render, a `pair.png` with PNG `sTER` mode 1, placement data and numerical results.
The eye SVGs still contain the turbulence, patterns, gradients, symbol instances and filter primitives.
PNG adds the format-required padding before the right view when its width is not divisible by eight.
The pixels of each view are unchanged.
No running desktop or physical display is used.

The profile requires a zero-origin viewBox and untransformed rectangular groups for its depth surfaces.
Depth on arbitrary leaves, transforms, CSS style resolution, live animation, script, external backdrop effects and general painted-boundary detection are outside this reference.
The normative rules and remaining implementation work are in [DEPTH.md](../DEPTH.md).
The Dockerfile pins the base digest; package versions are resolved at build time and should be recorded with any measurement.
