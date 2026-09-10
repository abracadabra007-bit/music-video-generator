"""Advanced beat synchronization module."""

import numpy as np
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class BeatEvent:
    """Represents a beat event in time."""
    time: float
    strength: float  # 0-1, how strong the beat is
    is_downbeat: bool  # True for main beats


class BeatSynchronizer:
    """Synchronizes visual effects with audio beats."""

    def __init__(self):
        """Initialize the beat synchronizer."""
        self.beat_events: List[BeatEvent] = []

    def analyze_beats(
        self, audio_data: Tuple[int, np.ndarray], beats: np.ndarray
    ) -> List[BeatEvent]:
        """Analyze beats and create synchronized events.

        Args:
            audio_data: Tuple of (sample_rate, audio_data)
            beats: Array of beat times in seconds

        Returns:
            List of BeatEvent objects
        """
        sr, y = audio_data
        beat_events = []

        for i, beat_time in enumerate(beats):
            # Convert time to sample index
            sample_idx = int(beat_time * sr)
            if sample_idx >= len(y):
                break

            # Calculate beat strength based on local energy
            window_size = sr // 10  # 100ms window
            start_idx = max(0, sample_idx - window_size // 2)
            end_idx = min(len(y), sample_idx + window_size // 2)

            if start_idx < end_idx:
                beat_energy = np.mean(np.abs(y[start_idx:end_idx]))
                # Normalize to 0-1 range
                strength = min(1.0, beat_energy * 2)
            else:
                strength = 0.5

            # Every 4th beat is typically a downbeat
            is_downbeat = (i % 4) == 0

            beat_event = BeatEvent(
                time=float(beat_time), strength=strength, is_downbeat=is_downbeat
            )
            beat_events.append(beat_event)

        self.beat_events = beat_events
        return beat_events

    def get_beat_at_time(self, current_time: float) -> Tuple[bool, float]:
        """Check if there's a beat at the current time.

        Args:
            current_time: Current time in seconds

        Returns:
            Tuple of (is_beat_time, beat_strength)
        """
        beat_threshold = 0.1  # 100ms window

        for event in self.beat_events:
            if abs(event.time - current_time) < beat_threshold:
                return True, event.strength

        return False, 0.0

    def get_beat_intensity_at_time(self, current_time: float) -> float:
        """Get the intensity of the beat at current time.

        Args:
            current_time: Current time in seconds

        Returns:
            Intensity value 0-1
        """
        decay_rate = 5.0  # How fast the beat fades
        max_intensity = 0.0

        for event in self.beat_events:
            time_diff = current_time - event.time
            if 0 <= time_diff < 0.5:  # Decay over 500ms
                intensity = event.strength * np.exp(-decay_rate * time_diff)
                max_intensity = max(max_intensity, intensity)

        return max_intensity

    def generate_beat_keyframes(
        self, duration: float, fps: int = 30
    ) -> List[Dict]:
        """Generate keyframes synchronized with beats.

        Args:
            duration: Video duration in seconds
            fps: Frames per second

        Returns:
            List of keyframe dictionaries
        """
        keyframes = []
        total_frames = int(duration * fps)
        frame_duration = 1.0 / fps

        for frame_idx in range(total_frames):
            current_time = frame_idx * frame_duration
            intensity = self.get_beat_intensity_at_time(current_time)
            is_beat, strength = self.get_beat_at_time(current_time)

            keyframe = {
                "frame": frame_idx,
                "time": current_time,
                "is_beat": is_beat,
                "beat_strength": strength,
                "intensity": intensity,
                "scale": 1.0 + (intensity * 0.2),  # 0% to 20% scale increase
                "opacity": 0.7 + (intensity * 0.3),  # 70% to 100% opacity
            }
            keyframes.append(keyframe)

        return keyframes

    def create_beat_pulse_animation(
        self, duration: float, fps: int = 30
    ) -> List[Dict]:
        """Create a pulsing animation synchronized with beats.

        Args:
            duration: Video duration in seconds
            fps: Frames per second

        Returns:
            List of animation dictionaries
        """
        keyframes = self.generate_beat_keyframes(duration, fps)
        animations = []

        for keyframe in keyframes:
            if keyframe["is_beat"]:
                animation = {
                    "type": "pulse",
                    "frame": keyframe["frame"],
                    "time": keyframe["time"],
                    "duration": 0.3,
                    "scale_from": 1.0,
                    "scale_to": 1.0 + (keyframe["beat_strength"] * 0.3),
                    "easing": "ease-out-cubic",
                }
                animations.append(animation)

        return animations

    def create_beat_strobe_effect(
        self, duration: float, fps: int = 30
    ) -> List[Dict]:
        """Create a strobe effect synchronized with beats.

        Args:
            duration: Video duration in seconds
            fps: Frames per second

        Returns:
            List of strobe effect dictionaries
        """
        keyframes = self.generate_beat_keyframes(duration, fps)
        effects = []

        for keyframe in keyframes:
            if keyframe["is_beat"]:
                effect = {
                    "type": "strobe",
                    "frame": keyframe["frame"],
                    "time": keyframe["time"],
                    "flash_duration": 0.05,
                    "intensity": keyframe["beat_strength"],
                    "color": (255, 255, 255),  # White flash
                }
                effects.append(effect)

        return effects
