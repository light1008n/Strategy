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

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("複数ユニット制御")

clock = pygame.time.Clock()

class Unit:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.attack = 20
        self.max_action_points = 2
        self.action_points = self.max_action_points

    def move(self, dx, dy, base, other_units):
        if self.action_points >= 1:
            new_x = self.x + dx
            new_y = self.y + dy
            if new_x == base.x and new_y == base.y:
                print("拠点には侵入できません")
                return
            if any(u.x == new_x and u.y == new_y for u in other_units if u is not self):
                print("他のユニットがいて移動できません")
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
                print("近接攻撃！ 拠点の残りHP:", base.hp)

    def reset_turn(self):
        self.action_points = self.max_action_points

    def draw(self, surface, selected=False):
        color = GREEN if selected else BLUE
        pygame.draw.rect(surface, color, (self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        font = pygame.font.SysFont(None, 24)
        ap_text = font.render(f"AP:{self.action_points}", True, WHITE)
        surface.blit(ap_text, (self.x * TILE_SIZE + 5, self.y * TILE_SIZE + 35))

class RangedUnit(Unit):
    def attack_base(self, base):
        if self.action_points >= 1:
            distance = abs(self.x - base.x) + abs(self.y - base.y)
            if 1 <= distance <= 2:
                base.hp -= self.attack
                self.action_points = 0
                print("遠距離攻撃！ 拠点の残りHP:", base.hp)

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

# 複数ユニットを用意
units = [
    RangedUnit(1, 1),
    Unit(2, 2),
    RangedUnit(3, 3),
]
selected_unit_index = 0
enemy_base = Base(5, 5)

running = True
while running:
    screen.fill(WHITE)

    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            pygame.draw.rect(screen, GRAY, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

    # 拠点とユニット描画
    enemy_base.draw(screen)
    for idx, unit in enumerate(units):
        unit.draw(screen, selected=(idx == selected_unit_index))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            current_unit = units[selected_unit_index]
            if event.key == pygame.K_r:
                for u in units:
                    u.reset_turn()
                print("全ユニットAP回復（ターン終了）")

            elif event.key == pygame.K_TAB:
                selected_unit_index = (selected_unit_index + 1) % len(units)
                print(f"ユニット切り替え → {selected_unit_index}")

            elif event.key == pygame.K_UP:
                current_unit.move(0, -1, enemy_base, units)
            elif event.key == pygame.K_DOWN:
                current_unit.move(0, 1, enemy_base, units)
            elif event.key == pygame.K_LEFT:
                current_unit.move(-1, 0, enemy_base, units)
            elif event.key == pygame.K_RIGHT:
                current_unit.move(1, 0, enemy_base, units)
            elif event.key == pygame.K_SPACE:
                current_unit.attack_base(enemy_base)

    clock.tick(60)

pygame.quit()
