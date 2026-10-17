import pygame

pygame.init()


SCREEN_WIDTH, SCREEN_HEIGHT = 500, 500

display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('My first game screen')

GREY = (58, 58, 58)

penguin_image = pygame.transform.scale(
    pygame.image.load("Module_6/Day_1/main.py/hello penguin.png").convert_alpha(),
    (300, 300)
)

penguin_rect = penguin_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

def game_loop():
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

      
        display_surface.fill(GREY)

      
        display_surface.blit(penguin_image, penguin_rect)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == '__main__':
    game_loop()