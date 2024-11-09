import pygame
import random

# Параметры игры
SCREEN_WIDTH = 640  # Ширина экрана
SCREEN_HEIGHT = 480  # Высота экрана
GRID_SIZE = 20  # Размер клетки сетки
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE  # Количество клеток по ширине
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE  # Количество клеток по высоте
UP = (0, -GRID_SIZE)  # Вектор для движения вверх
DOWN = (0, GRID_SIZE)  # Вектор для движения вниз
LEFT = (-GRID_SIZE, 0)  # Вектор для движения влево
RIGHT = (GRID_SIZE, 0)  # Вектор для движения вправо
BOARD_BACKGROUND_COLOR = (0, 0, 0)  # Цвет фона игрового поля
APPLE_COLOR = (255, 0, 0)  # Цвет яблока
SNAKE_COLOR = (0, 255, 0)  # Цвет змейки

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()


class GameObject:
    """
    Базовый класс для создания игровых объектов,
    таких как змейка и яблоко.
    """

    def __init__(self, body_color: tuple = (255, 255, 255),
                 position: tuple = (0, 0)):
        """
        Инициализирует объект с заданным цветом и позицией.

        :param body_color: Цвет объекта в формате RGB.
        :param position: Начальная позиция объекта в координатах экрана.
        """
        self.body_color = body_color
        self.position = position

    def draw(self, surface):
        """
        Рисует объект на переданной поверхности.

        Этот метод является заглушкой и должен быть
        переопределён в дочерних классах.

        :param surface: Поверхность, на которой будет отрисован объект.
        """
        pass


class Apple(GameObject):
    """Класс для создания и управления яблоком на игровом поле."""

    def __init__(self):
        """
        Создаёт яблоко и случайным образом определяет
        его положение на поле.
        """
        super().__init__(APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Определяет случайное положение яблока на игровом поле."""
        x = random.randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1) * GRID_SIZE
        y = random.randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self, surface):
        """
        Отображает яблоко на экране.

        :param surface: Поверхность, на которой рисуется яблоко.
        """
        pygame.draw.rect(
            surface, self.body_color, (*self.position, GRID_SIZE, GRID_SIZE)
        )


class Snake(GameObject):
    """Класс для создания и управления змейкой на игровом поле."""

    def __init__(self):
        """Создаёт змейку с начальной длиной и направлением движения вправо."""
        super().__init__(SNAKE_COLOR)
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = (GRID_SIZE, 0)  # Начальное движение вправо
        self.position = self.positions[0]

    def update_direction(self, new_direction: tuple):
        """
        Обновляет направление движения змейки,
        если оно не противоположно текущему.

        :param new_direction: Новый вектор направления движения.
        """
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def move(self):
        """
        Обновляет позиции сегментов змейки
        на основе текущего направления движения.

        Обрабатывает выход за границы экрана
        и проверяет самопересечения.
        """
        head_x, head_y = self.get_head_position()
        new_head_position = (head_x + self.direction[0],
                             head_y + self.direction[1])

        # Обеспечивает цикличное перемещение по экрану
        new_head_position = (
            new_head_position[0] % SCREEN_WIDTH,
            new_head_position[1] % SCREEN_HEIGHT,
        )

        # Проверка столкновения с телом змейки
        if new_head_position in self.positions[2:]:
            self.reset()
            return

        self.positions.insert(0, new_head_position)
        self.position = new_head_position

        if len(self.positions) > self.length:
            self.positions.pop()  # Удаление хвостового сегмента

    def draw(self, surface):
        """
        Отображает змейку на экране,
        включая её текущую позицию и очищение следа.

        :param surface: Поверхность, на которой рисуется змейка.
        """
        for position in self.positions:
            pygame.draw.rect(
                surface, self.body_color, (*position, GRID_SIZE, GRID_SIZE)
            )

        # Удаление хвостового следа при движении змейки
        if len(self.positions) > 1:
            tail_position = self.positions[-1]
            pygame.draw.rect(
                surface, BOARD_BACKGROUND_COLOR,
                (*tail_position, GRID_SIZE, GRID_SIZE)
            )

    def get_head_position(self):
        """
        Возвращает текущую позицию головы змейки.

        :return: Координаты головы змейки.
        """
        return self.positions[0]

    def reset(self):
        """Возвращает змейку в начальное состояние."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = (GRID_SIZE, 0)
        self.position = self.positions[0]


def handle_keys(snake):
    """
    Обрабатывает события нажатий клавиш для управления направлением змейки.

    :param snake: Объект змейки, управление которой осуществляется.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.update_direction(UP)
            elif event.key == pygame.K_DOWN:
                snake.update_direction(DOWN)
            elif event.key == pygame.K_LEFT:
                snake.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT:
                snake.update_direction(RIGHT)


def main():
    """Запускает основной игровой цикл и управляет основными событиями игры."""
    apple = Apple()
    snake = Snake()
    running = True

    while running:
        handle_keys(snake)
        snake.move()

        # Проверка столкновения змейки с яблоком
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        # Отображение объектов на экране
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.flip()
        clock.tick(10)  # Ограничение частоты обновления экрана

    pygame.quit()


if __name__ == "__main__":
    main()
