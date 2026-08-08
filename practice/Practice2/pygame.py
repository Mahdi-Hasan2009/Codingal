import pygame

# Initialize pygame
pygame.init()

# Set up display
pygame.display.set_mode((500, 500))
pygame.display.set_caption("My First Game")

def game_loop():
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update screen (for now, it's just blank)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

# Run the loop
game_loop()



if __name__ == '__main__':
    game_loop()      
    
