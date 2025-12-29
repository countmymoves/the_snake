import pygame
import random

# --- Константы ---
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
BOARD_COLOR = (0, 0, 0)
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)
FPS = 10

ALL_CELLS = {
    (x * GRID_SIZE, y * GRID_SIZE)
    for x in range(GRID_WIDTH)
    for y in range(GRID_HEIGHT)
}

# --- Базовый класс ---
class GameObject:
    """Базовый игровой объект."""

    def __init__(self, position, body_color):
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Метод для отрисовки объекта (переопределяется)."""
        pass


# --- Класс яблока ---
class Apple(GameObject):
    """Яблоко для змейки."""

    def __init__(self, snake_positions):
        super().__init__((0, 0), APPLE_COLOR)
        self.randomize_position(snake_positions)

    def randomize_position(self, snake_positions):
        """Выбирает случайную позицию для яблока вне змейки."""
        free_cells = list(ALL_CELLS - set(snake_positions))
        self.position = random.choice(free_cells)

    def draw(self, surface):
        pygame.draw.rect(
            surface, self.body_color, pygame.Rect(*self.position, GRID_SIZE, GRID_SIZE)
        )


# --- Класс змейки ---
class Snake(GameObject):
    """Змейка игрока."""

    def __init__(self):
        self.length = 1
        self.positions = [
            (
                (SCREEN_WIDTH // 2) // GRID_SIZE * GRID_SIZE,
                (SCREEN_HEIGHT // 2) // GRID_SIZE * GRID_SIZE,
            )
        ]
        self.direction = (GRID_SIZE, 0)
        self.next_direction = self.direction
        self.body_color = SNAKE_COLOR
        self.last = None

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление движения."""
        self.direction = self.next_direction

    def move(self):
        """Двигает змейку на одну клетку вперед."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
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
        self.positions = [
            (
                (SCREEN_WIDTH // 2) // GRID_SIZE * GRID_SIZE,
                (SCREEN_HEIGHT // 2) // GRID_SIZE * GRID_SIZE,
            )
        ]
        self.direction = (GRID_SIZE, 0)
        self.next_direction = self.direction
        self.last = None

    def draw(self, surface):
        """Отрисовывает сегменты змейки на экране."""
        for pos in self.positions:
            pygame.draw.rect(surface, self.body_color, pygame.Rect(*pos, GRID_SIZE, GRID_SIZE))
        if self.last:
            pygame.draw.rect(surface, BOARD_COLOR, pygame.Rect(*self.last, GRID_SIZE, GRID_SIZE))


KEY_DIRECTION = {
    (pygame.K_UP, (0, GRID_SIZE)): (0, -GRID_SIZE),
    (pygame.K_DOWN, (0, -GRID_SIZE)): (0, GRID_SIZE),
    (pygame.K_LEFT, (GRID_SIZE, 0)): (-GRID_SIZE, 0),
    (pygame.K_RIGHT, (-GRID_SIZE, 0)): (GRID_SIZE, 0),
}


def handle_keys(snake):
    """Обрабатывает нажатия клавиш игрока."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            key_tuple = (event.key, snake.direction)
            snake.next_direction = KEY_DIRECTION.get(key_tuple, snake.direction)


def main():
    """Основной игровой цикл."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Изгиб Питона")
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple(snake.positions)
    record_length = snake.length

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        if snake.length > record_length:
            record_length = snake.length

        pygame.display.set_caption(f"Изгиб Питона - Рекорд: {record_length}")

        screen.fill(BOARD_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
