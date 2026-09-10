"""Example usage of Music Video Generator with different configurations."""

import os
import sys
from pathlib import Path

# Add the parent directory to the path so we can import src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.main import MusicVideoGenerator
from config.defaults import DEFAULT_CONFIG


def example_basic_usage():
    """Basic example of using the Music Video Generator."""
    print("\n" + "="*60)
    print("Example 1: Basic Usage")
    print("="*60)
    
    generator = MusicVideoGenerator()
    
    print("\nMusic Video Generator initialized!")
    print(f"\nConfiguration:")
    print(f"  Video Resolution: {generator.config['video']['width']}x{generator.config['video']['height']}")
    print(f"  Video FPS: {generator.config['video']['fps']}")
    print(f"  Audio Sample Rate: {generator.config['audio']['sample_rate']} Hz")
    print(f"  Text Font Size: {generator.config['text']['default_fontsize']}")
    
    # Note: This would require actual audio and lyrics files
    # Uncomment to run with real files:
    # output = generator.create_video(
    #     audio_path="path/to/your/song.mp3",
    #     lyrics_path="path/to/your/lyrics.txt",
    #     output_path="output/my_music_video.mp4"
    # )
    # print(f"\nVideo saved to: {output}")


def example_with_custom_config():
    """Example with custom configuration."""
    print("\n" + "="*60)
    print("Example 2: Custom Configuration")
    print("="*60)
    
    custom_config = {
        "video": {
            "fps": 60,  # Higher frame rate for smoother video
            "width": 1280,
            "height": 720,
            "codec": "libx264",
            "audio_codec": "aac",
        },
        "text": {
            "default_fontsize": 60,
            "default_color": "yellow",
            "default_font": "Arial-Bold",
        },
    }
    
    generator = MusicVideoGenerator(config=custom_config)
    
    print("\nCustom configuration applied!")
    print(f"\nModified Settings:")
    print(f"  Video Resolution: {generator.config['video']['width']}x{generator.config['video']['height']}")
    print(f"  Video FPS: {generator.config['video']['fps']}")
    print(f"  Text Font Size: {generator.config['text']['default_fontsize']}")
    print(f"  Text Color: {generator.config['text']['default_color']}")


def example_audio_processing():
    """Example of audio processing features."""
    print("\n" + "="*60)
    print("Example 3: Audio Processing (Requires Audio File)")
    print("="*60)
    
    from src.audio_processor import AudioProcessor
    
    processor = AudioProcessor()
    print("\nAudioProcessor features:")
    print("  - load_audio(path): Load audio file and extract audio data")
    print("  - extract_tempo_and_beats(audio_data): Extract BPM and beat times")
    print("  - analyze_energy(audio_data): Analyze overall energy level")
    print("  - extract_spectral_features(audio_data): Extract detailed audio features")
    print("  - get_duration(audio_data): Get audio duration in seconds")
    
    print("\nExample usage:")
    print("""
    processor = AudioProcessor()
    audio_data = processor.load_audio("song.mp3")
    tempo, beats = processor.extract_tempo_and_beats(audio_data)
    energy = processor.analyze_energy(audio_data)
    print(f"Tempo: {tempo} BPM")
    print(f"Energy: {energy:.2f}")
    """)


def example_lyrics_parsing():
    """Example of lyrics parsing features."""
    print("\n" + "="*60)
    print("Example 4: Lyrics Parsing")
    print("="*60)
    
    from src.lyrics_parser import LyricsParser
    
    parser = LyricsParser()
    print("\nLyricsParser features:")
    print("  - load_lyrics(path): Load lyrics from text file")
    print("  - synchronize_lyrics(lyrics, audio_length, sr): Sync lyrics with audio")
    print("  - parse_timed_lyrics(path): Parse pre-timed lyrics (LRC format)")
    print("  - split_into_words(lyrics): Split lyrics into individual words")
    
    # Load sample lyrics
    sample_lyrics_path = Path(__file__).parent / "assets/sample_data/upbeat_sample.txt"
    if sample_lyrics_path.exists():
        print(f"\nLoading sample lyrics from: {sample_lyrics_path}")
        lyrics = parser.load_lyrics(str(sample_lyrics_path))
        print(f"Loaded {len(lyrics)} lines of lyrics")
        print("\nFirst 3 lines:")
        for i, line in enumerate(lyrics[:3], 1):
            print(f"  {i}. {line}")
    else:
        print("\nSample lyrics file not found.")


def example_mood_analysis():
    """Example of mood analysis features."""
    print("\n" + "="*60)
    print("Example 5: Mood Analysis")
    print("="*60)
    
    from src.mood_analyzer import MoodAnalyzer
    import numpy as np
    
    analyzer = MoodAnalyzer()
    
    print("\nMood detection based on tempo and energy:")
    print()
    
    test_cases = [
        (60, 0.2, "Calm"),
        (75, 0.35, "Melancholic"),
        (120, 0.5, "Moderate"),
        (130, 0.6, "Upbeat"),
        (160, 0.8, "Energetic"),
    ]
    
    for tempo, energy, description in test_cases:
        sr = 22050
        y = np.zeros(sr * 2)
        audio_data = (sr, y)
        detected_mood = analyzer.detect_mood(tempo, energy, audio_data)
        print(f"  {description:15} (Tempo: {tempo:3} BPM, Energy: {energy:.1f}) -> {detected_mood.upper()}")
    
    print("\nMood Characteristics:")
    moods = ["calm", "upbeat", "energetic"]
    for mood in moods:
        chars = analyzer.get_mood_characteristics(mood)
        print(f"\n  {mood.upper()}:")
        print(f"    - Animation Speed: {chars['animation_speed']}x")
        print(f"    - Transition Duration: {chars['transition_duration']}s")
        print(f"    - Effects: {', '.join(chars['effects'])}")


def example_visual_generation():
    """Example of visual generation features."""
    print("\n" + "="*60)
    print("Example 6: Visual Generation")
    print("="*60)
    
    from src.visual_generator import VisualGenerator
    import numpy as np
    
    generator = VisualGenerator(width=1920, height=1080)
    
    print("\nVisualGenerator features:")
    print("  - generate_assets(mood, audio_length, beats, images_path): Generate visual assets")
    print("  - generate_backgrounds(mood, num_frames): Create mood-based backgrounds")
    print("  - load_images(images_path): Load custom images")
    print("  - create_solid_color_frame(color, width, height): Create single-color frames")
    print("  - add_text_overlay(image, text, position, color): Add text to images")
    
    print("\nGenerating sample backgrounds for different moods:")
    for mood in ["calm", "upbeat", "energetic"]:
        backgrounds = generator.generate_backgrounds(mood, 3)
        print(f"\n  {mood.upper()}:")
        for bg in backgrounds:
            print(f"    - Color: RGB{bg['color']}, Duration: {bg['duration']}s")


def example_animation():
    """Example of animation features."""
    print("\n" + "="*60)
    print("Example 7: Animation Creation")
    print("="*60)
    
    from src.animator import Animator
    
    animator = Animator()
    
    print("\nAnimator features:")
    print("  - create_animations(assets, lyrics, tempo, mood): Generate animations")
    print(f"  - Available animation types: {', '.join(animator.animation_types)}")
    
    print("\nAnimation selection by mood:")
    moods_and_tempos = [
        ("calm", 70),
        ("upbeat", 130),
        ("energetic", 160),
    ]
    
    for mood, tempo in moods_and_tempos:
        anim_type = animator._select_animation_type(mood, 0)
        duration = animator._calculate_duration(tempo)
        easing = animator._select_easing(mood)
        print(f"\n  {mood.upper()} (Tempo {tempo} BPM):")
        print(f"    - Animation: {anim_type}")
        print(f"    - Duration: {duration}s")
        print(f"    - Easing: {easing}")


def example_complete_workflow():
    """Example showing a complete workflow (without actual rendering)."""
    print("\n" + "="*60)
    print("Example 8: Complete Workflow Demonstration")
    print("="*60)
    
    print("""
Step-by-step workflow for generating a music video:

1. Initialize the generator:
   >>> from src.main import MusicVideoGenerator
   >>> generator = MusicVideoGenerator()

2. Create video from audio and lyrics:
   >>> output = generator.create_video(
   ...     audio_path="path/to/song.mp3",
   ...     lyrics_path="path/to/lyrics.txt",
   ...     output_path="output/video.mp4",
   ...     mood="upbeat"  # Optional: auto-detected if not provided
   ... )

3. The generator will:
   ✓ Load and analyze the audio file
   ✓ Extract tempo, beats, and energy levels
   ✓ Parse the lyrics file
   ✓ Synchronize lyrics with the audio
   ✓ Detect the song's mood
   ✓ Generate appropriate visual assets
   ✓ Create animations matching the mood and tempo
   ✓ Render the final video with synced audio and lyrics

4. The output video will be saved to the specified path.

That's it! Your music video is ready.
    """)


def main():
    """Run all examples."""
    print("\n")
    print("#" * 60)
    print("#" + " " * 58 + "#")
    print("#  MUSIC VIDEO GENERATOR - USAGE EXAMPLES" + " " * 18 + "#")
    print("#" + " " * 58 + "#")
    print("#" * 60)
    
    example_basic_usage()
    example_with_custom_config()
    example_audio_processing()
    example_lyrics_parsing()
    example_mood_analysis()
    example_visual_generation()
    example_animation()
    example_complete_workflow()
    
    print("\n" + "="*60)
    print("All examples completed!")
    print("="*60)
    print("\nFor more information, see the README.md file.")
    print()


if __name__ == "__main__":
    main()
