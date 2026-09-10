"""Particle system for creating dynamic visual effects."""

import numpy as np
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class Particle:
    """Represents a single particle in the system."""
    x: float
    y: float
    vx: float  # Velocity X
    vy: float  # Velocity Y
    life: float  # 0-1, where 1 is fully alive
    color: Tuple[int, int, int]
    size: float


class ParticleSystem:
    """Manages particle effects for visual enhancement."""

    def __init__(self, width: int = 1920, height: int = 1080):
        """Initialize the particle system.

        Args:
            width: Canvas width in pixels
            height: Canvas height in pixels
        """
        self.width = width
        self.height = height
        self.particles: List[Particle] = []
        self.gravity = 0.2
        self.friction = 0.99

    def emit_particles(
        self,
        x: float,
        y: float,
        count: int,
        color: Tuple[int, int, int],
        velocity_range: float = 5.0,
        size_range: Tuple[float, float] = (2.0, 8.0),
    ) -> None:
        """Emit particles from a point.

        Args:
            x: X position
            y: Y position
            count: Number of particles to emit
            color: Particle color (R, G, B)
            velocity_range: Maximum velocity magnitude
            size_range: (min_size, max_size) tuple
        """
        for _ in range(count):
            angle = np.random.uniform(0, 2 * np.pi)
            speed = np.random.uniform(0, velocity_range)
            vx = speed * np.cos(angle)
            vy = speed * np.sin(angle)
            size = np.random.uniform(size_range[0], size_range[1])

            particle = Particle(
                x=x, y=y, vx=vx, vy=vy, life=1.0, color=color, size=size
            )
            self.particles.append(particle)

    def emit_burst(
        self,
        x: float,
        y: float,
        count: int = 50,
        color: Tuple[int, int, int] = (255, 255, 255),
    ) -> None:
        """Create a burst effect at a point.

        Args:
            x: X position
            y: Y position
            count: Number of particles
            color: Particle color
        """
        self.emit_particles(x, y, count, color, velocity_range=8.0)

    def emit_confetti(
        self,
        x: float,
        y: float,
        colors: List[Tuple[int, int, int]] = None,
        count: int = 100,
    ) -> None:
        """Create a confetti effect.

        Args:
            x: X position
            y: Y position
            colors: List of colors for confetti
            count: Number of particles
        """
        if colors is None:
            colors = [
                (255, 0, 0),
                (0, 255, 0),
                (0, 0, 255),
                (255, 255, 0),
                (255, 0, 255),
                (0, 255, 255),
            ]

        for _ in range(count):
            color = colors[np.random.randint(0, len(colors))]
            angle = np.random.uniform(0, 2 * np.pi)
            speed = np.random.uniform(2, 10)
            vx = speed * np.cos(angle)
            vy = speed * np.sin(angle) - 5  # Initial upward velocity

            particle = Particle(
                x=x,
                y=y,
                vx=vx,
                vy=vy,
                life=1.0,
                color=color,
                size=np.random.uniform(4.0, 12.0),
            )
            self.particles.append(particle)

    def emit_rain(
        self,
        count: int = 200,
        color: Tuple[int, int, int] = (100, 150, 255),
    ) -> None:
        """Create a rain effect across the top.

        Args:
            count: Number of particles
            color: Particle color
        """
        for _ in range(count):
            x = np.random.uniform(0, self.width)
            y = np.random.uniform(-100, 0)
            vx = np.random.uniform(-2, 2)
            vy = np.random.uniform(5, 15)

            particle = Particle(
                x=x, y=y, vx=vx, vy=vy, life=1.0, color=color, size=1.0
            )
            self.particles.append(particle)

    def update(self, dt: float = 1.0 / 30.0) -> None:
        """Update all particles.

        Args:
            dt: Delta time in seconds
        """
        particles_to_remove = []

        for particle in self.particles:
            # Apply physics
            particle.vy += self.gravity
            particle.vx *= self.friction
            particle.vy *= self.friction

            # Update position
            particle.x += particle.vx
            particle.y += particle.vy

            # Decrease life
            particle.life -= 0.02

            # Remove dead particles
            if particle.life <= 0 or particle.y > self.height + 100:
                particles_to_remove.append(particle)

        # Remove dead particles
        for particle in particles_to_remove:
            self.particles.remove(particle)

    def get_particles_as_dict(self) -> List[Dict]:
        """Get particles as dictionaries for rendering.

        Returns:
            List of particle dictionaries
        """
        return [
            {
                "x": particle.x,
                "y": particle.y,
                "color": particle.color,
                "size": particle.size,
                "opacity": particle.life,
            }
            for particle in self.particles
        ]

    def clear(self) -> None:
        """Clear all particles."""
        self.particles.clear()
