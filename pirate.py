import pygame
from pygame.sprite import Sprite

class Pirate(Sprite):
    """Класс, представляющий одного пирата"""

    def __init__(self, ai_game):
        """Инициализирует пирата и задает его начальную позицию"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Загрузка изображения пирата и назначение атрибута rect
        self.image = pygame.image.load('images/pirates.png')
        self.rect = self.image.get_rect()

        # Каждый новый пират появляется в правом верхнем углу экрана
        self.rect.x = self.screen_rect.width - 2 * self.rect.width
        self.rect.y = self.rect.height

        # Сохранение вертикальной позиции пирата
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)


    def check_edges(self):
        """Возвращает True, если пират находится у края экрана"""
        screen_rect = self.screen.get_rect()
        if self.rect.bottom >= screen_rect.bottom or self.rect.top <= 0:
            return True



    def update(self):
        """Перемещает пирата вниз"""
        self.y += (self.settings.pirate_speed_factor * self.settings.fleet_direction)
        self.rect.y = self.y
        self.x -= (self.settings.pirate_speed_factor)
        self.rect.x = self.x

