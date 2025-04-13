from screens.title_screen import TitleScreen
from screens.game_screen import GameScreen

class ScreenManager:
    def __init__(self, surface):
        self.surface = surface
        self.screens = {
            "title": TitleScreen(self),
            "game": GameScreen(self)
        }
        self.current_screen = None

    def set_screen(self, name):
        self.current_screen = self.screens[name]
        self.current_screen.on_enter()

    def handle_event(self, event):
        if self.current_screen:
            self.current_screen.handle_event(event)

    def update(self):
        if self.current_screen:
            self.current_screen.update()

    def draw(self):
        if self.current_screen:
            self.current_screen.draw()
