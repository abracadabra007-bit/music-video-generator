"""Animation generation module."""

from typing import List, Tuple, Dict, Optional
import numpy as np


class Animator:
    """Creates animations and transitions."""

    def __init__(self):
        """Initialize the animator."""
        self.animation_types = [
            "fade",
            "slide",
            "zoom",
            "pan",
            "rotate",
            "pulse",
            "drift",
            "shake",
        ]

    def create_animations(
        self,
        visual_assets: List[Dict],
        timed_lyrics: List[Tuple[str, float, float]],
        tempo: float,
        mood: str,
    ) -> List[Dict]:
        """Create animations for visual assets.

        Args:
            visual_assets: List of visual asset dictionaries
            timed_lyrics: List of (text, start_time, end_time) tuples
            tempo: Song tempo in BPM
            mood: Song mood

        Returns:
            List of animation dictionaries
        """
        animations = []

        # Create animations for each visual asset
        for i, asset in enumerate(visual_assets):
            animation = {
                "asset_index": i,
                "type": self._select_animation_type(mood, i),
                "duration": self._calculate_duration(tempo),
                "start_time": float(i * self._calculate_duration(tempo)),
                "easing": self._select_easing(mood),
            }
            animations.append(animation)

        # Add text animations for lyrics
        text_animations = self._create_text_animations(timed_lyrics, mood)
        animations.extend(text_animations)

        return animations

    def _select_animation_type(self, mood: str, frame_index: int) -> str:
        """Select an appropriate animation type for the mood.

        Args:
            mood: Song mood
            frame_index: Index of the frame

        Returns:
            Animation type string
        """
        mood_animations = {
            "calm": ["fade", "drift", "slow_zoom"],
            "melancholic": ["fade", "drift", "slow_pan"],
            "moderate": ["fade", "pan", "zoom"],
            "upbeat": ["slide", "zoom", "pulse"],
            "energetic": ["shake", "zoom", "spin"],
            "balanced": ["fade", "pan", "zoom"],
        }

        animations = mood_animations.get(mood, mood_animations["balanced"])
        return animations[frame_index % len(animations)]

    def _calculate_duration(self, tempo: float) -> float:
        """Calculate animation duration based on tempo.

        Args:
            tempo: Song tempo in BPM

        Returns:
            Duration in seconds
        """
        # Faster songs get shorter animations
        if tempo > 140:
            return 0.5
        elif tempo > 100:
            return 1.0
        else:
            return 2.0

    def _select_easing(self, mood: str) -> str:
        """Select an easing function based on mood.

        Args:
            mood: Song mood

        Returns:
            Easing function name
        """
        mood_easing = {
            "calm": "ease-in-out",
            "melancholic": "ease-in",
            "moderate": "linear",
            "upbeat": "ease-out",
            "energetic": "ease-out",
            "balanced": "ease-in-out",
        }
        return mood_easing.get(mood, "ease-in-out")

    def _create_text_animations(
        self, timed_lyrics: List[Tuple[str, float, float]], mood: str
    ) -> List[Dict]:
        """Create animations for text display.

        Args:
            timed_lyrics: List of (text, start_time, end_time) tuples
            mood: Song mood

        Returns:
            List of text animation dictionaries
        """
        animations = []

        for text, start_time, end_time in timed_lyrics:
            animation = {
                "type": "text",
                "text": text,
                "start_time": start_time,
                "end_time": end_time,
                "animation": self._select_text_animation(mood),
                "position": "center",
            }
            animations.append(animation)

        return animations

    def _select_text_animation(self, mood: str) -> str:
        """Select text animation based on mood.

        Args:
            mood: Song mood

        Returns:
            Text animation type
        """
        mood_text_animations = {
            "calm": "fade_in_out",
            "melancholic": "fade_in_out",
            "moderate": "slide_up",
            "upbeat": "pop",
            "energetic": "bounce",
            "balanced": "fade_in_out",
        }
        return mood_text_animations.get(mood, "fade_in_out")
