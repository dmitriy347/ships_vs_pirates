import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """Класс для управления кораблем."""

    def __init__(self, ai_game):
        """Инициализирует корабль и задает его начальную позицию."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Загружает изображение корабля и получает прямоугольник.
        self.image = pygame.image.load('images/battle.png')
        self.rect = self.image.get_rect()

        # Каждый новый корабль появляется по центру слева.
        self.rect.centery = self.screen_rect.centery

        # Сохраненение вещественной координаты центра корябля.
        self.y = float(self.rect.y)

        # Флаги перемещения (верх и вниз).
        self.moving_top = False
        self.moving_bottom = False

    def update(self):
        """Обновляет позицию корабля с учетом флагов."""
        # Обновляется атрибут y, не rect.
        if self.moving_top and self.rect.top > 0:
            self.y -= self.settings.ship_speed_factor

        if self.moving_bottom and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed_factor

        # Обновление атрибута rect на основании self.y
        self.rect.y = self.y

    def blitme(self):
        """Рисует корабль в текущей позиции"""
        self.screen.blit(self.image, self.rect)


    def center_ship(self):
        """Размещает корабль в центре левой стороны"""
        self.rect.centery = self.screen_rect.centery
        self.y = float(self.rect.y)