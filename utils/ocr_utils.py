import re
import numpy as np
import easyocr

_reader: easyocr.Reader | None = None


def get_reader() -> easyocr.Reader:
    """Return the cached EasyOCR Reader, constructing it on first call."""
    global _reader
    if _reader is None:
        _reader = easyocr.Reader(['en'], gpu=False)
    return _reader


def crop_overlay_region(image_rgb: np.ndarray) -> tuple[np.ndarray, int, int]:
    """
    Crop the bottom-left overlay region where NoteCam places its metadata.

    NoteCam overlays text in the bottom-left corner, approximately
    50% of image width and 40% of image height.

    Returns
    -------
    crop : np.ndarray  — RGB cropped region
    x_offset : int    — always 0 (crop starts at left edge)
    y_offset : int    — top y-coordinate of crop in full-image space
    """
    h, w = image_rgb.shape[:2]
    crop_w = int(w * 0.55)   # 55% width — covers full overlay width
    crop_h = int(h * 0.45)   # 45% height — captures overlay top with margin
    y_offset = h - crop_h
    x_offset = 0
    crop = image_rgb[y_offset:y_offset + crop_h, x_offset:x_offset + crop_w]
    return crop, x_offset, y_offset


def run_ocr_on_image(image_rgb: np.ndarray) -> list[dict]:
    """
    Detect and extract text from the NoteCam overlay region.

    Crops the bottom-left quadrant, runs EasyOCR, adjusts bounding
    box coordinates to full-image space, and sorts top-to-bottom.

    Returns
    -------
    list of dicts with keys:
        'bbox' : list of 4 [x, y] points in full-image coordinates
        'text' : str
        'conf' : float (0.0–1.0)
    """
    crop, x_off, y_off = crop_overlay_region(image_rgb)
    raw = get_reader().readtext(crop, detail=1, paragraph=False)

    results = []
    for bbox, text, conf in raw:
        if conf < 0.1:
            continue
        adjusted_bbox = [[pt[0] + x_off, pt[1] + y_off] for pt in bbox]
        results.append({'bbox': adjusted_bbox, 'text': text, 'conf': conf})

    results.sort(key=lambda r: min(pt[1] for pt in r['bbox']))
    return results


FIELD_PATTERNS: dict[str, str] = {
    'latitude':  r'Lat(?:itude)?[:\s]+([+-]?\d+\.?\d*)',
    'longitude': r'Lon(?:gitude)?[:\s]+([+-]?\d+\.?\d*)',
    'elevation': r'Elev(?:ation)?[:\s]+([^\n]+)',
    'accuracy':  r'Acc(?:uracy)?[:\s]+([^\n]+)',
    'time':      r'Time[:\s]+([^\n]+)',
    'note':      r'Note[:\s]+([^\n]+)',
}


def parse_fields(ocr_results: list[dict]) -> dict[str, str | None]:
    """
    Parse NoteCam metadata fields from OCR results.

    Tries newline-joined text first (primary), then space-joined as a
    fallback to handle cases where EasyOCR splits "Label: value" into
    two separate detections.

    Returns dict with keys: latitude, longitude, elevation, accuracy,
    time, note — each str or None if not matched.
    """
    texts = [r['text'] for r in ocr_results]
    full_newline = '\n'.join(texts)
    full_space = ' '.join(texts)

    fields: dict[str, str | None] = {}
    for key, pattern in FIELD_PATTERNS.items():
        m = re.search(pattern, full_newline, re.IGNORECASE)
        if not m:
            m = re.search(pattern, full_space, re.IGNORECASE)
        fields[key] = m.group(1).strip() if m else None

    return fields
