"""Audio processing module for extracting musical features."""

import numpy as np
import librosa
from typing import Tuple, List, Optional


class AudioProcessor:
    """Handles audio loading and analysis."""

    def __init__(self, sr: int = 22050):
        """Initialize the audio processor.

        Args:
            sr: Sample rate for audio processing (default: 22050 Hz)
        """
        self.sr = sr

    def load_audio(self, audio_path: str) -> Tuple[int, np.ndarray]:
        """Load an audio file.

        Args:
            audio_path: Path to the audio file

        Returns:
            Tuple of (sample_rate, audio_data)
        """
        y, sr = librosa.load(audio_path, sr=self.sr)
        return sr, y

    def extract_tempo_and_beats(
        self, audio_data: Tuple[int, np.ndarray]
    ) -> Tuple[float, np.ndarray]:
        """Extract tempo and beat times from audio.

        Args:
            audio_data: Tuple of (sample_rate, audio_data)

        Returns:
            Tuple of (tempo in BPM, beat times in seconds)
        """
        sr, y = audio_data
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
        beat_times = librosa.frames_to_time(beats, sr=sr)
        return float(tempo), beat_times

    def analyze_energy(self, audio_data: Tuple[int, np.ndarray]) -> float:
        """Analyze the overall energy of the audio.

        Args:
            audio_data: Tuple of (sample_rate, audio_data)

        Returns:
            Energy value between 0 and 1
        """
        sr, y = audio_data
        # Calculate RMS energy
        S = librosa.feature.melspectrogram(y=y, sr=sr)
        energy = librosa.feature.rms(S=S)[0]
        return float(np.mean(energy))

    def extract_spectral_features(
        self, audio_data: Tuple[int, np.ndarray]
    ) -> dict:
        """Extract spectral features from audio.

        Args:
            audio_data: Tuple of (sample_rate, audio_data)

        Returns:
            Dictionary with spectral features
        """
        sr, y = audio_data
        features = {}

        # Spectral centroid
        features["spectral_centroid"] = np.mean(
            librosa.feature.spectral_centroid(y=y, sr=sr)
        )

        # Mel-frequency cepstral coefficients
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        features["mfcc_mean"] = np.mean(mfcc, axis=1)

        # Zero crossing rate
        features["zero_crossing_rate"] = np.mean(librosa.feature.zero_crossing_rate(y)[0])

        return features

    def get_duration(self, audio_data: Tuple[int, np.ndarray]) -> float:
        """Get the duration of the audio in seconds.

        Args:
            audio_data: Tuple of (sample_rate, audio_data)

        Returns:
            Duration in seconds
        """
        sr, y = audio_data
        return float(len(y) / sr)
