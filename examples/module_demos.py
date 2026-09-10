"""Demonstration of individual module usage without full video rendering."""

import sys
import numpy as np
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.audio_processor import AudioProcessor
from src.lyrics_parser import LyricsParser
from src.mood_analyzer import MoodAnalyzer
from src.visual_generator import VisualGenerator
from src.animator import Animator


def demo_synthetic_audio():
    """Demonstrate audio processing with synthetic audio."""
    print("\n" + "="*60)
    print("Demo 1: Audio Processing with Synthetic Audio")
    print("="*60)
    
    processor = AudioProcessor(sr=22050)
    
    # Create synthetic audio (440 Hz sine wave for 3 seconds)
    sr = 22050
    duration = 3
    t = np.linspace(0, duration, sr * duration)
    y = np.sin(2 * np.pi * 440 * t) * 0.5  # 440 Hz with amplitude 0.5
    
    audio_data = (sr, y)
    
    print("\nGenerated synthetic audio:")
    print(f"  Sample Rate: {sr} Hz")
    print(f"  Duration: {duration} seconds")
    print(f"  Total Samples: {len(y):,}")
    print(f"  Frequency: 440 Hz (A note)")
    
    # Analyze energy
    energy = processor.analyze_energy(audio_data)
    print(f"\nAnalyzed Energy: {energy:.4f}")
    print(f"  (Values closer to 1.0 indicate higher energy)")
    
    duration = processor.get_duration(audio_data)
    print(f"\nCalculated Duration: {duration:.2f} seconds")


def demo_lyrics_workflow():
    """Demonstrate complete lyrics workflow."""
    print("\n" + "="*60)
    print("Demo 2: Lyrics Parsing and Synchronization")
    print("="*60)
    
    parser = LyricsParser()
    
    # Create sample lyrics
    lyrics = [
        "Wake up in the morning",
        "Sun is shining bright",
        "Gonna dance all day",
        "And party through the night"
    ]
    
    print("\nOriginal lyrics:")
    for i, line in enumerate(lyrics, 1):
        print(f"  {i}. {line}")
    
    # Synchronize with synthetic audio (6 seconds)
    sr = 22050
    audio_length = sr * 6
    timed_lyrics = parser.synchronize_lyrics(lyrics, audio_length, sr)
    
    print("\nSynchronized lyrics with 6-second audio:")
    for text, start, end in timed_lyrics:
        duration = end - start
        print(f"  [{start:6.2f}s - {end:6.2f}s] ({duration:5.2f}s) {text}")
    
    # Split into words
    words = parser.split_into_words(lyrics)
    print(f"\nTotal words: {len(words)}")
    print(f"Words: {', '.join(words)}")


def demo_mood_detection():
    """Demonstrate mood detection and characteristics."""
    print("\n" + "="*60)
    print("Demo 3: Mood Detection and Characteristics")
    print("="*60)
    
    analyzer = MoodAnalyzer()
    
    # Test different tempo and energy combinations
    test_cases = [
        (60, 0.2, "Slow ballad"),
        (80, 0.3, "Acoustic folk"),
        (100, 0.4, "Moderate rock"),
        (120, 0.6, "Upbeat pop"),
        (140, 0.7, "Fast dance"),
        (160, 0.9, "Intense electronic"),
    ]
    
    print("\nMood detection examples:")
    print("\n  Tempo (BPM) | Energy | Description        | Detected Mood")
    print("  " + "-" * 55)
    
    sr = 22050
    y = np.zeros(sr * 2)  # Dummy audio
    audio_data = (sr, y)
    
    for tempo, energy, description in test_cases:
        mood = analyzer.detect_mood(tempo, energy, audio_data)
        print(f"  {tempo:11} | {energy:6.1f} | {description:18} | {mood.upper():11}")
    
    # Show characteristics for one mood
    print("\nDetailed characteristics for 'UPBEAT' mood:")
    chars = analyzer.get_mood_characteristics("upbeat")
    print(f"  Primary Colors: {chars['primary_colors']}")
    print(f"  Animation Speed: {chars['animation_speed']}x")
    print(f"  Transition Duration: {chars['transition_duration']}s")
    print(f"  Effects: {', '.join(chars['effects'])}")


def demo_visual_generation():
    """Demonstrate visual asset generation."""
    print("\n" + "="*60)
    print("Demo 4: Visual Asset Generation")
    print("="*60)
    
    generator = VisualGenerator(width=1920, height=1080)
    
    print(f"\nVideo Resolution: {generator.width}x{generator.height}")
    
    # Generate backgrounds for different moods
    moods = ["calm", "upbeat", "energetic"]
    
    for mood in moods:
        backgrounds = generator.generate_backgrounds(mood, 3)
        print(f"\n{mood.upper()} Backgrounds:")
        for i, bg in enumerate(backgrounds, 1):
            print(f"  Background {i}:")
            print(f"    - Color (RGB): {bg['color']}")
            print(f"    - Duration: {bg['duration']}s")


def demo_animation_selection():
    """Demonstrate animation selection based on mood and tempo."""
    print("\n" + "="*60)
    print("Demo 5: Animation Selection Based on Mood and Tempo")
    print("="*60)
    
    animator = Animator()
    
    print(f"\nAvailable animation types: {', '.join(animator.animation_types)}")
    
    # Demonstrate animation selection
    scenarios = [
        ("calm", 60),
        ("moderate", 100),
        ("upbeat", 130),
        ("energetic", 160),
    ]
    
    print("\nAnimation selection by mood and tempo:")
    print("\n  Mood       | Tempo (BPM) | Animation Type | Duration | Easing")
    print("  " + "-" * 55)
    
    for mood, tempo in scenarios:
        anim_type = animator._select_animation_type(mood, 0)
        duration = animator._calculate_duration(tempo)
        easing = animator._select_easing(mood)
        print(f"  {mood:10} | {tempo:11} | {anim_type:14} | {duration:8.1f}s | {easing}")


def demo_full_workflow():
    """Demonstrate a complete workflow with synthetic data."""
    print("\n" + "="*60)
    print("Demo 6: Complete Workflow (Synthetic Data)")
    print("="*60)
    
    from src.audio_processor import AudioProcessor
    from src.lyrics_parser import LyricsParser
    from src.mood_analyzer import MoodAnalyzer
    from src.visual_generator import VisualGenerator
    from src.animator import Animator
    
    # Step 1: Process audio
    print("\nStep 1: Audio Processing")
    processor = AudioProcessor()
    sr = 22050
    duration = 10
    t = np.linspace(0, duration, sr * duration)
    y = np.sin(2 * np.pi * 440 * t) * 0.5
    audio_data = (sr, y)
    energy = processor.analyze_energy(audio_data)
    print(f"  ✓ Loaded synthetic audio: {duration}s @ {sr}Hz")
    print(f"  ✓ Analyzed energy: {energy:.4f}")
    
    # Step 2: Parse lyrics
    print("\nStep 2: Lyrics Parsing")
    parser = LyricsParser()
    lyrics = ["Line 1", "Line 2", "Line 3", "Line 4"]
    timed_lyrics = parser.synchronize_lyrics(lyrics, len(y), sr)
    print(f"  ✓ Loaded {len(lyrics)} lines of lyrics")
    print(f"  ✓ Synchronized with audio timing")
    
    # Step 3: Detect mood
    print("\nStep 3: Mood Detection")
    analyzer = MoodAnalyzer()
    tempo = 120  # Example tempo
    detected_mood = analyzer.detect_mood(tempo, energy, audio_data)
    print(f"  ✓ Detected mood: {detected_mood.upper()}")
    print(f"  ✓ Tempo: {tempo} BPM, Energy: {energy:.4f}")
    
    # Step 4: Generate visuals
    print("\nStep 4: Visual Generation")
    visual_gen = VisualGenerator()
    beats = np.linspace(0, duration, int(duration * 2))  # 2 beats per second
    assets = visual_gen.generate_assets(detected_mood, len(y), beats)
    print(f"  ✓ Generated {len(assets)} visual assets")
    
    # Step 5: Create animations
    print("\nStep 5: Animation Creation")
    anim = Animator()
    animations = anim.create_animations(assets, timed_lyrics, tempo, detected_mood)
    print(f"  ✓ Created {len(animations)} animation sequences")
    
    # Step 6: Ready to render
    print("\nStep 6: Ready for Video Rendering")
    print("  ✓ All components prepared")
    print(f"  ✓ Video resolution: 1920x1080")
    print(f"  ✓ FPS: 30")
    print(f"  ✓ Duration: {duration}s")
    print("  ✓ Ready to render (requires moviepy)")


def main():
    """Run all demonstrations."""
    print("\n" + "#" * 60)
    print("#  MUSIC VIDEO GENERATOR - MODULE DEMONSTRATIONS" + " " * 10 + "#")
    print("#" * 60)
    
    demo_synthetic_audio()
    demo_lyrics_workflow()
    demo_mood_detection()
    demo_visual_generation()
    demo_animation_selection()
    demo_full_workflow()
    
    print("\n" + "="*60)
    print("All demonstrations completed!")
    print("="*60)
    print()


if __name__ == "__main__":
    main()
