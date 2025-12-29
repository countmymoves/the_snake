import pygame
import random
import sys

# Константы
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
CELL_SIZE = 20
FPS = 10

# Цвета
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, position, color):
        """Инициализация объекта."""
        self.position = position
        self.color = color

    def draw(self, surface):
        """Рисует объект на экране."""
        pygame.draw.rect(
            surface, self.color, pygame.Rect(self.position[0], self.position[1], CELL_SIZE, CELL_SIZE)
        )


class Apple(GameObject):
    """Класс для яблока."""

    def __init__(self):
        """Инициализация яблока."""
        self.color = RED
        self.position = (0, 0)
        self.randomize_position()

    def randomize_position(self):
        """Случайное размещение яблока."""
        self.position = (random.randint(0, (SCREEN_WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
                         random.randint(0, (SCREEN_HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)


class Snake(GameObject):
    """Класс змейки."""

    DIRECTIONS = {
        'UP': (0, -CELL_SIZE),
        'DOWN': (0, CELL_SIZE),
        'LEFT': (-CELL_SIZE, 0),
        'RIGHT': (CELL_SIZE, 0)
    }

    def __init__(self):
        """Инициализация змейки."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = 'RIGHT'
        self.color = GREEN

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def update_direction(self, new_direction):
        """Обновляет направление змейки."""
        if new_direction in self.DIRECTIONS:
            self.direction = new_direction

    def move(self):
        """Двигает змейку на одну клетку."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.DIRECTIONS[self.direction]
        new_head = ((head_x + dx) % SCREEN_WIDTH, (head_y + dy) % SCREEN_HEIGHT)

        # Проверка на столкновение с телом
        if new_head in self.positions:
            self.reset()

        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def reset(self):
        """Сброс змейки в начальное состояние."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = 'RIGHT'


def handle_keys(snake):
    """Обрабатывает нажатие клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.update_direction('UP')
            elif event.key == pygame.K_DOWN:
                snake.update_direction('DOWN')
            elif event.key == pygame.K_LEFT:
                snake.update_direction('LEFT')
            elif event.key == pygame.K_RIGHT:
                snake.update_direction('RIGHT')


def main():
    """Основная функция игры."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Змейка')

    # Объекты игры
    snake = Snake()
    apple = Apple()

    clock = pygame.time.Clock()

    while True:
        handle_keys(snake)
        snake.move()

        # Проверка на съеденное яблоко
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        # Обновление экрана
        screen.fill(BLACK)
        apple.draw(screen)
        snake.draw(screen)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
