import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard():
    """Класс для вывода игровой информации"""
    def __init__(self, ai_game):
        """Инициализирует атрибуты подсчета очков"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Настройки шрифта для вывода счета
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None, 48)
        # Подготовка изображений счетов
        self.prep_images()


    def prep_images(self):
        """
        Объединяет методы подготовки изображений счетов
        для сокращения длины __init__
        """
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()


    def prep_score(self):
        """Преобразует текущий счет в графическое изображение"""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, 
            self.settings.bg_color)

        # Вывод счета в правой верхней части экрана
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20


    def prep_high_score(self):
        """Преобразует рекордный счет в графическое изображение"""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, 
            self.text_color, self.settings.bg_color)

        # Рекорд выравнивается по центру верхней строки
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top + 20


    def check_high_score(self):
        """Проверяет, появился ли новый рекорд"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()


    def prep_level(self):
        """Преобразует уровень в графическое изображение"""
        level_str = str(f'level {self.stats.level}')
        self.level_image = self.font.render(level_str, True,
            self.text_color, self.settings.bg_color)

        # Уровень выводится под текущим счетом
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10


    def prep_ships(self):
        """Сообщает количество оставшихся кораблей"""
        self.ships = Group()
        for ship_number in range(self.stats.ship_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)


    def save_to_record(self):
        """Сохраняет рекорд"""
        if self.stats.score == self.stats.high_score:
            self.stats.high_score = self.stats.score
            filename = 'record.txt'
            with open(filename, 'w') as file_object:
                file_object.write(str(self.stats.high_score))


    def show_score(self):
        """Выводит счет, рекорд и число оставшихся кораблей на экран"""
        self.screen.blit(self.score_image, self.score_rect) 
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)




