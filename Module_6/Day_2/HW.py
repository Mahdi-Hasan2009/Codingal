import pygame
pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("My first game screen")



white = (255, 255, 255)
blue = (0, 0, 255)
black = (0, 0, 0)


font = pygame.font.Font(None, 40)
text = font.render("Hello, Pygame!", True, black)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(white)

    
    pygame.draw.rect(screen, blue, (220, 190, 200, 100))

    
    screen.blit(text, (230, 100))

    
    pygame.display.update()

pygame.quit()
