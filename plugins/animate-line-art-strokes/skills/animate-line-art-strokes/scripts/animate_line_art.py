#!/usr/bin/env python3
"""Trace a raster line drawing and render one reviewed draw-on MP4."""

from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    import cv2
    import numpy as np
    from PIL import Image, ImageDraw
    from skimage.morphology import remove_small_objects, skeletonize
except ImportError as exc:
    raise SystemExit(
        "Missing local dependency. Require opencv-python, numpy, Pillow, "
        f"and scikit-image. Original error: {exc}"
    ) from exc


NEIGHBORS = (
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1),
)


def edge_key(
    a: tuple[int, int],
    b: tuple[int, int],
) -> tuple[tuple[int, int], tuple[int, int]]:
    return (a, b) if a <= b else (b, a)


def trace_paths(skeleton: np.ndarray) -> list[list[tuple[int, int]]]:
    """Split an 8-connected skeleton into continuous paths."""
    component_count, labels = cv2.connectedComponents(
        skeleton.astype(np.uint8), connectivity=8
    )
    paths: list[list[tuple[int, int]]] = []

    for label in range(1, component_count):
        ys, xs = np.where(labels == label)
        pixels = {(int(y), int(x)) for y, x in zip(ys, xs)}
        if len(pixels) < 4:
            continue

        adjacency: dict[tuple[int, int], list[tuple[int, int]]] = {}
        for y, x in pixels:
            adjacency[(y, x)] = [
                (y + dy, x + dx)
                for dy, dx in NEIGHBORS
                if (y + dy, x + dx) in pixels
            ]

        visited: set[
            tuple[tuple[int, int], tuple[int, int]]
        ] = set()
        nodes = sorted(point for point in pixels if len(adjacency[point]) != 2)

        def walk(
            start: tuple[int, int],
            nxt: tuple[int, int],
        ) -> list[tuple[int, int]]:
            path = [start, nxt]
            visited.add(edge_key(start, nxt))
            previous, current = start, nxt
            while len(adjacency[current]) == 2:
                candidates = [
                    point for point in adjacency[current] if point != previous
                ]
                if not candidates:
                    break
                candidate = candidates[0]
                key = edge_key(current, candidate)
                if key in visited:
                    break
                visited.add(key)
                path.append(candidate)
                previous, current = current, candidate
            return path

        for node in nodes:
            for neighbor in sorted(adjacency[node]):
                if edge_key(node, neighbor) not in visited:
                    paths.append(walk(node, neighbor))

        # Closed loops have no endpoints or junctions.
        for start in sorted(pixels):
            for neighbor in sorted(adjacency[start]):
                if edge_key(start, neighbor) not in visited:
                    paths.append(walk(start, neighbor))

    return [path for path in paths if len(path) >= 2]


def path_length(path: list[tuple[int, int]]) -> float:
    return sum(
        math.hypot(y2 - y1, x2 - x1)
        for (y1, x1), (y2, x2) in zip(path, path[1:])
    )


def path_features(
    path: list[tuple[int, int]],
    width: int,
    height: int,
) -> dict[str, Any]:
    ys = np.array([point[0] for point in path], dtype=np.float32)
    xs = np.array([point[1] for point in path], dtype=np.float32)
    x0, x1 = float(xs.min()), float(xs.max())
    y0, y1 = float(ys.min()), float(ys.max())
    cx, cy = float(xs.mean()), float(ys.mean())
    return {
        "bbox": [int(x0), int(y0), int(x1), int(y1)],
        "bbox_normalized": [
            x0 / width, y0 / height, x1 / width, y1 / height
        ],
        "centroid": [cx, cy],
        "centroid_normalized": [cx / width, cy / height],
        "span_normalized": max((x1 - x0) / width, (y1 - y0) / height),
        "length": path_length(path),
        "point_count": len(path),
    }


def load_order_map(path: Path | None) -> dict[str, Any] | None:
    if path is None:
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    stages = data.get("stages")
    if not isinstance(stages, list) or not stages:
        raise ValueError("Order map must contain a non-empty 'stages' array")
    for index, stage in enumerate(stages):
        if not isinstance(stage.get("name"), str):
            raise ValueError(f"Stage {index} needs a string 'name'")
        bbox = stage.get("bbox")
        if (
            not isinstance(bbox, list)
            or len(bbox) != 4
            or not all(isinstance(value, (int, float)) for value in bbox)
        ):
            raise ValueError(f"Stage {index} needs bbox [x0,y0,x1,y1]")
    return data


def assign_stage(
    features: dict[str, Any],
    order_map: dict[str, Any] | None,
) -> tuple[int, str]:
    if order_map is None:
        return 0, "auto-center"
    cx, cy = features["centroid_normalized"]
    bx0, by0, bx1, by1 = features["bbox_normalized"]
    span = features["span_normalized"]
    for index, stage in enumerate(order_map["stages"]):
        x0, y0, x1, y1 = stage["bbox"]
        max_span = float(stage.get("max_span", 1.0))
        centroid_inside = x0 <= cx <= x1 and y0 <= cy <= y1
        fully_contained = (
            bx0 >= x0 and by0 >= y0 and bx1 <= x1 and by1 <= y1
        )
        containment_ok = (
            fully_contained if stage.get("contain", False)
            else centroid_inside
        )
        if containment_ok and span <= max_span:
            return index, stage["name"]
    return len(order_map["stages"]), order_map.get(
        "fallback_name", "fallback"
    )


def sort_record(
    record: dict[str, Any],
    order_mode: str,
    width: int,
    height: int,
) -> tuple[float, float, float, float]:
    features = record["features"]
    cx, cy = features["centroid"]
    stage = float(record["stage_index"])
    if order_mode == "top-to-bottom":
        return stage, cy, cx, -features["length"]
    if order_mode == "left-to-right":
        return stage, cx, cy, -features["length"]
    # Centered subject first, then top-to-bottom within similar distance rings.
    distance = math.hypot(
        (cx - width / 2) / max(width, 1),
        (cy - height / 2) / max(height, 1),
    )
    return stage, round(distance, 2), cy, cx


def draw_partial_path(
    mask: np.ndarray,
    path: list[tuple[int, int]],
    fraction: float,
    thickness: int,
) -> None:
    if fraction <= 0:
        return
    point_count = max(
        2, min(len(path), int(math.ceil(len(path) * fraction)))
    )
    points = np.array(
        [(x, y) for y, x in path[:point_count]], dtype=np.int32
    )
    cv2.polylines(
        mask,
        [points],
        False,
        255,
        thickness=thickness,
        lineType=cv2.LINE_AA,
    )


def estimate_background(source: np.ndarray) -> np.ndarray:
    border = np.concatenate(
        (
            source[:8].reshape(-1, 3),
            source[-8:].reshape(-1, 3),
            source[:, :8].reshape(-1, 3),
            source[:, -8:].reshape(-1, 3),
        ),
        axis=0,
    )
    return np.median(border, axis=0).astype(np.uint8)


def pad_even(
    frame: np.ndarray,
    background: np.ndarray,
) -> tuple[np.ndarray, tuple[int, int]]:
    height, width = frame.shape[:2]
    pad_right = width % 2
    pad_bottom = height % 2
    if not pad_right and not pad_bottom:
        return frame, (0, 0)
    padded = np.full(
        (height + pad_bottom, width + pad_right, 3),
        background,
        dtype=np.uint8,
    )
    padded[:height, :width] = frame
    return padded, (pad_right, pad_bottom)


def make_strip(frame_paths: list[Path], output: Path) -> None:
    frames = [Image.open(path).convert("RGB") for path in frame_paths]
    thumb_width = 320
    thumb_height = int(frames[0].height * thumb_width / frames[0].width)
    strip = Image.new(
        "RGB",
        (thumb_width * len(frames), thumb_height + 38),
        "#faf9f4",
    )
    draw = ImageDraw.Draw(strip)
    for index, (frame, path) in enumerate(zip(frames, frame_paths)):
        frame.thumbnail(
            (thumb_width, thumb_height), Image.Resampling.LANCZOS
        )
        strip.paste(frame, (index * thumb_width, 0))
        draw.text(
            (index * thumb_width + 9, thumb_height + 10),
            path.stem,
            fill="#202020",
        )
    strip.save(output)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render one approved raster line drawing as a draw-on MP4."
    )
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--qa-dir", type=Path, required=True)
    parser.add_argument("--duration", type=float, default=6.0)
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--blank", type=float, default=0.3)
    parser.add_argument("--hold", type=float, default=1.0)
    parser.add_argument("--threshold", type=int, default=178)
    parser.add_argument("--min-object", type=int, default=7)
    parser.add_argument("--reveal-width", type=int)
    parser.add_argument(
        "--order",
        choices=("auto-center", "top-to-bottom", "left-to-right"),
        default="auto-center",
    )
    parser.add_argument("--order-map", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if shutil.which("ffmpeg") is None:
        raise SystemExit("ffmpeg is required but was not found")
    if args.duration <= args.blank + args.hold:
        raise SystemExit("duration must exceed blank + hold")
    if args.fps <= 0:
        raise SystemExit("fps must be positive")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.qa_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = args.output.parent / "paths.json"

    raw = cv2.imread(str(args.source), cv2.IMREAD_UNCHANGED)
    if raw is None:
        raise SystemExit(f"Could not read source: {args.source}")
    if raw.ndim == 2:
        source = cv2.cvtColor(raw, cv2.COLOR_GRAY2BGR)
    elif raw.shape[2] == 4:
        alpha = raw[:, :, 3:4].astype(np.float32) / 255.0
        background = np.full(raw[:, :, :3].shape, 250, dtype=np.uint8)
        source = (
            raw[:, :, :3].astype(np.float32) * alpha
            + background.astype(np.float32) * (1.0 - alpha)
        ).astype(np.uint8)
    else:
        source = raw[:, :, :3]

    height, width = source.shape[:2]
    background_color = estimate_background(source)
    source_padded, padding = pad_even(source, background_color)
    output_height, output_width = source_padded.shape[:2]

    gray = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)
    ink = gray < args.threshold
    ink = remove_small_objects(ink, min_size=args.min_object)
    skeleton = skeletonize(ink)
    paths = trace_paths(skeleton)
    if not paths:
        raise SystemExit(
            "No line paths detected. Adjust --threshold or inspect the source."
        )

    order_map = load_order_map(args.order_map)
    records: list[dict[str, Any]] = []
    for source_index, path in enumerate(paths):
        features = path_features(path, width, height)
        stage_index, stage_name = assign_stage(features, order_map)
        records.append(
            {
                "source_index": source_index,
                "stage_index": stage_index,
                "stage_name": stage_name,
                "features": features,
                "path": path,
            }
        )
    records.sort(
        key=lambda record: sort_record(
            record, args.order, width, height
        )
    )

    distance = cv2.distanceTransform(
        ink.astype(np.uint8), cv2.DIST_L2, 5
    )
    if args.reveal_width:
        reveal_width = args.reveal_width
    else:
        center_widths = distance[skeleton]
        reveal_width = max(
            3,
            int(round(float(np.percentile(center_widths, 80)) * 2.0)),
        )

    manifest = {
        "source": str(args.source),
        "canvas": [width, height],
        "padding_right_bottom": list(padding),
        "threshold": args.threshold,
        "reveal_width": reveal_width,
        "order": args.order,
        "order_map": str(args.order_map) if args.order_map else None,
        "paths": [],
    }
    for draw_index, record in enumerate(records):
        manifest["paths"].append(
            {
                "draw_index": draw_index,
                "stage_index": record["stage_index"],
                "stage_name": record["stage_name"],
                **record["features"],
                "points_yx": record["path"],
            }
        )
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    base = np.full_like(source, background_color)
    ink_alpha = np.clip(
        (205.0 - gray.astype(np.float32)) / 165.0, 0.0, 1.0
    )
    ink_alpha *= ink.astype(np.float32)
    ink_alpha = cv2.GaussianBlur(ink_alpha, (3, 3), 0.45)

    lengths = [
        max(float(record["features"]["length"]), 1.0)
        for record in records
    ]
    total_length = float(sum(lengths))
    total_frames = int(round(args.duration * args.fps))
    draw_duration = args.duration - args.blank - args.hold
    qa_times = [
        0.0,
        args.blank + draw_duration * 0.15,
        args.blank + draw_duration * 0.35,
        args.blank + draw_duration * 0.60,
        args.blank + draw_duration * 0.85,
        args.duration - 1 / args.fps,
    ]
    qa_indices = {
        min(total_frames - 1, int(round(time * args.fps))): time
        for time in qa_times
    }
    qa_paths: list[Path] = []

    command = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "bgr24",
        "-s", f"{output_width}x{output_height}",
        "-r", str(args.fps), "-i", "-",
        "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        str(args.output),
    ]
    encoder = subprocess.Popen(command, stdin=subprocess.PIPE)
    assert encoder.stdin is not None

    for frame_index in range(total_frames):
        time_seconds = frame_index / args.fps
        progress = float(np.clip(
            (time_seconds - args.blank) / draw_duration, 0.0, 1.0
        ))
        eased = progress * progress * (3.0 - 2.0 * progress)
        target_length = eased * total_length
        reveal = np.zeros((height, width), dtype=np.uint8)
        consumed = 0.0

        for record, length in zip(records, lengths):
            if target_length >= consumed + length:
                draw_partial_path(
                    reveal, record["path"], 1.0, reveal_width
                )
            elif target_length > consumed:
                draw_partial_path(
                    reveal,
                    record["path"],
                    (target_length - consumed) / length,
                    reveal_width,
                )
                break
            else:
                break
            consumed += length

        if progress >= 0.999:
            frame = source.copy()
        else:
            reveal_float = cv2.GaussianBlur(
                reveal.astype(np.float32) / 255.0, (3, 3), 0.35
            )
            visible = ink_alpha * reveal_float
            frame = (
                base.astype(np.float32) * (1.0 - visible[..., None])
                + source.astype(np.float32) * visible[..., None]
            ).astype(np.uint8)
        frame, _ = pad_even(frame, background_color)
        encoder.stdin.write(frame.tobytes())

        if frame_index in qa_indices:
            qa_path = args.qa_dir / (
                f"frame-{qa_indices[frame_index]:05.2f}s.png"
            )
            cv2.imwrite(str(qa_path), frame)
            qa_paths.append(qa_path)

    encoder.stdin.close()
    return_code = encoder.wait()
    if return_code != 0:
        raise SystemExit(f"ffmpeg encoding failed with exit code {return_code}")

    final_frame_path = args.qa_dir / "final-frame.png"
    decoded_path = args.qa_dir / "decoded-last-frame.png"
    cv2.imwrite(str(final_frame_path), source_padded)
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-sseof", "-0.04", "-i", str(args.output),
            "-frames:v", "1", str(decoded_path),
        ],
        check=True,
    )
    decoded = cv2.imread(str(decoded_path), cv2.IMREAD_COLOR)
    if decoded is None or decoded.shape != source_padded.shape:
        decoded_ok = False
        mean_diff = None
        max_diff = None
        pixels_over_12 = None
        ratio_over_12 = None
    else:
        decoded_ok = True
        difference = np.abs(
            source_padded.astype(np.int16) - decoded.astype(np.int16)
        )
        mean_diff = float(difference.mean())
        max_diff = int(difference.max())
        pixels_over_12 = int(
            (difference.max(axis=2) > 12).sum()
        )
        ratio_over_12 = pixels_over_12 / (
            output_width * output_height
        )

    make_strip(qa_paths, args.qa_dir / "motion-strip.png")
    technical_pass = bool(
        decoded_ok
        and mean_diff is not None
        and mean_diff <= 3.0
        and ratio_over_12 is not None
        and ratio_over_12 <= 0.001
    )
    report = {
        "source": str(args.source),
        "output": str(args.output),
        "resolution": [output_width, output_height],
        "source_resolution": [width, height],
        "padding_right_bottom": list(padding),
        "fps": args.fps,
        "duration_seconds": args.duration,
        "detected_paths": len(records),
        "skeleton_pixels": int(skeleton.sum()),
        "order": args.order,
        "order_map": str(args.order_map) if args.order_map else None,
        "reveal_width": reveal_width,
        "decoded": decoded_ok,
        "mean_abs_channel_diff": (
            round(mean_diff, 4) if mean_diff is not None else None
        ),
        "max_channel_diff": max_diff,
        "pixels_over_12": pixels_over_12,
        "ratio_over_12": (
            round(ratio_over_12, 8)
            if ratio_over_12 is not None else None
        ),
        "technical_pass": technical_pass,
        "human_review_required": True,
    }
    report_path = args.qa_dir / "qa-report.json"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if not technical_pass:
        sys.exit(2)


if __name__ == "__main__":
    main()
