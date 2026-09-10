"""Advanced keyframe animation system."""

import numpy as np
from typing import List, Dict, Callable, Optional, Tuple
from dataclasses import dataclass


@dataclass
class Keyframe:
    """Represents a single keyframe in an animation."""

    time: float
    value: float
    easing: str = "linear"


class EasingFunctions:
    """Collection of easing functions for smooth animations."""

    @staticmethod
    def linear(t: float) -> float:
        """Linear easing."""
        return t

    @staticmethod
    def ease_in_quad(t: float) -> float:
        """Quadratic ease-in."""
        return t * t

    @staticmethod
    def ease_out_quad(t: float) -> float:
        """Quadratic ease-out."""
        return 1 - (1 - t) ** 2

    @staticmethod
    def ease_in_out_quad(t: float) -> float:
        """Quadratic ease-in-out."""
        return 2 * t * t if t < 0.5 else -1 + (4 - 2 * t) * t

    @staticmethod
    def ease_in_cubic(t: float) -> float:
        """Cubic ease-in."""
        return t * t * t

    @staticmethod
    def ease_out_cubic(t: float) -> float:
        """Cubic ease-out."""
        return 1 - (1 - t) ** 3

    @staticmethod
    def ease_in_out_cubic(t: float) -> float:
        """Cubic ease-in-out."""
        return 4 * t * t * t if t < 0.5 else 1 - (-2 * t + 2) ** 3 / 2

    @staticmethod
    def ease_in_sine(t: float) -> float:
        """Sine ease-in."""
        return 1 - np.cos((t * np.pi) / 2)

    @staticmethod
    def ease_out_sine(t: float) -> float:
        """Sine ease-out."""
        return np.sin((t * np.pi) / 2)

    @staticmethod
    def ease_in_out_sine(t: float) -> float:
        """Sine ease-in-out."""
        return -(np.cos(np.pi * t) - 1) / 2

    @staticmethod
    def ease_in_expo(t: float) -> float:
        """Exponential ease-in."""
        return 0 if t == 0 else (2 ** (10 * t - 10))

    @staticmethod
    def ease_out_expo(t: float) -> float:
        """Exponential ease-out."""
        return 1 if t == 1 else (1 - 2 ** (-10 * t))

    @staticmethod
    def ease_in_out_expo(t: float) -> float:
        """Exponential ease-in-out."""
        if t == 0:
            return 0
        elif t == 1:
            return 1
        elif t < 0.5:
            return (2 ** (20 * t - 10)) / 2
        else:
            return (2 - 2 ** (-20 * t + 10)) / 2

    @staticmethod
    def ease_out_bounce(t: float) -> float:
        """Bounce ease-out."""
        n1, d1 = 7.5625, 2.75
        if t < 1 / d1:
            return n1 * t * t
        elif t < 2 / d1:
            t -= 1.5 / d1
            return n1 * t * t + 0.75
        elif t < 2.5 / d1:
            t -= 2.25 / d1
            return n1 * t * t + 0.9375
        else:
            t -= 2.625 / d1
            return n1 * t * t + 0.984375

    @classmethod
    def get_function(cls, name: str) -> Callable[[float], float]:
        """Get an easing function by name.

        Args:
            name: Easing function name

        Returns:
            Callable easing function
        """
        easing_map = {
            "linear": cls.linear,
            "ease-in-quad": cls.ease_in_quad,
            "ease-out-quad": cls.ease_out_quad,
            "ease-in-out-quad": cls.ease_in_out_quad,
            "ease-in-cubic": cls.ease_in_cubic,
            "ease-out-cubic": cls.ease_out_cubic,
            "ease-in-out-cubic": cls.ease_in_out_cubic,
            "ease-in-sine": cls.ease_in_sine,
            "ease-out-sine": cls.ease_out_sine,
            "ease-in-out-sine": cls.ease_in_out_sine,
            "ease-in-expo": cls.ease_in_expo,
            "ease-out-expo": cls.ease_out_expo,
            "ease-in-out-expo": cls.ease_in_out_expo,
            "ease-out-bounce": cls.ease_out_bounce,
        }
        return easing_map.get(name.lower(), cls.linear)


class KeyframeAnimation:
    """Manages keyframe-based animations."""

    def __init__(self, duration: float, fps: int = 30):
        """Initialize keyframe animation.

        Args:
            duration: Total animation duration in seconds
            fps: Frames per second
        """
        self.duration = duration
        self.fps = fps
        self.keyframes: List[Keyframe] = []

    def add_keyframe(self, time: float, value: float, easing: str = "linear") -> None:
        """Add a keyframe to the animation.

        Args:
            time: Time of the keyframe in seconds
            value: Value at this keyframe (0-1 normalized)
            easing: Easing function to use until next keyframe
        """
        keyframe = Keyframe(time=time, value=value, easing=easing)
        self.keyframes.append(keyframe)
        self.keyframes.sort(key=lambda k: k.time)

    def get_value_at_time(self, current_time: float) -> float:
        """Get the interpolated value at a specific time.

        Args:
            current_time: Time in seconds

        Returns:
            Interpolated value (0-1)
        """
        if not self.keyframes:
            return 0.0

        # Clamp time within duration
        current_time = max(0, min(current_time, self.duration))

        # Find surrounding keyframes
        prev_keyframe = None
        next_keyframe = None

        for i, keyframe in enumerate(self.keyframes):
            if keyframe.time <= current_time:
                prev_keyframe = keyframe
            if keyframe.time > current_time and next_keyframe is None:
                next_keyframe = keyframe
                break

        # Handle edge cases
        if prev_keyframe is None:
            return self.keyframes[0].value if self.keyframes else 0.0
        if next_keyframe is None:
            return prev_keyframe.value

        # Interpolate between keyframes
        time_diff = next_keyframe.time - prev_keyframe.time
        if time_diff == 0:
            return prev_keyframe.value

        t = (current_time - prev_keyframe.time) / time_diff
        easing_func = EasingFunctions.get_function(prev_keyframe.easing)
        eased_t = easing_func(t)

        interpolated = prev_keyframe.value + (
            next_keyframe.value - prev_keyframe.value
        ) * eased_t

        return interpolated

    def get_animation_data(self) -> List[Dict]:
        """Get animation data for all frames.

        Returns:
            List of frame data dictionaries
        """
        total_frames = int(self.duration * self.fps)
        animation_data = []

        for frame_idx in range(total_frames):
            current_time = frame_idx / self.fps
            value = self.get_value_at_time(current_time)

            frame_data = {
                "frame": frame_idx,
                "time": current_time,
                "value": value,
            }
            animation_data.append(frame_data)

        return animation_data

    def create_scale_animation(
        self, start_scale: float = 1.0, end_scale: float = 1.2
    ) -> List[Dict]:
        """Create a scale animation.

        Args:
            start_scale: Starting scale factor
            end_scale: Ending scale factor

        Returns:
            List of animation frames
        """
        self.add_keyframe(0, start_scale, "ease-out-cubic")
        self.add_keyframe(self.duration, end_scale, "linear")

        animation = self.get_animation_data()

        for frame in animation:
            frame["scale"] = start_scale + (end_scale - start_scale) * frame["value"]

        return animation

    def create_rotation_animation(
        self, start_rotation: float = 0.0, end_rotation: float = 360.0
    ) -> List[Dict]:
        """Create a rotation animation.

        Args:
            start_rotation: Starting rotation in degrees
            end_rotation: Ending rotation in degrees

        Returns:
            List of animation frames
        """
        self.add_keyframe(0, 0, "linear")
        self.add_keyframe(self.duration, 1, "linear")

        animation = self.get_animation_data()

        for frame in animation:
            frame["rotation"] = start_rotation + (
                end_rotation - start_rotation
            ) * frame["value"]

        return animation

    def create_opacity_animation(
        self, start_opacity: float = 1.0, end_opacity: float = 0.0
    ) -> List[Dict]:
        """Create an opacity (fade) animation.

        Args:
            start_opacity: Starting opacity (0-1)
            end_opacity: Ending opacity (0-1)

        Returns:
            List of animation frames
        """
        self.add_keyframe(0, start_opacity, "ease-in-out-cubic")
        self.add_keyframe(self.duration, end_opacity, "ease-in-out-cubic")

        animation = self.get_animation_data()

        for frame in animation:
            frame["opacity"] = start_opacity + (
                end_opacity - start_opacity
            ) * frame["value"]

        return animation
