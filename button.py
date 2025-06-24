import pygame.font

class Button():

    def __init__(self,ai_game, msg):
        """Инициализирует атрибуты кнопки"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Назначение размеров и свойств кнопки
        self.width, self.height = 300, 75
        self.button_color = (0, 139, 41)
        self.text_color = (170, 220, 255)
        # Подготовка атрибута font для вывода текста
        # None - означает шрифт по умолчанию, 48 - размер текста
        self.font = pygame.font.SysFont(None, 60)

        # Построение объекта rect кнопки и выравнивания по центру экрана
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Сообщение кнопки создается только один раз
        self._prep_msg(msg)


    def _prep_msg(self, msg):
        """
        Преобразует текст, который хранится в msg, в прямоугольник 
        и выравнивает текст по центру
        """
        self.msg_image = self.font.render(msg, True, self.text_color, 
            self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center


    def draw_button(self):
        """Отображение пустой кнопки и вывод сообщения"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

