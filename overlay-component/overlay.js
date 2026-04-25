/**
 * overlay.js  v1.0
 * Minimal JS for the geo-tag overlay component.
 *
 * Features:
 *  - Auto-grow textarea for Note field
 *  - Dispatches a custom `geo:change` event on every field edit
 *  - `GeoOverlay.getData(el)`  → current field values as an object
 *  - `GeoOverlay.setData(el, data)` → programmatically update fields
 *  - `GeoOverlay.reset(el)`    → restore original placeholder values
 *  - `GeoOverlay.lock(el)`     → disable editing (read-only mode)
 *  - `GeoOverlay.unlock(el)`   → re-enable editing
 *
 * No dependencies. Works with any number of overlays on the page.
 */

const GeoOverlay = (() => {

  /* ── Auto-grow textarea ─────────────────────────────────────────────── */

  function _autoGrow(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
  }

  /* ── Dispatch custom change event ───────────────────────────────────── */

  function _dispatchChange(overlayEl, fieldKey, value) {
    overlayEl.dispatchEvent(new CustomEvent('geo:change', {
      bubbles: true,
      detail: { field: fieldKey, value, all: getData(overlayEl) }
    }));
  }

  /* ── Wire up a single overlay element ──────────────────────────────── */

  function _init(overlayEl) {
    const inputs = overlayEl.querySelectorAll('.geo-val');

    inputs.forEach(input => {
      const key = input.dataset.field;

      // Auto-grow for textareas
      if (input.tagName === 'TEXTAREA') {
        _autoGrow(input);
        input.addEventListener('input', () => _autoGrow(input));
      }

      // Fire geo:change on every keystroke
      input.addEventListener('input', () => {
        if (key) _dispatchChange(overlayEl, key, input.value);
      });

      // Select all on focus for quick replacement
      input.addEventListener('focus', () => input.select());
    });
  }

  /* ── Public API ─────────────────────────────────────────────────────── */

  /**
   * Read current values from an overlay element.
   * @param  {Element} overlayEl  — .geo-overlay element
   * @returns {{ latitude, longitude, elevation, accuracy, time, note }}
   */
  function getData(overlayEl) {
    const result = {};
    overlayEl.querySelectorAll('.geo-val[data-field]').forEach(el => {
      result[el.dataset.field] = el.value;
    });
    return result;
  }

  /**
   * Programmatically set field values.
   * @param  {Element} overlayEl
   * @param  {Object}  data  — partial or full field map
   */
  function setData(overlayEl, data) {
    Object.entries(data).forEach(([key, val]) => {
      const el = overlayEl.querySelector(`.geo-val[data-field="${key}"]`);
      if (!el) return;
      el.value = val;
      if (el.tagName === 'TEXTAREA') _autoGrow(el);
    });
  }

  /**
   * Reset all fields to their original `data-original` values.
   * @param  {Element} overlayEl
   */
  function reset(overlayEl) {
    overlayEl.querySelectorAll('.geo-val[data-original]').forEach(el => {
      el.value = el.dataset.original;
      if (el.tagName === 'TEXTAREA') _autoGrow(el);
    });
  }

  /**
   * Disable all field editing (read-only visual mode).
   * @param  {Element} overlayEl
   */
  function lock(overlayEl) {
    overlayEl.classList.add('geo-overlay--locked');
    overlayEl.querySelectorAll('.geo-val').forEach(el => el.setAttribute('readonly', ''));
  }

  /**
   * Re-enable field editing.
   * @param  {Element} overlayEl
   */
  function unlock(overlayEl) {
    overlayEl.classList.remove('geo-overlay--locked');
    overlayEl.querySelectorAll('.geo-val').forEach(el => el.removeAttribute('readonly'));
  }

  /* ── Auto-init on DOMContentLoaded ─────────────────────────────────── */

  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.geo-overlay').forEach(_init);
  });

  return { getData, setData, reset, lock, unlock };

})();
