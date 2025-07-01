import pygame
import sys
import math

# Window size
WIDTH, HEIGHT = 800, 600

# Colors
BG_COLOR = (200, 240, 200)
BUILDING_COLOR = (180, 180, 230)
BUILDING_WINDOW = (200, 220, 255)
BUILDING_DOOR = (120, 80, 40)
CANTEEN_COLOR = (240, 220, 160)
CANTEEN_WINDOW = (255, 255, 255)
CANTEEN_DOOR = (180, 120, 60)
CANTEEN_SIGN = (200, 80, 80)
CARPARK_COLOR = (120, 120, 120)
CARPARK_LINE = (255, 255, 180)
CARPARK_BORDER = (80, 80, 80)
WALL_COLOR = (100, 100, 100)
PATH_COLOR = (180, 170, 120)
TREE_COLOR = (60, 180, 60)
MOVER_COLOR = (255, 180, 60)
MOVER_OUTLINE = (200, 100, 0)

# Map objects (x, y, w, h)
buildings = [
    (150, 100, 120, 240),  # Building 1
    (530, 100, 120, 240),  # Building 2
]
canteen = (340, 400, 120, 60)
carpark = (340, 500, 120, 60)

# Mover (pizza slice)
mover_pos = [WIDTH // 2, HEIGHT // 2]
mover_speed = 4
mover_size = 24
mover_angle = 0  # 0=up, 90=right, 180=down, 270=left

def draw_windows(screen, rect, rows, cols, color):
    x, y, w, h = rect
    margin_x = w // (cols + 1)
    margin_y = h // (rows + 1)
    win_w, win_h = margin_x // 2, margin_y // 2
    for row in range(rows):
        for col in range(cols):
            wx = x + margin_x * (col + 1) - win_w // 2
            wy = y + margin_y * (row + 1) - win_h // 2
            pygame.draw.rect(screen, color, (wx, wy, win_w, win_h))

def draw_door(screen, rect, color):
    x, y, w, h = rect
    door_w, door_h = w // 5, h // 8
    dx = x + w // 2 - door_w // 2
    dy = y + h - door_h - 4
    pygame.draw.rect(screen, color, (dx, dy, door_w, door_h))

def draw_building(screen, rect):
    pygame.draw.rect(screen, BUILDING_COLOR, rect, border_radius=8)
    draw_windows(screen, rect, 5, 3, BUILDING_WINDOW)
    draw_door(screen, rect, BUILDING_DOOR)

def draw_canteen(screen, rect):
    pygame.draw.rect(screen, CANTEEN_COLOR, rect, border_radius=8)
    draw_windows(screen, rect, 2, 3, CANTEEN_WINDOW)
    draw_door(screen, rect, CANTEEN_DOOR)
    # Draw sign
    x, y, w, h = rect
    sign_rect = (x + w//4, y - 18, w//2, 18)
    pygame.draw.rect(screen, CANTEEN_SIGN, sign_rect, border_radius=6)
    font = pygame.font.SysFont(None, 18)
    text = font.render('CANTEEN', True, (255,255,255))
    screen.blit(text, (sign_rect[0] + 8, sign_rect[1] + 2))

def draw_carpark(screen, rect):
    x, y, w, h = rect
    pygame.draw.rect(screen, CARPARK_COLOR, rect, border_radius=6)
    # Draw parking lines
    n_lines = 5
    for i in range(1, n_lines):
        px = x + i * w // n_lines
        pygame.draw.line(screen, CARPARK_LINE, (px, y + 8), (px, y + h - 8), 3)
    # Draw border
    pygame.draw.rect(screen, CARPARK_BORDER, rect, 4, border_radius=6)
    # Draw 'P' sign
    font = pygame.font.SysFont(None, 32)
    text = font.render('P', True, (255,255,255))
    screen.blit(text, (x + w - 32, y + 8))

def draw_walls(screen):
    # Outer campus wall
    pygame.draw.rect(screen, WALL_COLOR, (100, 60, 600, 520), 8, border_radius=16)
    # Car park wall
    pygame.draw.rect(screen, WALL_COLOR, (carpark[0]-8, carpark[1]-8, carpark[2]+16, carpark[3]+16), 4, border_radius=8)

def draw_path(screen):
    # Main path from canteen to buildings
    pygame.draw.rect(screen, PATH_COLOR, (390, 400, 20, 100))
    pygame.draw.rect(screen, PATH_COLOR, (210, 220, 400, 20))

def draw_trees(screen):
    # Draw some trees for decoration
    for (tx, ty) in [(130, 90), (670, 90), (130, 540), (670, 540), (400, 80), (400, 560)]:
        pygame.draw.circle(screen, TREE_COLOR, (tx, ty), 18)

def draw_map(screen):
    screen.fill(BG_COLOR)
    draw_path(screen)
    draw_walls(screen)
    draw_trees(screen)
    # Draw buildings
    for rect in buildings:
        draw_building(screen, rect)
    # Draw canteen
    draw_canteen(screen, canteen)
    # Draw car park
    draw_carpark(screen, carpark)

def draw_mover(screen, pos, angle):
    x, y = pos
    # Pizza slice triangle points
    points = [
        (x, y - mover_size),  # tip
        (x - mover_size//2, y + mover_size//2),
        (x + mover_size//2, y + mover_size//2),
    ]
    # Rotate points
    rotated = []
    for px, py in points:
        dx, dy = px - x, py - y
        rad = angle * math.pi / 180
        rx = dx * math.cos(rad) - dy * math.sin(rad)
        ry = dx * math.sin(rad) + dy * math.cos(rad)
        rotated.append((x + rx, y + ry))
    pygame.draw.polygon(screen, MOVER_COLOR, rotated)
    pygame.draw.polygon(screen, MOVER_OUTLINE, rotated, 2)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('UIT Map Simulation (2D)')
    clock = pygame.time.Clock()

    global mover_pos, mover_angle

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

        draw_map(screen)
        draw_mover(screen, mover_pos, mover_angle)
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
