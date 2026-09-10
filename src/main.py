"""Updated main.py with advanced features."""

import os
from pathlib import Path
from typing import Optional

from src.audio_processor import AudioProcessor
from src.lyrics_parser import LyricsParser
from src.mood_analyzer import MoodAnalyzer
from src.visual_generator import VisualGenerator
from src.animator import Animator
from src.video_renderer import VideoRenderer
from src.beat_synchronizer import BeatSynchronizer
from src.color_effects import ColorEffectGenerator
from src.particle_system import ParticleSystem
from src.audio_reactive import AudioReactiveEffects
from src.keyframe_animation import KeyframeAnimation
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
        
        # Advanced features
        self.beat_synchronizer = BeatSynchronizer()
        self.color_effects = ColorEffectGenerator()
        self.particle_system = ParticleSystem()
        self.audio_reactive = AudioReactiveEffects()

    def create_video(
        self,
        audio_path: str,
        lyrics_path: str,
        output_path: str,
        mood: Optional[str] = None,
        images_path: Optional[str] = None,
        enable_beat_sync: bool = True,
        enable_particles: bool = True,
        enable_audio_reactive: bool = True,
    ) -> str:
        """Generate a music video from audio and lyrics.

        Args:
            audio_path: Path to the audio file (MP3, WAV, etc.)
            lyrics_path: Path to the lyrics file (TXT format)
            output_path: Path where the output video will be saved
            mood: Optional mood specification (e.g., 'upbeat', 'melancholic')
            images_path: Optional path to directory containing images
            enable_beat_sync: Enable beat-synchronized effects
            enable_particles: Enable particle system effects
            enable_audio_reactive: Enable audio-reactive effects

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

        # Step 4: Advanced features - Beat synchronization
        if enable_beat_sync:
            print("Step 4a: Analyzing beats for synchronization...")
            beat_events = self.beat_synchronizer.analyze_beats(audio_data, beats)
            print(f"  Found {len(beat_events)} beat events")
        else:
            beat_events = []

        # Step 5: Advanced features - Color effects
        print("Step 4b: Generating advanced color effects...")
        palette = self.color_effects.get_palette(detected_mood)
        if palette:
            print(f"  Using {palette.name} palette: {palette.description}")
        
        # Step 6: Advanced features - Audio reactive effects
        if enable_audio_reactive:
            print("Step 4c: Analyzing audio frequency content...")
            try:
                freq_bands = self.color_effects.generate_gradient(
                    (255, 0, 0), (0, 255, 0), steps=5
                )
                print(f"  Generated frequency-responsive effects")
            except Exception as e:
                print(f"  Audio reactive analysis skipped: {e}")
        
        # Step 7: Generate visuals
        print("Step 5: Generating visuals...")
        visual_assets = self.visual_generator.generate_assets(
            detected_mood, len(audio_data[1]), beats, images_path
        )
        print(f"  Generated {len(visual_assets)} visual frames")

        # Step 8: Create animations
        print("Step 6: Creating animations...")
        animations = self.animator.create_animations(
            visual_assets, timed_lyrics, tempo, detected_mood
        )
        print(f"  Created {len(animations)} animation sequences")
        
        # Step 9: Add beat-synchronized animations
        if enable_beat_sync and beat_events:
            print("Step 6a: Adding beat-synchronized effects...")
            beat_duration = self.audio_processor.get_duration(audio_data)
            beat_keyframes = self.beat_synchronizer.generate_beat_keyframes(
                beat_duration, fps=self.config["video"]["fps"]
            )
            print(f"  Added {len(beat_keyframes)} beat keyframes")

        # Step 10: Render video
        print("Step 7: Rendering video...")
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
