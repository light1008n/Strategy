import pygame
from map.terrain import TerrainType

TILE_SIZE = 32

class MapView:
    def __init__(self, map_data, screen_rect):
        self.map_data = map_data
        self.map_width = len(map_data[0])
        self.map_height = len(map_data)
        self.scroll_x = 0
        self.scroll_y = 0
        self.screen_rect = screen_rect
        self.mini_width = 200
        self.mini_height = 150

    def handle_input(self, keys):
        if keys[pygame.K_LEFT]:
            self.scroll_x = (self.scroll_x - 5) % (self.map_width * TILE_SIZE)
        if keys[pygame.K_RIGHT]:
            self.scroll_x = (self.scroll_x + 5) % (self.map_width * TILE_SIZE)
        if keys[pygame.K_UP]:
            self.scroll_y = (self.scroll_y - 5) % (self.map_height * TILE_SIZE)
        if keys[pygame.K_DOWN]:
            self.scroll_y = (self.scroll_y + 5) % (self.map_height * TILE_SIZE)

    def draw(self, surface):
        start_col = self.scroll_x // TILE_SIZE
        start_row = self.scroll_y // TILE_SIZE
        offset_x = self.scroll_x % TILE_SIZE
        offset_y = self.scroll_y % TILE_SIZE

        rows = self.screen_rect.height // TILE_SIZE + 2
        cols = self.screen_rect.width // TILE_SIZE + 2

        for row in range(rows):
            for col in range(cols):
                map_x = (start_col + col) % self.map_width
                map_y = (start_row + row) % self.map_height
                terrain = self.map_data[map_y][map_x]
                color = terrain.color
                rect = pygame.Rect(col * TILE_SIZE - offset_x, row * TILE_SIZE - offset_y, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(surface, color, rect)

        self.draw_minimap(surface)

    def draw_minimap(self, surface):
        minimap = pygame.Surface((self.mini_width, self.mini_height))
        minimap.set_alpha(180)

        scale_x = self.mini_width / self.map_width
        scale_y = self.mini_height / self.map_height

        for y in range(self.map_height):
            for x in range(self.map_width):
                color = self.map_data[y][x].color
                minimap.set_at((int(x * scale_x), int(y * scale_y)), color)

        surface.blit(minimap, (self.screen_rect.width - self.mini_width - 10, 10))
