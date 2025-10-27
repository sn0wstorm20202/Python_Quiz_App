"""
Confetti Animation Module
Creates celebratory confetti animation using Tkinter Canvas
"""

import tkinter as tk
import random
import math


class ConfettiParticle:
    """Single confetti particle"""
    
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-8, -4)
        self.gravity = 0.3
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-15, 15)
        self.size = random.randint(6, 12)
        
        # Random color
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', 
                  '#F7DC6F', '#BB8FCE', '#85C1E2', '#F8B739', '#52B788']
        self.color = random.choice(colors)
        
        # Create confetti shape (oval or rectangle)
        shape_type = random.choice(['oval', 'rect'])
        if shape_type == 'oval':
            self.shape = canvas.create_oval(
                x, y, x + self.size, y + self.size,
                fill=self.color, outline=''
            )
        else:
            self.shape = canvas.create_rectangle(
                x, y, x + self.size, y + self.size // 2,
                fill=self.color, outline=''
            )
    
    def update(self):
        """Update particle position and rotation"""
        # Update velocity
        self.vy += self.gravity
        
        # Update position
        self.x += self.vx
        self.y += self.vy
        
        # Update rotation
        self.rotation += self.rotation_speed
        
        # Move on canvas
        self.canvas.coords(
            self.shape,
            self.x, self.y,
            self.x + self.size, self.y + self.size
        )
        
        # Check if off screen
        canvas_height = self.canvas.winfo_height()
        return self.y < canvas_height + 20
    
    def destroy(self):
        """Remove particle from canvas"""
        self.canvas.delete(self.shape)


class ConfettiAnimation:
    """Manages confetti animation"""
    
    def __init__(self, parent_frame, duration=3000):
        """
        Initialize confetti animation
        
        Args:
            parent_frame: Parent tkinter frame
            duration: Animation duration in milliseconds
        """
        self.parent = parent_frame
        self.duration = duration
        self.particles = []
        self.animation_id = None
        
        # Create transparent canvas overlay
        self.canvas = tk.Canvas(
            parent_frame,
            bg=parent_frame.cget('bg'),
            highlightthickness=0
        )
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.start_time = None
    
    def start(self):
        """Start confetti animation"""
        self.start_time = self.canvas.after(0)
        
        # Create initial burst of particles
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        # Create particles from multiple points
        spawn_points = [
            (width * 0.2, height * 0.2),
            (width * 0.5, height * 0.2),
            (width * 0.8, height * 0.2),
        ]
        
        for spawn_x, spawn_y in spawn_points:
            for _ in range(30):
                particle = ConfettiParticle(
                    self.canvas,
                    spawn_x + random.randint(-50, 50),
                    spawn_y
                )
                self.particles.append(particle)
        
        # Start animation loop
        self.animate()
    
    def animate(self):
        """Animation loop"""
        # Update all particles
        active_particles = []
        
        for particle in self.particles:
            if particle.update():
                active_particles.append(particle)
            else:
                particle.destroy()
        
        self.particles = active_particles
        
        # Continue animation if particles exist and duration not exceeded
        if self.particles:
            self.animation_id = self.canvas.after(30, self.animate)
        else:
            self.stop()
    
    def stop(self):
        """Stop animation and cleanup"""
        if self.animation_id:
            self.canvas.after_cancel(self.animation_id)
        
        # Remove all particles
        for particle in self.particles:
            particle.destroy()
        
        self.particles = []
        
        # Destroy canvas after a brief delay
        self.canvas.after(500, self.canvas.destroy)


def show_confetti(parent_frame, duration=3000):
    """
    Show confetti animation on a frame
    
    Args:
        parent_frame: Parent tkinter frame
        duration: Animation duration in milliseconds
    """
    animation = ConfettiAnimation(parent_frame, duration)
    animation.start()
    return animation
