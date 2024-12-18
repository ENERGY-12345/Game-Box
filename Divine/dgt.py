import pygame
import random

# Initialize Pygame
pygame.init()

# Screen Dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basic Battle Royale")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5
        self.health = 100
    
    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Ensure player stays within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

# Bullet Class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10
    
    def update(self):
        self.rect.x += self.speed
        if self.rect.right > WIDTH:
            self.kill()

# Function to handle game logic
def game_loop():
    # Create player
    player = Player(GREEN, WIDTH // 2, HEIGHT // 2)
    
    # Group for all sprites
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    
    # Group for bullets
    bullets = pygame.sprite.Group()
    
    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill(WHITE)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Shoot a bullet
                    bullet = Bullet(player.rect.centerx, player.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
        
        # Update player and bullets
        keys = pygame.key.get_pressed()
        player.update(keys)
        bullets.update()
        
        # Check for bullet collisions
        for bullet in bullets:
            if player.rect.colliderect(bullet.rect):
                player.health -= 10
                bullet.kill()
                if player.health <= 0:
                    running = False
                    print("You Died!")
        
        # Draw everything
        all_sprites.draw(screen)
        
        # Update display
        pygame.display.update()
        
        # Set framerate
        clock.tick(60)

# Start the game loop
game_loop()

# Quit pygame
pygame.quit()
