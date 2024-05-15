import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Game settings
GRAVITY = 0.25
FLAP_STRENGTH = -6
PIPE_GAP = 200
PIPE_WIDTH = 70
PIPE_VELOCITY = -4

# Load and resize images
BIRD_IMAGE = pygame.image.load('bird.png')
BIRD_IMAGE = pygame.transform.scale(BIRD_IMAGE, (50, 35))

PIPE_IMAGE = pygame.image.load('pipe.png')
PIPE_IMAGE = pygame.transform.scale(PIPE_IMAGE, (PIPE_WIDTH, 400))

BACKGROUND_IMAGE = pygame.image.load('background.png')
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Font setup
font = pygame.font.SysFont(None, 36)

class Bird:
    def __init__(self):
        self.image = BIRD_IMAGE
        self.rect = self.image.get_rect()
        self.rect.center = (50, SCREEN_HEIGHT // 2)
        self.velocity = 0

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(50, SCREEN_HEIGHT - PIPE_GAP)
        self.bottom_rect = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - self.height - PIPE_GAP)

    def update(self):
        self.x += PIPE_VELOCITY
        self.bottom_rect.x = self.x

    def draw(self, screen):
        screen.blit(PIPE_IMAGE, self.bottom_rect.topleft)

    def is_off_screen(self):
        return self.x < -PIPE_WIDTH

    def collides_with(self, bird):
        return self.bottom_rect.colliderect(bird.rect)

def show_game_over(screen, score):
    game_over_text = font.render('Game Over!', True, RED)
    score_text = font.render(f'Your Score: {score}', True, WHITE)
    restart_text = font.render('Press R to Restart', True, WHITE)
    
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    
    pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = [Pipe(SCREEN_WIDTH + i * (SCREEN_WIDTH // 2)) for i in range(2)]
    score = 0
    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird.flap()
                if event.key == pygame.K_r and game_over:
                    main()  # Restart the game

        if not game_over:
            bird.update()
            for pipe in pipes:
                pipe.update()
                if pipe.is_off_screen():
                    pipes.remove(pipe)
                    pipes.append(Pipe(SCREEN_WIDTH))
                    score += 1
                if pipe.collides_with(bird):
                    game_over = True

            if bird.rect.top <= 0 or bird.rect.bottom >= SCREEN_HEIGHT:
                game_over = True

            screen.blit(BACKGROUND_IMAGE, (0, 0))
            bird.draw(screen)
            for pipe in pipes:
                pipe.draw(screen)

            score_text = font.render(f'Score: {score}', True, WHITE)
            screen.blit(score_text, (10, 10))

        if game_over:
            show_game_over(screen, score)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
