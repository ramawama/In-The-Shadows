import pygame

# Class for music playback
class Music():
    def __init__(self):
        # Start menu music
        self.__current_music = 'init'
        self.__music = True
        pygame.mixer.init()

    # Toggles the current state (play/pause) of music
    def toggle(self):
        pygame.mixer.music.pause() if self.__music else pygame.mixer.music.unpause()
        self.__music = not self.__music

    # Changes music, automatically pauses if music was previous paused
    def play_music(self, choice):
        if choice != self.__current_music:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            pygame.mixer.music.load('./assets/sounds/' + choice + '.wav')
            pygame.mixer.music.play(-1)
            if not self.__music:
                pygame.mixer.music.pause()
            self.__current_music = choice