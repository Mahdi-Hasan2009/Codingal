# 🎯 Step 1: Import pygame
import pygame

# 🎯 Step 2: Initialize all pygame modules
pygame.init()

# 🎯 Step 3: Create game window (width, height)
screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption("🎮 My First Cocktail Game")

# 🎯 Step 4: Load an image (must be in same folder)
player_img = pygame.image.load("E:\Codingal\practice\practice1\pygamegpt.py\images.jpeg")  # তুমি ইচ্ছা মতো ছবি দাও (যেমন car.png)

# 🎯 Step 5: Create text using font
font = pygame.font.Font(None, 50)
title_text = font.render("Welcome to My Pygame World!", True, (255, 255, 255))
info_text = font.render("Press Q to Quit", True, (255, 255, 0))

# 🎯 Step 6: Position setup
x, y = 300, 250  # ছবির অবস্থান

# 🎯 Step 7: Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:     # window close করলে loop বন্ধ হবে
            running = False

        # কীবোর্ডে Q চাপলে গেম বন্ধ হবে
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

    # 🎯 Step 8: Background color
    screen.fill((0, 100, 180))  # নীল ব্যাকগ্রাউন্ড

    # 🎯 Step 9: Draw / blit image and text
    screen.blit(player_img, (x, y))        # ছবি দেখাও
    screen.blit(title_text, (120, 100))    # টেক্সট দেখাও
    screen.blit(info_text, (280, 420))     # নিচে ইনফো টেক্সট দেখাও

    # 🎯 Step 10: Update the screen
    pygame.display.update()

# 🎯 Step 11: Quit pygame
pygame.quit()
