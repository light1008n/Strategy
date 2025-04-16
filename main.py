import pygame

TILE_SIZE = 64
MAP_WIDTH = 10
MAP_HEIGHT = 8
SCREEN_WIDTH = TILE_SIZE * MAP_WIDTH
SCREEN_HEIGHT = TILE_SIZE * MAP_HEIGHT

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (50, 50, 255)
GREEN = (50, 255, 50)
RED = (255, 50, 50)
BLACK = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("AIプレイヤー追加")

clock = pygame.time.Clock()

class Unit:
    def __init__(self, x, y, is_enemy=False):
        self.x = x
        self.y = y
        self.attack = 20
        self.max_action_points = 2
        self.action_points = self.max_action_points
        self.is_enemy = is_enemy

    def move(self, dx, dy, base, other_units):
        if self.action_points >= 1:
            new_x = self.x + dx
            new_y = self.y + dy
            if new_x == base.x and new_y == base.y:
                return
            if any(u.x == new_x and u.y == new_y for u in other_units if u is not self):
                return
            if 0 <= new_x < MAP_WIDTH and 0 <= new_y < MAP_HEIGHT:
                self.x = new_x
                self.y = new_y
                self.action_points -= 1

    def attack_base(self, base):
        if self.action_points >= 1:
            dx = abs(self.x - base.x)
            dy = abs(self.y - base.y)
            if (dx == 1 and dy == 0) or (dx == 0 and dy == 1):
                base.hp -= self.attack
                self.action_points = 0
                print("近接攻撃！拠点の残りHP:", base.hp)

    def reset_turn(self):
        self.action_points = self.max_action_points

    def draw(self, surface, selected=False):
        if self.is_enemy:
            color = BLACK
        else:
            color = GREEN if selected else BLUE
        pygame.draw.rect(surface, color, (self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        font = pygame.font.SysFont(None, 24)
        ap_text = font.render(f"{self.action_points}", True, WHITE)
        surface.blit(ap_text, (self.x * TILE_SIZE + 5, self.y * TILE_SIZE + 35))

class RangedUnit(Unit):
    def attack_base(self, base):
        if self.action_points >= 1:
            distance = abs(self.x - base.x) + abs(self.y - base.y)
            if 1 <= distance <= 2:
                base.hp -= self.attack
                self.action_points = 0
                print("遠距離攻撃！拠点の残りHP:", base.hp)

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

# プレイヤーユニット
units = [
    RangedUnit(1, 1),
    Unit(2, 2),
]
selected_unit_index = 0

# 拠点
enemy_base = Base(5, 5)
player_base = Base(0, 0)

# AIユニット
ai_units = [
    Unit(8, 6, is_enemy=True),
    RangedUnit(9, 6, is_enemy=True),
]

def process_ai_turn():
    print("🔁 AIのターン開始")
    for ai in ai_units:
        ai.reset_turn()
        while ai.action_points > 0:
            dx = player_base.x - ai.x
            dy = player_base.y - ai.y
            distance = abs(dx) + abs(dy)

            # 攻撃できるなら攻撃
            if isinstance(ai, RangedUnit):
                if 1 <= distance <= 2:
                    ai.attack_base(player_base)
                    continue
            else:
                if (abs(dx) == 1 and dy == 0) or (abs(dy) == 1 and dx == 0):
                    ai.attack_base(player_base)
                    continue

            # 移動（最短経路のような単純ロジック）
            step_x = 1 if dx > 0 else -1 if dx < 0 else 0
            step_y = 1 if dy > 0 else -1 if dy < 0 else 0
            ai.move(step_x, step_y, player_base, ai_units + units)

running = True
while running:
    screen.fill(WHITE)

    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            pygame.draw.rect(screen, GRAY, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

    player_base.draw(screen)
    enemy_base.draw(screen)

    for idx, unit in enumerate(units):
        unit.draw(screen, selected=(idx == selected_unit_index))

    for ai in ai_units:
        ai.draw(screen)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            current_unit = units[selected_unit_index]
            if event.key == pygame.K_r:
                for u in units:
                    u.reset_turn()
                process_ai_turn()  # AIのターン実行
                print("🔄 ターン終了")

            elif event.key == pygame.K_TAB:
                selected_unit_index = (selected_unit_index + 1) % len(units)

            elif event.key == pygame.K_UP:
                current_unit.move(0, -1, enemy_base, units + ai_units)
            elif event.key == pygame.K_DOWN:
                current_unit.move(0, 1, enemy_base, units + ai_units)
            elif event.key == pygame.K_LEFT:
                current_unit.move(-1, 0, enemy_base, units + ai_units)
            elif event.key == pygame.K_RIGHT:
                current_unit.move(1, 0, enemy_base, units + ai_units)
            elif event.key == pygame.K_SPACE:
                current_unit.attack_base(enemy_base)

    clock.tick(60)

pygame.quit()
