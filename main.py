import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import glutInit, glutWireCube
import numpy as np

# Window size
WIDTH, HEIGHT = 800, 600

# Camera settings
camera_pos = [0.0, 1.0, 10.0]  # x, y, z
camera_front = [0.0, 0.0, -1.0]
camera_up = [0.0, 1.0, 0.0]
speed = 0.2

def draw_cube(x, y, z, w, h, d, color):
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(w, h, d)
    glColor3fv(color)
    glutWireCube(1)
    glPopMatrix()

def draw_scene():
    # Ground
    glColor3f(0.6, 0.8, 0.6)
    glBegin(GL_QUADS)
    glVertex3f(-50, 0, -50)
    glVertex3f(-50, 0, 50)
    glVertex3f(50, 0, 50)
    glVertex3f(50, 0, -50)
    glEnd()

    # Buildings (two 6-story blocks)
    draw_cube(-10, 3, 0, 8, 6, 8, (0.7, 0.7, 0.9))
    draw_cube(10, 3, 0, 8, 6, 8, (0.7, 0.7, 0.9))

    # Canteen
    draw_cube(0, 1, 15, 6, 2, 6, (0.9, 0.8, 0.6))

    # Underground car park (drawn as a sunken cube)
    draw_cube(0, -1, -15, 10, 2, 10, (0.5, 0.5, 0.5))

def main():
    pygame.init()
    pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption('UIT Map Simulation')

    glutInit()
    gluPerspective(60, WIDTH / HEIGHT, 0.1, 100.0)
    glEnable(GL_DEPTH_TEST)

    clock = pygame.time.Clock()
    running = True
    global camera_pos

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        keys = pygame.key.get_pressed()
        front = np.array(camera_front)
        right = np.cross(front, camera_up)
        right = right / np.linalg.norm(right)
        if keys[K_w]:
            camera_pos[0] += front[0] * speed
            camera_pos[2] += front[2] * speed
        if keys[K_s]:
            camera_pos[0] -= front[0] * speed
            camera_pos[2] -= front[2] * speed
        if keys[K_a]:
            camera_pos[0] -= right[0] * speed
            camera_pos[2] -= right[2] * speed
        if keys[K_d]:
            camera_pos[0] += right[0] * speed
            camera_pos[2] += right[2] * speed

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2],
                  camera_pos[0] + camera_front[0], camera_pos[1], camera_pos[2] + camera_front[2],
                  camera_up[0], camera_up[1], camera_up[2])
        draw_scene()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main() 