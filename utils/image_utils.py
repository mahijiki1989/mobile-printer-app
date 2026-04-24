import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FONT_PATHS = [
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
    """Load a TrueType font at the given pixel size, with fallbacks."""
    for path in FONT_PATHS:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def compute_overlay_bbox(
    ocr_results: list[dict],
    image_shape: tuple[int, int],
    padding: int = 10,
) -> tuple[int, int, int, int] | None:
    """
    Compute the full NoteCam overlay bounding box.

    The tight OCR bbox only covers text character pixels — the actual
    dark background box is much larger. This function:
      - Uses OCR results to find WHERE the overlay is (approximate y1)
      - Then anchors the box to the left and bottom edges (NoteCam always does)
      - Ensures minimum dimensions proportional to image size

    Returns (x1, y1, x2, y2) or None if ocr_results is empty.
    """
    if not ocr_results:
        return None

    all_x = [pt[0] for r in ocr_results for pt in r['bbox']]
    all_y = [pt[1] for r in ocr_results for pt in r['bbox']]

    h, w = image_shape

    ocr_y1 = max(0, int(min(all_y)) - padding)
    ocr_x2 = min(w, int(max(all_x)) + padding)

    # NoteCam overlay is always anchored to the bottom-left corner.
    # x1 is always 0; y2 is always the image bottom.
    x1 = 0
    y2 = h

    # The overlay box extends at least 42% of image width.
    x2 = max(ocr_x2, int(w * 0.42))
    x2 = min(x2, w)

    # The dark background box starts above the first text line.
    # Ensure at least 32% of image height is covered — this matches
    # the typical NoteCam overlay proportion.
    min_box_h = int(h * 0.32)
    y1 = min(ocr_y1, h - min_box_h)
    y1 = max(0, y1)

    return (x1, y1, x2, y2)


def build_inpaint_mask(
    image_shape: tuple[int, int],
    bbox: tuple[int, int, int, int],
) -> np.ndarray:
    """Build a uint8 binary mask: 255 inside bbox, 0 elsewhere."""
    h, w = image_shape
    mask = np.zeros((h, w), dtype=np.uint8)
    x1, y1, x2, y2 = bbox
    mask[y1:y2, x1:x2] = 255
    return mask


def inpaint_region(
    image_rgb: np.ndarray,
    mask: np.ndarray,
    inpaint_radius: int = 5,
) -> np.ndarray:
    """
    Remove the masked region using OpenCV TELEA inpainting.

    TELEA propagates texture from the boundary inward, producing
    smoother results on natural photographic backgrounds than NS.
    Returns the inpainted image in RGB format.
    """
    image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
    result_bgr = cv2.inpaint(image_bgr, mask, inpaint_radius, cv2.INPAINT_TELEA)
    return cv2.cvtColor(result_bgr, cv2.COLOR_BGR2RGB)


def render_text_overlay(
    image_rgb: np.ndarray,
    bbox: tuple[int, int, int, int],
    fields: dict[str, str | None],
    bg_alpha: int = 175,
    line_spacing_factor: float = 1.2,
) -> np.ndarray:
    """
    Re-render edited metadata overlay matching the NoteCam visual style.

    Font size is derived from the full overlay box height (not the tight
    OCR bbox) so text scales correctly with any image resolution.
    Padding scales proportionally with the box size.

    Parameters
    ----------
    image_rgb  : inpainted image in RGB format
    bbox       : (x1, y1, x2, y2) — the full overlay box position
    fields     : edited field values
    bg_alpha   : dark background opacity (0=transparent, 255=solid)
    line_spacing_factor : multiplier for advancing between lines

    Returns RGB numpy array with overlay composited in.
    """
    lines = [
        f'{label}: {fields.get(key) or ""}'
        for key, label in FIELD_ORDER
    ]

    x1, y1, x2, y2 = bbox
    box_h = y2 - y1
    box_w = x2 - x1
    n_lines = len(lines)

    # Font size: fit n_lines into box_h with top+bottom padding.
    # Divide box into (n_lines + 2) slots — 1 slot each for top/bottom padding.
    # Use 80% of each slot for the glyph, 20% for inter-line gap.
    slot_h = box_h / (n_lines + 2)
    font_size = max(10, int(slot_h * 0.80))
    font = _load_font(font_size)

    # Measure actual glyph height for the loaded font
    try:
        bb = font.getbbox('Ag')
        line_h = bb[3] - bb[1]
    except AttributeError:
        _, line_h = font.getsize('Ag')  # type: ignore[attr-defined]

    line_advance = int(line_h * line_spacing_factor)

    # Padding proportional to box size (at least a few pixels)
    left_pad = max(6, int(box_w * 0.025))
    top_pad  = max(4, int(slot_h * 0.6))   # ~1 slot of top breathing room

    base = Image.fromarray(image_rgb).convert('RGBA')
    overlay = Image.new('RGBA', base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Dark semi-transparent background rectangle
    draw.rectangle([x1, y1, x2, y2], fill=(0, 0, 0, bg_alpha))

    # White text lines
    text_x = x1 + left_pad
    text_y = y1 + top_pad
    for line in lines:
        draw.text((text_x, text_y), line, font=font, fill=(255, 255, 255, 255))
        text_y += line_advance

    result = Image.alpha_composite(base, overlay).convert('RGB')
    return np.array(result)


def process_image(
    image_rgb: np.ndarray,
    ocr_results: list[dict],
    fields: dict[str, str | None],
) -> np.ndarray | None:
    """
    Full pipeline: compute full overlay bbox → inpaint → re-render.

    Returns processed RGB image, or None if no OCR detections available.
    """
    bbox = compute_overlay_bbox(ocr_results, image_rgb.shape[:2])
    if bbox is None:
        return None

    mask = build_inpaint_mask(image_rgb.shape[:2], bbox)
    inpainted = inpaint_region(image_rgb, mask)
    return render_text_overlay(inpainted, bbox, fields)
