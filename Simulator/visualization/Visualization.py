import pygame
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class Visualization:
    def __init__(self):
        pygame.init()
        self.display = (800, 600)
        pygame.display.set_mode(self.display, pygame.DOUBLEBUF | pygame.OPENGL)
        self.init_opengl()

    def init_opengl(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (self.display[0] / self.display[1]), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        glTranslatef(0.0, 0.0, -5)

    def draw_particle_trace(self, particle):
        glBegin(GL_LINE_STRIP)
        glColor3f(1, 0, 0)  # Set color to red
        glVertex3f(particle.x, particle.y, particle.z)
        glEnd()
        print("CHeck")

    def render_particles(self, particles):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        for particle in particles:
            glPushMatrix()
            glTranslatef(particle.x, particle.y, particle.z)
            glutSolidSphere(particle.weight * 0.1, 20, 20)  # Adjust sphere size based on weight
            glPopMatrix()
            self.draw_particle_trace(particle)
        pygame.display.flip()
        
        pygame.time.wait(10)
