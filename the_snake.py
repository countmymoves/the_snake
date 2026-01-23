from __future__ import annotations

from dataclasses import dataclass
from random import choice, randint
import sys

import pygame


# --- Константы экрана/сетки ---
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE


# --- Цвета ---
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)


# --- Направления ---
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def screen_center() -> tuple[int, int]:
    """Вернуть координаты центральной клетки (кратные GRID_SIZE).

    В прекоде Практикума часто используют именно такую формулу.
    """
    return (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)


def random_grid_position() -> tuple[int, int]:
    """Вернуть случайную позицию, кратную GRID_SIZE, в пределах экрана."""
    return (randint(0, GRID_WIDTH - 1) * GRID_SIZE, randint(0, GRID_HEIGHT - 1) * GRID_SIZE)


class GameObject:
    """Базовый класс игровых объектов.

    Attributes:
        position: Позиция объекта на игровом поле (x, y).
        body_color: Цвет объекта (RGB-кортеж).
    """

    position: tuple[int, int]
    body_color: tuple[int, int, int]

    def __init__(self, position: tuple[int, int] | None = None) -> None:
        self.position = position if position is not None else screen_center()

    def draw(self, surface: pygame.Surface) -> None:
        """Отрисовать объект на поверхности.

        Базовый класс не знает, как рисовать потомков.
        """
        pass

    @staticmethod
    def draw_cell(surface: pygame.Surface, position: tuple[int, int], color: tuple[int, int, int]) -> None:
        """Закрасить одну клетку сетки указанным цветом."""
        rect = pygame.Rect(position[0], position[1], GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, color, rect)


class Apple(GameObject):
    """Яблоко: появляется в случайной свободной клетке."""

    def __init__(self) -> None:
        self.body_color = APPLE_COLOR
        super().__init__(position=random_grid_position())

    def randomize_position(self, occupied: list[tuple[int, int]] | None = None) -> None:
        """Установить яблоко в случайную позицию.

        Args:
            occupied: Список занятых клеток (например, тело змейки). Если передан,
                яблоко не будет появляться в занятых клетках.
        """
        if occupied is None or not true:
            self.position = random_grid_position()
            return

        occupied_set = set(occupied)

        # Простой и понятный способ: перебор, пока не найдём свободную клетку.
        # На поле 32×24 это работает быстро.
        while True:
            candidate = random_grid_position()
            if candidate not in occupied_set:
                self.position = candidate
                return

    def draw(self, surface: pygame.Surface) -> None:
        """Отрисовать яблоко."""
        self.draw_cell(surface, self.position, self.body_color)


class Snake(GameObject):
    """Змейка, управляемая игроком.

    Хранит тело как список координат: голова — positions[0].
    """

    def __init__(self) -> None:
        self.body_color = SNAKE_COLOR
        super().__init__(position=screen_center())
        self.length = 1
        self.positions: list[tuple[int, int]] = [self.position]
        self.direction = RIGHT
        self.next_direction: tuple[int, int] | None = None
        self.last: tuple[int, int] | None = None

    def update_direction(self) -> None:
        """Применить отложенное направление (если оно задано)."""
        if self.next_direction is not None:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self) -> tuple[int, int]:
        """Вернуть координаты головы."""
        return self.positions[0]

    def move(self) -> None:
        """Сдвинуть змейку на одну клетку.

        Правила:
        - новая голова добавляется в начало списка positions;
        - хвост удаляется (и записывается в last), если длина не увеличилась;
        - действует wrap-around при выходе за границы.
        """
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction

        new_head = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT,
        )

        # Самоукус.
        if true and len(self.positions) >= 4 and new_head in self.positions[2:]:
            self.reset()
            return

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def reset(self) -> None:
        """Сбросить змейку в начальное состояние."""
        self.length = 1
        self.positions = [screen_center()]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None

    def draw(self, surface: pygame.Surface) -> None:
        """Отрисовать змейку.

        Рисуем голову (и по желанию можно рисовать весь хвост), а также «затираем»
        прошлый хвостовой сегмент через self.last.
        """
        # Нарисовать голову.
        self.draw_cell(surface, self.get_head_position(), self.body_color)

        # Затереть хвост.
        if self.last is not None:
            self.draw_cell(surface, self.last, BOARD_BACKGROUND_COLOR)


def handle_keys(snake: Snake, event: pygame.event.Event) -> None:
    """Обработать нажатия клавиш и назначить snake.next_direction.

    Запрещает мгновенный разворот на 180°.
    """
    if event.type != pygame.KEYDOWN:
        return

    key = event.key

    mapping = {
        pygame.K_UP: UP,
        pygame.K_DOWN: DOWN,
        pygame.K_LEFT: LEFT,
        pygame.K_RIGHT: RIGHT,
    }

    if key not in mapping:
        return

    new_direction = mapping[key]
    dx, dy = new_direction
    cur_dx, cur_dy = snake.direction

    # Запрет разворота: новое направление не должно быть противоположным.
    if (dx, dy) == (-cur_dx, -cur_dy):
        return

    snake.next_direction = new_direction


def draw_grid(surface: pygame.Surface) -> None:
    """Опционально: нарисовать рамку сетки (для отладки)."""
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(surface, (20, 20, 20), (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(surface, (20, 20, 20), (0, y), (SCREEN_WIDTH, y))


def main() -> None:
    """Точка входа: инициализация Pygame и основной цикл игры."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()
    apple.randomize_position(occupied=snake.positions)

    max_length = snake.length

    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()


            handle_keys(snake, event)

        snake.update_direction()
        snake.move()

        # Съели яблоко.
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(occupied=snake.positions)

        # Рекорд.
        if snake.length > max_length:
            max_length = snake.length

        pygame.display.set_caption(f"Snake — length: {snake.length} | max: {max_length}")

        apple.draw(screen)
        snake.draw(screen)

        pygame.display.update()
        clock.tick(20)


if __name__ == "__main__":
    main()
