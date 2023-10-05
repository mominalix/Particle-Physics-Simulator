import pygame
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Initialize a list to store particle's previous positions
first_particle_trace = []

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
        self.gravitational_force = [0.0, 0.0, 0.0]  # Initialize gravitational force

# Initialize particle list
num_particles = 20
particles = [Particle(np.random.random(), np.random.random(), np.random.random(), 
                      0.01 * (np.random.random() - 0.2), 0.01 * (np.random.random() - 0.2), 0.01 * (np.random.random() - 0.2),  
                      np.random.uniform(1, 5.0)) for _ in range(num_particles)]

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
camera_z = -20

# Default camera position
default_camera_z = -5

# Camera transition speed
camera_transition_speed = 0.1

# Rotation transition speed
rotation_transition_speed = 0.01

# Default rotation angles
default_rotate_x, default_rotate_y = 0, 0
angle_x, angle_y = 0, 0

# Initialize transitioning variables
transitioning_camera = False
transitioning_rotation = False

# Target rotation angles
target_rotate_x, target_rotate_y = 0, 0

# Move the camera back
glMatrixMode(GL_MODELVIEW)
glTranslatef(0.0, 0.0, -5)

# Variables for mouse interaction
prev_mouse_x, prev_mouse_y = 0, 0
rotate_x, rotate_y = 95, 0
dragging = False  # Flag to indicate if mouse dragging is active

# Bounding box dimensions
box_min = -5
box_max = 5

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
            
            # Zoom in
            elif event.button == 4:  # Scroll up
                camera_z += 0.5

            # Zoom out
            elif event.button == 5:  # Scroll down
                camera_z -= 0.5

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                dragging = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # Press 'r' key
                transitioning_camera = True
                transitioning_rotation = True
                target_camera_z = default_camera_z
                target_rotate_x = 0
                target_rotate_y = 0

    if dragging:  # Perform camera rotation only when dragging
        mouse_x, mouse_y = pygame.mouse.get_pos()
        delta_x = mouse_x - prev_mouse_x
        delta_y = mouse_y - prev_mouse_y
        
        # Update rotation angles within the range of -pi to +pi radians
        rotate_x = np.clip(delta_y * 0.05, -np.pi, np.pi)
        rotate_y = np.clip(delta_x * 0.05, -np.pi, np.pi)
        angle_x += rotate_x
        angle_y += rotate_y

        # Reset Angles to 0 when limit crossed
        if rotate_x == np.pi or rotate_x == -np.pi:
            rotate_x = 0
        if rotate_y == np.pi or rotate_y == -np.pi:
            rotate_y = 0
        prev_mouse_x, prev_mouse_y = mouse_x, mouse_y
        # Apply rotation based on mouse movement
        if delta_y != 0 or delta_x != 0:
            glRotatef(rotate_x, 1, 0, 0)
            glRotatef(rotate_y, 0, 1, 0)
        
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    # Camera transition
    if transitioning_camera:
        if abs(camera_z - target_camera_z) < camera_transition_speed:
            camera_z = target_camera_z
            transitioning_camera = False
        elif camera_z < target_camera_z:
            camera_z += camera_transition_speed
        else:
            camera_z -= camera_transition_speed
        

    # Rotation transition
    if transitioning_rotation:
        glRotatef(-angle_x , 1, 0, 0)
        glRotatef(-angle_y, 0, 1, 0)
        transitioning_rotation = False
        angle_x, angle_y = 0, 0

    # Set perspective projection with zoom
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, camera_z)  # Apply zoom

    # Draw grid boundary
    glLineWidth(1)  # Adjust line width here
    glColor3f(0.2, 0.2, 0.2)  # Set color to gray
    glBegin(GL_LINES)
    for i in range(-5, 6):
        glVertex3f(i, box_min, box_min)
        glVertex3f(i, box_min, box_max)
        glVertex3f(i, box_min, box_min)
        glVertex3f(i, box_max, box_min)
        glVertex3f(box_min, box_min, i)
        glVertex3f(box_max, box_min, i)
        
        glVertex3f(i, box_max, box_max)  # Draw lines on the top face
        glVertex3f(i, box_min, box_max)
        glVertex3f(i, box_max, box_max)
        glVertex3f(i, box_max, box_min)

        glVertex3f(box_max, i, box_max)  # Draw lines on the right face
        glVertex3f(box_min, i, box_max)
        glVertex3f(box_max, i, box_max)
        glVertex3f(box_max, i, box_min)
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

    # Switch back to model view matrix
    glMatrixMode(GL_MODELVIEW)

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
                
                particle1.gravitational_force[0] += force * np.cos(angle)
                particle1.gravitational_force[1] += force * np.sin(angle)
                particle1.gravitational_force[2] += force * np.sin(angle_z)

    # Update particle positions and velocities
    for particle_index, particle in enumerate(particles):
        particle.x += particle.vx
        particle.y += particle.vy
        particle.z += particle.vz

        # Bounce off borders
        if particle.x <= box_min or particle.x >= box_max:
            particle.vx *= -1
        if particle.y <= box_min or particle.y >= box_max:
            particle.vy *= -1
        if particle.z <= box_min or particle.z >= box_max:
            particle.vz *= -1

        # Update particle's trace positions
        if particle_index == 0:
            if len(first_particle_trace) >= 1000:  # Limit the number of trace points
                first_particle_trace.pop(0)
            first_particle_trace.append((particle.x, particle.y, particle.z))

        # Apply gravitational forces to update velocities
        particle.vx += particle.gravitational_force[0] / particle.weight
        particle.vy += particle.gravitational_force[1] / particle.weight
        particle.vz += particle.gravitational_force[2] / particle.weight

    # Draw particles as spheres
    for particle in particles:
        glPushMatrix()
        glTranslatef(particle.x, particle.y, particle.z)
        glColor3f(0.5 * particle.weight, 1, 0.2 * particle.weight)
        sphere_radius = particle.weight * 0.1  # Adjust sphere size based on weight
        sphere_slices = 20
        sphere_stacks = 20
        quadric = gluNewQuadric()  # Create a new quadric object
        gluSphere(quadric, sphere_radius, sphere_slices, sphere_stacks)  # Render the sphere
        gluDeleteQuadric(quadric)  # Delete the quadric object
        glPopMatrix()

    # Draw particle trace line
    glLineWidth(1)  # Adjust line width here
    glColor3f(1, 0, 0)  # Set color to red
    glBegin(GL_LINE_STRIP)
    for trace_point in first_particle_trace:
        glVertex3f(*trace_point)
    glEnd()

    pygame.display.flip()
    pygame.time.wait(20)
