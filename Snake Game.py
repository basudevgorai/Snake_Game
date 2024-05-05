import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set the width and height of the game window
window_width = 800
window_height = 600

# Set the size of each grid cell and the number of cells
cell_size = 20
grid_width = window_width // cell_size
grid_height = window_height // cell_size

# Set the game speed (lower value means higher speed)
game_speed = 10

# Create the game window
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

# Snake class
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(grid_width // 2, grid_height // 2)]
        self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        self.color = GREEN

    def get_head_position(self):
        return self.positions[0]

    def move(self):
        current_x, current_y = self.get_head_position()

        if self.direction == "UP":
            new_position = (current_x, current_y - 1)
        elif self.direction == "DOWN":
            new_position = (current_x, current_y + 1)
        elif self.direction == "LEFT":
            new_position = (current_x - 1, current_y)
        else:
            new_position = (current_x + 1, current_y)

        self.positions.insert(0, new_position)

        if len(self.positions) > self.length:
            self.positions.pop()

    def change_direction(self, direction):
        if direction == "UP" and self.direction != "DOWN":
            self.direction = direction
        elif direction == "DOWN" and self.direction != "UP":
            self.direction = direction
        elif direction == "LEFT" and self.direction != "RIGHT":
            self.direction = direction
        elif direction == "RIGHT" and self.direction != "LEFT":
            self.direction = direction

    def draw(self):
        for position in self.positions:
            pygame.draw.rect(window, self.color, (position[0] * cell_size, position[1] * cell_size, cell_size, cell_size))

# Fruit class
class Fruit:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.spawn()

    def spawn(self):
        self.position = (random.randint(0, grid_width - 1), random.randint(0, grid_height - 1))

    def draw(self):
        pygame.draw.rect(window, self.color, (self.position[0] * cell_size, self.position[1] * cell_size, cell_size, cell_size))

# Game over function
def game_over():
    font = pygame.font.Font(None, 50)
    text = font.render("Game Over", True, WHITE)
    window.blit(text, (window_width // 2 - text.get_width() // 2, window_height // 2 - text.get_height() // 2))
    pygame.display.flip()
    time.sleep(2)

# Main game loop
def game_loop():
    snake = Snake()
    fruit = Fruit()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction("UP")
                elif event.key == pygame.K_DOWN:
                    snake.change_direction("DOWN")
                elif event.key == pygame.K_LEFT:
                    snake.change_direction("LEFT")
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction("RIGHT")

        snake.move()

        if snake.get_head_position() == fruit.position:
            snake.length += 1
            fruit.spawn()

        if (snake.get_head_position()[0] < 0 or snake.get_head_position()[0] >= grid_width
                or snake.get_head_position()[1] < 0 or snake.get_head_position()[1] >= grid_height
                or len(snake.positions) != len(set(snake.positions))):
            game_over()
            snake.__init__()

        window.fill(BLACK)
        snake.draw()
        fruit.draw()
        pygame.display.flip()
        clock.tick(game_speed)

# Start the game
game_loop()
pygame.quit()
