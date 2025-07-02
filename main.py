import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import sys
import math
import numpy as np
from PIL import Image

# Window size
WIDTH, HEIGHT = 800, 600

# Colors (RGB values 0-1 for OpenGL)
BG_COLOR = (0.78, 0.94, 0.78)
BUILDING_COLOR = (0.71, 0.71, 0.90)
BUILDING_WINDOW = (0.78, 0.86, 1.0)
BUILDING_DOOR = (0.47, 0.31, 0.16)
CANTEEN_COLOR = (0.94, 0.86, 0.63)
CANTEEN_WINDOW = (1.0, 1.0, 1.0)
CANTEEN_DOOR = (0.71, 0.47, 0.24)
CANTEEN_SIGN = (0.78, 0.31, 0.31)
CARPARK_COLOR = (0.47, 0.47, 0.47)
CARPARK_LINE = (1.0, 1.0, 0.71)
CARPARK_BORDER = (0.31, 0.31, 0.31)
WALL_COLOR = (0.39, 0.39, 0.39)
PATH_COLOR = (0.71, 0.67, 0.47)
TREE_COLOR = (0.24, 0.71, 0.24)

# Map objects (x, y, w, h)
buildings = [
    (150, 100, 120, 240),  # Building 1
    (530, 100, 120, 240),  # Building 2
]
canteen = (340, 400, 120, 60)
carpark = (340, 500, 120, 60)

# Mover (human)
mover_pos = [WIDTH // 2, HEIGHT // 2]
mover_speed = 4
mover_size = 24
mover_angle = 0  # 0=up, 90=right, 180=down, 270=left

# Texture ID for human image
human_texture = None

def load_texture(filename):
    """Load texture from image file"""
    image = Image.open(filename)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = image.convert("RGBA").tobytes()
    
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    return texture_id

def draw_rect(x, y, w, h, color):
    """Draw a colored rectangle"""
    glColor3f(*color)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + w, y)
    glVertex2f(x + w, y + h)
    glVertex2f(x, y + h)
    glEnd()
    glColor3f(1.0, 1.0, 1.0)  # Reset color

def draw_rect_outline(x, y, w, h, color, thickness=1):
    """Draw a rectangle outline"""
    glColor3f(*color)
    glLineWidth(thickness)
    glBegin(GL_LINE_LOOP)
    glVertex2f(x, y)
    glVertex2f(x + w, y)
    glVertex2f(x + w, y + h)
    glVertex2f(x, y + h)
    glEnd()
    glColor3f(1.0, 1.0, 1.0)  # Reset color

def draw_circle(x, y, radius, color):
    """Draw a filled circle"""
    glColor3f(*color)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x, y)
    segments = 32
    for i in range(segments + 1):
        angle = 2.0 * math.pi * i / segments
        glVertex2f(x + radius * math.cos(angle), y + radius * math.sin(angle))
    glEnd()
    glColor3f(1.0, 1.0, 1.0)  # Reset color

def draw_windows(x, y, w, h, rows, cols, color):
    """Draw windows on a building"""
    margin_x = w // (cols + 1)
    margin_y = h // (rows + 1)
    win_w, win_h = margin_x // 2, margin_y // 2
    for row in range(rows):
        for col in range(cols):
            wx = x + margin_x * (col + 1) - win_w // 2
            wy = y + margin_y * (row + 1) - win_h // 2
            draw_rect(wx, wy, win_w, win_h, color)

def draw_door(x, y, w, h, color):
    """Draw a door on a building"""
    door_w, door_h = w // 5, h // 8
    dx = x + w // 2 - door_w // 2
    dy = y + h - door_h - 4
    draw_rect(dx, dy, door_w, door_h, color)

def draw_building(rect):
    """Draw a building with windows and door"""
    x, y, w, h = rect
    draw_rect(x, y, w, h, BUILDING_COLOR)
    draw_windows(x, y, w, h, 5, 3, BUILDING_WINDOW)
    draw_door(x, y, w, h, BUILDING_DOOR)

def draw_canteen(rect):
    """Draw the canteen building"""
    x, y, w, h = rect
    draw_rect(x, y, w, h, CANTEEN_COLOR)
    draw_windows(x, y, w, h, 2, 3, CANTEEN_WINDOW)
    draw_door(x, y, w, h, CANTEEN_DOOR)
    # Draw sign
    sign_rect = (x + w//4, y - 18, w//2, 18)
    draw_rect(*sign_rect, CANTEEN_SIGN)

def draw_carpark(rect):
    """Draw the car park"""
    x, y, w, h = rect
    draw_rect(x, y, w, h, CARPARK_COLOR)
    # Draw parking lines
    n_lines = 5
    glColor3f(*CARPARK_LINE)
    glLineWidth(3)
    for i in range(1, n_lines):
        px = x + i * w // n_lines
        glBegin(GL_LINES)
        glVertex2f(px, y + 8)
        glVertex2f(px, y + h - 8)
        glEnd()
    # Draw border
    draw_rect_outline(x, y, w, h, CARPARK_BORDER, 4)

def draw_walls():
    """Draw campus walls"""
    # Outer campus wall
    draw_rect_outline(100, 60, 600, 520, WALL_COLOR, 8)
    # Car park wall
    draw_rect_outline(carpark[0]-8, carpark[1]-8, carpark[2]+16, carpark[3]+16, WALL_COLOR, 4)

def draw_path():
    """Draw paths"""
    # Main path from canteen to buildings
    draw_rect(390, 400, 20, 100, PATH_COLOR)
    draw_rect(210, 220, 400, 20, PATH_COLOR)

def draw_trees():
    """Draw decorative trees"""
    tree_positions = [(130, 90), (670, 90), (130, 540), (670, 540), (400, 80), (400, 560)]
    for (tx, ty) in tree_positions:
        draw_circle(tx, ty, 18, TREE_COLOR)

def draw_human(x, y, angle):
    """Draw the human sprite using texture"""
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, human_texture)
    
    # Calculate sprite corners
    half_size = mover_size // 2
    corners = [
        (-half_size, -half_size),
        (half_size, -half_size),
        (half_size, half_size),
        (-half_size, half_size)
    ]
    
    # Rotate corners
    rad = math.radians(angle)
    cos_a, sin_a = math.cos(rad), math.sin(rad)
    
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex2f(x + corners[0][0] * cos_a - corners[0][1] * sin_a,
               y + corners[0][0] * sin_a + corners[0][1] * cos_a)
    glTexCoord2f(1.0, 0.0)
    glVertex2f(x + corners[1][0] * cos_a - corners[1][1] * sin_a,
               y + corners[1][0] * sin_a + corners[1][1] * cos_a)
    glTexCoord2f(1.0, 1.0)
    glVertex2f(x + corners[2][0] * cos_a - corners[2][1] * sin_a,
               y + corners[2][0] * sin_a + corners[2][1] * cos_a)
    glTexCoord2f(0.0, 1.0)
    glVertex2f(x + corners[3][0] * cos_a - corners[3][1] * sin_a,
               y + corners[3][0] * sin_a + corners[3][1] * cos_a)
    glEnd()
    
    glDisable(GL_TEXTURE_2D)

def draw_map():
    """Draw the entire map"""
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    
    # Set up 2D orthographic projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, WIDTH, HEIGHT, 0)
    glMatrixMode(GL_MODELVIEW)
    
    # Draw background
    glClearColor(*BG_COLOR, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    
    draw_path()
    draw_walls()
    draw_trees()
    
    # Draw buildings
    for rect in buildings:
        draw_building(rect)
    
    # Draw canteen
    draw_canteen(canteen)
    
    # Draw car park
    draw_carpark(carpark)

def main():
    global human_texture, mover_pos, mover_angle
    
    pygame.init()
    pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption('UIT Map Simulation (OpenGL)')
    clock = pygame.time.Clock()
    
    # Load human texture
    try:
        human_texture = load_texture('human.png')
    except Exception as e:
        print(f"Error loading human.png: {e}")
        print("Make sure human.png exists in the current directory")
        pygame.quit()
        sys.exit(1)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        keys = pygame.key.get_pressed()
        move = [0, 0]
        if keys[pygame.K_w]:
            move[1] -= mover_speed
            mover_angle = 0
        if keys[pygame.K_s]:
            move[1] += mover_speed
            mover_angle = 180
        if keys[pygame.K_a]:
            move[0] -= mover_speed
            mover_angle = 270
        if keys[pygame.K_d]:
            move[0] += mover_speed
            mover_angle = 90
        
        mover_pos[0] += move[0]
        mover_pos[1] += move[1]
        
        # Keep in bounds
        mover_pos[0] = max(mover_size, min(WIDTH - mover_size, mover_pos[0]))
        mover_pos[1] = max(mover_size, min(HEIGHT - mover_size, mover_pos[1]))
        
        draw_map()
        draw_human(mover_pos[0], mover_pos[1], mover_angle)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
