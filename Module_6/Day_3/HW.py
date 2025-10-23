import pygame 
import random

pygame.init()
background_image = pygame.transform.scale(pygame.image.load("bg2.png"),(500,400))
font = pygame.font.SysFont("Times New Roman", 72)

class Sprite(pygame.sprite.Sprite):
  def __init__(self,color,height,width):
    super().__init__()
    self.image = pygame.Surface([width,height])
    self.image.fill(pygame.Color("dodgerblue"))
    pygame.draw.rect(self.image, color, pygame.Rect(0, 0, width, height))
    self.rect = self.image.get_rect()
    
screen = pygame.display.set_mode((500,400))
pygame.display.set_caption("multiple sprites")
all_sprites = pygame.sprite.Group()
#1
sprite1 = Sprite(pygame.Color('blue'), 20, 30)
sprite1.rect.x, sprite1.rect.y = random.randint(
    0, 500 - sprite1.rect.width), random.randint(
        0, 400 - sprite1.rect.height)
all_sprites.add(sprite1)
# 2
sprite2 = Sprite(pygame.Color('red'), 20, 30)
sprite2.rect.x, sprite2.rect.y = random.randint(
    0, 500 - sprite2.rect.width), random.randint(
        0, 400 - sprite2.rect.height)
all_sprites.add(sprite2)
running = True
clock = pygame.time.Clock()
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
  screen.blit(background_image, (0, 0))
  all_sprites.draw(screen)
  pygame.display.flip()
  clock.tick(90)

pygame.quit()