"""Audio-reactive effects that respond to frequency content."""

import numpy as np
from typing import Tuple, List, Dict


class AudioReactiveEffects:
    """Creates visual effects that respond to audio frequency analysis."""

    def __init__(self):
        """Initialize audio reactive effects."""
        self.frequency_bands = 5  # Number of frequency bands to analyze

    def extract_frequency_bands(
        self, audio_data: Tuple[int, np.ndarray], n_bands: int = 5
    ) -> np.ndarray:
        """Extract audio into frequency bands.

        Args:
            audio_data: Tuple of (sample_rate, audio_data)
            n_bands: Number of frequency bands

        Returns:
            Array of shape (n_bands,) with band energies
        """
        sr, y = audio_data

        try:
            import librosa
        except ImportError:
            raise ImportError("librosa is required for audio analysis")

        # Compute STFT
        S = librosa.stft(y)
        magnitude = np.abs(S)

        # Compute energy in each frequency band
        n_fft = magnitude.shape[0]
        band_size = n_fft // n_bands
        bands = np.zeros(n_bands)

        for i in range(n_bands):
            start_idx = i * band_size
            end_idx = (i + 1) * band_size if i < n_bands - 1 else n_fft
            bands[i] = np.mean(magnitude[start_idx:end_idx])

        # Normalize to 0-1 range
        bands = (bands - bands.min()) / (bands.max() - bands.min() + 1e-6)
        return bands

    def analyze_frequency_over_time(
        self, audio_data: Tuple[int, np.ndarray], n_bands: int = 5, hop_length: int = 512
    ) -> np.ndarray:
        """Analyze frequency content over time.

        Args:
            audio_data: Tuple of (sample_rate, audio_data)
            n_bands: Number of frequency bands
            hop_length: Number of samples between frames

        Returns:
            Array of shape (n_bands, n_frames) with band energies over time
        """
        sr, y = audio_data

        try:
            import librosa
        except ImportError:
            raise ImportError("librosa is required for audio analysis")

        # Compute STFT
        S = librosa.stft(y, hop_length=hop_length)
        magnitude = np.abs(S)

        # Compute energy in each frequency band over time
        n_fft = magnitude.shape[0]
        band_size = n_fft // n_bands
        n_frames = magnitude.shape[1]
        bands_over_time = np.zeros((n_bands, n_frames))

        for i in range(n_bands):
            start_idx = i * band_size
            end_idx = (i + 1) * band_size if i < n_bands - 1 else n_fft
            bands_over_time[i] = np.mean(magnitude[start_idx:end_idx], axis=0)

        # Normalize to 0-1 range
        bands_over_time = (bands_over_time - bands_over_time.min()) / (
            bands_over_time.max() - bands_over_time.min() + 1e-6
        )
        return bands_over_time

    def create_equalizer_bars(
        self,
        bands: np.ndarray,
        width: int = 1920,
        height: int = 1080,
        bar_width: int = 100,
        color: Tuple[int, int, int] = (0, 255, 0),
    ) -> List[Dict]:
        """Create equalizer bar visualization.

        Args:
            bands: Array of band energies
            width: Canvas width
            height: Canvas height
            bar_width: Width of each bar
            color: Bar color (R, G, B)

        Returns:
            List of bar dictionaries
        """
        n_bands = len(bands)
        bars = []

        # Calculate bar positioning
        total_bar_width = n_bands * bar_width
        start_x = (width - total_bar_width) / 2
        bar_height = height * 0.6  # Max bar height

        for i, energy in enumerate(bands):
            x = start_x + i * bar_width
            bar_len = energy * bar_height
            y = height - bar_len

            bar = {
                "type": "equalizer_bar",
                "x": x,
                "y": y,
                "width": bar_width * 0.8,  # Leave gap between bars
                "height": bar_len,
                "color": color,
                "energy": energy,
            }
            bars.append(bar)

        return bars

    def create_spectral_circle(
        self,
        bands: np.ndarray,
        center_x: int,
        center_y: int,
        base_radius: int = 100,
    ) -> List[Dict]:
        """Create a circular spectral visualization.

        Args:
            bands: Array of band energies
            center_x: Circle center X
            center_y: Circle center Y
            base_radius: Base radius of the circle

        Returns:
            List of segment dictionaries
        """
        n_bands = len(bands)
        segments = []

        angle_step = (2 * np.pi) / n_bands

        for i, energy in enumerate(bands):
            angle = i * angle_step
            radius = base_radius + (energy * 50)  # Pulsate based on energy

            x = center_x + radius * np.cos(angle)
            y = center_y + radius * np.sin(angle)

            segment = {
                "type": "spectral_segment",
                "x": x,
                "y": y,
                "radius": radius,
                "angle": angle,
                "energy": energy,
            }
            segments.append(segment)

        return segments

    def create_frequency_waveform(
        self, bands_over_time: np.ndarray, width: int = 1920, height: int = 1080
    ) -> List[Dict]:
        """Create a waveform visualization based on frequency content.

        Args:
            bands_over_time: Array of shape (n_bands, n_frames)
            width: Canvas width
            height: Canvas height

        Returns:
            List of waveform point dictionaries
        """
        n_bands, n_frames = bands_over_time.shape
        waveform = []

        # Use the first frequency band (lowest frequencies) for waveform
        base_band = bands_over_time[0]

        for frame_idx in range(n_frames):
            x = (frame_idx / n_frames) * width
            amplitude = base_band[frame_idx]
            y = height / 2 + (amplitude - 0.5) * height

            point = {"x": x, "y": y, "frame": frame_idx, "amplitude": amplitude}
            waveform.append(point)

        return waveform

    def detect_bass_drops(
        self, bands_over_time: np.ndarray, threshold: float = 0.8
    ) -> List[int]:
        """Detect bass drops in the audio.

        Args:
            bands_over_time: Array of shape (n_bands, n_frames)
            threshold: Energy threshold for drop detection (0-1)

        Returns:
            List of frame indices with bass drops
        """
        # Analyze the lowest frequency band
        bass_band = bands_over_time[0]

        drops = []
        for i in range(1, len(bass_band)):
            # Detect sudden increase in bass energy
            if bass_band[i] > threshold and bass_band[i - 1] < threshold * 0.5:
                drops.append(i)

        return drops
