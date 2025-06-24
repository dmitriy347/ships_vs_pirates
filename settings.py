class Settings():
    """Класс для хранения всех настроек игры Alien Invasion."""

    def __init__(self):
        """Инициализирует настройки игры"""
        # Параметры экрана.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (65, 135, 200)

        # Настройки корабля.
        self.ship_limit = 3

        # Параметры снаряда.
        self.bullet_width = 15
        self.bullet_height = 3
        self.bullet_color = (60, 60, 60)
        # Количество снарядов 
        self.bullets_allowed = 3

        self.fleet_drop_speed = 10

        # Темп ускорения игры
        self.speedup_scale = 1.05

        # Темп роста стоимости пиратов
        self.score_scale = 1.5

        self.initialize_dynamic_settings_easy()
        self.initialize_dynamic_settings_medium()
        self.initialize_dynamic_settings_hard()


    def initialize_dynamic_settings_easy(self):
        """Инициализирует настройки easy, изменяющиеся в ходе игры"""
        self.ship_speed_factor = 0.5
        self.bullet_speed_factor = 0.5
        self.pirate_speed_factor = 0.2

        # fleet_direction = 1 обозначает вниз, -1 обозначает вверх
        self.fleet_direction = 1
        
        # Подсчет очков
        self.pirate_points = 30


    def initialize_dynamic_settings_medium(self):
        """Инициализирует настройки medium, изменяющиеся в ходе игры"""
        self.ship_speed_factor = 0.6
        self.bullet_speed_factor = 0.6
        self.pirate_speed_factor = 0.2

        # fleet_direction = 1 обозначает вниз, -1 обозначает вверх
        self.fleet_direction = 1

        # Подсчет очков
        self.pirate_points = 50


    def initialize_dynamic_settings_hard(self):
        """Инициализирует настройки hard, изменяющиеся в ходе игры"""

        self.ship_speed_factor = 0.7
        self.bullet_speed_factor = 0.7
        self.pirate_speed_factor = 0.3

        # fleet_direction = 1 обозначает вниз, -1 обозначает вверх
        self.fleet_direction = 1
        
        # Подсчет очков
        self.pirate_points = 70


    def increase_speed(self):
        """Увеличивает настройки скорости и стоимости пиратов"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.pirate_speed_factor *= self.speedup_scale

        # int используется чтобы счет возрастал на целое количество очков
        self.pirate_points = int(self.pirate_points * self.score_scale)
