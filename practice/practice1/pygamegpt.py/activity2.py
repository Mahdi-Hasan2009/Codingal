import pygame

pygame.init()

screen = pygame.display.set_mode((800,500))
pygame.display.set_caption("My Pygame Kingdom")

kingdom_img = pygame.image.load("E:\Codingal\practice\practice1\pygamegpt.py\images1.jpeg")

font = pygame.font.Font(None,50)

running = True
while running:
  for event in pygame.event.get():
    if pygame.event == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_x):
      running = False
  screen.blit(kingdom_img,(150,200))
  screen.fill("lightblue")
  pygame.display.update()
      
pygame.quit()