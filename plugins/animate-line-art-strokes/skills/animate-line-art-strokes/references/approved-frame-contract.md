# Approved Frame Contract

## Source lock

Treat the user-approved raster as the sole visual source of truth:

- preserve its pixel dimensions and aspect ratio;
- preserve every subject's coordinates, scale, pose, line weight, and z-order;
- preserve the background and all intentional empty space;
- do not crop borders unless the approved source itself includes an unwanted
  capture border and the user approves its removal;
- do not repair, beautify, recolor, regenerate, or reinterpret the drawing.

For odd source dimensions, the renderer may add one background-colored pixel on
the right or bottom solely to satisfy H.264. Record this padding in QA.

## Motion lock

Reveal existing ink only. Do not translate, scale, rotate, morph, or replace
objects. Stroke ordering and timing are the only allowed creative decisions.

Keep a short blank lead and a full-frame hold unless the user specifies
otherwise. The exact approved source must be used as the uncompressed final
frame before encoding.

## Human gate

Show the approved source before animation. After rendering, show the MP4 and
motion strip. Human approval must assess:

1. whether the pen order feels intentional;
2. whether any line or object pops in suddenly;
3. whether pacing fits the intended narration slot;
4. whether the final frame is visibly identical to the approved still.

Do not treat numeric QA as a substitute for this review.
