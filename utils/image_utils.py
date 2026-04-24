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
    Compute the axis-aligned bounding box enclosing all OCR detections.

    Parameters
    ----------
    ocr_results : list[dict]  — from run_ocr_on_image()
    image_shape : (height, width)
    padding : pixels to expand on all sides

    Returns (x1, y1, x2, y2) clamped to image bounds, or None if empty.
    """
    if not ocr_results:
        return None

    all_x = [pt[0] for r in ocr_results for pt in r['bbox']]
    all_y = [pt[1] for r in ocr_results for pt in r['bbox']]

    h, w = image_shape
    x1 = max(0, int(min(all_x)) - padding)
    y1 = max(0, int(min(all_y)) - padding)
    x2 = min(w, int(max(all_x)) + padding)
    y2 = min(h, int(max(all_y)) + padding)
    return x1, y1, x2, y2


def build_inpaint_mask(
    image_shape: tuple[int, int],
    bbox: tuple[int, int, int, int],
) -> np.ndarray:
    """
    Build a uint8 binary mask for cv2.inpaint.

    255 inside the bounding box (region to erase), 0 elsewhere.
    """
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

    TELEA propagates texture from the boundary inward and produces
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
    bg_alpha: int = 160,
    left_pad: int = 8,
    top_pad: int = 6,
    line_spacing_factor: float = 1.15,
) -> np.ndarray:
    """
    Re-render edited metadata as a styled overlay at the original position.

    Draws a semi-transparent dark rectangle then white text lines using
    DejaVu Sans, matching the NoteCam visual style.

    Parameters
    ----------
    image_rgb      : inpainted image in RGB format
    bbox           : (x1, y1, x2, y2) overlay rectangle position
    fields         : edited field values
    bg_alpha       : background rectangle opacity (0=transparent, 255=solid)
    left_pad       : horizontal text padding inside rectangle (px)
    top_pad        : vertical text padding inside rectangle (px)
    line_spacing_factor : multiplier for advancing between lines

    Returns RGB numpy array with overlay composited in.
    """
    lines = [
        f'{label}: {fields.get(key) or ""}'
        for key, label in FIELD_ORDER
    ]

    x1, y1, x2, y2 = bbox
    bbox_h = y2 - y1
    n_lines = len(lines)
    font_size = max(10, int((bbox_h / n_lines) * 0.75))
    font = _load_font(font_size)

    # Measure line height — PIL 10+ uses getbbox; older uses getsize
    try:
        bb = font.getbbox('Ag')
        line_h = bb[3] - bb[1]
    except AttributeError:
        _, line_h = font.getsize('Ag')  # type: ignore[attr-defined]
    line_advance = int(line_h * line_spacing_factor)

    base = Image.fromarray(image_rgb).convert('RGBA')
    overlay = Image.new('RGBA', base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    draw.rectangle([x1, y1, x2, y2], fill=(0, 0, 0, bg_alpha))

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
    Full pipeline: detect overlay bbox → inpaint → re-render text.

    Returns the processed RGB image, or None if no overlay was detected
    (ocr_results empty → no bbox to work with).
    """
    bbox = compute_overlay_bbox(ocr_results, image_rgb.shape[:2])
    if bbox is None:
        return None

    mask = build_inpaint_mask(image_rgb.shape[:2], bbox)
    inpainted = inpaint_region(image_rgb, mask)
    return render_text_overlay(inpainted, bbox, fields)
