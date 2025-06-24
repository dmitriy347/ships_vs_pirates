class GameStats():
    """Отслеживание статистики для игры Alien Invasion"""

    def __init__(self, ai_game):
        """Инициализирует статистику"""
        self.settings = ai_game.settings
        self.reset_stats()
        # Игра запускается в неактивном состоянии
        self.game_active = False
        self.button_active = False

        self.high_score = self.load_high_score()


    def load_high_score(self):
        """Читает значение из файла"""
        try:
            with open('record.txt') as file_object:
                # Преобразуем строчнное значение файла str() 
                # в целое число int()
                return int(file_object.read())
                
        # Если файл не существует
        except FileNotFoundError:
            return 0


    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры"""
        self.ship_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
