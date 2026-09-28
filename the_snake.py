from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
GRID_CENTER = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject():
    """Родительский класс"""

    def __init__(self):
        """
        Инициализирует базовые атрибуты объекта,
        такие как его позиция и цвет.
        """
        self.position = GRID_CENTER
        self.body_color = None

    def draw(self):
        """Отрисовывает объект на экране."""
        raise NotImplementedError(
            'Метод draw() должен быть переопределён в дочеренем классе.'
        )


class Apple(GameObject):
    """
    Класс Apple, объявляются координаты яблока , цвет
    и метод его отрисовки draw()
    """

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR

    def randomize_position(self, snake):
        """
        Устанавливает случайное положение яблока на игровом поле
        — задаёт атрибуту position новое значение
        """
        while self.position in snake:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self):
        """Отрисовывает яблоко исходя координат и параметров игровой сетки"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Класс Snake, для змейки задаются атрибуты:
    длинны, координат, направления движения,
    следующего движения(будет применено после обработки нажатия клавиши),
    цвет, последний сегмент списка координат
    """

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.reset()

    def get_head_position(self):
        """Метод возвращает координаты головы змейки — первый элемент списка"""
        return self.positions[0]

    def move(self):
        """Метод бновления координат всех сегментов змейки"""
        head_x, head_y = self.get_head_position()
        vector_x, vector_y = self.direction
        new_head_position = (
            (head_x + vector_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + vector_y * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head_position)

        # Удаляем и сохраняем последний элемент списка координат ,
        # реализуется движение змейки
        if len(self.positions) > self.length:
            self.last = self.positions.pop(-1)

    def reset(self):
        """Метод возвращает змейку в начальное состояние и обновляет экран"""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """
        Метод обновляет текущее направление движения
          змейки на основе значения next_direction
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self):
        """
        Отрисовывает змейку на игровой поверхности по
        значению координат x,y в positions и параметров сетки игрового поля
        """
        head_rect = pygame.Rect(
            self.get_head_position(), (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def main():
    """Управляет игровым циклом"""
    pygame.init()
    snake = Snake()
    apple = Apple()
    apple.randomize_position(snake.positions)

    while True:
        """
        В цикле обрабатываются :
        Обрабатываются события клавиатуры.
        Обновляется направление движения змейки.
        Змейка перемещается.
        Проверяется, съела ли змейка яблоко.
        Проверяются столкновения змейки с собой.
        Отрисовываются объекты.
        Экран обновляется.
        """
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if apple.position == snake.get_head_position():
            snake.length += 1
            apple.randomize_position(snake.positions)

        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        snake.draw()
        apple.draw()

        pygame.display.update()


def handle_keys(game_object):
    """
    Обрабатывает нажатия клавиш, чтобы изменить
    направление движения змейки
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


if __name__ == '__main__':
    main()
