"""Advanced color effects and generation module."""

import numpy as np
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
import colorsys


@dataclass
class ColorPalette:
    """Represents a color palette for mood-based styling."""
    name: str
    colors: List[Tuple[int, int, int]]
    description: str


class ColorEffectGenerator:
    """Generates advanced color effects and palettes."""

    def __init__(self):
        """Initialize the color effect generator."""
        self.palettes = self._initialize_palettes()

    def _initialize_palettes(self) -> Dict[str, ColorPalette]:
        """Initialize color palettes for different moods.

        Returns:
            Dictionary of ColorPalette objects
        """
        return {
            "calm": ColorPalette(
                name="calm",
                colors=[
                    (135, 206, 235),  # Sky blue
                    (173, 216, 230),  # Light blue
                    (224, 255, 255),  # Light cyan
                    (176, 224, 230),  # Powder blue
                    (127, 255, 212),  # Aquamarine
                ],
                description="Cool, relaxing blues and cyans",
            ),
            "energetic": ColorPalette(
                name="energetic",
                colors=[
                    (255, 0, 0),  # Red
                    (255, 69, 0),  # Red-orange
                    (255, 140, 0),  # Dark orange
                    (255, 215, 0),  # Gold
                    (255, 20, 147),  # Deep pink
                ],
                description="Hot, vibrant reds, oranges, and yellows",
            ),
            "upbeat": ColorPalette(
                name="upbeat",
                colors=[
                    (255, 215, 0),  # Gold
                    (255, 165, 0),  # Orange
                    (50, 205, 50),  # Lime green
                    (0, 206, 209),  # Turquoise
                    (138, 43, 226),  # Blue violet
                ],
                description="Bright, diverse, playful colors",
            ),
            "melancholic": ColorPalette(
                name="melancholic",
                colors=[
                    (75, 0, 130),  # Indigo
                    (72, 61, 139),  # Dark slate blue
                    (47, 79, 79),  # Dark slate gray
                    (105, 105, 105),  # Dim gray
                    (128, 0, 128),  # Purple
                ],
                description="Deep, emotional dark tones",
            ),
            "tropical": ColorPalette(
                name="tropical",
                colors=[
                    (255, 20, 147),  # Deep pink
                    (0, 255, 255),  # Cyan
                    (34, 139, 34),  # Forest green
                    (255, 215, 0),  # Gold
                    (220, 20, 60),  # Crimson
                ],
                description="Vibrant tropical colors",
            ),
            "sunset": ColorPalette(
                name="sunset",
                colors=[
                    (255, 94, 77),  # Coral
                    (255, 152, 0),  # Amber
                    (255, 87, 34),  # Deep orange
                    (233, 30, 99),  # Pink
                    (156, 39, 176),  # Purple
                ],
                description="Warm sunset gradient colors",
            ),
        }

    def get_palette(self, mood: str) -> Optional[ColorPalette]:
        """Get a color palette for a mood.

        Args:
            mood: Mood name

        Returns:
            ColorPalette or None if not found
        """
        return self.palettes.get(mood.lower())

    def generate_gradient(
        self, color1: Tuple[int, int, int], color2: Tuple[int, int, int], steps: int = 10
    ) -> List[Tuple[int, int, int]]:
        """Generate a color gradient between two colors.

        Args:
            color1: Start color (R, G, B)
            color2: End color (R, G, B)
            steps: Number of steps in the gradient

        Returns:
            List of colors forming a gradient
        """
        gradient = []
        for i in range(steps):
            ratio = i / (steps - 1) if steps > 1 else 0
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            gradient.append((r, g, b))

        return gradient

    def generate_rainbow_gradient(self, steps: int = 10) -> List[Tuple[int, int, int]]:
        """Generate a rainbow gradient.

        Args:
            steps: Number of steps in the gradient

        Returns:
            List of rainbow colors
        """
        colors = []
        for i in range(steps):
            hue = i / steps
            saturation = 1.0
            value = 1.0
            r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
            colors.append((int(r * 255), int(g * 255), int(b * 255)))

        return colors

    def generate_analogous_colors(
        self, base_color: Tuple[int, int, int], count: int = 3
    ) -> List[Tuple[int, int, int]]:
        """Generate analogous colors (adjacent on color wheel).

        Args:
            base_color: Base color (R, G, B)
            count: Number of analogous colors to generate

        Returns:
            List of analogous colors
        """
        r, g, b = base_color
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)

        analogous = []
        angle_step = 30 / 360  # 30 degrees in HSV

        for i in range(-count // 2, count // 2 + 1):
            new_h = (h + i * angle_step) % 1.0
            r_new, g_new, b_new = colorsys.hsv_to_rgb(new_h, s, v)
            analogous.append((int(r_new * 255), int(g_new * 255), int(b_new * 255)))

        return analogous

    def generate_complementary_color(
        self, color: Tuple[int, int, int]
    ) -> Tuple[int, int, int]:
        """Generate the complementary color.

        Args:
            color: Color (R, G, B)

        Returns:
            Complementary color
        """
        r, g, b = color
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        h = (h + 0.5) % 1.0  # Opposite on color wheel
        r_new, g_new, b_new = colorsys.hsv_to_rgb(h, s, v)
        return (int(r_new * 255), int(g_new * 255), int(b_new * 255))

    def generate_triadic_colors(
        self, base_color: Tuple[int, int, int]
    ) -> List[Tuple[int, int, int]]:
        """Generate triadic colors (equally spaced on color wheel).

        Args:
            base_color: Base color (R, G, B)

        Returns:
            List of 3 triadic colors
        """
        r, g, b = base_color
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)

        triadic = []
        for i in range(3):
            new_h = (h + i * (1 / 3)) % 1.0
            r_new, g_new, b_new = colorsys.hsv_to_rgb(new_h, s, v)
            triadic.append((int(r_new * 255), int(g_new * 255), int(b_new * 255)))

        return triadic

    def shift_brightness(
        self, color: Tuple[int, int, int], factor: float
    ) -> Tuple[int, int, int]:
        """Shift the brightness of a color.

        Args:
            color: Color (R, G, B)
            factor: Brightness factor (1.0 = no change, 0.5 = darker, 2.0 = brighter)

        Returns:
            Adjusted color
        """
        r, g, b = color
        r = int(min(255, max(0, r * factor)))
        g = int(min(255, max(0, g * factor)))
        b = int(min(255, max(0, b * factor)))
        return (r, g, b)

    def shift_saturation(
        self, color: Tuple[int, int, int], factor: float
    ) -> Tuple[int, int, int]:
        """Shift the saturation of a color.

        Args:
            color: Color (R, G, B)
            factor: Saturation factor (1.0 = no change, 0.0 = grayscale)

        Returns:
            Adjusted color
        """
        r, g, b = color
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        s = max(0, min(1.0, s * factor))
        r_new, g_new, b_new = colorsys.hsv_to_rgb(h, s, v)
        return (int(r_new * 255), int(g_new * 255), int(b_new * 255))

    def get_contrasting_text_color(
        self, background_color: Tuple[int, int, int]
    ) -> Tuple[int, int, int]:
        """Get black or white text color for best contrast.

        Args:
            background_color: Background color (R, G, B)

        Returns:
            Black (0, 0, 0) or White (255, 255, 255)
        """
        # Calculate luminance
        r, g, b = background_color
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        return (255, 255, 255) if luminance < 0.5 else (0, 0, 0)

    def generate_color_animation(
        self, start_color: Tuple[int, int, int], end_color: Tuple[int, int, int],
        duration: float, fps: int = 30
    ) -> List[Dict]:
        """Generate a color animation from start to end color.

        Args:
            start_color: Starting color
            end_color: Ending color
            duration: Animation duration in seconds
            fps: Frames per second

        Returns:
            List of animation keyframes
        """
        total_frames = int(duration * fps)
        animation = []

        for frame_idx in range(total_frames):
            ratio = frame_idx / total_frames if total_frames > 0 else 0
            r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
            g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
            b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)

            keyframe = {
                "frame": frame_idx,
                "time": frame_idx / fps,
                "color": (r, g, b),
                "progress": ratio,
            }
            animation.append(keyframe)

        return animation
