# Import necessary libraries 
import pygame

#initialize required modules
pygame.init()


# Set up window geometry
screen = pygame.display.set_mode((400,500))

# create a loop to run till the game is quit by the user

done = False

while not done:
    #clear the event queue
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    #make the changes visible 
    pygame.display.flip()