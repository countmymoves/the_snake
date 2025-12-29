import random
import sys
import pygame

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
CELL_SIZE = 20
FPS = 20

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

ALL_CELLS = {
    (x, y)
    for x in range(0, SCREEN_WIDTH, CELL_SIZE)
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE)
}


class GameObject:
    """Базовый класс для объектов игры."""

    def __init__(self, position, body_color):
        """Инициализация объекта."""
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Метод для отрисовки объекта."""
        pass


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self):
        """Инициализация яблока."""
        self.body_color = RED
        self.position = (0, 0)
        self.randomize_position()

    def randomize_position(self, occupied=None):
        """Случайная позиция яблока, не попадая в occupied."""
        if occupied is None:
            occupied = set()
        free_cells = list(ALL_CELLS - set(occupied))
        self.position = random.choice(free_cells)

    def draw(self, surface):
        """Отрисовывает яблоко."""
        pygame.draw.rect(
            surface,
            self.body_color,
            pygame.Rect(self.position[0], self.position[1], CELL_SIZE, CELL_SIZE),
        )


class Snake(GameObject):
    """Класс змейки."""

    DIRECTIONS = {
        'UP': (0, -CELL_SIZE),
        'DOWN': (0, CELL_SIZE),
        'LEFT': (-CELL_SIZE, 0),
        'RIGHT': (CELL_SIZE, 0),
    }

    OPPOSITE = {
        'UP': 'DOWN',
        'DOWN': 'UP',
        'LEFT': 'RIGHT',
        'RIGHT': 'LEFT',
    }

    def __init__(self):
        """Инициализация змейки."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = 'RIGHT'
        self.next_direction = None
        self.body_color = GREEN
        self.last = None

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление змейки."""
        if self.next_direction and self.next_direction != self.OPPOSITE[self.direction]:
            self.direction = self.next_direction
        self.next_direction = None

    def move(self):
        """Передвигает змейку на одну клетку."""
        dx, dy = self.DIRECTIONS[self.direction]
        head_x, head_y = self.get_head_position()
        new_head = ((head_x + dx) % SCREEN_WIDTH, (head_y + dy) % SCREEN_HEIGHT)

        if new_head in self.positions[1:]:
            self.reset()
            return

        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = random.choice(list(self.DIRECTIONS.keys()))
        self.next_direction = None
        self.last = None

    def draw(self, surface):
        """Отрисовывает змейку на поверхности."""
        if self.last:
            pygame.draw.rect(
                surface,
                BLACK,
                pygame.Rect(self.last[0], self.last[1], CELL_SIZE, CELL_SIZE),
            )
        for pos in self.positions:
            pygame.draw.rect(
                surface,
                self.body_color,
                pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE),
            )


def handle_keys(snake):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_UP:
                snake.next_direction = 'UP'
            elif event.key == pygame.K_DOWN:
                snake.next_direction = 'DOWN'
            elif event.key == pygame.K_LEFT:
                snake.next_direction = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                snake.next_direction = 'RIGHT'


def main():
    """Основная функция игры."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Изгиб Питона')
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(occupied=snake.positions)

        screen.fill(BLACK)
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
