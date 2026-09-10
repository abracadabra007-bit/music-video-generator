"""Lyrics parsing and synchronization module."""

import re
from typing import List, Tuple, Optional
import numpy as np


class LyricsParser:
    """Handles lyrics parsing and synchronization with audio."""

    def load_lyrics(self, lyrics_path: str) -> List[str]:
        """Load lyrics from a text file.

        Args:
            lyrics_path: Path to the lyrics file

        Returns:
            List of lyrics lines
        """
        with open(lyrics_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        # Clean up lines
        return [line.strip() for line in lines if line.strip()]

    def synchronize_lyrics(
        self, lyrics: List[str], audio_length: int, sample_rate: int
    ) -> List[Tuple[str, float, float]]:
        """Synchronize lyrics with audio timing.

        This is a simple linear distribution. For production, you might want to use
        speech recognition or manual timing data.

        Args:
            lyrics: List of lyrics lines
            audio_length: Number of audio samples
            sample_rate: Audio sample rate

        Returns:
            List of tuples (lyrics_text, start_time, end_time) in seconds
        """
        duration = audio_length / sample_rate
        timed_lyrics = []

        if not lyrics:
            return timed_lyrics

        # Distribute lyrics evenly across the song duration
        time_per_line = duration / len(lyrics)

        for i, line in enumerate(lyrics):
            start_time = i * time_per_line
            end_time = (i + 1) * time_per_line
            timed_lyrics.append((line, start_time, end_time))

        return timed_lyrics

    def parse_timed_lyrics(self, lyrics_path: str) -> List[Tuple[str, float]]:
        """Parse lyrics with explicit timing (LRC format or similar).

        Expected format: [00:12.34] Lyrics text
        Or: {00:12.34} Lyrics text

        Args:
            lyrics_path: Path to the lyrics file with timing

        Returns:
            List of tuples (lyrics_text, time_in_seconds)
        """
        timed_lyrics = []
        time_pattern = r"[\[\{]([0-9]{2}):([0-9]{2})\.([0-9]{2})[\]\}]"

        with open(lyrics_path, "r", encoding="utf-8") as f:
            for line in f:
                match = re.search(time_pattern, line)
                if match:
                    minutes, seconds, centiseconds = match.groups()
                    time_seconds = (
                        int(minutes) * 60 + int(seconds) + int(centiseconds) / 100
                    )
                    lyrics_text = re.sub(time_pattern, "", line).strip()
                    if lyrics_text:
                        timed_lyrics.append((lyrics_text, time_seconds))

        return timed_lyrics

    def split_into_words(self, lyrics: List[str]) -> List[str]:
        """Split lyrics into individual words for word-by-word display.

        Args:
            lyrics: List of lyrics lines

        Returns:
            List of individual words
        """
        words = []
        for line in lyrics:
            words.extend(line.split())
        return words
