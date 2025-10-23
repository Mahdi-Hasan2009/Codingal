import pygame
pygame.init()

# ---------- Screen setup ----------
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sprite Group Collision Example")

# ---------- Define Player class ----------
class Player(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        # Parent class এর initialization কল করা
        super().__init__()

        # Surface (ছবির টুকরো) তৈরি করা
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # rect মানে হলো অবস্থান ও আকার
        self.rect = self.image.get_rect()
        self.speed = 5

    def update(self):
        """কীবোর্ড দিয়ে player সরানোর কাজ"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # যাতে player স্ক্রিনের বাইরে না যায়
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > SCREEN_WIDTH - self.rect.width:
            self.rect.x = SCREEN_WIDTH - self.rect.width
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > SCREEN_HEIGHT - self.rect.height:
            self.rect.y = SCREEN_HEIGHT - self.rect.height

# ---------- Sprite Group ----------
all_sprites = pygame.sprite.Group()

# ---------- Player & Enemy তৈরি ----------
player = Player((0,255,0), 30, 30)   # সবুজ বক্স
enemy = Player((255,0,0), 30, 30)    # লাল বক্স
enemy.rect.x = 300                   # enemy-এর অবস্থান
enemy.rect.y = 150

# গ্রুপে যোগ করা
all_sprites.add(player, enemy)

# ---------- Main Loop ----------
font = pygame.font.Font(None, 50)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update সব sprite (player-এর নড়াচড়া)
    all_sprites.update()

    # Collision চেক করা (player vs enemy)
    if player.rect.colliderect(enemy.rect):
        text = font.render("Collision Detected!", True, (255, 0, 0))
    else:
        text = font.render("No Collision", True, (0, 0, 0))

    # Draw অংশ
    screen.fill((255, 255, 255))         # সাদা ব্যাকগ্রাউন্ড
    all_sprites.draw(screen)             # সব sprite আঁকা
    screen.blit(text, (150, 30))         # টেক্সট দেখানো

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()

