import pygame
import time
import random

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 128, 0)
BLUE = (50, 153, 213)
LEVEL_COLORS = [(255, 255, 0), (128, 0, 128), (0, 128, 255), (255, 165, 0), (0, 255, 255)]

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Snake settings
SNAKE_SIZE = 20
SNAKE_SPEED = 10

# Font settings
font_style = pygame.font.SysFont("comicsansms", 35)
score_font = pygame.font.SysFont("comicsansms", 40)

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Enhanced Snake Game')

# Function for gradient background
def draw_gradient_background(start_color, end_color):
    for i in range(SCREEN_HEIGHT):
        color = (
            start_color[0] + (end_color[0] - start_color[0]) * i // SCREEN_HEIGHT,
            start_color[1] + (end_color[1] - start_color[1]) * i // SCREEN_HEIGHT,
            start_color[2] + (end_color[2] - start_color[2]) * i // SCREEN_HEIGHT
        )
        pygame.draw.line(screen, color, (0, i), (SCREEN_WIDTH, i))

# Particle effect class for food consumption
class Particle:
    def __init__(self, x, y, size, color, direction):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.direction = direction
        self.lifetime = 50

    def update(self):
        self.x += self.direction[0]
        self.y += self.direction[1]
        self.lifetime -= 1

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))

# Function to display score and time
def display_score_and_time(score, time_left, level):
    score_text = score_font.render(f"Score: {score}", True, BLUE)
    time_text = score_font.render(f"Time Left: {int(time_left)}s", True, BLUE)
    level_text = score_font.render(f"Level: {level}", True, BLUE)
    screen.blit(score_text, [10, 10])
    screen.blit(time_text, [10, 50])
    screen.blit(level_text, [10, 90])

# Function to draw the snake
def draw_snake(snake_body):
    for segment in snake_body:
        pygame.draw.circle(screen, GREEN, (segment[0] + SNAKE_SIZE // 2, segment[1] + SNAKE_SIZE // 2), SNAKE_SIZE // 2)

# Function to draw glowing food with animation
def draw_food_with_glow_and_animation(x, y, frame):
    glow_radius = SNAKE_SIZE + 10 + (frame % 10)  # Pulse effect for the food glow
    pygame.draw.circle(screen, (255, 100, 100), (x + SNAKE_SIZE // 2, y + SNAKE_SIZE // 2), glow_radius, 5)
    pygame.draw.rect(screen, RED, [x, y, SNAKE_SIZE, SNAKE_SIZE])

# Function for floating text pop-ups
class FloatingText:
    def __init__(self, text, x, y):
        self.text = score_font.render(text, True, WHITE)
        self.x = x
        self.y = y
        self.lifetime = 30  # Number of frames the text stays on screen

    def update(self):
        self.y -= 1  # Move up
        self.lifetime -= 1

    def draw(self, screen):
        screen.blit(self.text, (self.x, self.y))

# Main game loop
# Main game loop
def game_loop():
    global SNAKE_SPEED
    game_over = False
    game_close = False
    paused = False

    total_time = 300  # 5 minutes
    start_time = time.time()

    level = 1
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2
    x_change = 0
    y_change = 0
    snake_body = []
    snake_length = 1

    food_x = round(random.randrange(0, SCREEN_WIDTH - SNAKE_SIZE) / SNAKE_SIZE) * SNAKE_SIZE
    food_y = round(random.randrange(0, SCREEN_HEIGHT - SNAKE_SIZE) / SNAKE_SIZE) * SNAKE_SIZE

    score = 0
    clock = pygame.time.Clock()
    particles = []
    floating_texts = []

    frame = 0  # To track food animation frame

    # Snake speed range
    min_speed = 5
    max_speed = 30

    while not game_over:
        time_left = total_time - (time.time() - start_time)
        if time_left <= 0:
            game_close = True

        while game_close:
            screen.fill(BLACK)
            display_score_and_time(score, 0, level)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -SNAKE_SIZE
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = SNAKE_SIZE
                    y_change = 0
                elif event.key == pygame.K_UP:
                    y_change = -SNAKE_SIZE
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = SNAKE_SIZE
                    x_change = 0
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:  # '+' key increases speed
                    SNAKE_SPEED = min(SNAKE_SPEED + 1, max_speed)
                elif event.key == pygame.K_MINUS:  # '-' key decreases speed
                    SNAKE_SPEED = max(SNAKE_SPEED - 1, min_speed)

        if x >= SCREEN_WIDTH or x < 0 or y >= SCREEN_HEIGHT or y < 0:
            game_close = True

        x += x_change
        y += y_change

        # Draw gradient background
        draw_gradient_background((0, 0, 128), (0, 128, 255))

        # Draw animated, glowing food
        draw_food_with_glow_and_animation(food_x, food_y, frame)

        # Update and draw floating texts
        for text in floating_texts:
            text.update()
            text.draw(screen)
        floating_texts = [text for text in floating_texts if text.lifetime > 0]

        # Update particles and draw
        for particle in particles:
            particle.update()
            particle.draw(screen)
        particles = [p for p in particles if p.lifetime > 0]

        snake_head = [x, y]
        snake_body.append(snake_head)
        if len(snake_body) > snake_length:
            del snake_body[0]

        for segment in snake_body[:-1]:
            if segment == snake_head:
                game_close = True

        draw_snake(snake_body)
        display_score_and_time(score, time_left, level)
        pygame.display.update()

        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, SCREEN_WIDTH - SNAKE_SIZE) / SNAKE_SIZE) * SNAKE_SIZE
            food_y = round(random.randrange(0, SCREEN_HEIGHT - SNAKE_SIZE) / SNAKE_SIZE) * SNAKE_SIZE
            snake_length += 1
            score += 10

            # Add particles and floating text when food is eaten
            particles.extend([Particle(food_x, food_y, 5, RED, (random.randint(-5, 5), random.randint(-5, 5))) for _ in range(15)])
            floating_texts.append(FloatingText("+10", x, y))

        clock.tick(SNAKE_SPEED)
        frame += 1

    pygame.quit()
    quit()

# Start the game
game_loop()
