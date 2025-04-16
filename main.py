import pygame

# ゲーム設定
TILE_SIZE = 64
MAP_WIDTH = 10
MAP_HEIGHT = 8
SCREEN_WIDTH = TILE_SIZE * MAP_WIDTH
SCREEN_HEIGHT = TILE_SIZE * MAP_HEIGHT

# 色定義
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (50, 50, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)

# 初期化
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Civ風ストラテジー")

clock = pygame.time.Clock()

# ユニットクラス
class Unit:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.attack = 20
        self.has_moved = False

    def move(self, dx, dy):
        if not self.has_moved:
            new_x = self.x + dx
            new_y = self.y + dy
            if 0 <= new_x < MAP_WIDTH and 0 <= new_y < MAP_HEIGHT:
                self.x = new_x
                self.y = new_y
                self.has_moved = True

    def attack_base(self, base):
        if self.x == base.x and self.y == base.y:
            base.hp -= self.attack
            print("拠点に攻撃！ 残りHP:", base.hp)

    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, (self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# 拠点クラス
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

# ゲーム用の初期データ
player_unit = Unit(1, 1)
enemy_base = Base(5, 5)

# メインループ
running = True
while running:
    screen.fill(WHITE)

    # タイルの描画
    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            pygame.draw.rect(screen, GRAY, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

    # ユニットと拠点の描画
    player_unit.draw(screen)
    enemy_base.draw(screen)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                player_unit.has_moved = False  # ターンリセット
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
