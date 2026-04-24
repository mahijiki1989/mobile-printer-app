import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Roboto first (matches NoteCam's Android font), then fallbacks
FONT_PATHS = [
    '/usr/share/fonts/truetype/roboto/Roboto-Regular.ttf',
    '/usr/share/fonts/truetype/roboto/hinted/Roboto-Regular.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
    '/usr/share/fonts/truetype/freefont/FreeSans.ttf',
]

FIELD_ORDER = [
    ('latitude',  'Latitude'),
    ('longitude', 'Longitude'),
    ('elevation', 'Elevation'),
    ('accuracy',  'Accuracy'),
    ('time',      'Time'),
    ('note',      'Note'),
]


def _load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in FONT_PATHS:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


# ── OCR line grouping ─────────────────────────────────────────────────────────

def _bbox_of_group(group: list[dict]) -> tuple[int, int, int, int]:
    """Union bounding box of all detections in a line group."""
    all_x = [pt[0] for r in group for pt in r['bbox']]
    all_y = [pt[1] for r in group for pt in r['bbox']]
    return int(min(all_x)), int(min(all_y)), int(max(all_x)), int(max(all_y))


def group_ocr_into_lines(ocr_results: list[dict]) -> list[list[dict]]:
    """
    Cluster OCR detections into text lines by y-proximity.

    EasyOCR sometimes splits a single visual line into multiple tokens
    (e.g. "Latitude:" and "24.032752" as separate results). This groups
    tokens that are vertically close into a single logical line.
    """
    if not ocr_results:
        return []

    # Estimate typical glyph height to set a dynamic y-tolerance
    glyph_heights = [
        max(pt[1] for pt in r['bbox']) - min(pt[1] for pt in r['bbox'])
        for r in ocr_results
    ]
    median_h = float(np.median(glyph_heights)) if glyph_heights else 20.0
    y_tol = max(5, int(median_h * 0.55))

    sorted_results = sorted(ocr_results, key=lambda r: min(pt[1] for pt in r['bbox']))
    lines: list[list[dict]] = [[sorted_results[0]]]

    for r in sorted_results[1:]:
        curr_y = min(pt[1] for pt in r['bbox'])
        prev_y = min(pt[1] for pt in lines[-1][-1]['bbox'])
        if abs(curr_y - prev_y) <= y_tol:
            lines[-1].append(r)
        else:
            lines.append([r])

    return lines


def find_line_for_field(
    lines: list[list[dict]],
    label: str,
) -> list[dict] | None:
    """Return the line group whose combined text contains the field label."""
    label_lower = label.lower()
    for group in lines:
        combined = ' '.join(r['text'] for r in group).lower()
        if label_lower in combined or label_lower[:3] in combined:
            return group
    return None


# ── Background sampling ───────────────────────────────────────────────────────

def _sample_bg_near_line(
    image_rgb: np.ndarray,
    line_bbox: tuple[int, int, int, int],
    overlay_bbox: tuple[int, int, int, int],
) -> tuple[int, int, int]:
    """
    Sample the dark background color of the overlay box near a text line.

    Samples a thin strip just above the line (still within the overlay box),
    falling back to just below if the line is at the top of the box.
    """
    ox1, oy1, ox2, oy2 = overlay_bbox
    lx1, ly1, lx2, ly2 = line_bbox
    h_img, w_img = image_rgb.shape[:2]

    strip = 4  # px to sample

    # Try above the line
    sy1 = max(oy1, ly1 - strip - 2)
    sy2 = max(oy1, ly1 - 2)

    if sy2 - sy1 < 2:
        # Try below the line
        sy1 = min(oy2, ly2 + 2)
        sy2 = min(oy2, ly2 + strip + 2)

    sx1 = max(0, lx1)
    sx2 = min(w_img, lx2)

    region = image_rgb[sy1:sy2, sx1:sx2]
    if region.size == 0:
        # Last resort: sample the very first row of the overlay box
        region = image_rgb[oy1:oy1 + 4, ox1:ox2]

    if region.size == 0:
        return (20, 20, 20)

    return tuple(int(v) for v in np.median(region.reshape(-1, 3), axis=0))


# ── Single-line surgical replacement ─────────────────────────────────────────

def _replace_line(
    image_rgb: np.ndarray,
    line_bbox: tuple[int, int, int, int],
    label: str,
    new_value: str,
    bg_color: tuple[int, int, int],
) -> np.ndarray:
    """
    Replace one text line in the overlay with a new value.

    Steps:
      1. Fill the line area with the sampled background color (erases old text)
      2. Render "Label: new_value" in white at the same position

    Font size is measured from the line's actual pixel height so it matches
    the original regardless of image resolution.
    """
    h_img, w_img = image_rgb.shape[:2]
    x1, y1, x2, y2 = line_bbox

    # Add a small vertical padding so we fully cover descenders/ascenders
    pad = max(2, int((y2 - y1) * 0.12))
    fy1 = max(0, y1 - pad)
    fy2 = min(h_img, y2 + pad)

    line_h = y2 - y1
    font_size = max(8, int(line_h * 0.88))
    font = _load_font(font_size)

    result = image_rgb.copy()

    # Step 1: fill old text area with overlay background color
    result[fy1:fy2, x1:x2] = bg_color

    # Step 2: render new text
    pil = Image.fromarray(result)
    draw = ImageDraw.Draw(pil)
    draw.text((x1, y1), f'{label}: {new_value}', font=font,
              fill=(255, 255, 255))
    return np.array(pil)


# ── Overlay bbox (for bg sampling reference) ──────────────────────────────────

def compute_overlay_bbox(
    ocr_results: list[dict],
    image_shape: tuple[int, int],
    padding: int = 10,
) -> tuple[int, int, int, int] | None:
    """
    Compute the full NoteCam overlay bounding box (anchored to bottom-left).
    Used only for background color sampling — we do NOT inpaint this area.
    """
    if not ocr_results:
        return None

    all_x = [pt[0] for r in ocr_results for pt in r['bbox']]
    all_y = [pt[1] for r in ocr_results for pt in r['bbox']]
    h, w = image_shape

    ocr_y1 = max(0, int(min(all_y)) - padding)
    ocr_x2 = min(w, int(max(all_x)) + padding)

    x1 = 0
    y2 = h
    x2 = max(ocr_x2, int(w * 0.42))
    x2 = min(x2, w)

    min_box_h = int(h * 0.32)
    y1 = min(ocr_y1, h - min_box_h)
    y1 = max(0, y1)

    return (x1, y1, x2, y2)


# ── Public API ────────────────────────────────────────────────────────────────

def process_image(
    image_rgb: np.ndarray,
    ocr_results: list[dict],
    original_fields: dict[str, str | None],
    new_fields: dict[str, str | None],
) -> np.ndarray | None:
    """
    Surgically replace only the field values that the user changed.

    For each changed field:
      - Finds the exact pixel line in the original overlay via OCR
      - Fills that line with the sampled dark background color
        (so the overlay box itself is never touched)
      - Renders the new value text at the same position with the same
        measured font size → output is indistinguishable from original

    Returns the modified image, or None if no OCR results are available.
    """
    if not ocr_results:
        return None

    overlay_bbox = compute_overlay_bbox(ocr_results, image_rgb.shape[:2])
    if overlay_bbox is None:
        return None

    lines = group_ocr_into_lines(ocr_results)
    result = image_rgb.copy()
    changed = 0

    for key, label in FIELD_ORDER:
        old_val = (original_fields.get(key) or '').strip()
        new_val = (new_fields.get(key) or '').strip()

        if old_val == new_val:
            continue  # unchanged — leave original pixels untouched

        group = find_line_for_field(lines, label)
        if group is None:
            # OCR missed this line; skip rather than corrupt the image
            continue

        line_bbox = _bbox_of_group(group)
        bg_color  = _sample_bg_near_line(result, line_bbox, overlay_bbox)
        result    = _replace_line(result, line_bbox, label, new_val, bg_color)
        changed  += 1

    return result if changed > 0 else image_rgb
