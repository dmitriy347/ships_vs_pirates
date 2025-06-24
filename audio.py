import pygame

class Audio:
    """Класс для звуковых эффектов"""
    def __init__(self):
        pygame.mixer.init()
        self.sound_effects = {'shot': pygame.mixer.Sound("shot.wav")}

    def play_sound(self, sound_name):
        """Воспроизведение звукового эффекта"""
        if sound_name in self.sound_effects:
            self.sound_effects[sound_name].play()
            self.set_sound_volume(0.01)

    def set_sound_volume(self, volume):
        """Настройска громкости звуковых эффектов"""
        for sound in self.sound_effects.values():
            sound.set_volume(volume)


