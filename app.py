import hashlib
import io

import numpy as np
import streamlit as st
from PIL import Image

from utils.image_utils import process_image
from utils.ocr_utils import parse_fields, run_ocr_on_image

# ── Page configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NoteCam Metadata Editor",
    page_icon="📷",
    layout="wide",
)

# ── Session state defaults ────────────────────────────────────────────────────
_DEFAULTS = {
    'image_rgb': None,
    'ocr_results': [],
    'fields': {},
    'result_rgb': None,
    'ocr_done': False,
    '_file_hash': None,
}
for key, val in _DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = val


# ── Helpers ───────────────────────────────────────────────────────────────────

def decode_upload(file_bytes: bytes) -> np.ndarray:
    """Decode raw image bytes to an RGB numpy array via PIL."""
    return np.array(Image.open(io.BytesIO(file_bytes)).convert('RGB'))


def encode_jpeg(image_rgb: np.ndarray, quality: int = 95) -> bytes:
    """Encode an RGB numpy array to JPEG bytes."""
    buf = io.BytesIO()
    Image.fromarray(image_rgb).save(buf, format='JPEG', quality=quality)
    return buf.getvalue()


# ── Header ────────────────────────────────────────────────────────────────────
st.title("NoteCam Image Metadata Editor")
st.caption(
    "Upload a NoteCam photo to extract its GPS metadata overlay via OCR, "
    "edit the fields, then download the seamlessly updated image."
)

# ── Upload ────────────────────────────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "Upload a NoteCam image",
    type=["jpg", "jpeg", "png", "webp"],
    help=(
        "The app expects a photo taken with the NoteCam app — it should have "
        "a dark metadata overlay (Latitude, Longitude, Elevation, Accuracy, "
        "Time, Note) in the bottom-left corner."
    ),
)

if uploaded_file is not None:
    raw_bytes = uploaded_file.read()
    file_hash = hashlib.md5(raw_bytes).hexdigest()

    # Reset all derived state when a genuinely new image is uploaded
    if st.session_state['_file_hash'] != file_hash:
        st.session_state['_file_hash'] = file_hash
        st.session_state['image_rgb'] = decode_upload(raw_bytes)
        st.session_state['ocr_results'] = []
        st.session_state['fields'] = {}
        st.session_state['result_rgb'] = None
        st.session_state['ocr_done'] = False

# ── Main UI (only shown after a file is uploaded) ─────────────────────────────
if st.session_state['image_rgb'] is not None:
    image_rgb: np.ndarray = st.session_state['image_rgb']

    col_img, col_form = st.columns([1, 1], gap="large")

    # ── Original image preview ────────────────────────────────────────────────
    with col_img:
        st.subheader("Original Image")
        st.image(image_rgb, use_container_width=True)

    # ── Extracted metadata form ───────────────────────────────────────────────
    with col_form:
        st.subheader("Extracted Metadata")

        # Run OCR once per upload; the ocr_done flag prevents re-running
        # on every widget interaction that triggers a Streamlit rerun.
        if not st.session_state['ocr_done']:
            with st.spinner(
                "Running OCR on the overlay region — "
                "this may take 10–30 s on first run while the model loads..."
            ):
                try:
                    results = run_ocr_on_image(image_rgb)
                    st.session_state['ocr_results'] = results
                    st.session_state['fields'] = parse_fields(results)
                    st.session_state['ocr_done'] = True
                except Exception as exc:
                    st.error(f"OCR failed: {exc}")
                    st.stop()

        if not st.session_state['ocr_results']:
            st.warning(
                "No text was detected in the bottom-left overlay region. "
                "Make sure the image is a NoteCam photo with a visible "
                "metadata overlay. You can still fill the fields manually."
            )

        f = st.session_state['fields']

        lat   = st.text_input("Latitude",  value=f.get('latitude')  or '')
        lon   = st.text_input("Longitude", value=f.get('longitude') or '')
        elev  = st.text_input("Elevation", value=f.get('elevation') or '')
        acc   = st.text_input("Accuracy",  value=f.get('accuracy')  or '')
        time_ = st.text_input("Date / Time", value=f.get('time')    or '')
        note  = st.text_area("Note",       value=f.get('note')      or '',
                              height=80)

        # Show raw OCR lines for debugging if needed
        with st.expander("Raw OCR output"):
            if st.session_state['ocr_results']:
                for r in st.session_state['ocr_results']:
                    st.write(f"`{r['text']}`  — confidence: {r['conf']:.2f}")
            else:
                st.write("_(nothing detected)_")

    # ── Process & Update button ───────────────────────────────────────────────
    st.divider()
    if st.button("Process & Update", type="primary", use_container_width=False):
        edited_fields = {
            'latitude':  lat,
            'longitude': lon,
            'elevation': elev,
            'accuracy':  acc,
            'time':      time_,
            'note':      note,
        }
        with st.spinner("Inpainting original overlay and re-rendering edited text..."):
            try:
                result = process_image(
                    image_rgb,
                    st.session_state['ocr_results'],
                    edited_fields,
                )
                if result is None:
                    st.error(
                        "Could not determine the overlay bounding box — "
                        "no OCR detections were available. "
                        "Try re-uploading the image or adjusting the photo."
                    )
                else:
                    st.session_state['result_rgb'] = result
                    st.success("Image updated successfully.")
            except Exception as exc:
                st.error(f"Processing failed: {exc}")

    # ── Before / After comparison + Download ─────────────────────────────────
    if st.session_state['result_rgb'] is not None:
        result_rgb: np.ndarray = st.session_state['result_rgb']

        st.subheader("Before / After Comparison")
        before_col, after_col = st.columns(2)
        with before_col:
            st.caption("Before (original)")
            st.image(image_rgb, use_container_width=True)
        with after_col:
            st.caption("After (edited)")
            st.image(result_rgb, use_container_width=True)

        st.download_button(
            label="Download Edited Image",
            data=encode_jpeg(result_rgb),
            file_name="notecam_edited.jpg",
            mime="image/jpeg",
            type="primary",
        )
