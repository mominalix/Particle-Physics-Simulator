import pygame
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Particle class to store particle properties
class Particle:
    def __init__(self, x, y, z, vx, vy, vz, weight):
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.weight = weight

# Initialize particle list
num_particles = 2
particles = [Particle(np.random.random(), np.random.random(), np.random.random(), # Positions
                      #0.01 * (np.random.random() - 0.2), 0.01 * (np.random.random() - 0.2), 0.01 * (np.random.random() - 0.2),  # Velocities
                      0.001,0.001,0.001,
                      np.random.uniform(0.1, 2.0)) for _ in range(num_particles)] # Weights

# Initialize Pygame
pygame.init()

# Set window dimensions
width, height = 1000, 800

# Create a windowed mode window and set display flags
display = (width, height)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
pygame.mouse.set_visible(True)  # Hide the mouse cursor

# Set perspective projection
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

# Move the camera back
glMatrixMode(GL_MODELVIEW)
glTranslatef(0.0, 0.0, -5)

# Variables for mouse interaction
prev_mouse_x, prev_mouse_y = 0, 0
rotate_x, rotate_y = 0, 0
dragging = False  # Flag to indicate if mouse dragging is active

# Main simulation loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                prev_mouse_x, prev_mouse_y = pygame.mouse.get_pos()
                dragging = True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                dragging = False
                rotate_x, rotate_y = 0, 0  # Reset rotation angles


    if dragging:  # Perform camera rotation only when dragging
        mouse_x, mouse_y = pygame.mouse.get_pos()
        delta_x = mouse_x - prev_mouse_x
        delta_y = mouse_y - prev_mouse_y
        rotate_x += delta_y * 0.01  # Adjust the sensitivity here
        rotate_y += delta_x * 0.01
        prev_mouse_x, prev_mouse_y = mouse_x, mouse_y

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Gravitational Effects
    G = 0.0005  # Gravitational constant

    for particle1 in particles:
        for particle2 in particles:
            if particle1 != particle2:
                dx = particle2.x - particle1.x
                dy = particle2.y - particle1.y
                dz = particle2.z - particle1.z
                distance = max(np.sqrt(dx**2 + dy**2 + dz**2), 0.1)
                force = (G * particle1.weight * particle2.weight) / (distance ** 2)
                angle = np.arctan2(dy, dx)
                angle_z = np.arctan2(dz, np.sqrt(dx**2 + dy**2))
                
                particle1.vx += force * np.cos(angle) / particle1.weight
                particle1.vy += force * np.sin(angle) / particle1.weight
                particle1.vz += force * np.sin(angle_z) / particle1.weight

    # Update particle positions and velocities
    for particle in particles:
        particle.x += particle.vx
        particle.y += particle.vy
        particle.z += particle.vz

        # Bounce off borders
        if particle.x <= -2 or particle.x >= 2:
            particle.vx *= -1
        if particle.y <= -2 or particle.y >= 2:
            particle.vy *= -1
        if particle.z <= -2 or particle.z >= 2:
            particle.vz *= -1
            
    # Draw particles as points using OpenGL
    glPointSize(5)  # Adjust point size here
    glColor3f(1, 1, 1)
    glBegin(GL_POINTS)
    for particle in particles:
        glVertex3f(particle.x, particle.y, particle.z)
    glEnd()


    # Draw grid boundary
    glLineWidth(1)  # Adjust line width here
    glColor3f(0.5, 0.5, 0.5)  # Set color to gray
    glBegin(GL_LINES)
    for i in range(-2, 3):  # Draw lines along x, y, and z axes
        glVertex3f(i, -2, -2)
        glVertex3f(i, -2, 2)
        glVertex3f(i, -2, -2)
        glVertex3f(i, 2, -2)
        glVertex3f(-2, -2, i)
        glVertex3f(2, -2, i)
    glEnd()
    
    # Draw axis lines
    glBegin(GL_LINES)
    glColor3f(1, 0, 0)  # Red X-axis
    glVertex3f(0, 0, 0)
    glVertex3f(1, 0, 0)
    glColor3f(0, 1, 0)  # Green Y-axis
    glVertex3f(0, 0, 0)
    glVertex3f(0, 1, 0)
    glColor3f(0, 0, 1)  # Blue Z-axis
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, 1)
    glEnd()

    # Apply rotation based on mouse movement
    glRotatef(rotate_x, 1, 0, 0)
    glRotatef(rotate_y, 0, 1, 0)

    pygame.display.flip()
    pygame.time.wait(10)
