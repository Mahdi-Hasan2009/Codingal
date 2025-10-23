import pygame 

pygame.init()

screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Basic Pygame Functions")

# image load

image = pygame.image.load("images")

running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_x):
      running = False
  screen.fill((0,150,200))
  pygame.display.update() # ***

pygame.quit()
  