import random
import sys

import pygame


SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GRID_SIZE = 20
FPS = 10

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)


class Snake:
    """Class representing the snake."""

    def __init__(self):
        """Initialize the snake."""
        self.positions = [(300, 300)]
        self.direction = (1, 0)
        self.grow = False

    def move(self):
        """Move the snake one step."""
        head_x, head_y = self.positions[0]
        dir_x, dir_y = self.direction

        new_position = (
            (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT,
        )

        self.positions.insert(0, new_position)

        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False

    def change_direction(self, direction):
        """Change movement direction."""
        self.direction = direction

    def draw(self, surface):
        """Draw the snake."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, GREEN, rect)

    def check_self_collision(self):
        """Check collision with itself."""
        return self.positions[0] in self.positions[1:]


class Apple:
    """Class representing the apple."""

    def __init__(self):
        """Initialize the apple."""
        self.position = self._random_position()

    def _random_position(self):
        """Generate a random position."""
        x = random.randrange(0, SCREEN_WIDTH, GRID_SIZE)
        y = random.randrange(0, SCREEN_HEIGHT, GRID_SIZE)
        return x, y

    def respawn(self):
        """Respawn the apple."""
        self.position = self._random_position()

    def draw(self, surface):
        """Draw the apple."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, RED, rect)


def main():
    """Run the snake game."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Snake')
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((1, 0))

        snake.move()

        if snake.positions[0] == apple.position:
            snake.grow = True
            apple.respawn()

        if snake.check_self_collision():
            running = False

        screen.fill(BLACK)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
