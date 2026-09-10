"""Updated setup.py with CLI entry points."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="music-video-generator",
    version="0.1.0",
    author="abracadabra007-bit",
    description="Automatically generate simple music videos from songs and lyrics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abracadabra007-bit/music-video-generator",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'mvg=src.cli:cli',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
)
