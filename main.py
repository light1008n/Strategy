import pygame
import sys

# 定数
TILE_SIZE = 64
MAP_WIDTH = 10
MAP_HEIGHT = 8
SCREEN_WIDTH = TILE_SIZE * MAP_WIDTH
SCREEN_HEIGHT = TILE_SIZE * MAP_HEIGHT + 100

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (50, 50, 255)
GREEN = (50, 255, 50)
RED = (255, 50, 50)
BLACK = (0, 0, 0)

unit_img = pygame.image.load("images/unit.png")
unit_img = pygame.transform.scale(unit_img, (TILE_SIZE, TILE_SIZE))

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("シヴィ風ゲーム")
clock = pygame.time.Clock()
font = pygame.font.SysFont("msgothic", 24)

# ========================== クラス定義 ==========================
class Unit:
    def __init__(self, x, y, is_enemy=False):
        self.x = x
        self.y = y
        self.attack = 20
        self.hp = 100
        self.max_action_points = 2
        self.action_points = self.max_action_points
        self.is_enemy = is_enemy

    def move(self, dx, dy, base, all_units):
        if self.action_points >= 1:
            new_x = self.x + dx
            new_y = self.y + dy
            if new_x == base.x and new_y == base.y:
                return
            if any(u.x == new_x and u.y == new_y for u in all_units if u is not self):
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

    def attack_unit(self, target):
        if self.action_points >= 1:
            dx = abs(self.x - target.x)
            dy = abs(self.y - target.y)
            if (dx == 1 and dy == 0) or (dx == 0 and dy == 1):
                target.hp -= self.attack
                self.action_points = 0

    def reset_turn(self):
        self.action_points = self.max_action_points

    def draw(self, surface, selected=False):
        color = RED if self.is_enemy else BLUE
        
        colored_img = unit_img.copy()
        color_surface = pygame.Surface(colored_img.get_size()).convert_alpha()
        color_surface.fill(color)
        colored_img.blit(color_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        surface.blit(colored_img, (self.x * TILE_SIZE, self.y * TILE_SIZE))

        ap_text = font.render(f"{self.action_points}", True, WHITE)
        surface.blit(ap_text, (self.x * TILE_SIZE + 5, self.y * TILE_SIZE + 35))
        hp_bar_width = int(TILE_SIZE * (self.hp / 100))
        pygame.draw.rect(surface, RED, (self.x * TILE_SIZE, self.y * TILE_SIZE, hp_bar_width, 5))

        # 選択中の枠線
        if selected:
            pygame.draw.rect(surface, GREEN, (self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 3)

class RangedUnit(Unit):
    def attack_base(self, base):
        if self.action_points >= 1:
            distance = abs(self.x - base.x) + abs(self.y - base.y)
            if 1 <= distance <= 2:
                base.hp -= self.attack
                self.action_points = 0

    def attack_unit(self, target):
        if self.action_points >= 1:
            distance = abs(self.x - target.x) + abs(self.y - target.y)
            if 1 <= distance <= 2:
                target.hp -= self.attack
                self.action_points = 0

class Base:
    def __init__(self, x, y, hp=100):
        self.x = x
        self.y = y
        self.hp = hp

    def draw(self, surface):
        color = RED if self.hp > 0 else GRAY
        pygame.draw.rect(surface, color, (self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        hp_text = font.render(f"{self.hp}", True, WHITE)
        surface.blit(hp_text, (self.x * TILE_SIZE + 5, self.y * TILE_SIZE + 5))

# ========================== ユーティリティ関数 ==========================
player_resources = 100  # 初期資源
resource_tiles = [(3, 3), (6, 1), (1, 5)]  # 任意の座標

def draw_ui(surface, current_unit, base, turn_text):
    pygame.draw.rect(surface, WHITE, (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))
    pygame.draw.line(surface, GRAY, (0, SCREEN_HEIGHT - 100), (SCREEN_WIDTH, SCREEN_HEIGHT - 100), 2)
    turn_label = font.render(turn_text, True, BLACK)
    surface.blit(turn_label, (10, SCREEN_HEIGHT - 90))
    if current_unit:
        info = f"選択中: {'敵' if current_unit.is_enemy else '味方'} (HP:{current_unit.hp}, AP:{current_unit.action_points}, ATK:{current_unit.attack})"
        unit_info = font.render(info, True, BLACK)
        surface.blit(unit_info, (10, SCREEN_HEIGHT - 60))
    bar_x = 10
    bar_y = SCREEN_HEIGHT - 30
    bar_width = 200
    bar_height = 20
    hp_ratio = max(0, base.hp) / 100
    pygame.draw.rect(surface, GRAY, (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(surface, RED, (bar_x, bar_y, int(bar_width * hp_ratio), bar_height))
    hp_text = font.render(f"拠点HP: {base.hp}/100", True, BLACK)
    surface.blit(hp_text, (bar_x + 210, bar_y))
    res_text = font.render(f"資源: {player_resources}", True, BLACK)
    surface.blit(res_text, (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 90))

def draw_start_screen():
    screen.fill(WHITE)
    title = font.render("シヴィ風ストラテジーゲーム", True, BLACK)
    start_msg = font.render("スペースキーで開始", True, BLACK)
    screen.blit(title, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
    screen.blit(start_msg, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
    pygame.display.flip()

def process_ai_turn(ai_units, units, player_base):
    for ai in ai_units:
        ai.reset_turn()
        while ai.action_points > 0:
            for target in units:
                ai.attack_unit(target)
                if ai.action_points == 0:
                    break
            else:
                dx = player_base.x - ai.x
                dy = player_base.y - ai.y
                distance = abs(dx) + abs(dy)
                if isinstance(ai, RangedUnit) and 1 <= distance <= 2:
                    ai.attack_base(player_base)
                    continue
                elif not isinstance(ai, RangedUnit) and ((abs(dx) == 1 and dy == 0) or (abs(dy) == 1 and dx == 0)):
                    ai.attack_base(player_base)
                    continue
                step_x = 1 if dx > 0 else -1 if dx < 0 else 0
                step_y = 1 if dy > 0 else -1 if dy < 0 else 0
                ai.move(step_x, step_y, player_base, ai_units + units)

def initialize_game():
    return [RangedUnit(1, 1), Unit(2, 2)], 0, [Unit(8, 6, is_enemy=True), RangedUnit(9, 6, is_enemy=True)], Base(5, 5), Base(0, 0)

# ========================== メインループ ==========================
game_active = False
units, selected_index, ai_units, enemy_base, player_base = initialize_game()

running = True
while running:
    if not game_active:
        draw_start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                units, selected_index, ai_units, enemy_base, player_base = initialize_game()
                game_active = True
        continue

    screen.fill(WHITE)
    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            pygame.draw.rect(screen, GRAY, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

    # 資源タイルを描画（緑色）
    for (x, y) in resource_tiles:
        pygame.draw.rect(screen, (0, 200, 0), (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    player_base.draw(screen)
    enemy_base.draw(screen)

    ai_units = [u for u in ai_units if u.hp > 0]
    units = [u for u in units if u.hp > 0]
    if selected_index >= len(units):
        selected_index = 0

    for i, unit in enumerate(units):
        unit.draw(screen, selected=(i == selected_index))
    for enemy in ai_units:
        enemy.draw(screen)

    if units:
        draw_ui(screen, units[selected_index], player_base, "プレイヤーターン")
    else:
        draw_ui(screen, None, player_base, "味方ユニット全滅…")

    pygame.display.flip()

    # === 勝利 / 敗北処理 ===
    if enemy_base.hp <= 0:
        draw_ui(screen, None, player_base, "🎉 勝利！Rキーでリスタート")
        pygame.display.flip()
        game_active = False
        continue
    elif player_base.hp <= 0 or not units:
        draw_ui(screen, None, player_base, "💀 敗北…Rキーでリスタート")
        pygame.display.flip()
        game_active = False
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if not game_active and event.key == pygame.K_r:
                units, selected_index, ai_units, enemy_base, player_base = initialize_game()
                game_active = True

            if game_active and units:
                current_unit = units[selected_index]
                if event.key == pygame.K_r:
                    for u in units:
                        u.reset_turn()
                    # 資源タイル上にユニットがいれば +5
                    for u in units:
                        if (u.x, u.y) in resource_tiles:
                            player_resources += 5
                    player_resources += 10  # 毎ターン +10
                    process_ai_turn(ai_units, units, player_base)
                elif event.key == pygame.K_TAB:
                    selected_index = (selected_index + 1) % len(units)
                elif event.key == pygame.K_UP:
                    current_unit.move(0, -1, enemy_base, units + ai_units)
                elif event.key == pygame.K_DOWN:
                    current_unit.move(0, 1, enemy_base, units + ai_units)
                elif event.key == pygame.K_LEFT:
                    current_unit.move(-1, 0, enemy_base, units + ai_units)
                elif event.key == pygame.K_RIGHT:
                    current_unit.move(1, 0, enemy_base, units + ai_units)
                elif event.key == pygame.K_SPACE:
                    attacked = False
                    for enemy in ai_units:
                        current_unit.attack_unit(enemy)
                        if current_unit.action_points == 0:
                            attacked = True
                            break
                    if not attacked:
                        current_unit.attack_base(enemy_base)
                elif event.key == pygame.K_s:
                    if current_unit.x == player_base.x and current_unit.y == player_base.y:
                        if player_resources >= 30:
                        # 拠点の周囲マスを探す
                            for dx in range(-1, 2):
                                for dy in range(-1, 2):
                                    new_x = player_base.x + dx
                                    new_y = player_base.y + dy
                                    if 0 <= new_x < MAP_WIDTH and 0 <= new_y < MAP_HEIGHT:
                                        if all(u.x != new_x or u.y != new_y for u in units + ai_units):
                                            units.append(Unit(new_x, new_y))
                                            player_resources -= 30
                                            break
                                else:
                                    continue
                                break
                elif event.key == pygame.K_d:
                    if current_unit.x == player_base.x and current_unit.y == player_base.y:
                        if player_resources >= 50:
                            for dx in range(-1, 2):
                                for dy in range(-1, 2):
                                    new_x = player_base.x + dx
                                    new_y = player_base.y + dy
                                    if 0 <= new_x < MAP_WIDTH and 0 <= new_y < MAP_HEIGHT:
                                        if all(u.x != new_x or u.y != new_y for u in units + ai_units):
                                            units.append(RangedUnit(new_x, new_y))
                                            player_resources -= 50
                                            break
                                else:
                                    continue
                                break

    clock.tick(60)

pygame.quit()
sys.exit()
