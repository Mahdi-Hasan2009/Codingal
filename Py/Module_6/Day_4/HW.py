import pygame
pygame.init()

screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption("Custom Event Example")

COLOR_CHANGE = pygame.USEREVENT + 1



pygame.time.set_timer(COLOR_CHANGE, 2000)

color = (255, 0, 0) 

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
            
        if event.type == COLOR_CHANGE:

            if color == (255, 0, 0):
                color = (0, 255, 0)
            else:
                color = (255, 0, 0)

    screen.fill(color)
    pygame.display.flip()

pygame.quit()
