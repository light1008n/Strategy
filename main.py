import pygame

TILE_SIZE = 64
MAP_WIDTH = 10
MAP_HEIGHT = 8
SCREEN_WIDTH = TILE_SIZE * MAP_WIDTH
SCREEN_HEIGHT = TILE_SIZE * MAP_HEIGHT

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (50, 50, 255)
RED = (255, 50, 50)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Civ風ストラテジー（AP制+攻撃全消費）")

clock = pygame.time.Clock()

class Unit:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.attack = 20
        self.max_action_points = 2
        self.action_points = self.max_action_points

    def move(self, dx, dy):
        if self.action_points >= 1:
            new_x = self.x + dx
            new_y = self.y + dy
            if 0 <= new_x < MAP_WIDTH and 0 <= new_y < MAP_HEIGHT:
                self.x = new_x
                self.y = new_y
                self.action_points -= 1

    def attack_base(self, base):
        if self.action_points >= 1:
            dx = abs(self.x - base.x)
            dy = abs(self.y - base.y)
            if (dx == 1 and dy == 0) or (dx == 0 and dy == 1):  # ← 隣接判定（上下左右）
                base.hp -= self.attack
                self.action_points = 0
                print("拠点に攻撃！ 残りHP:", base.hp)


    def reset_turn(self):
        self.action_points = self.max_action_points

    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, (self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        font = pygame.font.SysFont(None, 24)
        ap_text = font.render(f"AP:{self.action_points}", True, WHITE)
        surface.blit(ap_text, (self.x * TILE_SIZE + 5, self.y * TILE_SIZE + 35))

class Base:
    def __init__(self, x, y, hp=100):
        self.x = x
        self.y = y
        self.hp = hp

    def draw(self, surface):
        color = RED if self.hp > 0 else GRAY
        pygame.draw.rect(surface, color, (self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        font = pygame.font.SysFont(None, 24)
        hp_text = font.render(f"{self.hp}", True, WHITE)
        surface.blit(hp_text, (self.x * TILE_SIZE + 5, self.y * TILE_SIZE + 5))

player_unit = Unit(1, 1)
enemy_base = Base(5, 5)

running = True
while running:
    screen.fill(WHITE)

    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            pygame.draw.rect(screen, GRAY, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

    player_unit.draw(screen)
    enemy_base.draw(screen)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                player_unit.reset_turn()
                print("ターン終了 → AP回復")
            elif event.key == pygame.K_UP:
                player_unit.move(0, -1)
            elif event.key == pygame.K_DOWN:
                player_unit.move(0, 1)
            elif event.key == pygame.K_LEFT:
                player_unit.move(-1, 0)
            elif event.key == pygame.K_RIGHT:
                player_unit.move(1, 0)
            elif event.key == pygame.K_SPACE:
                player_unit.attack_base(enemy_base)

    clock.tick(60)

pygame.quit()
