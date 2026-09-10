"""Video rendering module for composing all elements into a final video."""

from typing import List, Tuple, Optional
from pathlib import Path


class VideoRenderer:
    """Renders the final video from all components."""

    def __init__(self, fps: int = 30, resolution: Tuple[int, int] = (1920, 1080)):
        """Initialize the video renderer.

        Args:
            fps: Frames per second for output video
            resolution: (width, height) in pixels
        """
        self.fps = fps
        self.resolution = resolution
        self.width, self.height = resolution

    def render(
        self,
        audio_path: str,
        animations: List[dict],
        timed_lyrics: List[Tuple[str, float, float]],
        output_path: str,
    ) -> str:
        """Render the final video.

        Args:
            audio_path: Path to the audio file
            animations: List of animation dictionaries
            timed_lyrics: List of timed lyrics
            output_path: Path where to save the output video

        Returns:
            Path to the rendered video file
        """
        try:
            from moviepy.editor import (
                AudioFileClip,
                VideoClip,
                CompositeVideoClip,
                TextClip,
                ColorClip,
            )
        except ImportError:
            raise ImportError(
                "MoviePy is required for video rendering. "
                "Install it with: pip install moviepy"
            )

        print(f"Starting video render to: {output_path}")
        print(f"Resolution: {self.width}x{self.height} @ {self.fps} FPS")

        # Load audio
        audio_clip = AudioFileClip(audio_path)
        duration = audio_clip.duration

        # Create base video with background color
        background = ColorClip(size=self.resolution, color=(0, 0, 0))
        base_video = background.set_duration(duration)

        # Create text clips for lyrics
        text_clips = []
        for text, start_time, end_time in timed_lyrics:
            try:
                txt_clip = TextClip(
                    text,
                    fontsize=70,
                    color="white",
                    font="Arial",
                    method="caption",
                    size=(self.width - 100, None),
                ).set_position("center").set_start(start_time).set_end(end_time)
                text_clips.append(txt_clip)
            except Exception as e:
                print(f"Warning: Could not create text clip for '{text}': {e}")
                continue

        # Compose video
        clips_to_compose = [base_video] + text_clips
        final_video = CompositeVideoClip(clips_to_compose, size=self.resolution)
        final_video = final_video.set_audio(audio_clip)

        # Write to file
        output_path = str(output_path)
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        print("Rendering video (this may take a while)...")
        final_video.write_videofile(
            output_path,
            fps=self.fps,
            codec="libx264",
            audio_codec="aac",
            verbose=False,
            logger=None,
        )

        print(f"Video rendering complete: {output_path}")
        return output_path
