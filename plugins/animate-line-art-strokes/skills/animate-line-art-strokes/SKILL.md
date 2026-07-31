---
name: animate-line-art-strokes
description: Convert one user-approved black-line raster drawing (PNG, JPG, or WebP) into a local draw-on MP4 by tracing, ordering, and progressively revealing its strokes while locking the approved composition and verifying the decoded final frame. Use for a single static doodle, stick-figure frame, whiteboard illustration, diagram, or similar line-art animation. Do not use for scriptwriting, storyboarding, image generation, character design, multi-shot assembly, subtitles, voice-over, or complete-video production.
---

# Animate Line Art Strokes

Turn one approved still into one reviewed draw-on animation. Treat the source
image as immutable.

## Hard boundaries

- Require explicit approval of the exact source image before tracing it.
- Keep the source width, height, crop, subject coordinates, scale, background,
  and final appearance locked.
- Never generate, redraw, edit, relayout, caption, or add objects to the source.
- Never write narration, assemble multiple shots, or create audio.
- Use only the bundled local script. Do not call image, video, or voice services.
- Stop after producing the single-shot MP4 and QA artifacts for human review.

If the user asks for a topic-to-video workflow, route that work to a separate
full-production skill. This skill may be called by that orchestrator only after
the still for a shot is approved.

## Workflow

1. Record the approved source path, duration, FPS, output directory, and desired
   stroke order. Copy the approved source into the run directory.
2. Read [approved-frame-contract.md](references/approved-frame-contract.md).
3. Use `auto-center` ordering for simple centered drawings. For complex scenes,
   write an order-map JSON after reading
   [stroke-order-map.md](references/stroke-order-map.md).
4. Run:

   ```bash
   python3 scripts/animate_line_art.py APPROVED_IMAGE OUTPUT.mp4 \
     --qa-dir QA_DIR \
     --duration 6 \
     --fps 30 \
     --order auto-center
   ```

   Add `--order-map PATH.json` when semantic regions must draw in an explicit
   sequence.
5. Inspect the MP4 and `qa/motion-strip.png` at full resolution. Check that
   strokes grow rather than appear as whole objects, the chosen semantic order
   reads naturally, and no object drifts.
6. Read `qa/qa-report.json`. Accept the technical render only when:
   - the MP4 decodes;
   - the source and decoded final frame have the same locked content area;
   - mean absolute channel difference is at most `3/255`;
   - pixels with channel difference above `12` are at most `0.1%`;
   - no unexpected crop, scale, translation, or final-frame substitution occurs.
7. Present the MP4 and motion strip to the user. Mark the shot approved only
   after explicit human review. Revise only timing or stroke order unless the
   user separately approves a different source image.

## Output contract

Use this stable structure:

```text
shot-run/
  approved-source.png
  order-map.json              # optional
  line-reveal.mp4
  paths.json
  qa/
    motion-strip.png
    final-frame.png
    decoded-last-frame.png
    frame-*.png
    qa-report.json
```

The final full-quality frame before H.264 encoding must be the exact approved
source. Compression residue is measured, not silently ignored.

## Dependencies

Require local `python3`, `ffmpeg`, OpenCV, NumPy, Pillow, and scikit-image. If a
dependency is missing, report it and stop; do not substitute a paid service.
