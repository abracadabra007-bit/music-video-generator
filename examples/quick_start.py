#!/usr/bin/env python
"""Simple CLI script to generate a music video."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.main import MusicVideoGenerator


def main():
    """
    CLI usage:
    python examples/quick_start.py <audio_file> <lyrics_file> <output_file> [mood]
    
    Example:
    python examples/quick_start.py song.mp3 lyrics.txt output.mp4 upbeat
    """
    if len(sys.argv) < 4:
        print("Usage: python examples/quick_start.py <audio_file> <lyrics_file> <output_file> [mood]")
        print()
        print("Example:")
        print("  python examples/quick_start.py song.mp3 lyrics.txt output.mp4")
        print("  python examples/quick_start.py song.mp3 lyrics.txt output.mp4 upbeat")
        print()
        print("Supported moods:")
        print("  - calm, melancholic, moderate, upbeat, energetic, balanced")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    lyrics_file = sys.argv[2]
    output_file = sys.argv[3]
    mood = sys.argv[4] if len(sys.argv) > 4 else None
    
    # Validate input files
    if not Path(audio_file).exists():
        print(f"Error: Audio file not found: {audio_file}")
        sys.exit(1)
    
    if not Path(lyrics_file).exists():
        print(f"Error: Lyrics file not found: {lyrics_file}")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("Music Video Generator - Quick Start")
    print("="*60)
    print(f"Audio File: {audio_file}")
    print(f"Lyrics File: {lyrics_file}")
    print(f"Output File: {output_file}")
    if mood:
        print(f"Mood: {mood}")
    print("="*60 + "\n")
    
    try:
        generator = MusicVideoGenerator()
        output_path = generator.create_video(
            audio_path=audio_file,
            lyrics_path=lyrics_file,
            output_path=output_file,
            mood=mood
        )
        print(f"\n✓ Video generated successfully!")
        print(f"Output: {output_path}")
    except Exception as e:
        print(f"\n✗ Error generating video: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
