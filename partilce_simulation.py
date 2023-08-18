import pygame
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *

# Particle class to store particle properties
class Particle:
    def __init__(self, x, y, vx, vy, weight):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.weight = weight

# Initialize particle list
num_particles = 2
particles = [Particle(np.random.random(), np.random.random(), 0.01 * (np.random.random() - 0.5), 0.01 * (np.random.random() - 0.5), np.random.uniform(0.1, 2.0)) for _ in range(num_particles)]

# Initialize Pygame
pygame.init()

# Set window dimensions
width, height = 1000 , 800

# Create a windowed mode window and set display flags
display = (width, height)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# Set OpenGL viewport
glViewport(0, 0, width, height)

# Main simulation loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Gravitational Effects
    G = 0.0005  # Gravitational constant

    for particle1 in particles:
        for particle2 in particles:
            if particle1 != particle2:
                dx = particle2.x - particle1.x
                dy = particle2.y - particle1.y
                distance = max(np.sqrt(dx**2 + dy**2), 0.1)
                force = (G * particle1.weight * particle2.weight) / (distance ** 2)
                angle = np.arctan2(dy, dx)
                
                particle1.vx += force * np.cos(angle) / particle1.weight
                particle1.vy += force * np.sin(angle) / particle1.weight

    # Update particle positions and velocities
    for particle in particles:
        particle.x += particle.vx
        particle.y += particle.vy

        # Bounce off borders
        if particle.x <= 0 or particle.x >= 1:
            particle.vx *= -1
        if particle.y <= 0 or particle.y >= 1:
            particle.vy *= -1
            
    # Draw particles as points using OpenGL
    glPointSize(3)
    glBegin(GL_POINTS)
    for particle in particles:
        glVertex2f(particle.x * 2 - 1, particle.y * 2 - 1)  # Adjust coordinates to match OpenGL range
    glEnd()
    pygame.display.flip()
    pygame.time.wait(80)
