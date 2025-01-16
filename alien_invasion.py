import sys

import pygame

# Импортируем класс Settings
from settings import Settings

# Импортируем класс Ship
from ship import Ship

class AlienInvasion:
    """Класс для управления ресурсами и поведением игры."""

    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы."""
        # Функция pygame.init() инициализирует настроки, необходимые для работы
        pygame.init()


        # Создаем экземпляр Settings и сохраняем его в self.settings 
        self.settings = Settings()

        # Создается окно, размером 1200 на 800
        # Объект окна присваивается артибуту self.screen, что позволяет-
        # -работать с ним во всех классах
        # Используем артибуты объекта self.settings:
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))


        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)


    # Этот метод управляет процессом игры
    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            self._check_events()
            self.ship.update()
            self._update_screen()


    def _check_events(self):
        """Обрабатывает нажатия клавиш и события мыши"""
        # Отслеживание событий клавиатуры и мыши.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # Добавим блоки elif для выполнения кода при обнаружении событий
            # При нажатии (KEYDOWN)
            # При отпускании (KEYUP)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    # Переместить корабль вправо.
                    self.ship.moving_right = True
                elif event.key == pygame.K_LEFT:
                    # Переместить корабль влево.
                    self.ship.moving_left = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = False

    def _update_screen(self):
        """Обновляет изображение на экране и отображает новый экран"""
        # При каждом проходе цикла перерисовывается экран.
        # Для этого вызываем метод fill()
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        # Отображение последнего прорисованного экрана.
        pygame.display.flip()

if __name__ == '__main__':
    # Создание экземпляра и запуск игры.
    ai = AlienInvasion()
    ai.run_game()
