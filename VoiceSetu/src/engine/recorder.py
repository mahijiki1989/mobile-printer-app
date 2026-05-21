"""
Audio recorder for VoiceSetu.
Handles microphone input using sounddevice.
Includes basic silence detection for auto-stop.
"""

import logging
import threading
import time
from typing import Callable, List, Optional, Tuple

import numpy as np

logger = logging.getLogger(__name__)

SAMPLE_RATE = 16000
CHANNELS = 1
DTYPE = "float32"
BLOCK_SIZE = 1024


class AudioRecorder:
    """
    Records audio from microphone with silence detection.
    Uses sounddevice for cross-platform audio capture.
    """

    def __init__(
        self,
        sample_rate: int = SAMPLE_RATE,
        silence_threshold: float = 1.0,
        device_index: Optional[int] = None,
        vad_enabled: bool = True,
        vad_threshold: float = 0.3,
    ):
        self._sample_rate = sample_rate
        self._silence_threshold = silence_threshold
        self._device_index = device_index if device_index and device_index >= 0 else None
        self._vad_enabled = vad_enabled
        self._vad_threshold = vad_threshold
        self._is_recording = False
        self._audio_buffer: List[np.ndarray] = []
        self._stream = None
        self._lock = threading.Lock()
        self._silence_start: Optional[float] = None
        self._has_speech = False
        self._energy_threshold = 0.008
        self._on_silence_detected: Optional[Callable] = None

    @property
    def is_recording(self) -> bool:
        return self._is_recording

    @staticmethod
    def get_microphones() -> List[Tuple[int, str]]:
        """Get list of available input devices as (index, name) tuples."""
        try:
            import sounddevice as sd
            devices = sd.query_devices()
            microphones = []
            for i, dev in enumerate(devices):
                if dev.get("max_input_channels", 0) > 0:
                    name = dev.get("name", f"Device {i}")
                    microphones.append((i, name))
            return microphones
        except Exception as e:
            logger.error(f"Error querying microphones: {e}")
            return []

    @staticmethod
    def get_default_device_index() -> Optional[int]:
        """Get the default input device index."""
        try:
            import sounddevice as sd
            default = sd.default.device[0]
            return int(default) if default is not None else None
        except Exception:
            return None

    def set_device(self, device_index: Optional[int]) -> None:
        """Set the recording device."""
        self._device_index = device_index if device_index and device_index >= 0 else None

    def set_silence_threshold(self, seconds: float) -> None:
        """Set the silence threshold for auto-stop."""
        self._silence_threshold = seconds

    def set_on_silence_detected(self, callback: Optional[Callable]) -> None:
        """Set callback for when silence is detected (auto-stop)."""
        self._on_silence_detected = callback

    def start_recording(self) -> bool:
        """Start recording audio from the microphone."""
        import sounddevice as sd

        if self._is_recording:
            return True

        self._audio_buffer = []
        self._silence_start = None
        self._has_speech = False

        try:
            self._stream = sd.InputStream(
                samplerate=self._sample_rate,
                channels=CHANNELS,
                dtype=DTYPE,
                blocksize=BLOCK_SIZE,
                device=self._device_index,
                callback=self._audio_callback,
            )
            self._stream.start()
            self._is_recording = True
            logger.info("Recording started")
            return True
        except Exception as e:
            logger.error(f"Failed to start recording: {e}")
            self._is_recording = False
            return False

    def stop_recording(self) -> Optional[np.ndarray]:
        """
        Stop recording and return the recorded audio as a numpy array.
        Returns None if no audio was captured.
        """
        if not self._is_recording:
            return None

        self._is_recording = False

        try:
            if self._stream:
                self._stream.stop()
                self._stream.close()
                self._stream = None
        except Exception as e:
            logger.error(f"Error stopping stream: {e}")

        with self._lock:
            if not self._audio_buffer:
                return None
            audio = np.concatenate(self._audio_buffer, axis=0).flatten()
            self._audio_buffer = []

        logger.info(f"Recording stopped. Audio length: {len(audio) / self._sample_rate:.1f}s")
        return audio

    def _audio_callback(self, indata: np.ndarray, frames: int, time_info, status) -> None:
        """Callback for sounddevice stream. Buffers audio and checks for silence."""
        if status:
            logger.warning(f"Audio stream status: {status}")

        if not self._is_recording:
            return

        audio_chunk = indata.copy()

        with self._lock:
            self._audio_buffer.append(audio_chunk)

        energy = np.sqrt(np.mean(audio_chunk ** 2))

        if energy > self._energy_threshold:
            self._has_speech = True
            self._silence_start = None
        else:
            if self._has_speech and self._silence_start is None:
                self._silence_start = time.time()
            elif self._has_speech and self._silence_start is not None:
                silence_duration = time.time() - self._silence_start
                if silence_duration >= self._silence_threshold:
                    if self._on_silence_detected:
                        self._on_silence_detected()

    def get_current_level(self) -> float:
        """Get the current audio input level (0.0 to 1.0)."""
        with self._lock:
            if self._audio_buffer:
                last_chunk = self._audio_buffer[-1]
                energy = np.sqrt(np.mean(last_chunk ** 2))
                return min(1.0, energy * 10)
        return 0.0
