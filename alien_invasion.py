import sys

from time import sleep

import pygame

# Импортируем класс Settings
from settings import Settings

from game_stats import GameStats

from scoreboard import Scoreboard

from button import Button

from button_medium import Button_medium

from button_easy import Button_easy

from button_hard import Button_hard

# Импортируем класс Ship
from ship import Ship

# Импортируем класс Bullet
from bullet import Bullet

from pirate import Pirate

from random import randint

from audio import Audio

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

        # Создание экземпляра для хранения игровой статистики
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.pirates = pygame.sprite.Group()

        self._create_fleet()

        # Создание кнопки Easy
        self.play_button_easy = Button_easy(self, 'Easy')

        # Создание кнопки Medium
        self.play_button_medium = Button_medium(self, 'Medium')
        
        # Создание кнопки Hard
        self.play_button_hard = Button_hard(self, 'Hard')
        
        # Создание кнопки Play
        self.play_button = Button(self, 'Play')

        self.audio = Audio()
        


    # Этот метод управляет процессом игры
    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_pirates()
            self._update_screen()


    def _check_events(self):
        """Обрабатывает нажатия клавиш и события мыши"""
        # Отслеживание событий клавиатуры и мыши.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.sb.save_to_record()
                sys.exit()
            # Добавим блоки elif для выполнения кода при обнаружении событий
            # При нажатии (KEYDOWN)
            # При отпускании (KEYUP)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_button_medium(mouse_pos)
                self._check_button_easy(mouse_pos)
                self._check_button_hard(mouse_pos)


    def start_game(self):
        """Запускает игру либо нажатием мыши по Play, либо кнопкой P"""
        # Сброс игровой статистики
        self.stats.reset_stats()
        
        self.stats.game_active = True

        # Выводим изображения счетов
        self.sb.prep_images()

        # Очистка списков пиратов и снарядов
        self.pirates.empty()
        self.bullets.empty()

        # Создание нового флота и размещение корабля в центре
        self._create_fleet()
        self.ship.center_ship()

        # Указатель мыши скрывается
        pygame.mouse.set_visible(False)


    def _check_play_button(self, mouse_pos):
        """
        Запускает новую игру при нажатии кнопки Play
        и меняет флаг button_active=False
        """
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active and self.stats.button_active:
            self.start_game()
            self.stats.button_active = False


    def _check_button_easy(self, mouse_pos):
        """
        При нажатии на Easy меняет флаг button_active=True
        и выбирает сложность
        """
        button_clicked = self.play_button_easy.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.stats.button_active = True
            self.settings.initialize_dynamic_settings_easy()

    def _check_button_medium(self, mouse_pos):
        """
        При нажатии на Medium меняет флаг button_active=True
        и выбирает сложность
        """
        button_clicked = self.play_button_medium.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.stats.button_active = True
            self.settings.initialize_dynamic_settings_medium()
            

    def _check_button_hard(self, mouse_pos):
        """
        При нажатии на Hard меняет флаг button_active=True
        и выбирает сложность
        """
        button_clicked = self.play_button_hard.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.stats.button_active = True
            self.settings.initialize_dynamic_settings_hard()


    def _check_keydown_events(self, event):
        """Реагирует на нажатие клавиш"""
        if event.key == pygame.K_UP:
            # Переместить корабль вверх.
            self.ship.moving_top = True
        elif event.key == pygame.K_DOWN:
            # Переместить корабль вниз.
            self.ship.moving_bottom = True
        # Добавим выход из программы нажатием клавиши q
        elif event.key == pygame.K_q:
            self.sb.save_to_record()
            sys.exit()

        # При нажатии на пробел вызывается метод _fire_bullet()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

        # При нажатии на P запускается игра
        elif event.key == pygame.K_p:
            if self.stats.button_active:
                self.start_game()
                self.stats.button_active = False


    def _check_keyup_events(self, event):
        """Реагирует на отпускание клавиш"""
        if event.key == pygame.K_UP:
            self.ship.moving_top = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_bottom = False


    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу bullets"""
        # Создаем экземпляр Bullet, которому присваиваем имя new_bullet
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            # Он включается в группу bullets вызовом метода add()
            self.bullets.add(new_bullet)


    def _update_bullets(self):
        """Обновляет позиции снарядов и уничтожает старые снаряды"""
        # Обновление позиций снарядов
        # Вызов update() для группы приводит к автоматическому-
        # -вызову update() для каждого спрайта в группе
        # Эта строка вызывает bullet.update() для каждого снаряда,
        # включенного в группу bullets
        self.bullets.update()
        # Удаление снарядов, вышедших за экран
        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.ship.screen_rect.right:
                self.bullets.remove(bullet)

        self._check_bullet_pirate_collisions()


    def _check_bullet_pirate_collisions(self):
        """Обработка коллизий снарядов с пиратами"""
        # Удаление снарядов и пиратов, участующих в коллизиях 
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.pirates, True, True)            

        if collisions:
            # Переберем словарь collisions и убедимся в том, что очки
            # начисляются за КАЖДОГО подбитого пришельца
            for pirates in collisions.values():
                self.stats.score += self.settings.pirate_points * len(pirates)
            self.sb.prep_score()
            self.sb.check_high_score()
            self.audio.play_sound('shot')

        if not self.pirates:
            # Уничтожение существующих снарядов и создание нового флота
            self.start_new_level()



    def start_new_level(self):
        """Уничтожение существующих снарядов и создание нового флота
        при запуске новой игры
        """
        self.bullets.empty()
        self._create_fleet()
        self.settings.increase_speed()

        self.stats.level += 1
        self.sb.prep_level()


    def _update_pirates(self):
        """
        Проверяет, достиг ли флот края экрана,
        с последующим обновлением позиции всех пиратов во флоте
        """
        self._check_fleet_edges()
        self.pirates.update()
        self.bullets.update()

        # Проверка коллизий "пират - корабль"
        if pygame.sprite.spritecollideany(self.ship, self.pirates):
            self._ship_hit()

        # Проверить добрались ли пираты до левого края экрана
        self._check_pirates_left()


    def _ship_hit(self):
        """Обрабатывает столкновение корабля с пиратом"""
        if self.stats.ship_left > 0:
            # Уменьшение ship_left
            self.stats.ship_left -= 1
            self.sb.prep_ships()

            # Очистка списков пришельцев и снарядов
            self.pirates.empty()
            self.bullets.empty()

            # Создание нового флота
            self._create_fleet()
            self.ship.center_ship()

            # Пауза
            sleep(0.5)

        if self.stats.ship_left == 0:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_pirates_left(self):
        """Проверяет, добрались ли пираты до левого края экрана"""
        screen_rect = self.screen.get_rect()
        for pirate in self.pirates.sprites():
            if pirate.rect.left <= 0:
                # Происходит то же, что при столкновении с кораблем
                self._ship_hit()
                break


    def _create_fleet(self):
        """Создания флота вторжения"""
        # Создание пирата и вычисление количества пиратов в ряду
        # Интервал между пирами равен высоте пирата
        pirate = Pirate(self)
        pirate_height, pirate_width = pirate.rect.size
        available_space_y = self.settings.screen_height - 2 * pirate_height
        number_pirates_y = available_space_y // (2 * pirate_height)

        # Определяет количество рядов, помещающихся на экране
        number_rows = 2

        # Создание флота пиратов
        for row_number in range(number_rows):
            # Создание первого ряда пиратов
            for pirate_number in range (number_pirates_y):
                self._create_pirate(pirate_number, row_number)


    def _create_pirate(self, pirate_number, row_number):
        """Создание пирата и размещение его в ряду"""
        pirate = Pirate(self)
        pirate_height, pirate_width = pirate.rect.size
        pirate.y = pirate_height + 2 * pirate_height * pirate_number
        pirate.rect.y = pirate.y
        screen_rect = self.screen.get_rect()
        pirate.rect.x = self.settings.screen_width - (pirate_width + 2 * 
            pirate_width * row_number)
        self.pirates.add(pirate)


    def _check_fleet_edges(self):
        """Реагирует на достижение пиратом края экрана"""
        for pirate in self.pirates.sprites():
            if pirate.check_edges():
                self._change_fleet_direction()
                break


    def _change_fleet_direction(self):
        """Двигает весь флот влево и меняет направление флота"""
        for pirate in self.pirates.sprites():
            pirate.rect.x -= self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _update_screen(self):
        """Обновляет изображение на экране и отображает новый экран"""
        # При каждом проходе цикла перерисовывается экран.
        # Для этого вызываем метод fill()
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.pirates.draw(self.screen)

        self.sb.show_score()

        # Кнопки Easy, Medium и Hard отображаются в том случае, 
        # если button_active == False
        if not self.stats.button_active and not self.stats.game_active:   
            self.play_button_medium.draw_button_medium()            
            self.play_button_easy.draw_button_easy()
            self.play_button_hard.draw_button_hard()

        # Кнопка Play отображается в том случае, если игра неактивна
        # И button_active == True
        if not self.stats.game_active and self.stats.button_active: 
            self.play_button.draw_button()

        # Отображение последнего прорисованного экрана.
        pygame.display.flip()

if __name__ == '__main__':
    # Создание экземпляра и запуск игры.
    ai = AlienInvasion()
    ai.run_game()
