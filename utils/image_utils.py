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
    all_x = [pt[0] for r in group for pt in r['bbox']]
    all_y = [pt[1] for r in group for pt in r['bbox']]
    return int(min(all_x)), int(min(all_y)), int(max(all_x)), int(max(all_y))


def group_ocr_into_lines(ocr_results: list[dict]) -> list[list[dict]]:
    """Cluster OCR detections into text lines by y-proximity."""
    if not ocr_results:
        return []
    glyph_heights = [
        max(pt[1] for pt in r['bbox']) - min(pt[1] for pt in r['bbox'])
        for r in ocr_results
    ]
    median_h = float(np.median(glyph_heights)) if glyph_heights else 20.0
    y_tol = max(5, int(median_h * 0.55))

    sorted_r = sorted(ocr_results, key=lambda r: min(pt[1] for pt in r['bbox']))
    lines: list[list[dict]] = [[sorted_r[0]]]
    for r in sorted_r[1:]:
        curr_y = min(pt[1] for pt in r['bbox'])
        prev_y = min(pt[1] for pt in lines[-1][-1]['bbox'])
        if abs(curr_y - prev_y) <= y_tol:
            lines[-1].append(r)
        else:
            lines.append([r])
    return lines


def find_line_for_field(lines: list[list[dict]], label: str) -> list[dict] | None:
    label_lower = label.lower()
    for group in lines:
        combined = ' '.join(r['text'] for r in group).lower()
        if label_lower in combined or label_lower[:3] in combined:
            return group
    return None


# ── Pixel-accurate text erasing ───────────────────────────────────────────────

def _erase_text_pixels(
    image_rgb: np.ndarray,
    line_bbox: tuple[int, int, int, int],
) -> np.ndarray:
    """
    Erase ONLY the white text character pixels within a line bounding box.

    Steps:
      1. Crop the line region (with a small vertical pad for ascenders/descenders)
      2. Use Otsu's method to threshold bright (text) vs dark (background) pixels
      3. Dilate the mask slightly to cover antialiased edges
      4. Inpaint only those pixels — OpenCV reconstructs the dark background
         from the surrounding dark box pixels, making it seamless

    The dark overlay box itself is never touched.
    """
    h_img, w_img = image_rgb.shape[:2]
    x1, y1, x2, y2 = line_bbox

    # Vertical padding to catch ascenders/descenders fully
    v_pad = max(3, int((y2 - y1) * 0.18))
    px1 = max(0, x1 - 2)
    py1 = max(0, y1 - v_pad)
    px2 = min(w_img, x2 + 2)
    py2 = min(h_img, y2 + v_pad)

    region = image_rgb[py1:py2, px1:px2]
    gray   = cv2.cvtColor(region, cv2.COLOR_RGB2GRAY)

    # Otsu threshold: automatically separates bright text from dark background
    _, raw_mask = cv2.threshold(gray, 0, 255,
                                cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Sanity check: if Otsu marks >60% as "text", the region is unusual —
    # fall back to a fixed high threshold (very bright white only)
    if raw_mask.mean() > 153:
        _, raw_mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    # Dilate to cover antialiased pixel edges around each character
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    text_mask_region = cv2.dilate(raw_mask, kernel, iterations=1)

    # Build a full-image uint8 mask (zeros everywhere except detected text)
    full_mask = np.zeros((h_img, w_img), dtype=np.uint8)
    full_mask[py1:py2, px1:px2] = text_mask_region

    # Inpaint only the text pixels
    bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
    inpainted_bgr = cv2.inpaint(bgr, full_mask, inpaintRadius=3,
                                flags=cv2.INPAINT_TELEA)
    return cv2.cvtColor(inpainted_bgr, cv2.COLOR_BGR2RGB)


# ── Text rendering ────────────────────────────────────────────────────────────

def _render_new_text(
    image_rgb: np.ndarray,
    line_bbox: tuple[int, int, int, int],
    label: str,
    new_value: str,
) -> np.ndarray:
    """
    Render "Label: new_value" at the same position as the original line.

    Font size is derived from the line's pixel height so it matches the
    original text size regardless of image resolution.
    """
    x1, y1, x2, y2 = line_bbox
    line_h = y2 - y1
    font_size = max(8, int(line_h * 0.88))
    font = _load_font(font_size)

    pil = Image.fromarray(image_rgb)
    draw = ImageDraw.Draw(pil)
    draw.text((x1, y1), f'{label}: {new_value}',
              font=font, fill=(255, 255, 255))
    return np.array(pil)


# ── Overlay bbox (needed to skip if no detections) ────────────────────────────

def compute_overlay_bbox(
    ocr_results: list[dict],
    image_shape: tuple[int, int],
) -> tuple[int, int, int, int] | None:
    if not ocr_results:
        return None
    all_x = [pt[0] for r in ocr_results for pt in r['bbox']]
    all_y = [pt[1] for r in ocr_results for pt in r['bbox']]
    h, w = image_shape
    return (0, max(0, int(min(all_y)) - 10),
            min(w, max(int(max(all_x)) + 10, int(w * 0.42))), h)


# ── Public API ────────────────────────────────────────────────────────────────

def process_image(
    image_rgb: np.ndarray,
    ocr_results: list[dict],
    original_fields: dict[str, str | None],
    new_fields: dict[str, str | None],
) -> np.ndarray | None:
    """
    Word-document-style text editing for NoteCam overlays.

    For each field the user changed:
      1. Finds the exact pixel line via OCR grouping
      2. Erases ONLY the white text characters (Otsu mask + inpainting)
         — dark box, photo, everything else is pixel-identical to original
      3. Renders the new value at the exact same position with the same
         measured font size

    Unchanged fields: zero pixels are touched.
    Returns None if no OCR detections are available.
    """
    if not ocr_results:
        return None

    if compute_overlay_bbox(ocr_results, image_rgb.shape[:2]) is None:
        return None

    lines  = group_ocr_into_lines(ocr_results)
    result = image_rgb.copy()
    changed = 0

    for key, label in FIELD_ORDER:
        old_val = (original_fields.get(key) or '').strip()
        new_val = (new_fields.get(key) or '').strip()

        if old_val == new_val:
            continue  # not changed — original pixels untouched

        group = find_line_for_field(lines, label)
        if group is None:
            continue  # OCR missed this line — skip rather than corrupt

        line_bbox = _bbox_of_group(group)

        # Step 1: erase old text characters (dark box untouched)
        result = _erase_text_pixels(result, line_bbox)

        # Step 2: write new value at the same position
        result = _render_new_text(result, line_bbox, label, new_val)
        changed += 1

    return result if changed > 0 else image_rgb
