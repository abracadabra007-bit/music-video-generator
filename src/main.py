"""Main entry point for the Music Video Generator."""

import os
from pathlib import Path
from typing import Optional

from src.audio_processor import AudioProcessor
from src.lyrics_parser import LyricsParser
from src.mood_analyzer import MoodAnalyzer
from src.visual_generator import VisualGenerator
from src.animator import Animator
from src.video_renderer import VideoRenderer
from config.defaults import DEFAULT_CONFIG


class MusicVideoGenerator:
    """Main class for generating music videos."""

    def __init__(self, config: Optional[dict] = None):
        """Initialize the Music Video Generator.

        Args:
            config: Optional configuration dictionary. Uses defaults if not provided.
        """
        self.config = {**DEFAULT_CONFIG, **(config or {})}
        self.audio_processor = AudioProcessor()
        self.lyrics_parser = LyricsParser()
        self.mood_analyzer = MoodAnalyzer()
        self.visual_generator = VisualGenerator()
        self.animator = Animator()
        self.video_renderer = VideoRenderer()

    def create_video(
        self,
        audio_path: str,
        lyrics_path: str,
        output_path: str,
        mood: Optional[str] = None,
        images_path: Optional[str] = None,
    ) -> str:
        """Generate a music video from audio and lyrics.

        Args:
            audio_path: Path to the audio file (MP3, WAV, etc.)
            lyrics_path: Path to the lyrics file (TXT format)
            output_path: Path where the output video will be saved
            mood: Optional mood specification (e.g., 'upbeat', 'melancholic')
            images_path: Optional path to directory containing images

        Returns:
            Path to the generated video file
        """
        print(f"Generating music video from: {audio_path}")

        # Step 1: Process audio
        print("Step 1: Processing audio...")
        audio_data = self.audio_processor.load_audio(audio_path)
        tempo, beats = self.audio_processor.extract_tempo_and_beats(audio_data)
        energy = self.audio_processor.analyze_energy(audio_data)
        print(f"  Tempo: {tempo} BPM, Energy: {energy:.2f}")

        # Step 2: Parse lyrics
        print("Step 2: Parsing lyrics...")
        lyrics = self.lyrics_parser.load_lyrics(lyrics_path)
        timed_lyrics = self.lyrics_parser.synchronize_lyrics(
            lyrics, len(audio_data[1]), audio_data[0]
        )
        print(f"  Loaded {len(lyrics)} lines of lyrics")

        # Step 3: Analyze mood
        print("Step 3: Analyzing mood...")
        detected_mood = mood or self.mood_analyzer.detect_mood(
            tempo, energy, audio_data
        )
        print(f"  Detected mood: {detected_mood}")

        # Step 4: Generate visuals
        print("Step 4: Generating visuals...")
        visual_assets = self.visual_generator.generate_assets(
            detected_mood, len(audio_data[1]), beats, images_path
        )
        print(f"  Generated {len(visual_assets)} visual frames")

        # Step 5: Create animations
        print("Step 5: Creating animations...")
        animations = self.animator.create_animations(
            visual_assets, timed_lyrics, tempo, detected_mood
        )
        print(f"  Created {len(animations)} animation sequences")

        # Step 6: Render video
        print("Step 6: Rendering video...")
        output_file = self.video_renderer.render(
            audio_path, animations, timed_lyrics, output_path
        )
        print(f"Video generated successfully: {output_file}")

        return output_file


if __name__ == "__main__":
    # Example usage
    generator = MusicVideoGenerator()
    # generator.create_video(
    #     audio_path="sample_song.mp3",
    #     lyrics_path="sample_lyrics.txt",
    #     output_path="output.mp4"
    # )
    print("Music Video Generator initialized successfully!")
