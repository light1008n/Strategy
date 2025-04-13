import pygame
from map.map_generator import MapGenerator
from map.map_view import MapView

class GameScreen:
    def __init__(self, manager):
        self.manager = manager
        self.surface = manager.surface
        self.font = pygame.font.SysFont(None, 36)
        self.map_view = None

    def on_enter(self):
        map_gen = MapGenerator(width=100, height=75)  # 約4倍マップ
        map_data = map_gen.generate()
        self.map_view = MapView(map_data, self.surface.get_rect())

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.manager.set_screen("title")

    def update(self):
        keys = pygame.key.get_pressed()
        self.map_view.handle_input(keys)

    def draw(self):
        self.map_view.draw(self.surface)
        info = self.font.render("←↑↓→ でスクロール, ESCで戻る", True, (255, 255, 255))
        self.surface.blit(info, (10, self.surface.get_height() - 40))
