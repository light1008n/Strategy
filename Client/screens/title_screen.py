import pygame

class TitleScreen:
    def __init__(self, manager):
        self.manager = manager
        self.surface = manager.surface
        self.font = pygame.font.SysFont(None, 64)
        self.button_rect = pygame.Rect(300, 300, 200, 60)

    def on_enter(self):
        pass

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(event.pos):
                self.manager.set_screen("game")

    def update(self):
        pass

    def draw(self):
        self.surface.fill((30, 30, 30))
        title_text = self.font.render("Civ-Like Game", True, (255, 255, 255))
        self.surface.blit(title_text, (250, 150))
        pygame.draw.rect(self.surface, (70, 130, 180), self.button_rect)
        button_text = self.font.render("Start", True, (255, 255, 255))
        self.surface.blit(button_text, (self.button_rect.x + 50, self.button_rect.y + 10))
