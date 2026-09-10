"""Default configuration settings."""

DEFAULT_CONFIG = {
    "video": {
        "fps": 30,
        "width": 1920,
        "height": 1080,
        "codec": "libx264",
        "audio_codec": "aac",
    },
    "audio": {
        "sample_rate": 22050,
    },
    "text": {
        "default_fontsize": 70,
        "default_color": "white",
        "default_font": "Arial",
    },
    "animation": {
        "default_fps": 30,
        "easing": "ease-in-out",
    },
    "output": {
        "default_extension": ".mp4",
        "quality": "high",
    },
}
