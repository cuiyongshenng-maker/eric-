# Eric Codex Plugins

This repository contains personal Codex plugins.

## Plugins

- `vibe-coding`: a Codex workflow skill for building software through focused natural-language iteration.
- `animate-line-art-strokes`: turns one approved black-line drawing into a local draw-on MP4 with decoded final-frame QA.

## Local Installation

Add this repository as a Codex marketplace, then install the animation plugin:

```bash
codex plugin marketplace add cuiyongshenng-maker/eric- --ref main
codex plugin add animate-line-art-strokes@eric
```

The animation renderer also requires local Python packages and FFmpeg:

```bash
brew install ffmpeg
python3 -m pip install opencv-python numpy Pillow scikit-image
```

Restart Codex after installation. The installed skill is
`$animate-line-art-strokes`.

Plugin source folders:

```text
plugins/vibe-coding
plugins/animate-line-art-strokes
```
