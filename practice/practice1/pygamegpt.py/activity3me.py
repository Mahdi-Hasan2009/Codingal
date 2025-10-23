import pygame 

pygame.init()

screen =pygame.display.set_mode((800,500))

pygame.display.set_caption("Ball Game")

# Ball location
x ,y = 400,250
radius = 25
speed = 0.1

running = True
while running :
  for event in pygame.event.get():
    if pygame.event == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q ):
      running = False
  keys = pygame.key.get_pressed()
  if keys[pygame.K_LEFT] and x > radius:
    x -=speed
  if keys[pygame.K_RIGHT] and x <  800 - radius:
    x +=speed
  if keys[pygame.K_UP] and y > radius:
    y -= speed
  if keys[pygame.K_DOWN] and y < 500 - radius:
    y += speed
    
  screen.fill((0,100,200))
  pygame.draw.circle(screen, (255,255,0), (x,y), radius)
  pygame.display.update()

pygame.quit()