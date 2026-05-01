import pygame
import random
import sys
import json
import os
import math

# ===================== تنظیمات اولیه =====================
pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("NeonPulse: Starstrike 🌌🚀")

# رنگ‌ها
BLACK = (10, 10, 20)
NEON_CYAN = (0, 255, 255)
NEON_PINK = (255, 0, 255)
NEON_YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
STAR_GRAY = (150, 150, 150)
GREEN = (0, 255, 0)
DARK_GRAY = (50, 50, 50)

# تم‌های بک‌گراند بر اساس لِوِل
BACKGROUND_THEMES = [
    {"bg_color": (10, 10, 30), "star_color": STAR_GRAY, "particle_colors": [NEON_CYAN, NEON_PINK]},      # لِوِل 1-3: آبی-بنفش
    {"bg_color": (30, 10, 20), "star_color": (200, 150, 150), "particle_colors": [NEON_PINK, NEON_YELLOW]}, # لِوِل 4-6: صورتی-قرمز
    {"bg_color": (10, 30, 10), "star_color": (150, 200, 150), "particle_colors": [NEON_YELLOW, GREEN]},    # لِوِل 7+: زرد-سبز
    {"bg_color": (20, 10, 40), "star_color": (200, 200, 255), "particle_colors": [NEON_CYAN, WHITE]},     # باس فایت: بنفش عمیق
]

# فونت‌ها
font_big = pygame.font.SysFont("consolas", 48, bold=True)
font_small = pygame.font.SysFont("consolas", 24)
font_tiny = pygame.font.SysFont("consolas", 18)

# ستاره‌ها
stars = [(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), random.randint(1, 3))
         for _ in range(100)]

# مسیر فایل‌های صوتی
SOUND_PATH = "assets"
SOUNDS = {
    "menu_music": os.path.join(SOUND_PATH, "menu_music.mp3"),
    "bg_music": os.path.join(SOUND_PATH, "background.mp3"),
    "laser": os.path.join(SOUND_PATH, "laser.wav"),
    "explosion": os.path.join(SOUND_PATH, "explosion.wav"),
    "powerup": os.path.join(SOUND_PATH, "powerup.wav"),
    "boss_hit": os.path.join(SOUND_PATH, "hit.wav"),
    "boss_explosion": os.path.join(SOUND_PATH, "boss_explosion.wav"),
    "select": os.path.join(SOUND_PATH, "select.wav"),
    "combo": os.path.join(SOUND_PATH, "combo.wav")  # اختیاری - اگر فایل صوتی داری
}

# متغیرهای تنظیمات صدا
music_volume = 0.5
sfx_volume = 0.7
mute_all = False
current_music = None

# لود صداها
sound_objects = {}

def load_music(music_name):
    global current_music
    if mute_all:
        return
    try:
        if music_name in SOUNDS:
            pygame.mixer.music.load(SOUNDS[music_name])
            pygame.mixer.music.set_volume(music_volume)
            pygame.mixer.music.play(-1)
            current_music = music_name
        else:
            print(f"موسیقی {music_name} پیدا نشد")
    except Exception as e:
        print(f"خطا در لود موسیقی {music_name}: {e}")

for name, path in SOUNDS.items():
    try:
        if name not in ["bg_music", "menu_music"]:
            sound_objects[name] = pygame.mixer.Sound(path)
            sound_objects[name].set_volume(sfx_volume)
    except Exception as e:
        print(f"خطا در لود فایل صوتی {name}: {e}")

# ===================== صفحه ارائه ساده (Ali Kamrani Presents) =====================
game_state = "presents"  # بازی از این صفحه شروع می‌شود

presents_alpha = 0
presents_timer = 0
presents_phase = "fade_in"  # fade_in → hold → fade_out

def draw_presents_screen():
    global presents_alpha, presents_timer, presents_phase, game_state

    screen.fill((0, 0, 0))  # صفحه کاملاً سیاه

    text = font_small.render("Ali Kamrani Presents", True, NEON_CYAN)
    text.set_alpha(int(presents_alpha))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)

    presents_timer += 1

    if presents_phase == "fade_in":
        presents_alpha = min(255, presents_alpha + 3)
        if presents_alpha >= 255:
            presents_phase = "hold"
            presents_timer = 0

    elif presents_phase == "hold":
        if presents_timer >= 180:  # حدود 3 ثانیه نگه داشتن
            presents_phase = "fade_out"

    elif presents_phase == "fade_out":
        presents_alpha = max(0, presents_alpha - 4)
        if presents_alpha <= 0:
            game_state = "menu"
            title_y = -50
            title_alpha = 0
            load_music("menu_music")  # آهنگ منو بعد از صفحه ارائه شروع می‌شود

    pygame.display.flip()

# ===================== توابع کمکی =====================
HIGH_SCORE_FILE = "neonpulse_highscore.json"
SETTINGS_FILE = "neonpulse_settings.json"

def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as f:
            data = json.load(f)
            return data.get("classic", 0), data.get("survival", 0), data.get("boss_rush", 0)
    return 0, 0, 0

def save_high_score(classic, survival, boss_rush):
    with open(HIGH_SCORE_FILE, "w") as f:
        json.dump({"classic": classic, "survival": survival, "boss_rush": boss_rush}, f)

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            settings = json.load(f)
            return (
                settings.get("difficulty", 1.0),
                settings.get("music_volume", 0.5),
                settings.get("sfx_volume", 0.7),
                settings.get("mute_all", False)
            )
    return 1.0, 0.5, 0.7, False

def save_settings(difficulty, music_vol, sfx_vol, mute):
    with open(SETTINGS_FILE, "w") as f:
        json.dump({
            "difficulty": difficulty,
            "music_volume": music_vol,
            "sfx_volume": sfx_vol,
            "mute_all": mute
        }, f)

# لیست‌های جدید
particles = []
background_particles = []
score_popups = []
combo_popups = []

# متغیرهای جدید
combo_count = 0
combo_timer = 0
score_multiplier = 1.0
last_kill_time = 0
game_mode = "classic"  # classic, survival, boss_rush

def reset_game():
    global player, score, level, wave_count, boss_active, particles, shake_timer
    global background_particles, score_popups, combo_popups, combo_count, combo_timer, score_multiplier, last_kill_time
    
    all_sprites.empty()
    bullets.empty()
    enemy_bullets.empty()
    enemies.empty()
    powerups.empty()
    particles.clear()
    background_particles.clear()
    score_popups.clear()
    combo_popups.clear()

    # بک‌گراند پویا
    theme = get_current_theme()
    for _ in range(50):
        background_particles.append(Particle(
            random.randint(0, SCREEN_WIDTH),
            random.randint(-50, SCREEN_HEIGHT),
            random.choice(theme["particle_colors"]),
            trail=True
        ))

    player = Player()
    all_sprites.add(player)
    score = 0
    level = 1
    wave_count = 0
    boss_active = False
    shake_timer = 0
    combo_count = 0
    combo_timer = 0
    score_multiplier = 1.0
    last_kill_time = 0

    if game_mode == "survival":
        player.hp = 1

def get_current_theme():
    if boss_active:
        return BACKGROUND_THEMES[3]
    level_group = (level - 1) // 3
    return BACKGROUND_THEMES[min(level_group, len(BACKGROUND_THEMES) - 2)]

def spawn_enemy_wave():
    count = int(4 + level * difficulty)
    for i in range(count):
        x = 80 + (SCREEN_WIDTH - 160) * i / max(1, count - 1)
        typ = "shooter" if random.random() < 0.15 * level * difficulty else "normal"
        enemy = Enemy(x, -40, typ)
        all_sprites.add(enemy)
        enemies.add(enemy)

def create_particles(x, y, color, count=30):
    for _ in range(count):
        particles.append(Particle(x, y, random.choice([color, NEON_CYAN, WHITE])))

def draw_stars():
    global stars, background_particles
    theme = get_current_theme()
    screen.fill(theme["bg_color"])
    
    new_stars = []
    for x, y, size in stars:
        y += size * 0.6 * difficulty
        if y > SCREEN_HEIGHT:
            y = 0
            x = random.randint(0, SCREEN_WIDTH)
        new_stars.append((x, y, size))
        pygame.draw.circle(screen, theme["star_color"], (int(x), int(y)), size)
    stars = new_stars

    new_bg = []
    for p in background_particles:
        p.update()
        if p.y > SCREEN_HEIGHT + 20:
            p.y = -20
            p.x = random.randint(0, SCREEN_WIDTH)
        else:
            new_bg.append(p)
        p.draw()
    background_particles = new_bg

def draw_hud():
    theme = get_current_theme()
    pygame.draw.rect(screen, DARK_GRAY, (10, SCREEN_HEIGHT - 40, 150, 20))
    hp_width = (player.hp / (1 if game_mode == "survival" else 3)) * 140
    pygame.draw.rect(screen, NEON_CYAN, (15, SCREEN_HEIGHT - 35, hp_width, 10))
    pygame.draw.rect(screen, WHITE, (10, SCREEN_HEIGHT - 40, 150, 20), 2)
    shield_text = font_tiny.render(f"Shield: {player.shield}", True, GREEN)
    screen.blit(shield_text, (170, SCREEN_HEIGHT - 35))

    texts = [
        f"Score: {int(score)}",
        f"Level: {level}",
        f"Wave: {wave_count}",
        f"Mode: {game_mode.capitalize()}"
    ]
    for i, txt in enumerate(texts):
        scale = 1.0 + 0.1 * math.sin(score_pulse * 0.1) if i == 0 else 1.0
        surf = font_small.render(txt, True, WHITE)
        surf = pygame.transform.scale(surf, (int(surf.get_width() * scale), int(surf.get_height() * scale)))
        screen.blit(surf, (10, 10 + i * 35))

    if combo_count > 1:
        combo_text = font_small.render(f"COMBO x{combo_count}", True, NEON_YELLOW)
        mult_text = font_small.render(f"x{score_multiplier:.1f}", True, NEON_PINK)
        screen.blit(combo_text, (SCREEN_WIDTH - 150, 50))
        screen.blit(mult_text, (SCREEN_WIDTH - 150, 80))

    if player.powerup_timer > 0:
        timer_text = font_tiny.render(f"Power-Up: {player.powerup_timer//60}s", True, NEON_YELLOW)
        screen.blit(timer_text, (SCREEN_WIDTH - 150, 10))

    if boss_active and any(isinstance(e, Boss) for e in enemies):
        boss = next((e for e in enemies if isinstance(e, Boss)), None)
        if boss and boss.alive:
            pygame.draw.rect(screen, DARK_GRAY, (SCREEN_WIDTH - 210, 10, 200, 20))
            hp_width = (boss.health / boss.max_health) * 190
            pygame.draw.rect(screen, NEON_PINK, (SCREEN_WIDTH - 205, 15, hp_width, 10))
            pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH - 210, 10, 200, 20), 2)
            hp_text = font_tiny.render(f"Boss HP: {boss.health}/{boss.max_health}", True, WHITE)
            screen.blit(hp_text, (SCREEN_WIDTH - 210, 35))

# ===================== کلاس‌های انیمیشن =====================
class Particle:
    def __init__(self, x, y, color, trail=False):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 6) if not trail else 2
        self.speed = random.uniform(3, 8) if not trail else 3.5
        self.angle = random.uniform(0, math.tau) if not trail else 0
        self.lifetime = random.randint(20, 50) if not trail else 30
        self.trail = trail

    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed if not self.trail else self.speed
        self.lifetime -= 1
        self.size = max(1, self.size - 0.2)

    def draw(self):
        if self.lifetime <= 0:
            return
        alpha = int(255 * (self.lifetime / 50.0))
        alpha = max(0, min(255, alpha))
        surf = pygame.Surface((int(self.size * 2 + 4), int(self.size * 2 + 4)), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*self.color, alpha), (int(self.size + 2), int(self.size + 2)), int(self.size + 1))
        screen.blit(surf, (int(self.x - self.size - 2), int(self.y - self.size - 2)))

class ScorePopup:
    def __init__(self, x, y, points):
        self.x = x
        self.y = y
        self.points = points
        self.timer = 60
        self.alpha = 255
        self.color = NEON_YELLOW if points >= 80 else WHITE

    def update(self):
        self.y -= 1.5
        self.timer -= 1
        self.alpha = 255 * (self.timer / 60)

    def draw(self):
        text = font_tiny.render(f"+{self.points}", True, self.color)
        text.set_alpha(int(self.alpha))
        rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, rect)

class ComboPopup:
    def __init__(self, x, y, count):
        self.x = x
        self.y = y
        self.count = count
        self.timer = 90
        self.alpha = 255
        self.scale = 0.5

    def update(self):
        self.y -= 2
        self.timer -= 1
        self.alpha = 255 * (self.timer / 90)
        self.scale = 1.0 + 0.5 * math.sin(self.timer * 0.2)

    def draw(self):
        text = font_small.render(f"COMBO x{self.count}!", True, NEON_YELLOW)
        text.set_alpha(int(self.alpha))
        scaled = pygame.transform.scale(text, (int(text.get_width() * self.scale), int(text.get_height() * self.scale)))
        rect = scaled.get_rect(center=(self.x, self.y))
        screen.blit(scaled, rect)

class GlowEffect:
    def __init__(self):
        self.alpha = 0
        self.direction = 1
        self.speed = 5

    def update(self):
        self.alpha += self.direction * self.speed
        if self.alpha >= 100:
            self.alpha = 100
            self.direction = -1
        elif self.alpha <= 0:
            self.alpha = 0
            self.direction = 1
        return self.alpha / 255

# ===================== کلاس‌های بازی =====================
class MenuShip(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 40), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, NEON_CYAN, [(15, 0), (0, 40), (30, 40)])
        pygame.draw.polygon(self.image, WHITE, [(15, 0), (0, 40), (30, 40)], 2)
        self.rect = self.image.get_rect(center=(random.randint(50, SCREEN_WIDTH-50), random.randint(50, SCREEN_HEIGHT-50)))
        self.speed = 2
        self.angle = random.uniform(0, math.tau)
        self.timer = 0

    def update(self):
        self.timer += 1
        self.rect.x += math.cos(self.angle) * self.speed
        self.rect.y += math.sin(self.angle) * self.speed
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.angle = math.pi - self.angle
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.angle = -self.angle
        if self.timer > 120:
            self.angle = random.uniform(0, math.tau)
            self.timer = 0

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.base_image = pygame.Surface((40, 50), pygame.SRCALPHA)
        pygame.draw.polygon(self.base_image, NEON_CYAN, [(20, 0), (0, 50), (40, 50)])
        pygame.draw.polygon(self.base_image, WHITE, [(20, 0), (0, 50), (40, 50)], 2)
        self.image = self.base_image
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT-40))
        self.speed = 6
        self.shoot_delay = 0
        self.hp = 3
        self.shield = 0
        self.triple_shot = False
        self.speed_boost = False
        self.powerup_timer = 0
        self.shield_flash_timer = 0

    def update(self):
        keys = pygame.key.get_pressed()
        speed = self.speed * 1.5 if self.speed_boost else self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x = max(0, self.rect.x - speed)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x = min(SCREEN_WIDTH - self.rect.width, self.rect.x + speed)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.rect.y = max(SCREEN_HEIGHT*0.65, self.rect.y - speed)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.rect.y = min(SCREEN_HEIGHT - self.rect.height, self.rect.y + speed)
        self.shoot_delay = max(0, self.shoot_delay - 1)

        if self.powerup_timer > 0:
            self.powerup_timer -= 1
            if self.powerup_timer <= 0:
                self.triple_shot = False
                self.speed_boost = False

        if self.shield_flash_timer > 0:
            self.shield_flash_timer -= 1

        if self.triple_shot or self.speed_boost:
            scale = 1.0 + 0.1 * math.sin(pygame.time.get_ticks() / 100)
            self.image = pygame.transform.scale(self.base_image, (int(40 * scale), int(50 * scale)))
            self.rect = self.image.get_rect(center=self.rect.center)
        else:
            self.image = self.base_image

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 14), pygame.SRCALPHA)
        pygame.draw.rect(self.image, NEON_YELLOW, (0, 0, 4, 14))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -14
        self.trail_timer = 0

    def update(self):
        self.rect.y += self.speed
        self.trail_timer += 1
        if self.trail_timer >= 2:
            particles.append(Particle(self.rect.centerx, self.rect.bottom, NEON_YELLOW, trail=True))
            self.trail_timer = 0
        if self.rect.bottom < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type="normal"):
        super().__init__()
        self.type = enemy_type
        size = (40, 40) if enemy_type == "shooter" else (30, 30)
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        if enemy_type == "shooter":
            pygame.draw.rect(self.image, NEON_PINK, (0, 0, *size))
            pygame.draw.rect(self.image, WHITE, (0, 0, *size), 2)
        else:
            pygame.draw.circle(self.image, NEON_PINK, (size[0]//2, size[1]//2), size[0]//2)
            pygame.draw.circle(self.image, WHITE, (size[0]//2, size[1]//2), size[0]//2, 2)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = random.randint(3, 6) * difficulty
        self.wave = random.uniform(-0.06, 0.06)
        self.shoot_timer = random.randint(60, 120) if enemy_type == "shooter" else 0

    def update(self):
        self.rect.y += self.speed
        self.rect.x += int(self.wave * SCREEN_WIDTH * 0.1)
        if self.type == "shooter" and self.shoot_timer > 0:
            self.shoot_timer -= 1
            if self.shoot_timer <= 0:
                bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
                all_sprites.add(bullet)
                enemy_bullets.add(bullet)
                self.shoot_timer = random.randint(80, 150)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 14), pygame.SRCALPHA)
        pygame.draw.rect(self.image, NEON_PINK, (0, 0, 4, 14))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 8 * difficulty
        self.trail_timer = 0

    def update(self):
        self.rect.y += self.speed
        self.trail_timer += 1
        if self.trail_timer >= 2:
            particles.append(Particle(self.rect.centerx, self.rect.top, NEON_PINK, trail=True))
            self.trail_timer = 0
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((160, 100), pygame.SRCALPHA)
        pygame.draw.rect(self.image, NEON_PINK, (0, 0, 160, 100))
        pygame.draw.rect(self.image, WHITE, (0, 0, 160, 100), 4)
        self.rect = self.image.get_rect(centerx=SCREEN_WIDTH//2, y=-120)
        self.speed = 2.5 * difficulty
        self.health = int(60 * difficulty)
        self.max_health = self.health
        self.direction = 1
        self.shoot_timer = 40
        self.alive = True
        self.intro_timer = 60
        self.pulse_timer = 0

    def update(self):
        if not self.alive:
            return
        self.pulse_timer += 0.1

        if self.intro_timer > 0:
            self.rect.y += self.speed * 2
            self.intro_timer -= 1
            return

        if self.rect.top < 80:
            self.rect.y += self.speed
        self.rect.x += self.speed * self.direction
        if self.rect.left < 40 or self.rect.right > SCREEN_WIDTH - 40:
            self.direction *= -1

        self.shoot_timer -= 1
        if self.shoot_timer <= 0:
            for offset in [-20, 0, 20]:
                bullet = EnemyBullet(self.rect.centerx + offset, self.rect.bottom)
                all_sprites.add(bullet)
                enemy_bullets.add(bullet)
            self.shoot_timer = 35

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, ptype):
        super().__init__()
        self.ptype = ptype
        self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
        color = NEON_YELLOW if ptype in ["triple", "speed"] else GREEN
        pygame.draw.circle(self.image, color, (12, 12), 12)
        pygame.draw.circle(self.image, WHITE, (12, 12), 12, 2)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 3.5
        self.pulse_timer = random.uniform(0, math.tau)

    def update(self):
        self.rect.y += self.speed
        self.pulse_timer += 0.1
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# ===================== توابع منو =====================
def draw_menu():
    global menu_pulse, title_y, title_alpha
    screen.fill(BLACK)
    draw_stars()
    menu_ships.update()
    menu_ships.draw(screen)
    menu_pulse += 1
    glow_alpha = glow_effect.update()

    if title_y < 100:
        title_y += 5
        title_alpha = min(title_alpha + 10, 255)
    title = font_big.render("NeonPulse: Starstrike", True, NEON_CYAN)
    title.set_alpha(title_alpha)
    title_rect = title.get_rect(center=(SCREEN_WIDTH//2, title_y))
    screen.blit(title, title_rect)

    glow_surf = pygame.Surface((title_rect.width + 20, title_rect.height + 20), pygame.SRCALPHA)
    pygame.draw.rect(glow_surf, (*NEON_CYAN, int(50 * glow_alpha)), (0, 0, title_rect.width + 20, title_rect.height + 20), 5)
    screen.blit(glow_surf, (title_rect.x - 10, title_rect.y - 10))

    menu_items = ["Classic Mode", "Survival Mode", "Boss Rush", "Difficulty", "Sound Settings", "About", "Quit"]
    mouse_pos = pygame.mouse.get_pos()
    for i, item in enumerate(menu_items):
        y = 180 + i * 55
        is_selected = i == menu_selection
        is_hovered = SCREEN_WIDTH//2 - 150 <= mouse_pos[0] <= SCREEN_WIDTH//2 + 150 and y - 20 <= mouse_pos[1] <= y + 20
        color = NEON_CYAN if is_selected or is_hovered else WHITE
        scale = 1.0 + 0.1 * math.sin(menu_pulse * 0.1) if is_selected or is_hovered else 1.0
        text = font_small.render(item, True, color)
        text = pygame.transform.scale(text, (int(text.get_width() * scale), int(text.get_height() * scale)))
        rect = text.get_rect(center=(SCREEN_WIDTH//2, y))
        screen.blit(text, rect)
        if is_selected or is_hovered:
            glow_surf = pygame.Surface((rect.width + 10, rect.height + 10), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (*NEON_CYAN, int(50 * glow_alpha)), (0, 0, rect.width + 10, rect.height + 10), 3)
            screen.blit(glow_surf, (rect.x - 5, rect.y - 5))

    pygame.display.flip()

def draw_difficulty_menu():
    screen.fill(BLACK)
    draw_stars()
    glow_alpha = glow_effect.update()
    title = font_small.render("Select Difficulty", True, NEON_CYAN)
    screen.blit(title, title.get_rect(center=(SCREEN_WIDTH//2, 100)))

    difficulties = [("Easy", "Less enemies, slower pace", 0.8), ("Normal", "Balanced challenge", 1.0), ("Hard", "Ultimate test!", 1.2)]
    mouse_pos = pygame.mouse.get_pos()
    for i, (name, desc, diff) in enumerate(difficulties):
        y = 200 + i * 80
        is_selected = i == selected_difficulty
        is_hovered = SCREEN_WIDTH//2 - 150 <= mouse_pos[0] <= SCREEN_WIDTH//2 + 150 and y - 30 <= mouse_pos[1] <= y + 30
        color = NEON_CYAN if is_selected or is_hovered else WHITE
        pygame.draw.rect(screen, color, (SCREEN_WIDTH//2 - 150, y, 300, 60), 3)
        name_text = font_small.render(name, True, color)
        desc_text = font_tiny.render(desc, True, WHITE)
        screen.blit(name_text, (SCREEN_WIDTH//2 - name_text.get_width()//2, y + 10))
        screen.blit(desc_text, (SCREEN_WIDTH//2 - desc_text.get_width()//2, y + 40))
        if is_selected or is_hovered:
            glow_surf = pygame.Surface((310, 70), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (*NEON_CYAN, int(50 * glow_alpha)), (0, 0, 310, 70), 5)
            screen.blit(glow_surf, (SCREEN_WIDTH//2 - 155, y - 5))

    back_text = font_small.render("Back (B)", True, WHITE)
    screen.blit(back_text, back_text.get_rect(center=(SCREEN_WIDTH//2, 460)))
    pygame.display.flip()

def draw_sound_settings():
    global music_volume, sfx_volume, mute_all
    screen.fill(BLACK)
    draw_stars()
    glow_alpha = glow_effect.update()
    title = font_small.render("Sound Settings", True, NEON_CYAN)
    screen.blit(title, title.get_rect(center=(SCREEN_WIDTH//2, 100)))

    mouse_pos = pygame.mouse.get_pos()
    settings = [("Music Volume", music_volume), ("SFX Volume", sfx_volume), ("Mute All", mute_all)]
    for i, (name, value) in enumerate(settings):
        y = 200 + i * 80
        is_selected = i == menu_selection
        is_hovered = SCREEN_WIDTH//2 - 150 <= mouse_pos[0] <= SCREEN_WIDTH//2 + 150 and y - 30 <= mouse_pos[1] <= y + 30
        color = NEON_CYAN if is_selected or is_hovered else WHITE
        if name == "Mute All":
            text = font_small.render(f"{name}: {'On' if value else 'Off'}", True, color)
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, y + 10))
        else:
            text = font_small.render(f"{name}: {int(value * 100)}%", True, color)
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, y + 10))
            bar_width = 200
            pygame.draw.rect(screen, DARK_GRAY, (SCREEN_WIDTH//2 - 100, y + 40, bar_width, 10))
            fill_width = bar_width * value
            pygame.draw.rect(screen, NEON_CYAN, (SCREEN_WIDTH//2 - 100, y + 40, fill_width, 10))
            pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH//2 - 100, y + 40, bar_width, 10), 2)
        if is_selected or is_hovered:
            glow_surf = pygame.Surface((310, 70), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (*NEON_CYAN, int(50 * glow_alpha)), (0, 0, 310, 70), 5)
            screen.blit(glow_surf, (SCREEN_WIDTH//2 - 155, y - 5))

    back_text = font_small.render("Back (B)", True, WHITE)
    screen.blit(back_text, back_text.get_rect(center=(SCREEN_WIDTH//2, 460)))
    pygame.display.flip()

def draw_about():
    screen.fill(BLACK)
    draw_stars()
    glow_alpha = glow_effect.update()
    title = font_big.render("About", True, NEON_CYAN)
    credit = font_small.render("This Game is created by Ali Kamrani", True, WHITE)
    back_text = font_small.render("Back (B)", True, WHITE)
    title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
    screen.blit(title, title_rect)
    screen.blit(credit, credit.get_rect(center=(SCREEN_WIDTH//2, 250)))
    screen.blit(back_text, back_text.get_rect(center=(SCREEN_WIDTH//2, 400)))
    glow_surf = pygame.Surface((title_rect.width + 20, title_rect.height + 20), pygame.SRCALPHA)
    pygame.draw.rect(glow_surf, (*NEON_CYAN, int(50 * glow_alpha)), (0, 0, title_rect.width + 20, title_rect.height + 20), 5)
    screen.blit(glow_surf, (title_rect.x - 10, title_rect.y - 10))
    pygame.display.flip()

def draw_game_over():
    global game_over_alpha
    screen.fill(BLACK)
    draw_stars()
    game_over_alpha = min(game_over_alpha + 5, 255)
    go = font_big.render("GAME OVER", True, NEON_PINK)
    mode = font_small.render(f"Mode: {game_mode.capitalize()}", True, WHITE)
    sc = font_small.render(f"Score: {int(score)}", True, WHITE)
    hs = font_small.render(f"High Score ({game_mode.capitalize()}): {high_score_classic if game_mode == 'classic' else high_score_survival if game_mode == 'survival' else high_score_boss_rush}", True, WHITE)
    restart = font_small.render("SPACE - Restart    M - Menu", True, WHITE)
    for surf in [go, mode, sc, hs, restart]:
        surf.set_alpha(game_over_alpha)
    screen.blit(go, go.get_rect(center=(SCREEN_WIDTH//2, 120)))
    screen.blit(mode, mode.get_rect(center=(SCREEN_WIDTH//2, 180)))
    screen.blit(sc, sc.get_rect(center=(SCREEN_WIDTH//2, 220)))
    screen.blit(hs, hs.get_rect(center=(SCREEN_WIDTH//2, 260)))
    screen.blit(restart, restart.get_rect(center=(SCREEN_WIDTH//2, 340)))
    glow_alpha = glow_effect.update()
    glow_surf = pygame.Surface((go.get_width() + 20, go.get_height() + 20), pygame.SRCALPHA)
    pygame.draw.rect(glow_surf, (*NEON_PINK, int(50 * glow_alpha)), (0, 0, go.get_width() + 20, go.get_height() + 20), 5)
    glow_surf.set_alpha(game_over_alpha)
    screen.blit(glow_surf, (SCREEN_WIDTH//2 - go.get_width()//2 - 10, 110))
    pygame.display.flip()

# ===================== متغیرهای بازی =====================
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
powerups = pygame.sprite.Group()
menu_ships = pygame.sprite.Group()
for _ in range(3):
    menu_ships.add(MenuShip())

player = None
score = 0
level = 1
wave_count = 0
boss_active = False
shake_timer = 0
selected_difficulty = 1
score_pulse = 0
menu_selection = 0
menu_pulse = 0
title_y = -50
title_alpha = 0
game_over_alpha = 0
glow_effect = GlowEffect()

high_score_classic, high_score_survival, high_score_boss_rush = load_high_score()
difficulty, music_volume, sfx_volume, mute_all = load_settings()
pygame.mixer.music.set_volume(music_volume)
for sound in sound_objects.values():
    sound.set_volume(sfx_volume)

# ===================== حلقه اصلی =====================
clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)
    
    current_time = pygame.time.get_ticks()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_state == "menu":
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    menu_selection = (menu_selection + 1) % 7
                    if "select" in sound_objects and not mute_all:
                        sound_objects["select"].play()
                elif event.key in (pygame.K_UP, pygame.K_w):
                    menu_selection = (menu_selection - 1) % 7
                    if "select" in sound_objects and not mute_all:
                        sound_objects["select"].play()
                elif event.key == pygame.K_RETURN:
                    if "select" in sound_objects and not mute_all:
                        sound_objects["select"].play()
                    if menu_selection == 0:
                        game_mode = "classic"
                        reset_game()
                        game_state = "playing"
                        difficulty = [0.8, 1.0, 1.2][selected_difficulty]
                        save_settings(difficulty, music_volume, sfx_volume, mute_all)
                        pygame.mixer.music.fadeout(500)
                        load_music("bg_music")
                    elif menu_selection == 1:
                        game_mode = "survival"
                        reset_game()
                        game_state = "playing"
                        difficulty = [0.8, 1.0, 1.2][selected_difficulty]
                        save_settings(difficulty, music_volume, sfx_volume, mute_all)
                        pygame.mixer.music.fadeout(500)
                        load_music("bg_music")
                    elif menu_selection == 2:
                        game_mode = "boss_rush"
                        reset_game()
                        wave_count = 4
                        game_state = "playing"
                        difficulty = [0.8, 1.0, 1.2][selected_difficulty]
                        save_settings(difficulty, music_volume, sfx_volume, mute_all)
                        pygame.mixer.music.fadeout(500)
                        load_music("bg_music")
                    elif menu_selection == 3:
                        game_state = "difficulty"
                    elif menu_selection == 4:
                        game_state = "sound_settings"
                        menu_selection = 0
                    elif menu_selection == 5:
                        game_state = "about"
                    elif menu_selection == 6:
                        running = False
            elif game_state == "difficulty":
                if event.key == pygame.K_UP:
                    selected_difficulty = (selected_difficulty - 1) % 3
                    if "select" in sound_objects and not mute_all:
                        sound_objects["select"].play()
                elif event.key == pygame.K_DOWN:
                    selected_difficulty = (selected_difficulty + 1) % 3
                    if "select" in sound_objects and not mute_all:
                        sound_objects["select"].play()
                elif event.key == pygame.K_b:
                    game_state = "menu"
                    menu_selection = 3
                    if current_music != "menu_music" and not mute_all:
                        pygame.mixer.music.fadeout(500)
                        load_music("menu_music")
                    if "select" in sound_objects and not mute_all:
                        sound_objects["select"].play()
            elif game_state == "sound_settings":
                if event.key in (pygame.K_UP, pygame.K_w):
                    menu_selection = (menu_selection - 1) % 3
                    if "select" in sound_objects and not mute_all:
                        sound_objects["select"].play()
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    menu_selection = (menu_selection + 1) % 3
                    if "select" in sound_objects and not mute_all:
                        sound_objects["select"].play()
                elif event.key in (pygame.K_LEFT, pygame.K_a) and not mute_all:
                    if menu_selection == 0:
                        music_volume = max(0.0, music_volume - 0.1)
                        pygame.mixer.music.set_volume(music_volume)
                    elif menu_selection == 1:
                        sfx_volume = max(0.0, sfx_volume - 0.1)
                        for sound in sound_objects.values():
                            sound.set_volume(sfx_volume)
                    if "select" in sound_objects and not mute_all:
                        sound_objects["select"].play()
                elif event.key in (pygame.K_RIGHT, pygame.K_d) and not mute_all:
                    if menu_selection == 0:
                        music_volume = min(1.0, music_volume + 0.1)
                        pygame.mixer.music.set_volume(music_volume)
                    elif menu_selection == 1:
                        sfx_volume = min(1.0, sfx_volume + 0.1)
                        for sound in sound_objects.values():
                            sound.set_volume(sfx_volume)
                    if "select" in sound_objects and not mute_all:
                        sound_objects["select"].play()
                elif event.key == pygame.K_RETURN and menu_selection == 2:
                    mute_all = not mute_all
                    if mute_all:
                        pygame.mixer.music.stop()
                    else:
                        load_music("menu_music")
                    if "select" in sound_objects and not mute_all:
                        sound_objects["select"].play()
                elif event.key == pygame.K_b:
                    game_state = "menu"
                    menu_selection = 4
                    save_settings(difficulty, music_volume, sfx_volume, mute_all)
                    if "select" in sound_objects and not mute_all:
                        sound_objects["select"].play()
            elif game_state == "about":
                if event.key == pygame.K_b:
                    game_state = "menu"
                    menu_selection = 5
                    if current_music != "menu_music" and not mute_all:
                        pygame.mixer.music.fadeout(500)
                        load_music("menu_music")
                    if "select" in sound_objects and not mute_all:
                        sound_objects["select"].play()
            elif game_state == "playing":
                if event.key == pygame.K_SPACE and player.shoot_delay == 0:
                    shots = 3 if player.triple_shot else 1
                    for i in range(shots):
                        offset = (i-1)*12 if shots == 3 else 0
                        bullet = Bullet(player.rect.centerx + offset, player.rect.top)
                        all_sprites.add(bullet)
                        bullets.add(bullet)
                    player.shoot_delay = 12
                    if "laser" in sound_objects and not mute_all:
                        sound_objects["laser"].play()
            elif game_state == "game_over":
                if event.key == pygame.K_SPACE:
                    reset_game()
                    game_state = "playing"
                    game_over_alpha = 0
                    pygame.mixer.music.fadeout(500)
                    load_music("bg_music")
                    if "select" in sound_objects and not mute_all:
                        sound_objects["select"].play()
                elif event.key == pygame.K_m:
                    game_state = "menu"
                    game_over_alpha = 0
                    menu_selection = 0
                    title_y = -50
                    title_alpha = 0
                    pygame.mixer.music.fadeout(500)
                    load_music("menu_music")
                    if "select" in sound_objects and not mute_all:
                        sound_objects["select"].play()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if game_state == "menu":
                draw_menu()
                menu_items = ["Classic Mode", "Survival Mode", "Boss Rush", "Difficulty", "Sound Settings", "About", "Quit"]
                for i, item in enumerate(menu_items):
                    y = 180 + i * 55
                    rect = pygame.Rect(SCREEN_WIDTH//2 - 150, y - 20, 300, 40)
                    if rect.collidepoint(mouse_pos):
                        menu_selection = i
                        if "select" in sound_objects and not mute_all:
                            sound_objects["select"].play()
                        if item == "Classic Mode":
                            game_mode = "classic"
                            reset_game()
                            game_state = "playing"
                            difficulty = [0.8, 1.0, 1.2][selected_difficulty]
                            save_settings(difficulty, music_volume, sfx_volume, mute_all)
                            pygame.mixer.music.fadeout(500)
                            load_music("bg_music")
                        elif item == "Survival Mode":
                            game_mode = "survival"
                            reset_game()
                            game_state = "playing"
                            difficulty = [0.8, 1.0, 1.2][selected_difficulty]
                            save_settings(difficulty, music_volume, sfx_volume, mute_all)
                            pygame.mixer.music.fadeout(500)
                            load_music("bg_music")
                        elif item == "Boss Rush":
                            game_mode = "boss_rush"
                            reset_game()
                            wave_count = 4
                            game_state = "playing"
                            difficulty = [0.8, 1.0, 1.2][selected_difficulty]
                            save_settings(difficulty, music_volume, sfx_volume, mute_all)
                            pygame.mixer.music.fadeout(500)
                            load_music("bg_music")
                        elif item == "Difficulty":
                            game_state = "difficulty"
                        elif item == "Sound Settings":
                            game_state = "sound_settings"
                            menu_selection = 0
                        elif item == "About":
                            game_state = "about"
                        elif item == "Quit":
                            running = False

    # مدیریت صفحه ارائه
    if game_state == "presents":
        draw_presents_screen()

    elif game_state == "playing":
        all_sprites.update()
        score_pulse += 1

        for p in particles[:]:
            p.update()
            if p.lifetime <= 0:
                particles.remove(p)

        if combo_timer > 0:
            combo_timer -= 1
        else:
            if combo_count > 1:
                combo_count = 0
                score_multiplier = 1.0

        if len(enemies) == 0 and not boss_active:
            wave_count += 1
            if game_mode == "boss_rush" or (wave_count % 5 == 0 and score > 20):
                boss = Boss()
                all_sprites.add(boss)
                enemies.add(boss)
                boss_active = True
            else:
                spawn_enemy_wave()

        if random.random() < 0.008 * difficulty:
            ptype = random.choice(["triple", "speed", "shield"])
            pu = PowerUp(random.randint(60, SCREEN_WIDTH-60), -30, ptype)
            all_sprites.add(pu)
            powerups.add(pu)

        hits = pygame.sprite.groupcollide(enemies, bullets, False, True)
        for enemy, bullets_hit in hits.items():
            damage = len(bullets_hit)
            current_time = pygame.time.get_ticks()
            if isinstance(enemy, Boss):
                enemy.health -= damage
                if "boss_hit" in sound_objects and not mute_all:
                    sound_objects["boss_hit"].play()
                if enemy.health <= 0:
                    points = int(80 * score_multiplier)
                    score += points
                    score_popups.append(ScorePopup(enemy.rect.centerx, enemy.rect.centery - 40, points))
                    create_particles(enemy.rect.centerx, enemy.rect.centery, NEON_YELLOW, 100)
                    enemy.kill()
                    enemy.alive = False
                    boss_active = False
                    shake_timer = 40
                    if "boss_explosion" in sound_objects and not mute_all:
                        sound_objects["boss_explosion"].play()
                else:
                    shake_timer = max(shake_timer, 3)
            else:
                time_since_last = current_time - last_kill_time
                if time_since_last < 2000:
                    combo_count += 1
                    combo_timer = 180
                    score_multiplier = 1.0 + (combo_count * 0.2)
                    if combo_count % 5 == 0:
                        combo_popups.append(ComboPopup(enemy.rect.centerx, enemy.rect.centery - 50, combo_count))
                        if "combo" in sound_objects and not mute_all:
                            sound_objects["combo"].play()
                else:
                    combo_count = 1
                    score_multiplier = 1.0
                last_kill_time = current_time
                points = int(5 * score_multiplier)
                score += points
                score_popups.append(ScorePopup(enemy.rect.centerx, enemy.rect.centery - 20, points))
                create_particles(enemy.rect.centerx, enemy.rect.centery, NEON_PINK, 50)
                enemy.kill()
                if "explosion" in sound_objects and not mute_all:
                    sound_objects["explosion"].play()

        for pu in pygame.sprite.spritecollide(player, powerups, True):
            if pu.ptype == "triple":
                player.triple_shot = True
                player.powerup_timer = 360
            elif pu.ptype == "speed":
                player.speed_boost = True
                player.powerup_timer = 360
            elif pu.ptype == "shield":
                player.shield += 1
                player.shield_flash_timer = 30
            if "powerup" in sound_objects and not mute_all:
                sound_objects["powerup"].play()

        if pygame.sprite.spritecollide(player, enemies, True) or pygame.sprite.spritecollide(player, enemy_bullets, True):
            if player.shield > 0:
                player.shield -= 1
                player.shield_flash_timer = 30
            else:
                player.hp -= 1
                if player.hp <= 0:
                    game_state = "game_over"
                    pygame.mixer.music.fadeout(500)

        if score >= level * 120:
            level += 1
        if score > {"classic": high_score_classic, "survival": high_score_survival, "boss_rush": high_score_boss_rush}[game_mode]:
            if game_mode == "classic":
                high_score_classic = score
            elif game_mode == "survival":
                high_score_survival = score
            elif game_mode == "boss_rush":
                high_score_boss_rush = score
            save_high_score(high_score_classic, high_score_survival, high_score_boss_rush)

        draw_stars()
        all_sprites.draw(screen)

        for p in particles:
            p.draw()

        if player.shield > 0 or player.shield_flash_timer > 0:
            flash_alpha = 200 if player.shield_flash_timer > 15 else int(200 * (player.shield_flash_timer / 15))
            shield_surf = pygame.Surface((100, 100), pygame.SRCALPHA)
            pygame.draw.circle(shield_surf, (*NEON_CYAN, flash_alpha), (50, 50), 50, 5)
            screen.blit(shield_surf, (player.rect.centerx - 50, player.rect.centery - 50))

        for enemy in enemies:
            if isinstance(enemy, Boss) and enemy.alive:
                pulse_alpha = 60 + 40 * math.sin(enemy.pulse_timer)
                glow_surf = pygame.Surface((200, 140), pygame.SRCALPHA)
                pygame.draw.rect(glow_surf, (*NEON_PINK, int(pulse_alpha)), (0, 0, 200, 140), 6)
                screen.blit(glow_surf, (enemy.rect.x - 20, enemy.rect.y - 20))

        for pu in powerups:
            pulse_alpha = 70 + 30 * math.sin(pu.pulse_timer)
            color = NEON_YELLOW if pu.ptype in ["triple", "speed"] else GREEN
            glow_surf = pygame.Surface((60, 60), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (*color, int(pulse_alpha)), (30, 30), 30, 5)
            screen.blit(glow_surf, (pu.rect.centerx - 30, pu.rect.centery - 30))

        for popup in score_popups[:]:
            popup.update()
            if popup.timer <= 0:
                score_popups.remove(popup)
            else:
                popup.draw()

        for popup in combo_popups[:]:
            popup.update()
            if popup.timer <= 0:
                combo_popups.remove(popup)
            else:
                popup.draw()

        draw_hud()

        if shake_timer > 0:
            offset = (random.randint(-8, 8), random.randint(-8, 8))
            screen.blit(screen, offset)
            shake_timer -= 1

        pygame.display.flip()

    elif game_state == "menu":
        draw_menu()

    elif game_state == "difficulty":
        draw_difficulty_menu()
    elif game_state == "sound_settings":
        draw_sound_settings()
    elif game_state == "about":
        draw_about()
    elif game_state == "game_over":
        draw_game_over()

pygame.quit()
sys.exit()
