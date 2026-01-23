"""Проект Яндекс Практикума «Изгиб Питона» (Snake).

Однофайловая реализация игры «Змейка» на Pygame с ООП:
- GameObject — базовый класс;
- Apple — яблоко;
- Snake — змейка.

Правила:
- поле 640×480, клетка 20×20;
- змейка проходит сквозь стены (wrap-around);
- яблоко не появляется на змейке;
- при самоукусе змейка сбрасывается до головы.
"""

from __future__ import annotations

import sys
from random import choice, randint
from typing import List, Optional, Tuple

import pygame


# --- Размеры экрана/сетки ---
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Частота обновления (тика) игры.
SPEED = 20


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


Position = Tuple[int, int]
Color = Tuple[int, int, int]
Direction = Tuple[int, int]


def screen_center() -> Position:
    """Вернуть координаты центральной клетки экрана."""
    return (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)


def random_grid_position() -> Position:
    """Вернуть случайную позицию, кратную GRID_SIZE, в пределах экрана."""
    return (
        randint(0, GRID_WIDTH - 1) * GRID_SIZE,
        randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
    )


class GameObject:
    """Базовый класс игровых объектов.

    Attributes:
        position: Координаты (x, y) верхнего левого угла клетки.
        body_color: Цвет объекта (RGB-кортеж).
    """

    def __init__(
        self,
        position: Optional[Position] = None,
        body_color: Optional[Color] = None,
    ) -> None:
        self.position = position if position is not None else screen_center()
        self.body_color = body_color

    def draw(self, surface: pygame.Surface) -> None:
        """Отрисовать объект.

        Базовый класс не знает, как рисовать потомков.
        """
        pass

    @staticmethod
    def draw_cell(surface: pygame.Surface, position: Position, color: Color) -> None:
        """Нарисовать одну клетку сетки заданным цветом."""
        rect = pygame.Rect(position[0], position[1], GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Яблоко: появляется в случайной свободной клетке."""

    def __init__(self) -> None:
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self, occupied: Optional[List[Position]] = None) -> None:
        """Установить яблоко в случайную позицию.

        Args:
            occupied: Список занятых клеток (например, positions змейки).
                Если передан, яблоко не появится в этих клетках.
        """
        occupied_set = set(occupied) if occupied else set()

        while True:
            candidate = random_grid_position()
            if candidate not in occupied_set:
                self.position = candidate
                return

    def draw(self, surface: pygame.Surface) -> None:
        """Отрисовать яблоко на поверхности."""
        color = self.body_color if self.body_color is not None else APPLE_COLOR
        self.draw_cell(surface, self.position, color)


class Snake(GameObject):
    """Змейка, управляемая игроком.

    Тело змейки хранится в списке positions: голова — positions[0].
    """

    def __init__(self) -> None:
        super().__init__(position=screen_center(), body_color=SNAKE_COLOR)
        self.length = 1
        self.positions: List[Position] = [self.position]
        self.direction: Direction = RIGHT
        self.next_direction: Optional[Direction] = None
        self.last: Optional[Position] = None

        self.reset_triggered = False
        self._positions_to_clear: List[Position] = []

    def update_direction(self) -> None:
        """Применить отложенное направление движения."""
        if self.next_direction is not None:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self) -> Position:
        """Вернуть координаты головы змейки."""
        return self.positions[0]

    def move(self) -> None:
        """Сдвинуть змейку на одну клетку, учитывая wrap-around.

        Правила:
        - новая голова добавляется в начало списка positions;
        - хвост удаляется (и сохраняется в last), если длина не увеличилась;
        - при самоукусе выполняется reset.
        """
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction

        new_head = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT,
        )

        # Самоукус: проверяем без головы и «шеи».
        if len(self.positions) >= 4 and new_head in self.positions[2:]:
            self.reset()
            return

        self.positions.insert(0, new_head)
        self.position = new_head

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def reset(self) -> None:
        """Сбросить змейку в начальное состояние."""
        self.reset_triggered = True
        self._positions_to_clear = self.positions[:]

        self.length = 1
        self.position = screen_center()
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None

    def draw(self, surface: pygame.Surface) -> None:
        """Отрисовать змейку и затереть след."""
        if self._positions_to_clear:
            for pos in self._positions_to_clear:
                self.draw_cell(surface, pos, BOARD_BACKGROUND_COLOR)
            self._positions_to_clear = []

        color = self.body_color if self.body_color is not None else SNAKE_COLOR
        self.draw_cell(surface, self.get_head_position(), color)

        if self.last is not None:
            self.draw_cell(surface, self.last, BOARD_BACKGROUND_COLOR)


def handle_keys(snake: Snake, event: pygame.event.Event) -> None:
    """Обработать нажатия клавиш и назначить snake.next_direction.

    Запрещает разворот на 180°.
    """
    if event.type != pygame.KEYDOWN:
        return

    mapping = {
        pygame.K_UP: UP,
        pygame.K_DOWN: DOWN,
        pygame.K_LEFT: LEFT,
        pygame.K_RIGHT: RIGHT,
    }

    if event.key not in mapping:
        return

    new_direction = mapping[event.key]

    # Запрет мгновенного разворота.
    cur_dx, cur_dy = snake.direction
    new_dx, new_dy = new_direction
    if (new_dx, new_dy) == (-cur_dx, -cur_dy):
        return

    snake.next_direction = new_direction


def main() -> None:
    """Точка входа: инициализация Pygame и основной игровой цикл."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption('Snake')

    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()
    apple.randomize_position(occupied=snake.positions)

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

        if snake.reset_triggered:
            snake.reset_triggered = False
            apple.randomize_position(occupied=snake.positions)

        # Съели яблоко.
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(occupied=snake.positions)

        apple.draw(screen)
        snake.draw(screen)

        pygame.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
