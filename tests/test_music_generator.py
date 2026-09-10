"""Test suite for Music Video Generator."""

import pytest
import os
import tempfile
from pathlib import Path
import numpy as np


class TestAudioProcessor:
    """Tests for audio processing module."""

    def test_import(self):
        """Test that audio processor can be imported."""
        from src.audio_processor import AudioProcessor
        assert AudioProcessor is not None

    def test_initialization(self):
        """Test audio processor initialization."""
        from src.audio_processor import AudioProcessor
        processor = AudioProcessor(sr=22050)
        assert processor.sr == 22050

    def test_energy_analysis(self):
        """Test energy analysis with synthetic audio."""
        from src.audio_processor import AudioProcessor
        processor = AudioProcessor()
        
        # Create synthetic audio
        sr = 22050
        duration = 2  # seconds
        t = np.linspace(0, duration, sr * duration)
        y = np.sin(2 * np.pi * 440 * t)  # 440 Hz sine wave
        
        audio_data = (sr, y)
        energy = processor.analyze_energy(audio_data)
        
        assert 0 <= energy <= 1, "Energy should be between 0 and 1"


class TestLyricsParser:
    """Tests for lyrics parsing module."""

    def test_import(self):
        """Test that lyrics parser can be imported."""
        from src.lyrics_parser import LyricsParser
        assert LyricsParser is not None

    def test_initialization(self):
        """Test lyrics parser initialization."""
        from src.lyrics_parser import LyricsParser
        parser = LyricsParser()
        assert parser is not None

    def test_load_lyrics(self):
        """Test loading lyrics from a file."""
        from src.lyrics_parser import LyricsParser
        parser = LyricsParser()
        
        # Create a temporary lyrics file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("Line 1\n")
            f.write("Line 2\n")
            f.write("Line 3\n")
            temp_path = f.name
        
        try:
            lyrics = parser.load_lyrics(temp_path)
            assert len(lyrics) == 3
            assert lyrics[0] == "Line 1"
        finally:
            os.unlink(temp_path)

    def test_synchronize_lyrics(self):
        """Test lyrics synchronization."""
        from src.lyrics_parser import LyricsParser
        parser = LyricsParser()
        
        lyrics = ["Line 1", "Line 2", "Line 3"]
        sr = 22050
        audio_length = sr * 6  # 6 seconds of audio
        
        timed_lyrics = parser.synchronize_lyrics(lyrics, audio_length, sr)
        
        assert len(timed_lyrics) == 3
        assert timed_lyrics[0][0] == "Line 1"
        assert timed_lyrics[0][1] >= 0
        assert timed_lyrics[0][2] > timed_lyrics[0][1]

    def test_split_into_words(self):
        """Test splitting lyrics into words."""
        from src.lyrics_parser import LyricsParser
        parser = LyricsParser()
        
        lyrics = ["Hello world", "This is a test"]
        words = parser.split_into_words(lyrics)
        
        assert "Hello" in words
        assert "world" in words
        assert "test" in words
        assert len(words) == 5


class TestMoodAnalyzer:
    """Tests for mood analysis module."""

    def test_import(self):
        """Test that mood analyzer can be imported."""
        from src.mood_analyzer import MoodAnalyzer
        assert MoodAnalyzer is not None

    def test_initialization(self):
        """Test mood analyzer initialization."""
        from src.mood_analyzer import MoodAnalyzer
        analyzer = MoodAnalyzer()
        assert analyzer is not None

    def test_detect_mood_calm(self):
        """Test mood detection for calm music."""
        from src.mood_analyzer import MoodAnalyzer
        analyzer = MoodAnalyzer()
        
        sr = 22050
        y = np.zeros(sr * 2)
        audio_data = (sr, y)
        
        mood = analyzer.detect_mood(tempo=60, energy=0.2, audio_data=audio_data)
        assert mood == "calm"

    def test_detect_mood_energetic(self):
        """Test mood detection for energetic music."""
        from src.mood_analyzer import MoodAnalyzer
        analyzer = MoodAnalyzer()
        
        sr = 22050
        y = np.zeros(sr * 2)
        audio_data = (sr, y)
        
        mood = analyzer.detect_mood(tempo=160, energy=0.8, audio_data=audio_data)
        assert mood == "energetic"

    def test_get_mood_characteristics(self):
        """Test getting characteristics for each mood."""
        from src.mood_analyzer import MoodAnalyzer
        analyzer = MoodAnalyzer()
        
        moods = ["calm", "melancholic", "moderate", "upbeat", "energetic", "balanced"]
        
        for mood in moods:
            characteristics = analyzer.get_mood_characteristics(mood)
            assert "primary_colors" in characteristics
            assert "animation_speed" in characteristics
            assert "transition_duration" in characteristics
            assert "effects" in characteristics


class TestVisualGenerator:
    """Tests for visual generation module."""

    def test_import(self):
        """Test that visual generator can be imported."""
        from src.visual_generator import VisualGenerator
        assert VisualGenerator is not None

    def test_initialization(self):
        """Test visual generator initialization."""
        from src.visual_generator import VisualGenerator
        generator = VisualGenerator(width=1920, height=1080)
        assert generator.width == 1920
        assert generator.height == 1080

    def test_generate_backgrounds(self):
        """Test background generation."""
        from src.visual_generator import VisualGenerator
        generator = VisualGenerator()
        
        backgrounds = generator.generate_backgrounds("upbeat", 5)
        assert len(backgrounds) > 0
        assert backgrounds[0]["type"] == "background"

    def test_create_solid_color_frame(self):
        """Test creating a solid color frame."""
        from src.visual_generator import VisualGenerator
        generator = VisualGenerator(width=640, height=480)
        
        frame = generator.create_solid_color_frame((255, 0, 0))
        assert frame.size == (640, 480)
        assert frame.mode == "RGB"


class TestAnimator:
    """Tests for animation module."""

    def test_import(self):
        """Test that animator can be imported."""
        from src.animator import Animator
        assert Animator is not None

    def test_initialization(self):
        """Test animator initialization."""
        from src.animator import Animator
        animator = Animator()
        assert len(animator.animation_types) > 0

    def test_create_animations(self):
        """Test animation creation."""
        from src.animator import Animator
        animator = Animator()
        
        visual_assets = [
            {"type": "background", "color": (255, 0, 0)},
            {"type": "background", "color": (0, 255, 0)},
        ]
        timed_lyrics = [
            ("Line 1", 0.0, 2.0),
            ("Line 2", 2.0, 4.0),
        ]
        
        animations = animator.create_animations(visual_assets, timed_lyrics, tempo=120, mood="upbeat")
        assert len(animations) > 0

    def test_select_animation_type(self):
        """Test animation type selection."""
        from src.animator import Animator
        animator = Animator()
        
        anim_type = animator._select_animation_type("calm", 0)
        assert anim_type in animator.animation_types or anim_type in ["slow_zoom", "slow_pan", "spin"]


class TestVideoRenderer:
    """Tests for video rendering module."""

    def test_import(self):
        """Test that video renderer can be imported."""
        from src.video_renderer import VideoRenderer
        assert VideoRenderer is not None

    def test_initialization(self):
        """Test video renderer initialization."""
        from src.video_renderer import VideoRenderer
        renderer = VideoRenderer(fps=30, resolution=(1920, 1080))
        assert renderer.fps == 30
        assert renderer.resolution == (1920, 1080)
        assert renderer.width == 1920
        assert renderer.height == 1080


class TestMusicVideoGenerator:
    """Tests for main Music Video Generator."""

    def test_import(self):
        """Test that main module can be imported."""
        from src.main import MusicVideoGenerator
        assert MusicVideoGenerator is not None

    def test_initialization(self):
        """Test main generator initialization."""
        from src.main import MusicVideoGenerator
        generator = MusicVideoGenerator()
        assert generator.audio_processor is not None
        assert generator.lyrics_parser is not None
        assert generator.mood_analyzer is not None
        assert generator.visual_generator is not None
        assert generator.animator is not None
        assert generator.video_renderer is not None

    def test_initialization_with_config(self):
        """Test initialization with custom config."""
        from src.main import MusicVideoGenerator
        config = {"video": {"fps": 60}}
        generator = MusicVideoGenerator(config=config)
        assert generator.config["video"]["fps"] == 60


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
