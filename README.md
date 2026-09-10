# Music Video Generator

A Python application that automatically generates simple music videos from songs and lyrics. The program creates visually appealing videos with synchronized text, basic animations, and still images—requiring minimal manual editing.

## Features

- **Automatic Video Generation**: Create music videos from audio files and lyrics
- **Synchronized Lyrics**: Display lyrics in perfect sync with the music
- **Visual Elements**: Support for still images, video clips, and basic animations
- **Mood-Based Styling**: Adapt visuals to match the song's mood and rhythm
- **Minimal Manual Editing**: Straightforward input → automated output workflow

## Project Structure

```
music-video-generator/
├── src/
│   ├── __init__.py
│   ├── main.py                 # Entry point
│   ├── audio_processor.py      # Audio analysis and extraction
│   ├── lyrics_parser.py        # Lyrics parsing and timing
│   ├── visual_generator.py     # Visual asset management
│   ├── animator.py             # Animation generation
│   ├── video_renderer.py       # Video composition and rendering
│   └── mood_analyzer.py        # Analyze song mood
├── config/
│   └── defaults.py             # Configuration settings
├── assets/
│   ├── templates/              # Visual templates
│   ├── effects/                # Built-in effects
│   └── sample_data/            # Example songs and lyrics
├── tests/
│   └── test_*.py               # Unit tests
├── requirements.txt            # Python dependencies
├── setup.py                    # Package configuration
└── README.md                   # This file
```

## Installation

```bash
git clone https://github.com/abracadabra007-bit/music-video-generator.git
cd music-video-generator
pip install -r requirements.txt
```

## Usage

```python
from src.main import MusicVideoGenerator

# Initialize the generator
generator = MusicVideoGenerator()

# Generate a video
generator.create_video(
    audio_path="path/to/song.mp3",
    lyrics_path="path/to/lyrics.txt",
    output_path="output/video.mp4",
    mood="upbeat"  # Optional: helps determine visual style
)
```

## How It Works

1. **Audio Processing**: Extract tempo, rhythm, and energy levels from the audio
2. **Lyrics Parsing**: Parse lyrics and sync timing with the music
3. **Mood Analysis**: Determine the song's mood to guide visual selection
4. **Visual Generation**: Select or generate appropriate visual assets
5. **Animation**: Create smooth transitions and animations
6. **Rendering**: Compose all elements into a final video file

## Dependencies

- `librosa` - Audio analysis
- `moviepy` - Video composition and rendering
- `opencv-python` - Image and video processing
- `numpy` - Numerical operations
- `pydub` - Audio processing
- `pillow` - Image manipulation

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

This project is open source and available under the MIT License.

## Roadmap

- [ ] Basic audio analysis and beat detection
- [ ] Lyrics sync engine
- [ ] Simple animation framework
- [ ] Video rendering pipeline
- [ ] Mood detection system
- [ ] Built-in visual templates
- [ ] Support for custom effects
- [ ] CLI interface
- [ ] Web interface
