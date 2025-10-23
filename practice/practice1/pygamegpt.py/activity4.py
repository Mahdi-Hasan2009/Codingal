import pygame
pygame.init()

# Screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Collision Detection Demo")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Rectangles
player = pygame.Rect(100, 150, 60, 60)   # চলমান rectangle
enemy = pygame.Rect(300, 150, 80, 80)    # স্থির rectangle

speed = 5
font = pygame.font.Font(None, 48)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Keyboard movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= speed
    if keys[pygame.K_RIGHT]:
        player.x += speed
    if keys[pygame.K_UP]:
        player.y -= speed
    if keys[pygame.K_DOWN]:
        player.y += speed

    # Collision check
    collision = player.colliderect(enemy)

    # Draw everything
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, player)   # Player rectangle
    pygame.draw.rect(screen, RED, enemy)     # Enemy rectangle

    if collision:
        text = font.render("Collision Detected!", True, GREEN)
        screen.blit(text, (150, 50))

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()