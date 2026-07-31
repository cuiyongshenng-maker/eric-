# Stroke Order Map

Use a region order map when the default center-first result does not match the
semantic drawing order.

Coordinates are normalized to the source canvas:

```json
{
  "stages": [
    {
      "name": "character-head",
      "bbox": [0.35, 0.20, 0.65, 0.62],
      "max_span": 0.40,
      "contain": true
    },
    {
      "name": "character-body",
      "bbox": [0.32, 0.45, 0.68, 0.78]
    },
    {
      "name": "foreground",
      "bbox": [0.05, 0.65, 0.95, 1.00]
    }
  ],
  "fallback_name": "connectors-and-accents"
}
```

Each traced path is assigned to the first stage whose bounding box contains the
path centroid. `max_span` is optional; it prevents a long connector crossing a
region from being mistaken for a local object. It is the maximum of normalized
path width and height.

Set `contain` to `true` when every point of the path must stay inside the
region. This is useful for drawing a character before long connector lines that
cross the character's bounding box. Without it, assignment uses the path
centroid.

Write stages in desired draw order. Inside a stage, paths draw top-to-bottom
then left-to-right. Put the main character before facial details only when the
regions can separate them reliably; otherwise use a single character stage and
judge the result visually.

Default `auto-center` ordering works best for one centered subject with
peripheral props. Use a map for multi-object scenes, long connecting lines, or
an explicit narrative sequence.
