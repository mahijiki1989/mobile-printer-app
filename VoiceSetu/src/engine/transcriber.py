"""
Transcription engine for VoiceSetu.
Uses faster-whisper for offline speech-to-text.
SPEED OPTIMIZED: tiny model + beam_size=1 + greedy decoding for instant results.
Supports Hindi and English with optional auto-detection.
"""

import logging
import os
import threading
import time
from pathlib import Path
from typing import Callable, Optional, Tuple

import numpy as np

logger = logging.getLogger(__name__)

LANGUAGE_CODES = {
    "en": "en",
    "hi": "hi",
    "auto": None,
}

MODEL_SIZES = ["tiny", "base", "small", "medium", "large-v2"]


class TranscriptionEngine:
    """
    Manages the faster-whisper model for offline speech recognition.
    SPEED PRIORITY: Uses greedy decoding (beam=1), max CPU threads,
    and tiny/base model for near-instant transcription.
    """

    def __init__(
        self,
        model_size: str = "tiny",
        compute_type: str = "int8",
        model_path: str = "",
        beam_size: int = 1,
    ):
        self._model = None
        self._model_size = model_size
        self._compute_type = compute_type
        self._custom_model_path = model_path
        self._beam_size = beam_size
        self._is_loaded = False
        self._is_loading = False
        self._lock = threading.Lock()

    @property
    def is_loaded(self) -> bool:
        return self._is_loaded

    @property
    def is_loading(self) -> bool:
        return self._is_loading

    def load_model(self, on_progress: Optional[Callable[[str], None]] = None) -> bool:
        """
        Load the whisper model. Uses max CPU threads for speed.
        Returns True if successful, False otherwise.
        """
        with self._lock:
            if self._is_loaded:
                return True
            if self._is_loading:
                return False
            self._is_loading = True

        try:
            from faster_whisper import WhisperModel

            if on_progress:
                on_progress("Loading speech model...")

            model_path = self._custom_model_path if self._custom_model_path else self._model_size

            # Use ALL available CPU threads for maximum speed
            cpu_count = os.cpu_count() or 4

            self._model = WhisperModel(
                model_path,
                device="cpu",
                compute_type=self._compute_type,
                cpu_threads=cpu_count,
                num_workers=2,
            )

            self._is_loaded = True
            self._is_loading = False

            if on_progress:
                on_progress("Model loaded successfully")

            logger.info(f"Model '{model_path}' loaded with {cpu_count} threads")
            return True

        except Exception as e:
            self._is_loaded = False
            self._is_loading = False
            logger.error(f"Failed to load model: {e}")
            if on_progress:
                on_progress(f"Error loading model: {str(e)}")
            return False

    def load_model_async(
        self,
        on_complete: Optional[Callable[[bool], None]] = None,
        on_progress: Optional[Callable[[str], None]] = None,
    ) -> None:
        """Load the model in a background thread."""

        def _load():
            success = self.load_model(on_progress=on_progress)
            if on_complete:
                on_complete(success)

        thread = threading.Thread(target=_load, daemon=True)
        thread.start()

    def unload_model(self) -> None:
        """Unload the current model to free memory."""
        with self._lock:
            self._model = None
            self._is_loaded = False
            self._is_loading = False

    def change_model(
        self,
        model_size: str = "",
        model_path: str = "",
        compute_type: str = "",
    ) -> None:
        """Change model configuration. Must call load_model() after."""
        self.unload_model()
        if model_size:
            self._model_size = model_size
        if model_path:
            self._custom_model_path = model_path
        if compute_type:
            self._compute_type = compute_type

    def transcribe(
        self,
        audio_data: np.ndarray,
        language: str = "en",
        auto_detect: bool = False,
    ) -> Tuple[str, str, float]:
        """
        Transcribe audio data to text. SPEED OPTIMIZED.

        Uses beam_size=1 (greedy decoding) for fastest possible results.
        VAD filter removes silence for faster processing.

        Args:
            audio_data: numpy array of audio samples (float32, 16kHz mono)
            language: language code ('en', 'hi', or 'auto')
            auto_detect: if True, let the model detect language

        Returns:
            Tuple of (transcribed_text, detected_language, confidence)
        """
        if not self._is_loaded or self._model is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")

        if audio_data is None or len(audio_data) == 0:
            return ("", language, 0.0)

        audio_float = audio_data.astype(np.float32)
        if audio_float.max() > 1.0:
            audio_float = audio_float / 32768.0

        lang_param = None if auto_detect else LANGUAGE_CODES.get(language, language)

        try:
            segments, info = self._model.transcribe(
                audio_float,
                language=lang_param,
                beam_size=1,
                best_of=1,
                temperature=0.0,
                condition_on_previous_text=False,
                vad_filter=True,
                vad_parameters=dict(
                    min_silence_duration_ms=300,
                    speech_pad_ms=100,
                    threshold=0.3,
                ),
                without_timestamps=True,
                word_timestamps=False,
            )

            text_parts = []
            for segment in segments:
                text_parts.append(segment.text.strip())

            full_text = " ".join(text_parts).strip()
            detected_lang = info.language if info else language
            confidence = info.language_probability if info else 0.0

            return (full_text, detected_lang, confidence)

        except Exception as e:
            logger.error(f"Transcription error: {e}")
            raise

    def detect_language(self, audio_data: np.ndarray) -> Tuple[str, float]:
        """
        Detect the language of an audio sample.

        Returns:
            Tuple of (language_code, probability)
        """
        if not self._is_loaded or self._model is None:
            raise RuntimeError("Model not loaded.")

        audio_float = audio_data.astype(np.float32)
        if audio_float.max() > 1.0:
            audio_float = audio_float / 32768.0

        try:
            _, info = self._model.transcribe(
                audio_float[:16000 * 30],
                language=None,
                beam_size=1,
                without_timestamps=True,
            )
            return (info.language, info.language_probability)
        except Exception as e:
            logger.error(f"Language detection error: {e}")
            return ("en", 0.0)
