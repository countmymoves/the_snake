import random
import sys

import pygame


SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
CELL_SIZE = 20
FPS = 10

BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

ALL_CELLS = {
    (x, y)
    for x in range(0, SCREEN_WIDTH, CELL_SIZE)
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE)
}


class GameObject:
    """Базовый класс игровых объектов."""

    def __init__(self, position):
        self.position = position

    def draw(self, surface):
        """Отрисовать объект на экране."""
        raise NotImplementedError


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self, occupied):
        super().__init__(self._get_free_position(occupied))

    @staticmethod
    def _get_free_position(occupied):
        """Вернуть свободную позицию на поле."""
        return random.choice(tuple(ALL_CELLS - set(occupied)))

    def draw(self, surface):
        """Отрисовать яблоко."""
        rect = pygame.Rect(*self.position, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, RED, rect)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        center_x = SCREEN_WIDTH // 2 // CELL_SIZE * CELL_SIZE
        center_y = SCREEN_HEIGHT // 2 // CELL_SIZE * CELL_SIZE
        super().__init__((center_x, center_y))
        self.segments = [(center_x, center_y)]
        self.direction = (CELL_SIZE, 0)

    def move(self):
        """Переместить змейку."""
        head_x, head_y = self.segments[0]
        dir_x, dir_y = self.direction
        new_head = (
            (head_x + dir_x) % SCREEN_WIDTH,
            (head_y + dir_y) % SCREEN_HEIGHT,
        )

        if new_head in self.segments:
            self.segments = [new_head]
        else:
            self.segments.insert(0, new_head)
            self.segments.pop()

    def grow(self):
        """Увеличить длину змейки."""
        self.segments.append(self.segments[-1])

    def change_direction(self, new_direction):
        """Изменить направление движения."""
        opposite = (-self.direction[0], -self.direction[1])
        if new_direction != opposite:
            self.direction = new_direction

    def draw(self, surface):
        """Отрисовать змейку."""
        for segment in self.segments:
            rect = pygame.Rect(*segment, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, GREEN, rect)


def handle_events(snake):
    """Обработать пользовательский ввод."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_UP:
                snake.change_direction((0, -CELL_SIZE))
            if event.key == pygame.K_DOWN:
                snake.change_direction((0, CELL_SIZE))
            if event.key == pygame.K_LEFT:
                snake.change_direction((-CELL_SIZE, 0))
            if event.key == pygame.K_RIGHT:
                snake.change_direction((CELL_SIZE, 0))


def main():
    """Запуск игры."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Snake')
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple(snake.segments)

    while True:
        handle_events(snake)
        snake.move()

        if snake.segments[0] == apple.position:
            snake.grow()
            apple = Apple(snake.segments)

        screen.fill(BLACK)
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
