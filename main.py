import pygame
import sys
import math

# Window size
WIDTH, HEIGHT = 800, 600

# Colors
BG_COLOR = (200, 240, 200)
BUILDING_COLOR = (180, 180, 230)
CANTEEN_COLOR = (240, 220, 160)
CARPARK_COLOR = (120, 120, 120)
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

def draw_map(screen):
    screen.fill(BG_COLOR)
    # Draw buildings
    for rect in buildings:
        pygame.draw.rect(screen, BUILDING_COLOR, rect)
    # Draw canteen
    pygame.draw.rect(screen, CANTEEN_COLOR, canteen)
    # Draw car park
    pygame.draw.rect(screen, CARPARK_COLOR, carpark)

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
