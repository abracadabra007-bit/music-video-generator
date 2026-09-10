"""Mood analysis module to determine the emotional tone of a song."""

from typing import Tuple
import numpy as np


class MoodAnalyzer:
    """Analyzes audio features to determine song mood."""

    def detect_mood(self, tempo: float, energy: float, audio_data: Tuple) -> str:
        """Detect the mood of a song based on its features.

        Args:
            tempo: Tempo in BPM
            energy: Energy level (0-1)
            audio_data: Tuple of (sample_rate, audio_data)

        Returns:
            Mood string (e.g., 'upbeat', 'melancholic', 'calm', 'energetic')
        """
        # Simple mood detection based on tempo and energy
        if tempo < 80 and energy < 0.4:
            return "calm"
        elif tempo < 100 and energy < 0.5:
            return "melancholic"
        elif tempo >= 100 and tempo < 140 and energy < 0.6:
            return "moderate"
        elif tempo >= 140 or energy >= 0.7:
            return "energetic"
        elif 100 <= tempo < 140 and 0.5 <= energy < 0.7:
            return "upbeat"
        else:
            return "balanced"

    def get_mood_characteristics(self, mood: str) -> dict:
        """Get visual and animation characteristics for a mood.

        Args:
            mood: Mood string

        Returns:
            Dictionary with mood characteristics
        """
        mood_profiles = {
            "calm": {
                "primary_colors": ["#87CEEB", "#E0FFFF", "#F0FFFF"],
                "animation_speed": 0.5,
                "transition_duration": 2.0,
                "effects": ["fade", "slow_zoom"],
            },
            "melancholic": {
                "primary_colors": ["#4B0082", "#2F4F4F", "#191970"],
                "animation_speed": 0.6,
                "transition_duration": 1.5,
                "effects": ["fade", "drift"],
            },
            "moderate": {
                "primary_colors": ["#FFB6C1", "#DDA0DD", "#F08080"],
                "animation_speed": 1.0,
                "transition_duration": 1.0,
                "effects": ["fade", "pan"],
            },
            "upbeat": {
                "primary_colors": ["#FFD700", "#FFA500", "#FF6347"],
                "animation_speed": 1.2,
                "transition_duration": 0.8,
                "effects": ["zoom", "slide", "pulse"],
            },
            "energetic": {
                "primary_colors": ["#FF0000", "#FF1493", "#FFD700"],
                "animation_speed": 1.5,
                "transition_duration": 0.5,
                "effects": ["shake", "zoom", "spin"],
            },
            "balanced": {
                "primary_colors": ["#00CED1", "#20B2AA", "#3CB371"],
                "animation_speed": 1.0,
                "transition_duration": 1.0,
                "effects": ["fade", "pan", "zoom"],
            },
        }

        return mood_profiles.get(mood, mood_profiles["balanced"])
