"""Visual asset generation module."""

from typing import List, Optional, Dict
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import os


class VisualGenerator:
    """Generates visual assets for the video."""

    def __init__(self, width: int = 1920, height: int = 1080):
        """Initialize the visual generator.

        Args:
            width: Video width in pixels
            height: Video height in pixels
        """
        self.width = width
        self.height = height

    def generate_assets(
        self,
        mood: str,
        audio_length: int,
        beats: np.ndarray,
        images_path: Optional[str] = None,
    ) -> List[Dict]:
        """Generate visual assets for the video.

        Args:
            mood: Mood of the song
            audio_length: Total audio samples
            beats: Beat times
            images_path: Optional path to custom images

        Returns:
            List of visual asset dictionaries
        """
        assets = []

        if images_path and os.path.exists(images_path):
            # Load custom images
            images = self.load_images(images_path)
            assets.extend(images)
        else:
            # Generate default visual backgrounds
            backgrounds = self.generate_backgrounds(mood, len(beats))
            assets.extend(backgrounds)

        return assets

    def generate_backgrounds(self, mood: str, num_frames: int) -> List[Dict]:
        """Generate background images based on mood.

        Args:
            mood: Mood of the song
            num_frames: Number of frames to generate

        Returns:
            List of background image dictionaries
        """
        mood_colors = {
            "calm": [(135, 206, 235), (224, 255, 255)],  # Light blue, cyan
            "melancholic": [(75, 0, 130), (47, 79, 79)],  # Indigo, dark slate
            "moderate": [(255, 182, 193), (221, 160, 221)],  # Light pink, plum
            "upbeat": [(255, 215, 0), (255, 165, 0)],  # Gold, orange
            "energetic": [(255, 0, 0), (255, 20, 147)],  # Red, deep pink
            "balanced": [(0, 206, 209), (32, 178, 170)],  # Turquoise, light sea green
        }

        colors = mood_colors.get(mood, mood_colors["balanced"])
        backgrounds = []

        for i in range(min(num_frames, 10)):  # Limit to 10 distinct backgrounds
            # Alternate between mood colors
            color = colors[i % len(colors)]
            bg = {
                "type": "background",
                "color": color,
                "frame_index": i,
                "duration": 1.0,  # Duration in seconds
            }
            backgrounds.append(bg)

        return backgrounds

    def load_images(self, images_path: str) -> List[Dict]:
        """Load images from a directory.

        Args:
            images_path: Path to directory containing images

        Returns:
            List of image dictionaries
        """
        images = []
        supported_formats = (".jpg", ".jpeg", ".png", ".gif", ".bmp")

        if not os.path.isdir(images_path):
            return images

        for filename in sorted(os.listdir(images_path)):
            if filename.lower().endswith(supported_formats):
                filepath = os.path.join(images_path, filename)
                img_dict = {
                    "type": "image",
                    "path": filepath,
                    "filename": filename,
                    "duration": 1.0,
                }
                images.append(img_dict)

        return images

    def create_solid_color_frame(
        self, color: tuple, width: Optional[int] = None, height: Optional[int] = None
    ) -> Image.Image:
        """Create a solid color frame.

        Args:
            color: RGB color tuple
            width: Frame width (defaults to self.width)
            height: Frame height (defaults to self.height)

        Returns:
            PIL Image object
        """
        w = width or self.width
        h = height or self.height
        return Image.new("RGB", (w, h), color)

    def add_text_overlay(
        self, image: Image.Image, text: str, position: tuple, color: tuple
    ) -> Image.Image:
        """Add text overlay to an image.

        Args:
            image: PIL Image object
            text: Text to add
            position: (x, y) position tuple
            color: RGB color tuple

        Returns:
            Modified PIL Image object
        """
        draw = ImageDraw.Draw(image)
        # Note: Using default font for simplicity
        draw.text(position, text, fill=color)
        return image
