import pygame
import random

# Initialize Pygame
pygame.init()

# Custom events
SPRITE_COLOR_CHANGE_EVENT = pygame.USEREVENT + 1
BACKGROUND_COLOR_CHANGE_EVENT = pygame.USEREVENT + 2

# Define colors
BLUE = pygame.Color('blue')
LIGHTBLUE = pygame.Color('lightblue')
DARKBLUE = pygame.Color('darkblue')

YELLOW = pygame.Color('yellow')
MAGENTA = pygame.Color('magenta')
ORANGE = pygame.Color('orange')
WHITE = pygame.Color('white')

# --- Sprite setup (No class used) ---
sprite_width = 30
sprite_height = 20
sprite_color = WHITE
sprite = pygame.Surface([sprite_width, sprite_height])
sprite.fill(sprite_color)
sprite_rect = sprite.get_rect()

# Random start position
sprite_rect.x = random.randint(0, 480)
sprite_rect.y = random.randint(0, 370)

# Random initial direction
velocity = [random.choice([-1, 1]), random.choice([-1, 1])]

# Background setup
bg_color = BLUE

# Window setup
screen = pygame.display.set_mode((500, 400))
pygame.display.set_caption("Colorful Bounce")

clock = pygame.time.Clock()
running = True


# Function to change sprite color
def change_sprite_color():
    global sprite_color
    sprite_color = random.choice([YELLOW, MAGENTA, ORANGE, WHITE])
    sprite.fill(sprite_color)


# Function to change background color
def change_background_color():
    global bg_color
    bg_color = random.choice([BLUE, LIGHTBLUE, DARKBLUE])


# --- Main Game Loop ---
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == SPRITE_COLOR_CHANGE_EVENT:
            change_sprite_color()
        elif event.type == BACKGROUND_COLOR_CHANGE_EVENT:
            change_background_color()

    # --- Sprite movement ---
    sprite_rect.move_ip(velocity)

    boundary_hit = False

    if sprite_rect.left <= 0 or sprite_rect.right >= 500:
        velocity[0] = -velocity[0]
        boundary_hit = True
    if sprite_rect.top <= 0 or sprite_rect.bottom >= 400:
        velocity[1] = -velocity[1]
        boundary_hit = True

    if boundary_hit:
        pygame.event.post(pygame.event.Event(SPRITE_COLOR_CHANGE_EVENT))
        pygame.event.post(pygame.event.Event(BACKGROUND_COLOR_CHANGE_EVENT))

    # --- Drawing section ---
    screen.fill(bg_color)
    screen.blit(sprite, sprite_rect)

    pygame.display.flip()
    clock.tick(240)

pygame.quit()
