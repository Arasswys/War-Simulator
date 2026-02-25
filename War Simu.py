import pygame
import sys
import math
import random
from enum import Enum

pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("⚔️ Sultan Wars - Epic Battle ⚔️")

clock = pygame.time.Clock()
FPS = 60

GOLD = (255, 215, 0)
BRIGHT_GOLD = (255, 235, 50)
DARK_GOLD = (200, 170, 0)
YELLOW = (255, 255, 0)
YELLOW_LIGHT = (255, 255, 150)
RED = (220, 20, 20)
BRIGHT_RED = (255, 50, 50)
DARK_RED = (150, 10, 10)
RED_LIGHT = (255, 100, 100)
CRIMSON = (180, 20, 40)
GREEN = (0, 200, 50)
BRIGHT_GREEN = (50, 255, 80)
DARK_GREEN = (0, 140, 30)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (40, 40, 40)
LIGHT_GRAY = (180, 180, 180)
BROWN = (139, 90, 43)
DARK_BROWN = (80, 50, 20)
WATER_BLUE = (55, 115, 185)
WATER_LIGHT = (80, 140, 210)
CANNON_GRAY = (80, 80, 90)
SMOKE_COLOR = (160, 160, 160)
ORANGE = (255, 140, 0)
FIRE_RED = (255, 80, 20)
CYAN = (0, 200, 200)
MAGENTA = (255, 0, 255)
STEEL = (170, 175, 185)

WORLD_WIDTH = 8000
WORLD_HEIGHT = 6000


def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def ang_to(p1, p2):
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])


def clamp(v, mn, mx):
    return max(mn, min(mx, v))


class Camera:
    def __init__(self):
        self.x = WORLD_WIDTH // 2 - SCREEN_WIDTH // 2
        self.y = WORLD_HEIGHT // 2 - SCREEN_HEIGHT // 2
        self.target_x = self.x
        self.target_y = self.y
        self.edge_scroll_speed = 14
        self.drag = False
        self.drag_start = (0, 0)
        self.drag_cam_start = (0, 0)

    def update(self, follow_target=None):
        if follow_target:
            self.target_x = follow_target[0] - SCREEN_WIDTH // 2
            self.target_y = follow_target[1] - SCREEN_HEIGHT // 2
        mx, my = pygame.mouse.get_pos()
        if mx < 20: self.target_x -= self.edge_scroll_speed
        if mx > SCREEN_WIDTH - 20: self.target_x += self.edge_scroll_speed
        if my < 20: self.target_y -= self.edge_scroll_speed
        if my > SCREEN_HEIGHT - 20: self.target_y += self.edge_scroll_speed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: self.target_x -= self.edge_scroll_speed
        if keys[pygame.K_RIGHT]: self.target_x += self.edge_scroll_speed
        if keys[pygame.K_UP]: self.target_y -= self.edge_scroll_speed
        if keys[pygame.K_DOWN]: self.target_y += self.edge_scroll_speed
        self.target_x = clamp(self.target_x, 0, WORLD_WIDTH - SCREEN_WIDTH)
        self.target_y = clamp(self.target_y, 0, WORLD_HEIGHT - SCREEN_HEIGHT)
        self.x += (self.target_x - self.x) * 0.1
        self.y += (self.target_y - self.y) * 0.1

    def world_to_screen(self, wx, wy):
        return (int(wx - self.x), int(wy - self.y))

    def screen_to_world(self, sx, sy):
        return (sx + self.x, sy + self.y)

    def on_screen(self, wx, wy, margin=100):
        sx, sy = self.world_to_screen(wx, wy)
        return -margin < sx < SCREEN_WIDTH + margin and -margin < sy < SCREEN_HEIGHT + margin


def draw_star(surface, color, center, outer_r, inner_r, points=5, rot=0, border_c=None, border_w=2, glow=False):
    if glow:
        for i in range(4):
            gr = outer_r + (4 - i) * 3
            gc = (min(255, color[0] + 50), min(255, color[1] + 50), min(255, color[2] + 50))
            gs = pygame.Surface((gr * 4, gr * 4), pygame.SRCALPHA)
            pts = []
            for j in range(points * 2):
                a = rot + (j * math.pi / points) - math.pi / 2
                r = gr if j % 2 == 0 else inner_r + (4 - i) * 2
                pts.append((gr * 2 + r * math.cos(a), gr * 2 + r * math.sin(a)))
            if len(pts) >= 3:
                pygame.draw.polygon(gs, (*gc, 25 - i * 5), pts)
            surface.blit(gs, (center[0] - gr * 2, center[1] - gr * 2))
    pts = []
    for i in range(points * 2):
        a = rot + (i * math.pi / points) - math.pi / 2
        r = outer_r if i % 2 == 0 else inner_r
        pts.append((center[0] + r * math.cos(a), center[1] + r * math.sin(a)))
    if len(pts) >= 3:
        pygame.draw.polygon(surface, color, pts)
        if border_c: pygame.draw.polygon(surface, border_c, pts, border_w)
        hc = (min(255, color[0] + 70), min(255, color[1] + 70), min(255, color[2] + 70))
        ip = []
        for i in range(points * 2):
            a = rot + (i * math.pi / points) - math.pi / 2
            r2 = (outer_r if i % 2 == 0 else inner_r) * 0.4
            ip.append((center[0] + r2 * math.cos(a) - 1, center[1] + r2 * math.sin(a) - 1))
        if len(ip) >= 3: pygame.draw.polygon(surface, hc, ip)


def draw_glow(surface, color, center, radius, intensity=5):
    for i in range(intensity):
        r = radius + i * 2
        a = max(0, 50 - i * 10)
        s = pygame.Surface((r * 4, r * 4), pygame.SRCALPHA)
        pygame.draw.circle(s, (*color[:3], a), (r * 2, r * 2), r)
        surface.blit(s, (int(center[0] - r * 2), int(center[1] - r * 2)))


def draw_hp_bar(surface, pos, hp, max_hp, w=40, h=4):
    bx, by = pos[0] - w // 2, pos[1] - 20
    ratio = max(0, hp / max_hp)
    pygame.draw.rect(surface, (30, 30, 30), (bx - 1, by - 1, w + 2, h + 2))
    pygame.draw.rect(surface, (50, 50, 50), (bx, by, w, h))
    bc = (40, 200, 40) if ratio > 0.6 else ((230, 160, 0) if ratio > 0.3 else (230, 40, 40))
    pygame.draw.rect(surface, bc, (bx, by, int(w * ratio), h))


def draw_sword(surface, cx, cy, angle, length=18, swing=0):
    sa = angle + swing
    tip_x = cx + math.cos(sa) * length
    tip_y = cy + math.sin(sa) * length
    pygame.draw.line(surface, STEEL, (cx, cy), (int(tip_x), int(tip_y)), 3)
    pygame.draw.line(surface, WHITE, (cx, cy), (int(tip_x), int(tip_y)), 1)
    gx = cx + math.cos(sa) * 5
    gy = cy + math.sin(sa) * 5
    perp = sa + math.pi / 2
    g1x = gx + math.cos(perp) * 4
    g1y = gy + math.sin(perp) * 4
    g2x = gx - math.cos(perp) * 4
    g2y = gy - math.sin(perp) * 4
    pygame.draw.line(surface, DARK_BROWN, (int(g1x), int(g1y)), (int(g2x), int(g2y)), 2)
    hx = cx - math.cos(sa) * 4
    hy = cy - math.sin(sa) * 4
    pygame.draw.line(surface, BROWN, (cx, cy), (int(hx), int(hy)), 3)
    if abs(swing) > 0.3:
        pygame.draw.circle(surface, WHITE, (int(tip_x), int(tip_y)), 2)


class Tree:
    def __init__(self, x, y):
        self.x = x; self.y = y
        self.trunk_h = random.randint(15, 30)
        self.trunk_w = random.randint(4, 7)
        self.canopy_r = random.randint(14, 24)
        self.canopy_layers = random.randint(2, 4)
        self.sway = random.uniform(0, math.pi * 2)
        self.sway_speed = random.uniform(0.005, 0.015)
        self.leaf_color_base = (random.randint(25, 45), random.randint(90, 130), random.randint(20, 40))

    def draw(self, surface, cam, frame):
        if not cam.on_screen(self.x, self.y, 80): return
        sx, sy = cam.world_to_screen(self.x, self.y)
        sway = math.sin(frame * self.sway_speed + self.sway) * 2
        pygame.draw.ellipse(surface, (25, 50, 18, 100), (sx - self.canopy_r, sy + 4, self.canopy_r * 2, self.canopy_r // 2))
        trunk_pts = [(sx - self.trunk_w // 2, sy), (sx - self.trunk_w // 2 - 1, sy - self.trunk_h),
                     (sx + self.trunk_w // 2 + 1, sy - self.trunk_h), (sx + self.trunk_w // 2, sy)]
        pygame.draw.polygon(surface, DARK_BROWN, trunk_pts)
        for i in range(self.canopy_layers):
            ly = sy - self.trunk_h + 5 - i * (self.canopy_r // self.canopy_layers)
            lr = self.canopy_r - i * 2
            lx = sx + int(sway * (i + 1) * 0.3)
            shade = i * 12
            lc = (self.leaf_color_base[0] + shade, self.leaf_color_base[1] + shade, self.leaf_color_base[2] + shade)
            pygame.draw.circle(surface, lc, (lx, ly), lr)
            pygame.draw.circle(surface, (lc[0] - 15, lc[1] - 15, lc[2] - 10), (lx, ly), lr, 1)


class Cannonball:
    def __init__(self, x, y, tx, ty, team, damage):
        self.x, self.y = float(x), float(y)
        self.sx, self.sy = float(x), float(y)
        self.tx, self.ty = float(tx), float(ty)
        self.team = team; self.damage = damage
        self.alive = True; self.speed = 4.0; self.splash = 55
        self.trail = []; self.progress = 0.0
        self.total_d = max(1, dist((x, y), (tx, ty)))
        self.arc_h = min(180, self.total_d * 0.25)

    def update(self):
        if not self.alive: return
        self.progress += self.speed / self.total_d
        self.x = self.sx + (self.tx - self.sx) * self.progress
        base_y = self.sy + (self.ty - self.sy) * self.progress
        arc = -4 * self.arc_h * self.progress * (self.progress - 1)
        self.y = base_y - arc
        self.trail.append((self.x, self.y))
        if len(self.trail) > 20: self.trail.pop(0)
        if self.progress >= 1.0: self.alive = False

    def draw(self, surface, cam):
        if not self.alive: return
        for i, p in enumerate(self.trail):
            sp = cam.world_to_screen(p[0], p[1])
            r = max(1, int(3 * i / max(1, len(self.trail))))
            c = 80 + int(75 * i / max(1, len(self.trail)))
            pygame.draw.circle(surface, (c, c, c), sp, r)
        sp = cam.world_to_screen(self.x, self.y)
        pygame.draw.circle(surface, ORANGE, sp, 7)
        pygame.draw.circle(surface, FIRE_RED, sp, 5)
        pygame.draw.circle(surface, YELLOW, sp, 2)

    def get_splash(self, enemies):
        t = []
        for e in enemies:
            if e.alive:
                d = dist((self.tx, self.ty), (e.x, e.y))
                if d <= self.splash: t.append((e, 1.0 - d / self.splash * 0.5))
        return t


class Explosion:
    def __init__(self, x, y):
        self.x = x; self.y = y; self.life = 35; self.max_life = 35; self.alive = True
        self.parts = []
        for _ in range(25):
            a = random.uniform(0, math.pi * 2); s = random.uniform(1, 6)
            self.parts.append({'x': x, 'y': y, 'vx': math.cos(a) * s, 'vy': math.sin(a) * s,
                               'size': random.uniform(2, 7),
                               'color': random.choice([ORANGE, FIRE_RED, YELLOW, WHITE, SMOKE_COLOR])})

    def update(self):
        self.life -= 1
        if self.life <= 0: self.alive = False
        for p in self.parts:
            p['x'] += p['vx']; p['y'] += p['vy']; p['vx'] *= 0.94; p['vy'] *= 0.94

    def draw(self, surface, cam):
        if not cam.on_screen(self.x, self.y, 60): return
        r = self.life / self.max_life
        sp = cam.world_to_screen(self.x, self.y)
        cs = int(35 * r)
        if cs > 0:
            pygame.draw.circle(surface, ORANGE, sp, cs)
            pygame.draw.circle(surface, YELLOW, sp, max(1, cs // 2))
        for p in self.parts:
            pp = cam.world_to_screen(p['x'], p['y'])
            s = max(1, int(p['size'] * r))
            pygame.draw.circle(surface, p['color'], pp, s)


class Particle:
    def __init__(self, x, y, color, size=3, life=30):
        self.x = x; self.y = y; self.color = color; self.size = size
        self.life = life; self.max_life = life
        self.vx = random.uniform(-3, 3); self.vy = random.uniform(-3, 3); self.alive = True

    def update(self):
        self.x += self.vx; self.y += self.vy; self.vx *= 0.94; self.vy *= 0.94
        self.life -= 1
        if self.life <= 0: self.alive = False

    def draw(self, surface, cam):
        if not self.alive: return
        sp = cam.world_to_screen(self.x, self.y)
        s = max(1, int(self.size * (self.life / self.max_life)))
        pygame.draw.circle(surface, self.color, sp, s)


class Waypoint:
    def __init__(self, x, y):
        self.x = x; self.y = y; self.pulse = 0; self.life = 180

    def draw(self, surface, cam):
        self.pulse += 0.06; self.life -= 1
        sp = cam.world_to_screen(self.x, self.y)
        r = int(14 + math.sin(self.pulse) * 3)
        pygame.draw.circle(surface, (0, 230, 100), sp, r, 2)
        pygame.draw.circle(surface, (0, 255, 120), sp, 4)


class UnitType(Enum):
    SULTAN = 1
    COMMANDER = 2
    SOLDIER = 3
    CANNON = 4


class Unit:
    def __init__(self, x, y, team, unit_type):
        self.x = float(x); self.y = float(y); self.team = team; self.unit_type = unit_type
        self.alive = True; self.rotation = random.uniform(0, math.pi * 2)
        self.rot_spd = random.uniform(0.004, 0.01)
        self.target = None; self.atk_cd = 0; self.anim_t = 0; self.hit_flash = 0
        self.vx = 0; self.vy = 0; self.facing = 0
        self.move_target = None
        self.group_id = 0; self.selected = False
        self.player_controlled = False
        self.operating_cannon = None
        self.cannon_target_override = None
        self.custom_name = ""
        self.sword_swing = 0.0
        self.sword_swing_dir = 1

        if unit_type == UnitType.SULTAN:
            self.hp = 800; self.max_hp = 800; self.attack = 30; self.speed = 1.8
            self.atk_range = 55; self.size = 28; self.atk_spd = 45; self.engage_r = 200
        elif unit_type == UnitType.COMMANDER:
            self.hp = 350; self.max_hp = 350; self.attack = 22; self.speed = 0.65
            self.atk_range = 45; self.size = 20; self.atk_spd = 35; self.engage_r = 350
        elif unit_type == UnitType.SOLDIER:
            self.hp = 120; self.max_hp = 120; self.attack = 12; self.speed = 0.7
            self.atk_range = 30; self.size = 10; self.atk_spd = 30; self.engage_r = 600
        elif unit_type == UnitType.CANNON:
            self.hp = 200; self.max_hp = 200; self.attack = 60; self.speed = 0.3
            self.atk_range = 550; self.size = 18; self.atk_spd = 160; self.engage_r = 550
            self.cannon_angle = math.pi if team == "red" else 0
            self.fire_anim = 0
            self.crew = None

    def has_crew(self):
        if self.unit_type != UnitType.CANNON: return True
        if self.crew and self.crew.alive:
            d = dist((self.x, self.y), (self.crew.x, self.crew.y))
            return d < 80
        return False

    def find_target(self, enemies):
        if not enemies: return None
        if self.unit_type == UnitType.CANNON:
            if not self.has_crew(): return None
            best = None; bd = float('inf')
            for e in enemies:
                if e.alive:
                    d = dist((self.x, self.y), (e.x, e.y))
                    if d <= self.atk_range and d < bd: bd = d; best = e
            return best
        if self.unit_type == UnitType.SULTAN:
            best = None; bd = float('inf')
            for e in enemies:
                if e.alive:
                    d = dist((self.x, self.y), (e.x, e.y))
                    if d <= self.engage_r and d < bd: bd = d; best = e
            return best
        cands = []
        for e in enemies:
            if not e.alive: continue
            d = dist((self.x, self.y), (e.x, e.y))
            if self.unit_type == UnitType.SOLDIER:
                if e.unit_type == UnitType.SOLDIER: p = 0.7
                elif e.unit_type == UnitType.COMMANDER: p = 1.0
                elif e.unit_type == UnitType.CANNON: p = 1.1
                else: p = 2.5
            elif self.unit_type == UnitType.COMMANDER:
                if e.unit_type == UnitType.SOLDIER: p = 0.8
                elif e.unit_type == UnitType.COMMANDER: p = 0.7
                elif e.unit_type == UnitType.CANNON: p = 0.9
                else: p = 1.8
            else: p = 1.0
            cands.append((d * p, e))
        if not cands: return None
        cands.sort(key=lambda c: c[0])
        return cands[0][1]

    def find_nearest_enemy(self, enemies):
        best = None; bd = float('inf')
        for e in enemies:
            if e.alive:
                d = dist((self.x, self.y), (e.x, e.y))
                if d < bd: bd = d; best = e
        return best, bd

    def update(self, enemies, allies, cannonballs=None, obstacles=None, battle_started=True):
        if not self.alive: return
        self.anim_t += 1; self.rotation += self.rot_spd
        if self.hit_flash > 0: self.hit_flash -= 1
        if self.atk_cd > 0: self.atk_cd -= 1

        if self.unit_type in (UnitType.SOLDIER, UnitType.COMMANDER, UnitType.SULTAN):
            if self.atk_cd > self.atk_spd - 8:
                self.sword_swing += 0.25 * self.sword_swing_dir
                if abs(self.sword_swing) > 1.2: self.sword_swing_dir *= -1
            else:
                self.sword_swing *= 0.85
                if abs(self.sword_swing) < 0.05: self.sword_swing = 0

        if self.player_controlled and self.unit_type != UnitType.CANNON:
            keys = pygame.key.get_pressed()
            dx = dy = 0
            if keys[pygame.K_w]: dy = -self.speed
            if keys[pygame.K_s]: dy = self.speed
            if keys[pygame.K_a]: dx = -self.speed
            if keys[pygame.K_d]: dx = self.speed
            if dx != 0 and dy != 0: dx *= 0.707; dy *= 0.707
            if dx != 0 or dy != 0: self.facing = math.atan2(dy, dx)
            self.x += dx; self.y += dy
            self.x = clamp(self.x, 30, WORLD_WIDTH - 30)
            self.y = clamp(self.y, 30, WORLD_HEIGHT - 30)
            if battle_started:
                if self.target is None or not self.target.alive:
                    self.target = self.find_target(enemies)
                if self.target and self.target.alive:
                    self.facing = ang_to((self.x, self.y), (self.target.x, self.target.y))
                    d = dist((self.x, self.y), (self.target.x, self.target.y))
                    if d <= self.atk_range and self.atk_cd <= 0:
                        dmg = self.attack + random.randint(-3, 5)
                        self.target.hp -= dmg; self.target.hit_flash = 8
                        self.sword_swing_dir = random.choice([-1, 1])
                        if self.target.hp <= 0: self.target.alive = False; self.target = None
                        self.atk_cd = self.atk_spd
            return

        if self.player_controlled and self.unit_type == UnitType.CANNON:
            if hasattr(self, 'fire_anim') and self.fire_anim > 0: self.fire_anim -= 1
            keys = pygame.key.get_pressed()
            dx = dy = 0
            if keys[pygame.K_w]: dy = -self.speed
            if keys[pygame.K_s]: dy = self.speed
            if keys[pygame.K_a]: dx = -self.speed
            if keys[pygame.K_d]: dx = self.speed
            if dx != 0 and dy != 0: dx *= 0.707; dy *= 0.707
            self.x += dx; self.y += dy
            self.x = clamp(self.x, 30, WORLD_WIDTH - 30)
            self.y = clamp(self.y, 30, WORLD_HEIGHT - 30)
            if not battle_started: return
            if not self.has_crew(): return
            if self.cannon_target_override:
                tx, ty = self.cannon_target_override
                self.cannon_angle = ang_to((self.x, self.y), (tx, ty))
                d = dist((self.x, self.y), (tx, ty))
                if d <= self.atk_range and self.atk_cd <= 0:
                    if cannonballs is not None:
                        cannonballs.append(Cannonball(self.x, self.y,
                                                     tx + random.randint(-25, 25),
                                                     ty + random.randint(-25, 25),
                                                     self.team, self.attack))
                    self.atk_cd = self.atk_spd; self.fire_anim = 15
                    self.cannon_target_override = None
            return

        if self.unit_type == UnitType.CANNON:
            if hasattr(self, 'fire_anim') and self.fire_anim > 0: self.fire_anim -= 1
            if not battle_started: return
            if not self.has_crew(): return

            nearest, nd = self.find_nearest_enemy(enemies)

            if nearest:
                if nd > self.atk_range * 0.7:
                    a = ang_to((self.x, self.y), (nearest.x, nearest.y))
                    self.vx += math.cos(a) * self.speed * 0.05
                    self.vy += math.sin(a) * self.speed * 0.05
                    spd = math.sqrt(self.vx ** 2 + self.vy ** 2)
                    if spd > self.speed:
                        self.vx = (self.vx / spd) * self.speed
                        self.vy = (self.vy / spd) * self.speed
                else:
                    self.vx *= 0.85; self.vy *= 0.85

            if self.move_target:
                d = dist((self.x, self.y), self.move_target)
                if d > 20:
                    a = ang_to((self.x, self.y), self.move_target)
                    self.vx += math.cos(a) * self.speed * 0.06
                    self.vy += math.sin(a) * self.speed * 0.06
                    spd = math.sqrt(self.vx ** 2 + self.vy ** 2)
                    if spd > self.speed:
                        self.vx = (self.vx / spd) * self.speed
                        self.vy = (self.vy / spd) * self.speed
                else:
                    self.move_target = None

            for a2 in allies:
                if a2 is not self and a2.alive:
                    ad = dist((self.x, self.y), (a2.x, a2.y))
                    md = (self.size + a2.size) * 1.8
                    if ad < md and ad > 0:
                        pa = ang_to((a2.x, a2.y), (self.x, self.y))
                        pf = (md - ad) * 0.03
                        self.vx += math.cos(pa) * pf; self.vy += math.sin(pa) * pf

            self.vx *= 0.93; self.vy *= 0.93
            self.x += self.vx; self.y += self.vy
            self.x = clamp(self.x, 30, WORLD_WIDTH - 30)
            self.y = clamp(self.y, 30, WORLD_HEIGHT - 30)

            if self.target is None or not self.target.alive:
                self.target = self.find_target(enemies)
            if self.target and self.target.alive and self.atk_cd <= 0:
                d = dist((self.x, self.y), (self.target.x, self.target.y))
                if d <= self.atk_range:
                    self.cannon_angle = ang_to((self.x, self.y), (self.target.x, self.target.y))
                    if cannonballs is not None:
                        cannonballs.append(Cannonball(self.x, self.y,
                                                     self.target.x + random.randint(-25, 25),
                                                     self.target.y + random.randint(-25, 25),
                                                     self.team, self.attack))
                    self.atk_cd = self.atk_spd; self.fire_anim = 15
            return

        if self.operating_cannon and self.operating_cannon.alive and not self.player_controlled:
            cannon = self.operating_cannon
            ca = cannon.cannon_angle if hasattr(cannon, 'cannon_angle') else 0
            stand_x = cannon.x - math.cos(ca) * 30
            stand_y = cannon.y - math.sin(ca) * 30
            sd = dist((self.x, self.y), (stand_x, stand_y))
            if sd > 10:
                a = ang_to((self.x, self.y), (stand_x, stand_y))
                self.vx += math.cos(a) * self.speed * 0.08
                self.vy += math.sin(a) * self.speed * 0.08
                spd = math.sqrt(self.vx ** 2 + self.vy ** 2)
                ms = max(self.speed, 1.2)
                if spd > ms: self.vx = (self.vx / spd) * ms; self.vy = (self.vy / spd) * ms
            else:
                self.vx *= 0.5; self.vy *= 0.5
            self.vx *= 0.91; self.vy *= 0.91
            self.x += self.vx; self.y += self.vy
            self.x = clamp(self.x, 30, WORLD_WIDTH - 30); self.y = clamp(self.y, 30, WORLD_HEIGHT - 30)
            if battle_started:
                close_enemy = None; cd2 = float('inf')
                for e in enemies:
                    if e.alive:
                        ed = dist((self.x, self.y), (e.x, e.y))
                        if ed < 50 and ed < cd2: cd2 = ed; close_enemy = e
                if close_enemy and self.atk_cd <= 0:
                    self.facing = ang_to((self.x, self.y), (close_enemy.x, close_enemy.y))
                    d = dist((self.x, self.y), (close_enemy.x, close_enemy.y))
                    if d <= self.atk_range:
                        dmg = self.attack + random.randint(-3, 5)
                        close_enemy.hp -= dmg; close_enemy.hit_flash = 8
                        self.sword_swing_dir = random.choice([-1, 1])
                        if close_enemy.hp <= 0: close_enemy.alive = False
                        self.atk_cd = self.atk_spd
            return

        if not battle_started:
            if self.move_target:
                d = dist((self.x, self.y), self.move_target)
                if d > 18:
                    a = ang_to((self.x, self.y), self.move_target)
                    self.facing = a
                    self.vx += math.cos(a) * self.speed * 0.08
                    self.vy += math.sin(a) * self.speed * 0.08
                    spd = math.sqrt(self.vx ** 2 + self.vy ** 2)
                    if spd > self.speed: self.vx = (self.vx / spd) * self.speed; self.vy = (self.vy / spd) * self.speed
                else:
                    self.move_target = None; self.vx *= 0.5; self.vy *= 0.5
            for a2 in allies:
                if a2 is not self and a2.alive:
                    ad = dist((self.x, self.y), (a2.x, a2.y))
                    md = (self.size + a2.size) * 1.6
                    if ad < md and ad > 0:
                        pa = ang_to((a2.x, a2.y), (self.x, self.y))
                        pf = (md - ad) * 0.04
                        self.vx += math.cos(pa) * pf; self.vy += math.sin(pa) * pf
            self.vx *= 0.91; self.vy *= 0.91
            self.x += self.vx; self.y += self.vy
            self.x = clamp(self.x, 30, WORLD_WIDTH - 30); self.y = clamp(self.y, 30, WORLD_HEIGHT - 30)
            return

        if self.move_target:
            d = dist((self.x, self.y), self.move_target)
            if d > 30:
                a = ang_to((self.x, self.y), self.move_target)
                self.facing = a
                self.vx += math.cos(a) * self.speed * 0.1
                self.vy += math.sin(a) * self.speed * 0.1
                spd = math.sqrt(self.vx ** 2 + self.vy ** 2)
                if spd > self.speed: self.vx = (self.vx / spd) * self.speed; self.vy = (self.vy / spd) * self.speed
                close_enemy = None; cd2 = float('inf')
                for e in enemies:
                    if e.alive:
                        ed = dist((self.x, self.y), (e.x, e.y))
                        if ed < self.atk_range and ed < cd2: cd2 = ed; close_enemy = e
                if close_enemy and self.atk_cd <= 0:
                    self.facing = ang_to((self.x, self.y), (close_enemy.x, close_enemy.y))
                    dmg = self.attack + random.randint(-3, 5)
                    close_enemy.hp -= dmg; close_enemy.hit_flash = 8
                    self.sword_swing_dir = random.choice([-1, 1])
                    if close_enemy.hp <= 0: close_enemy.alive = False
                    self.atk_cd = self.atk_spd
            else:
                self.move_target = None
        else:
            if self.target is None or not self.target.alive:
                self.target = self.find_target(enemies)
            if self.target and self.target.alive:
                d = dist((self.x, self.y), (self.target.x, self.target.y))
                self.facing = ang_to((self.x, self.y), (self.target.x, self.target.y))
                if d <= self.atk_range:
                    self.vx *= 0.5; self.vy *= 0.5
                    if self.atk_cd <= 0:
                        dmg = self.attack + random.randint(-3, 5)
                        self.target.hp -= dmg; self.target.hit_flash = 8
                        self.sword_swing_dir = random.choice([-1, 1])
                        if self.target.hp <= 0: self.target.alive = False; self.target = None
                        self.atk_cd = self.atk_spd
                else:
                    a = ang_to((self.x, self.y), (self.target.x, self.target.y))
                    self.vx += math.cos(a) * self.speed * 0.1
                    self.vy += math.sin(a) * self.speed * 0.1
                    spd = math.sqrt(self.vx ** 2 + self.vy ** 2)
                    if spd > self.speed: self.vx = (self.vx / spd) * self.speed; self.vy = (self.vy / spd) * self.speed
            else:
                self.vx *= 0.9; self.vy *= 0.9

        for a2 in allies:
            if a2 is not self and a2.alive:
                ad = dist((self.x, self.y), (a2.x, a2.y))
                md = (self.size + a2.size) * 1.5
                if ad < md and ad > 0:
                    pa = ang_to((a2.x, a2.y), (self.x, self.y))
                    pf = (md - ad) * 0.05
                    self.vx += math.cos(pa) * pf; self.vy += math.sin(pa) * pf
        self.vx *= 0.92; self.vy *= 0.92
        self.x += self.vx; self.y += self.vy
        self.x = clamp(self.x, 30, WORLD_WIDTH - 30); self.y = clamp(self.y, 30, WORLD_HEIGHT - 30)

    def draw(self, surface, cam):
        if not self.alive: return
        if not cam.on_screen(self.x, self.y, 50): return
        sp = cam.world_to_screen(self.x, self.y)
        ix, iy = sp

        if self.selected:
            pygame.draw.circle(surface, (0, 220, 0), (ix, iy), self.size + 14, 2)
        if self.player_controlled:
            pulse = abs(math.sin(self.anim_t * 0.07)) * 4
            pygame.draw.circle(surface, MAGENTA, (ix, iy), int(self.size + 18 + pulse), 3)
            try:
                cf = pygame.font.SysFont("Arial", 10)
                ct = cf.render("CTRL", True, MAGENTA)
                surface.blit(ct, (ix - ct.get_width() // 2, iy + self.size + 8))
            except: pass

        if self.unit_type == UnitType.CANNON:
            self._draw_cannon(surface, ix, iy); return

        if self.unit_type in (UnitType.SOLDIER, UnitType.COMMANDER, UnitType.SULTAN):
            sword_len = 14 if self.unit_type == UnitType.SOLDIER else (20 if self.unit_type == UnitType.COMMANDER else 24)
            sword_x = ix + math.cos(self.facing + 0.5) * (self.size * 0.6)
            sword_y = iy + math.sin(self.facing + 0.5) * (self.size * 0.6)
            draw_sword(surface, int(sword_x), int(sword_y), self.facing, sword_len, self.sword_swing)

        if self.unit_type == UnitType.SULTAN:
            mc = BRIGHT_GOLD if self.team == "gold" else BRIGHT_RED
            if self.hit_flash > 0: mc = WHITE
            bc = DARK_GOLD if self.team == "gold" else DARK_RED
            gc = YELLOW if self.team == "gold" else RED
            draw_glow(surface, gc, (ix, iy), self.size + 10, 7)
            cp = math.sin(self.anim_t * 0.04) * 3
            pygame.draw.circle(surface, gc, (ix, iy), int(self.size + 15 + cp), 2)
            draw_star(surface, mc, (ix, iy), self.size, self.size * 0.45, 5, self.rotation, bc, 3, True)
            for i in range(5):
                a = self.rotation + (i * math.pi * 2 / 5) - math.pi / 2
                tx2 = ix + math.cos(a) * (self.size + 8); ty2 = iy + math.sin(a) * (self.size + 8)
                pygame.draw.circle(surface, YELLOW if self.team == "gold" else RED_LIGHT, (int(tx2), int(ty2)), 3)
        elif self.unit_type == UnitType.COMMANDER:
            if self.team == "gold":
                mc = BRIGHT_GREEN if self.hit_flash == 0 else WHITE; bc = DARK_GREEN; gc = GREEN
            else:
                mc = CRIMSON if self.hit_flash == 0 else WHITE; bc = DARK_RED; gc = RED
            draw_glow(surface, gc, (ix, iy), self.size + 5, 4)
            pygame.draw.circle(surface, gc, (ix, iy), self.size + 8, 2)
            draw_star(surface, mc, (ix, iy), self.size, self.size * 0.4, 5, self.rotation, bc, 2, True)
        else:
            if self.team == "gold":
                mc = BRIGHT_GOLD if self.hit_flash == 0 else WHITE; bc = DARK_GOLD; gc = YELLOW
            else:
                mc = BRIGHT_RED if self.hit_flash == 0 else WHITE; bc = DARK_RED; gc = RED
            if self.operating_cannon and self.operating_cannon.alive:
                pygame.draw.circle(surface, CANNON_GRAY, (ix, iy), self.size + 6, 1)
            draw_glow(surface, gc, (ix, iy), self.size + 2, 3)
            pygame.draw.circle(surface, mc, (ix, iy), self.size)
            pygame.draw.circle(surface, bc, (ix, iy), self.size, 2)
            hc = (min(255, mc[0] + 70), min(255, mc[1] + 70), min(255, mc[2] + 70))
            pygame.draw.circle(surface, hc, (ix - self.size // 3, iy - self.size // 3), self.size // 3)

        draw_hp_bar(surface, (ix, iy), self.hp, self.max_hp, w=self.size * 2, h=4)
        if self.custom_name:
            try:
                nf = pygame.font.SysFont("Arial", 10)
                nt = nf.render(self.custom_name, True, WHITE)
                surface.blit(nt, (ix - nt.get_width() // 2, iy - self.size - 28))
            except: pass
        if self.atk_cd > self.atk_spd - 5 and self.target and self.target.alive:
            ac = YELLOW if self.team == "gold" else RED_LIGHT
            tp = cam.world_to_screen(self.target.x, self.target.y)
            pygame.draw.line(surface, ac, (ix, iy), tp, 1)

    def _draw_cannon(self, surface, ix, iy):
        if self.team == "gold":
            bc2 = (170, 150, 55) if self.hit_flash == 0 else WHITE
        else:
            bc2 = (150, 45, 45) if self.hit_flash == 0 else WHITE
        has_crew = self.has_crew()
        pygame.draw.ellipse(surface, (20, 35, 12), (ix - 20, iy + 10, 40, 12))
        pygame.draw.circle(surface, DARK_BROWN, (ix - 12, iy + 5), 8)
        pygame.draw.circle(surface, DARK_BROWN, (ix + 12, iy + 5), 8)
        pygame.draw.circle(surface, BROWN, (ix - 12, iy + 5), 4)
        pygame.draw.circle(surface, BROWN, (ix + 12, iy + 5), 4)
        pygame.draw.rect(surface, bc2, (ix - 14, iy - 8, 28, 16), border_radius=3)
        ca = self.cannon_angle if hasattr(self, 'cannon_angle') else 0
        bx = ix + math.cos(ca) * 25; by = iy + math.sin(ca) * 25
        pygame.draw.line(surface, CANNON_GRAY, (ix, iy), (int(bx), int(by)), 6)
        pygame.draw.circle(surface, CANNON_GRAY, (int(bx), int(by)), 4)
        if not has_crew:
            try:
                cf = pygame.font.SysFont("Arial", 10)
                ct = cf.render("NO CREW", True, RED)
                surface.blit(ct, (ix - ct.get_width() // 2, iy - 32))
            except: pass
            pygame.draw.line(surface, RED, (ix - 15, iy - 15), (ix + 15, iy + 15), 2)
            pygame.draw.line(surface, RED, (ix + 15, iy - 15), (ix - 15, iy + 15), 2)
        if self.player_controlled:
            range_surf = pygame.Surface((self.atk_range * 2 + 4, self.atk_range * 2 + 4), pygame.SRCALPHA)
            pygame.draw.circle(range_surf, (255, 255, 0, 25), (self.atk_range + 2, self.atk_range + 2), self.atk_range, 1)
            surface.blit(range_surf, (ix - self.atk_range - 2, iy - self.atk_range - 2))
        fa = self.fire_anim if hasattr(self, 'fire_anim') else 0
        if fa > 10:
            fs = (fa - 10) * 4
            pygame.draw.circle(surface, YELLOW, (int(bx), int(by)), fs)
            pygame.draw.circle(surface, ORANGE, (int(bx), int(by)), fs + 3)
            for _ in range(3):
                sx2 = bx + random.randint(-10, 10); sy2 = by + random.randint(-10, 10)
                pygame.draw.circle(surface, SMOKE_COLOR, (int(sx2), int(sy2)), random.randint(3, 7))
        elif fa > 0:
            for _ in range(2):
                sx2 = bx + random.randint(-12, 12); sy2 = by + random.randint(-15, 5)
                pygame.draw.circle(surface, SMOKE_COLOR, (int(sx2), int(sy2)), random.randint(3, 8))
        draw_hp_bar(surface, (ix, iy), self.hp, self.max_hp, w=36, h=4)
        if self.custom_name:
            try:
                nf = pygame.font.SysFont("Arial", 10)
                nt = nf.render(self.custom_name, True, WHITE)
                surface.blit(nt, (ix - nt.get_width() // 2, iy - 38))
            except: pass


class GameMap:
    def __init__(self, map_type="normal"):
        self.map_type = map_type
        self.trees = []; self.ground_details = []
        self.generate()

    def generate(self):
        self.trees.clear(); self.ground_details.clear()
        if self.map_type == "normal":
            for _ in range(200):
                x = random.randint(100, WORLD_WIDTH - 100); y = random.randint(100, WORLD_HEIGHT - 100)
                if abs(x - WORLD_WIDTH // 2) > 400 or abs(y - WORLD_HEIGHT // 2) > 500:
                    self.trees.append(Tree(x, y))
        elif self.map_type == "eflak":
            for _ in range(350):
                self.trees.append(Tree(random.randint(50, WORLD_WIDTH - 50), random.randint(50, WORLD_HEIGHT - 50)))
        elif self.map_type == "sandbox":
            for _ in range(150):
                self.trees.append(Tree(random.randint(100, WORLD_WIDTH - 100), random.randint(100, WORLD_HEIGHT - 100)))
        for _ in range(500):
            x = random.randint(0, WORLD_WIDTH); y = random.randint(0, WORLD_HEIGHT)
            c = random.choice([(70, 130, 45), (55, 115, 35), (80, 140, 55), (65, 120, 40)])
            self.ground_details.append((x, y, c, random.randint(8, 25)))

    def draw(self, surface, cam, frame):
        if self.map_type == "eflak": surface.fill((35, 75, 30))
        elif self.map_type == "sandbox": surface.fill((50, 100, 40))
        else: surface.fill((45, 95, 35))
        for gx, gy, gc, gs in self.ground_details:
            if cam.on_screen(gx, gy, gs + 5):
                sp = cam.world_to_screen(gx, gy)
                pygame.draw.circle(surface, gc, sp, gs)
        if self.map_type == "normal":
            rx = WORLD_WIDTH // 2
            for y in range(0, WORLD_HEIGHT, 3):
                if cam.on_screen(rx, y, 50):
                    w = math.sin(y * 0.015 + frame * 0.02) * 20
                    wd = 30 + int(math.sin(y * 0.008) * 12)
                    sp = cam.world_to_screen(int(rx + w) - wd, y)
                    pygame.draw.rect(surface, WATER_BLUE, (sp[0], sp[1], wd * 2, 3))
        if self.map_type == "eflak":
            for i in range(20):
                fy = 100 + i * 300
                if cam.on_screen(WORLD_WIDTH // 2, fy, 200):
                    spy = cam.world_to_screen(0, fy)[1]
                    fs = pygame.Surface((SCREEN_WIDTH, 60), pygame.SRCALPHA)
                    alpha = int(12 + math.sin(frame * 0.008 + i) * 6)
                    pygame.draw.rect(fs, (180, 190, 200, alpha), (0, 0, SCREEN_WIDTH, 60))
                    surface.blit(fs, (0, spy))
        for tree in self.trees: tree.draw(surface, cam, frame)


class Game:
    def __init__(self):
        self.state = "MENU"
        self.camera = Camera()
        self.game_map = GameMap()
        self.gold_units = []; self.red_units = []
        self.cannonballs = []; self.explosions = []; self.particles = []
        self.waypoints = []
        self.battle_started = False; self.battle_paused = False
        self.winner = None
        self.frame = 0; self.cam_shake = 0
        self.kills_gold = 0; self.kills_red = 0
        self.map_mode = "normal"
        self.soldier_count = 25; self.commander_count = 3; self.cannon_count = 3
        self.menu_btns = []; self.atk_btn = None; self.vic_btns = []
        self.sandbox_mode = False; self.sandbox_placing = None; self.sandbox_team = "gold"
        self.clicked_unit = None; self.controlled_unit = None
        self.box_selecting = False; self.box_start = None; self.box_end = None
        self.box_selected_units = []
        self.naming_mode = False; self.naming_unit = None; self.naming_text = ""

        # ===== SAVAŞ HIZI SİSTEMİ =====
        self.speed_options = [0.25, 0.5, 1.0, 2.0, 3.0, 5.0]
        self.battle_speed = 1.0  # Mevcut hız çarpanı
        self.speed_accumulator = 0.0  # Kesirli hız biriktiricisi
        self.speed_btn_rects = []  # UI buton dikdörtgenleri

        try:
            self.f_title = pygame.font.SysFont("Arial", 56, bold=True)
            self.f_large = pygame.font.SysFont("Arial", 36, bold=True)
            self.f_med = pygame.font.SysFont("Arial", 24, bold=True)
            self.f_small = pygame.font.SysFont("Arial", 17)
            self.f_tiny = pygame.font.SysFont("Arial", 14)
            self.f_mini = pygame.font.SysFont("Arial", 11)
        except:
            self.f_title = pygame.font.Font(None, 56); self.f_large = pygame.font.Font(None, 36)
            self.f_med = pygame.font.Font(None, 24); self.f_small = pygame.font.Font(None, 17)
            self.f_tiny = pygame.font.Font(None, 14); self.f_mini = pygame.font.Font(None, 11)

    def cycle_speed_up(self):
        """Hızı bir kademe artır"""
        idx = -1
        for i, s in enumerate(self.speed_options):
            if abs(s - self.battle_speed) < 0.01:
                idx = i
                break
        if idx < len(self.speed_options) - 1:
            self.battle_speed = self.speed_options[idx + 1]

    def cycle_speed_down(self):
        """Hızı bir kademe azalt"""
        idx = -1
        for i, s in enumerate(self.speed_options):
            if abs(s - self.battle_speed) < 0.01:
                idx = i
                break
        if idx > 0:
            self.battle_speed = self.speed_options[idx - 1]

    def set_speed(self, speed):
        """Hızı doğrudan ayarla"""
        self.battle_speed = speed

    def assign_cannon_crews(self, units):
        cannons = [u for u in units if u.unit_type == UnitType.CANNON and u.alive]
        available = [u for u in units if u.unit_type == UnitType.SOLDIER and u.alive and u.operating_cannon is None]
        for cannon in cannons:
            if cannon.crew and cannon.crew.alive: continue
            cannon.crew = None
            if available:
                best = None; bd = float('inf')
                for s in available:
                    d = dist((s.x, s.y), (cannon.x, cannon.y))
                    if d < bd: bd = d; best = s
                if best:
                    cannon.crew = best; best.operating_cannon = cannon
                    available.remove(best)

    def setup_armies(self):
        self.gold_units.clear(); self.red_units.clear()
        self.cannonballs.clear(); self.explosions.clear(); self.particles.clear(); self.waypoints.clear()
        self.battle_started = False; self.battle_paused = False; self.winner = None
        self.kills_gold = 0; self.kills_red = 0
        self.clicked_unit = None; self.controlled_unit = None
        self.box_selected_units = []
        self.naming_mode = False; self.naming_unit = None; self.naming_text = ""
        self.battle_speed = 1.0; self.speed_accumulator = 0.0

        if self.sandbox_mode: return

        mx = WORLD_WIDTH // 2; my = WORLD_HEIGHT // 2
        sc = self.soldier_count; cc = self.commander_count; tc = self.cannon_count
        left_base = mx - 1200; right_base = mx + 1200

        if self.map_mode == "eflak":
            gold_sc = int(sc * 1.5); gold_cc = cc + 2; gold_tc = tc + 1
            red_sc = sc; red_cc = cc; red_tc = 0
        else:
            gold_sc = sc; gold_cc = cc; gold_tc = tc
            red_sc = sc; red_cc = cc; red_tc = tc

        p = Unit(left_base, my, "gold", UnitType.SULTAN)
        self.gold_units.append(p)
        for i in range(gold_tc):
            spacing = 800 // max(1, gold_tc)
            self.gold_units.append(Unit(left_base + 80, my - 400 + i * spacing, "gold", UnitType.CANNON))
        for i in range(gold_cc):
            spacing = 600 // max(1, gold_cc)
            self.gold_units.append(Unit(left_base + 200, my - 300 + i * spacing, "gold", UnitType.COMMANDER))
        for i in range(gold_sc):
            r = i // 6; c = i % 6
            self.gold_units.append(Unit(left_base + 350 + r * 40, my - 200 + c * 72, "gold", UnitType.SOLDIER))

        self.red_units.append(Unit(right_base, my, "red", UnitType.SULTAN))
        for i in range(red_tc):
            spacing = 800 // max(1, red_tc)
            self.red_units.append(Unit(right_base - 80, my - 400 + i * spacing, "red", UnitType.CANNON))
        for i in range(red_cc):
            spacing = 600 // max(1, red_cc)
            self.red_units.append(Unit(right_base - 200, my - 300 + i * spacing, "red", UnitType.COMMANDER))
        for i in range(red_sc):
            r = i // 6; c = i % 6
            self.red_units.append(Unit(right_base - 350 - r * 40, my - 200 + c * 72, "red", UnitType.SOLDIER))

        self.assign_cannon_crews(self.gold_units)
        self.assign_cannon_crews(self.red_units)
        self.camera.target_x = left_base - SCREEN_WIDTH // 2 + 200
        self.camera.target_y = my - SCREEN_HEIGHT // 2

    def sandbox_place(self, wx, wy):
        if self.sandbox_placing is None: return
        u = Unit(wx, wy, self.sandbox_team, self.sandbox_placing)
        if self.sandbox_team == "gold":
            self.gold_units.append(u)
            self.assign_cannon_crews(self.gold_units)
        else:
            self.red_units.append(u)
            self.assign_cannon_crews(self.red_units)

    def try_select_unit_at(self, wx, wy):
        best = None; best_d = float('inf')
        for u in self.gold_units + self.red_units:
            if not u.alive: continue
            d = dist((u.x, u.y), (wx, wy))
            if d < u.size + 12 and d < best_d: best_d = d; best = u
        if self.clicked_unit: self.clicked_unit.selected = False
        self.clicked_unit = best
        if best: best.selected = True
        return best

    def toggle_control(self):
        if self.clicked_unit is None or not self.clicked_unit.alive: return
        u = self.clicked_unit
        if u.player_controlled:
            u.player_controlled = False; self.controlled_unit = None; return
        if self.controlled_unit and self.controlled_unit.alive:
            self.controlled_unit.player_controlled = False
        u.player_controlled = True; self.controlled_unit = u

    def release_control(self):
        if self.controlled_unit and self.controlled_unit.alive:
            self.controlled_unit.player_controlled = False
        self.controlled_unit = None

    def get_box_rect_world(self):
        if not self.box_start or not self.box_end: return None
        wx1, wy1 = self.camera.screen_to_world(*self.box_start)
        wx2, wy2 = self.camera.screen_to_world(*self.box_end)
        return (min(wx1, wx2), min(wy1, wy2), max(wx1, wx2), max(wy1, wy2))

    def select_units_in_box(self):
        rect = self.get_box_rect_world()
        if not rect: return
        x1, y1, x2, y2 = rect
        for u in self.box_selected_units: u.selected = False
        self.box_selected_units = []
        for u in self.gold_units:
            if not u.alive: continue
            if u.operating_cannon and u.operating_cannon.alive: continue
            if x1 <= u.x <= x2 and y1 <= u.y <= y2:
                u.selected = True; self.box_selected_units.append(u)

    def send_selected_to(self, wx, wy):
        if not self.box_selected_units: return
        n = len(self.box_selected_units)
        cols = max(1, int(math.sqrt(n))); spacing = 35
        for i, u in enumerate(self.box_selected_units):
            r = i // cols; c = i % cols
            u.move_target = (wx + (c - cols // 2) * spacing, wy + (r - (n // cols) // 2) * spacing)
        self.waypoints.append(Waypoint(wx, wy))

    def fire_controlled_cannon(self):
        ctrl = self.controlled_unit
        if not ctrl or not ctrl.alive: return
        if ctrl.unit_type != UnitType.CANNON: return
        if not ctrl.has_crew(): return
        if ctrl.atk_cd > 0: return
        mx, my = pygame.mouse.get_pos()
        wx, wy = self.camera.screen_to_world(mx, my)
        d = dist((ctrl.x, ctrl.y), (wx, wy))
        if d <= ctrl.atk_range:
            ctrl.cannon_target_override = (wx, wy)

    def start_naming(self):
        if not self.clicked_unit or not self.clicked_unit.alive: return
        self.naming_mode = True
        self.naming_unit = self.clicked_unit
        self.naming_text = self.clicked_unit.custom_name

    def _do_one_sim_tick(self):
        """Tek bir simülasyon adımı - hız sistemi bunu tekrarlar"""
        prev_g = {id(u): u.alive for u in self.gold_units}
        prev_r = {id(u): u.alive for u in self.red_units}

        for u in self.gold_units:
            u.update(self.red_units, self.gold_units, self.cannonballs, None, self.battle_started)
        for u in self.red_units:
            u.update(self.gold_units, self.red_units, self.cannonballs, None, self.battle_started)

        for b in self.cannonballs:
            b.update()
            if not b.alive:
                self.explosions.append(Explosion(b.tx, b.ty))
                self.cam_shake = max(self.cam_shake, 6)
                enemies = self.gold_units if b.team == "red" else self.red_units
                for e, dr in b.get_splash(enemies):
                    dmg = int(b.damage * dr) + random.randint(-5, 5)
                    e.hp -= dmg; e.hit_flash = 10
                    if e.hp <= 0: e.alive = False
        self.cannonballs = [b for b in self.cannonballs if b.alive]
        for e in self.explosions: e.update()
        self.explosions = [e for e in self.explosions if e.alive]

        for u in self.gold_units:
            if prev_g.get(id(u), False) and not u.alive:
                for _ in range(12):
                    self.particles.append(Particle(u.x, u.y, YELLOW, random.randint(2, 5), random.randint(20, 45)))
                self.kills_red += 1; u.hp = -9999
                if u is self.controlled_unit: self.controlled_unit = None
                if u is self.clicked_unit: self.clicked_unit = None
                if u.operating_cannon: u.operating_cannon.crew = None
                if u.unit_type == UnitType.CANNON and hasattr(u, 'crew') and u.crew:
                    u.crew.operating_cannon = None; u.crew = None
        for u in self.red_units:
            if prev_r.get(id(u), False) and not u.alive:
                for _ in range(12):
                    self.particles.append(Particle(u.x, u.y, RED, random.randint(2, 5), random.randint(20, 45)))
                self.kills_gold += 1; u.hp = -9999
                if u is self.controlled_unit: self.controlled_unit = None
                if u is self.clicked_unit: self.clicked_unit = None
                if u.operating_cannon: u.operating_cannon.crew = None
                if u.unit_type == UnitType.CANNON and hasattr(u, 'crew') and u.crew:
                    u.crew.operating_cannon = None; u.crew = None

    def update(self):
        self.frame += 1
        if self.cam_shake > 0: self.cam_shake -= 1

        if self.state == "BATTLE":
            ctrl = self.controlled_unit
            if ctrl and ctrl.alive:
                self.camera.update((ctrl.x, ctrl.y))
            else:
                self.camera.update()

            if ctrl and ctrl.alive and ctrl.unit_type == UnitType.CANNON and ctrl.player_controlled:
                mx, my = pygame.mouse.get_pos()
                wx, wy = self.camera.screen_to_world(mx, my)
                ctrl.cannon_angle = ang_to((ctrl.x, ctrl.y), (wx, wy))

            if self.battle_paused: return

            # ===== HIZ SİSTEMİ: Accumulator tabanlı =====
            self.speed_accumulator += self.battle_speed
            ticks_this_frame = int(self.speed_accumulator)
            self.speed_accumulator -= ticks_this_frame

            # Performans koruması: çerçeve başına max 10 tick
            ticks_this_frame = min(ticks_this_frame, 10)

            for _ in range(ticks_this_frame):
                self._do_one_sim_tick()

            # Periyodik crew atama (hıza bağlı olarak daha seyrek kontrol)
            if self.frame % max(30, int(120 / max(0.25, self.battle_speed))) == 0:
                self.assign_cannon_crews(self.gold_units)
                self.assign_cannon_crews(self.red_units)

            if self.battle_started and not self.sandbox_mode:
                ga = sum(1 for u in self.gold_units if u.alive)
                ra = sum(1 for u in self.red_units if u.alive)
                if ga == 0: self.winner = "RED"; self.state = "VICTORY"
                elif ra == 0: self.winner = "GOLD"; self.state = "VICTORY"

        self.waypoints = [w for w in self.waypoints if w.life > 0]
        for p in self.particles: p.update()
        self.particles = [p for p in self.particles if p.alive]

    def draw_menu(self, surface):
        surface.fill((25, 35, 20))
        for i in range(0, SCREEN_WIDTH, 40):
            for j in range(0, SCREEN_HEIGHT, 40):
                if (i + j) % 80 == 0:
                    pygame.draw.rect(surface, (30, 40, 25), (i, j, 40, 40))
        ov = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(ov, (0, 0, 0, 100), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        surface.blit(ov, (0, 0))

        cy = 50
        t = self.f_title.render("SULTAN WARS", True, GOLD)
        surface.blit(t, t.get_rect(center=(SCREEN_WIDTH // 2, cy)))
        cy += 45
        t2 = self.f_med.render("Epic Battle - Strategy & Tactics", True, LIGHT_GRAY)
        surface.blit(t2, t2.get_rect(center=(SCREEN_WIDTH // 2, cy)))
        cy += 35
        draw_star(surface, BRIGHT_GOLD, (SCREEN_WIDTH // 2 - 180, cy), 20, 9, 5, self.frame * 0.02, DARK_GOLD, 2, True)
        draw_star(surface, BRIGHT_RED, (SCREEN_WIDTH // 2 + 180, cy), 20, 9, 5, -self.frame * 0.02, DARK_RED, 2, True)
        surface.blit(self.f_large.render("VS", True, WHITE),
                     self.f_large.render("VS", True, WHITE).get_rect(center=(SCREEN_WIDTH // 2, cy)))

        cy += 50
        panel = pygame.Rect(SCREEN_WIDTH // 2 - 280, cy, 560, 150)
        ps = pygame.Surface((560, 150), pygame.SRCALPHA)
        pygame.draw.rect(ps, (15, 15, 30, 200), (0, 0, 560, 150), border_radius=10)
        surface.blit(ps, (panel.x, panel.y))
        pygame.draw.rect(surface, GOLD, panel, 2, border_radius=10)
        surface.blit(self.f_med.render("ARMY SETTINGS", True, GOLD),
                     self.f_med.render("ARMY SETTINGS", True, GOLD).get_rect(center=(SCREEN_WIDTH // 2, cy + 18)))

        settings = [(f"Soldiers: {self.soldier_count}", cy + 42, "s"),
                    (f"Commanders: {self.commander_count}", cy + 70, "c"),
                    (f"Cannons: {self.cannon_count}", cy + 98, "t")]
        self.menu_btns = []
        for txt, sy, key in settings:
            surface.blit(self.f_small.render(txt, True, WHITE), (SCREEN_WIDTH // 2 - 180, sy))
            m = pygame.Rect(SCREEN_WIDTH // 2 + 80, sy - 2, 40, 24)
            p2 = pygame.Rect(SCREEN_WIDTH // 2 + 130, sy - 2, 40, 24)
            mh = m.collidepoint(pygame.mouse.get_pos()); ph = p2.collidepoint(pygame.mouse.get_pos())
            pygame.draw.rect(surface, BRIGHT_RED if mh else RED, m, border_radius=5)
            pygame.draw.rect(surface, BRIGHT_GREEN if ph else GREEN, p2, border_radius=5)
            lbl = "-5" if key == "s" else "-1"; lbl2 = "+5" if key == "s" else "+1"
            surface.blit(self.f_small.render(lbl, True, WHITE), self.f_small.render(lbl, True, WHITE).get_rect(center=m.center))
            surface.blit(self.f_small.render(lbl2, True, WHITE), self.f_small.render(lbl2, True, WHITE).get_rect(center=p2.center))
            self.menu_btns.append(("minus_" + key, m)); self.menu_btns.append(("plus_" + key, p2))

        cy2 = cy + 165; bw = 260; bh = 48; mp = pygame.mouse.get_pos()

        btn_n = pygame.Rect(SCREEN_WIDTH // 2 - bw // 2, cy2, bw, bh)
        h1 = btn_n.collidepoint(mp)
        pygame.draw.rect(surface, BRIGHT_GOLD if h1 else GOLD, btn_n, border_radius=10)
        surface.blit(self.f_med.render("Normal Battle", True, BLACK),
                     self.f_med.render("Normal Battle", True, BLACK).get_rect(center=btn_n.center))
        self.menu_btns.append(("normal", btn_n))
        surface.blit(self.f_mini.render("Equal armies - Yellow vs Red", True, LIGHT_GRAY),
                     self.f_mini.render("Equal armies - Yellow vs Red", True, LIGHT_GRAY).get_rect(center=(SCREEN_WIDTH // 2, cy2 + bh + 8)))

        cy2 += 70
        btn_e = pygame.Rect(SCREEN_WIDTH // 2 - bw // 2, cy2, bw, bh)
        h2 = btn_e.collidepoint(mp)
        pygame.draw.rect(surface, BRIGHT_GREEN if h2 else DARK_GREEN, btn_e, border_radius=10)
        surface.blit(self.f_med.render("Wallachia Campaign", True, WHITE),
                     self.f_med.render("Wallachia Campaign", True, WHITE).get_rect(center=btn_e.center))
        self.menu_btns.append(("eflak", btn_e))
        surface.blit(self.f_mini.render("Yellow has more troops, Red has NO cannons", True, LIGHT_GRAY),
                     self.f_mini.render("Yellow has more troops, Red has NO cannons", True, LIGHT_GRAY).get_rect(center=(SCREEN_WIDTH // 2, cy2 + bh + 8)))

        cy2 += 70
        btn_s = pygame.Rect(SCREEN_WIDTH // 2 - bw // 2, cy2, bw, bh)
        h3 = btn_s.collidepoint(mp)
        pygame.draw.rect(surface, CYAN if h3 else (0, 150, 150), btn_s, border_radius=10)
        surface.blit(self.f_med.render("Sandbox Mode", True, WHITE),
                     self.f_med.render("Sandbox Mode", True, WHITE).get_rect(center=btn_s.center))
        self.menu_btns.append(("sandbox", btn_s))

        cy2 += 60
        btn_x = pygame.Rect(SCREEN_WIDTH // 2 - bw // 2, cy2, bw, bh)
        h4 = btn_x.collidepoint(mp)
        pygame.draw.rect(surface, GRAY if h4 else DARK_GRAY, btn_x, border_radius=10)
        surface.blit(self.f_med.render("EXIT", True, WHITE),
                     self.f_med.render("EXIT", True, WHITE).get_rect(center=btn_x.center))
        self.menu_btns.append(("exit", btn_x))

        cy2 += 65
        infos = [
            "RMB drag: Box select | LMB: Send selected | Click unit + F: Control",
            "WASD: Move | LMB: Fire cannon | P: Pause | N: Name unit (Sandbox)",
            "SPACE: Start battle | ESC: Menu | [ ] : Speed control",
        ]
        for i, info in enumerate(infos):
            surface.blit(self.f_tiny.render(info, True, LIGHT_GRAY),
                         self.f_tiny.render(info, True, LIGHT_GRAY).get_rect(center=(SCREEN_WIDTH // 2, cy2 + i * 18)))

    def draw_battle(self, surface):
        sx = random.randint(-self.cam_shake, self.cam_shake) if self.cam_shake > 0 else 0
        sy = random.randint(-self.cam_shake, self.cam_shake) if self.cam_shake > 0 else 0

        bs = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.game_map.draw(bs, self.camera, self.frame)
        for wp in self.waypoints: wp.draw(bs, self.camera)

        all_u = self.gold_units + self.red_units
        for layer in [UnitType.SOLDIER, UnitType.CANNON, UnitType.COMMANDER, UnitType.SULTAN]:
            for u in all_u:
                if u.unit_type == layer and u.alive: u.draw(bs, self.camera)

        for b in self.cannonballs: b.draw(bs, self.camera)
        for e in self.explosions: e.draw(bs, self.camera)
        for p in self.particles: p.draw(bs, self.camera)

        ctrl = self.controlled_unit
        if ctrl and ctrl.alive and ctrl.unit_type == UnitType.CANNON and ctrl.player_controlled:
            mx, my = pygame.mouse.get_pos()
            pygame.draw.line(bs, YELLOW, (mx - 15, my), (mx + 15, my), 1)
            pygame.draw.line(bs, YELLOW, (mx, my - 15), (mx, my + 15), 1)
            pygame.draw.circle(bs, YELLOW, (mx, my), 10, 1)
            pygame.draw.circle(bs, YELLOW, (mx, my), 3)
            wx, wy = self.camera.screen_to_world(mx, my)
            d = dist((ctrl.x, ctrl.y), (wx, wy))
            in_range = d <= ctrl.atk_range
            col = GREEN if in_range else RED
            ready = ctrl.atk_cd <= 0 and ctrl.has_crew()
            status = "READY" if ready else f"CD: {ctrl.atk_cd}"
            try:
                cf = pygame.font.SysFont("Arial", 12)
                ct = cf.render(f"{'IN RANGE' if in_range else 'OUT OF RANGE'} | {status}", True, col)
                bs.blit(ct, (mx + 15, my - 20))
            except: pass

        if self.box_selecting and self.box_start and self.box_end:
            bx1 = min(self.box_start[0], self.box_end[0])
            by1 = min(self.box_start[1], self.box_end[1])
            bx2 = max(self.box_start[0], self.box_end[0])
            by2 = max(self.box_start[1], self.box_end[1])
            w = max(1, bx2 - bx1); h = max(1, by2 - by1)
            sel_surf = pygame.Surface((w, h), pygame.SRCALPHA)
            pygame.draw.rect(sel_surf, (0, 255, 0, 40), (0, 0, w, h))
            bs.blit(sel_surf, (bx1, by1))
            pygame.draw.rect(bs, (0, 255, 0), (bx1, by1, w, h), 2)

        surface.blit(bs, (sx, sy))
        self._draw_ui(surface)

        if self.sandbox_mode:
            self._draw_sandbox_panel(surface)
        else:
            self._draw_side_panel(surface)

        self._draw_control_info(surface)

        # ===== HIZ KONTROL PANELİ =====
        self._draw_speed_panel(surface)

        if self.battle_paused and self.battle_started:
            pov = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            pygame.draw.rect(pov, (0, 0, 0, 80), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            surface.blit(pov, (0, 0))
            pt = self.f_title.render("PAUSED", True, WHITE)
            surface.blit(pt, pt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)))
            pt2 = self.f_med.render("Press P to resume", True, LIGHT_GRAY)
            surface.blit(pt2, pt2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30)))

        if not self.battle_started:
            bw2 = 300; bh2 = 50
            btn = pygame.Rect(SCREEN_WIDTH // 2 - bw2 // 2, SCREEN_HEIGHT - 75, bw2, bh2)
            h = btn.collidepoint(pygame.mouse.get_pos())
            pulse = abs(math.sin(self.frame * 0.06))
            bc = (255, int(80 + pulse * 175), int(pulse * 80))
            pygame.draw.rect(surface, BRIGHT_RED if h else RED, btn, border_radius=12)
            pygame.draw.rect(surface, bc, btn, 3, border_radius=12)
            surface.blit(self.f_med.render("ATTACK ORDER [SPACE]", True, WHITE),
                         self.f_med.render("ATTACK ORDER [SPACE]", True, WHITE).get_rect(center=btn.center))
            self.atk_btn = btn
        else:
            self.atk_btn = None

        if self.box_selected_units:
            cnt = len(self.box_selected_units)
            gt = self.f_small.render(f"{cnt} units selected - Left click to send", True, (100, 255, 100))
            surface.blit(gt, gt.get_rect(center=(SCREEN_WIDTH // 2, 82)))

        if self.naming_mode:
            self._draw_naming_dialog(surface)

        self._draw_minimap(surface)

    def _draw_speed_panel(self, surface):
        """Savaş hızı kontrol panelini çizer"""
        # Panel konumu: üst orta, UI barının altında
        panel_w = 340
        panel_h = 42
        panel_x = SCREEN_WIDTH // 2 - panel_w // 2
        panel_y = 74

        # Panel arka planı
        ps = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        pygame.draw.rect(ps, (0, 0, 0, 180), (0, 0, panel_w, panel_h), border_radius=8)
        surface.blit(ps, (panel_x, panel_y))

        # Hız ikonu ve başlık
        # Hız göstergesi - sol taraf
        speed_text = f"⚡ {self.battle_speed:.2g}x"
        speed_color = WHITE
        if self.battle_speed < 1.0:
            speed_color = (100, 180, 255)  # Yavaş = mavi
        elif self.battle_speed > 1.0:
            speed_color = ORANGE  # Hızlı = turuncu
        if self.battle_speed >= 3.0:
            speed_color = FIRE_RED  # Çok hızlı = kırmızı

        st = self.f_small.render(speed_text, True, speed_color)
        surface.blit(st, (panel_x + 8, panel_y + 12))

        # Hız butonları
        self.speed_btn_rects = []
        btn_w = 38
        btn_h = 26
        btn_y = panel_y + 8
        start_x = panel_x + 75
        mp = pygame.mouse.get_pos()

        for i, spd in enumerate(self.speed_options):
            bx = start_x + i * (btn_w + 4)
            btn_rect = pygame.Rect(bx, btn_y, btn_w, btn_h)
            is_active = abs(self.battle_speed - spd) < 0.01
            is_hover = btn_rect.collidepoint(mp)

            # Buton rengi
            if is_active:
                if spd < 1.0:
                    btn_color = (40, 120, 200)
                    border_color = (80, 180, 255)
                elif spd == 1.0:
                    btn_color = (40, 160, 60)
                    border_color = (80, 220, 100)
                elif spd <= 2.0:
                    btn_color = (200, 120, 20)
                    border_color = (255, 180, 50)
                else:
                    btn_color = (200, 40, 40)
                    border_color = (255, 80, 80)
            elif is_hover:
                btn_color = (70, 70, 90)
                border_color = (140, 140, 160)
            else:
                btn_color = (45, 45, 60)
                border_color = (80, 80, 100)

            pygame.draw.rect(surface, btn_color, btn_rect, border_radius=5)
            pygame.draw.rect(surface, border_color, btn_rect, 2 if is_active else 1, border_radius=5)

            # Aktif buton glow efekti
            if is_active:
                glow_surf = pygame.Surface((btn_w + 8, btn_h + 8), pygame.SRCALPHA)
                pygame.draw.rect(glow_surf, (*border_color, 40), (0, 0, btn_w + 8, btn_h + 8), border_radius=7)
                surface.blit(glow_surf, (bx - 4, btn_y - 4))

            # Buton yazısı
            label = f"{spd:.2g}x"
            txt_color = WHITE if is_active else (LIGHT_GRAY if is_hover else (130, 130, 140))
            lt = self.f_mini.render(label, True, txt_color)
            surface.blit(lt, lt.get_rect(center=btn_rect.center))

            self.speed_btn_rects.append((spd, btn_rect))

        # Klavye kısayolu bilgisi
        kb_text = "[ ] keys"
        kbt = self.f_mini.render(kb_text, True, (100, 100, 120))
        surface.blit(kbt, (panel_x + panel_w - kbt.get_width() - 8, panel_y + 14))

        # Hız çubuğu animasyonu (aktif hızın altında ince çizgi)
        if self.battle_started and not self.battle_paused:
            bar_progress = (self.frame * self.battle_speed * 0.02) % 1.0
            bar_x = panel_x + 4
            bar_w = int((panel_w - 8) * bar_progress)
            bar_color = speed_color
            pygame.draw.rect(surface, (*bar_color[:3],), (bar_x, panel_y + panel_h - 3, bar_w, 2), border_radius=1)

    def _draw_naming_dialog(self, surface):
        dw = 400; dh = 120
        dx = SCREEN_WIDTH // 2 - dw // 2; dy = SCREEN_HEIGHT // 2 - dh // 2
        ds = pygame.Surface((dw, dh), pygame.SRCALPHA)
        pygame.draw.rect(ds, (10, 10, 30, 230), (0, 0, dw, dh), border_radius=12)
        pygame.draw.rect(ds, CYAN, (0, 0, dw, dh), 3, border_radius=12)
        surface.blit(ds, (dx, dy))
        type_names = {UnitType.SULTAN: "Sultan", UnitType.COMMANDER: "Commander",
                      UnitType.SOLDIER: "Soldier", UnitType.CANNON: "Cannon"}
        uname = type_names.get(self.naming_unit.unit_type, "Unit") if self.naming_unit else "Unit"
        surface.blit(self.f_med.render(f"Name your {uname}", True, CYAN),
                     self.f_med.render(f"Name your {uname}", True, CYAN).get_rect(center=(SCREEN_WIDTH // 2, dy + 20)))
        ib = pygame.Rect(dx + 30, dy + 48, dw - 60, 30)
        pygame.draw.rect(surface, (30, 30, 50), ib, border_radius=5)
        pygame.draw.rect(surface, WHITE, ib, 2, border_radius=5)
        cursor = "|" if (self.frame // 30) % 2 == 0 else ""
        surface.blit(self.f_small.render(self.naming_text + cursor, True, WHITE), (ib.x + 8, ib.y + 6))
        surface.blit(self.f_tiny.render("Enter: Confirm | Esc: Cancel", True, LIGHT_GRAY),
                     self.f_tiny.render("Enter: Confirm | Esc: Cancel", True, LIGHT_GRAY).get_rect(center=(SCREEN_WIDTH // 2, dy + 100)))

    def _draw_control_info(self, surface):
        pw = 250; ph = 110; px = 5; py = SCREEN_HEIGHT - ph - 10
        if self.clicked_unit and self.clicked_unit.alive:
            u = self.clicked_unit
            ps = pygame.Surface((pw, ph), pygame.SRCALPHA)
            pygame.draw.rect(ps, (0, 0, 0, 170), (0, 0, pw, ph), border_radius=8)
            border_c = MAGENTA if u.player_controlled else (0, 220, 0)
            pygame.draw.rect(ps, border_c, (0, 0, pw, ph), 2, border_radius=8)
            surface.blit(ps, (px, py))
            type_names = {UnitType.SULTAN: "Sultan", UnitType.COMMANDER: "Commander",
                          UnitType.SOLDIER: "Soldier", UnitType.CANNON: "Cannon"}
            team_name = "Yellow" if u.team == "gold" else "Red"
            tc = GOLD if u.team == "gold" else RED
            name_str = f' "{u.custom_name}"' if u.custom_name else ""
            surface.blit(self.f_small.render(f"{type_names[u.unit_type]}{name_str} ({team_name})", True, tc), (px + 8, py + 6))
            surface.blit(self.f_mini.render(f"HP: {max(0, u.hp)}/{u.max_hp}  ATK: {u.attack}  SPD: {u.speed}", True, WHITE), (px + 8, py + 26))
            if u.player_controlled:
                if u.unit_type == UnitType.CANNON:
                    surface.blit(self.f_small.render("CTRL: WASD+LMB fire, F release", True, MAGENTA), (px + 8, py + 44))
                else:
                    surface.blit(self.f_small.render("CTRL: WASD move, F release", True, MAGENTA), (px + 8, py + 44))
            elif u.unit_type == UnitType.CANNON:
                crew_txt = "Has crew" if u.has_crew() else "NO CREW!"
                crew_c = GREEN if u.has_crew() else RED
                surface.blit(self.f_small.render(f"Cannon - {crew_txt}", True, crew_c), (px + 8, py + 44))
            else:
                surface.blit(self.f_small.render("Press F to control", True, (100, 255, 100)), (px + 8, py + 44))
            if u.operating_cannon and u.operating_cannon.alive:
                surface.blit(self.f_mini.render("Assigned as cannon crew", True, CANNON_GRAY), (px + 8, py + 64))
            else:
                surface.blit(self.f_mini.render(f"Pos: ({int(u.x)}, {int(u.y)})", True, LIGHT_GRAY), (px + 8, py + 64))
            if u.unit_type == UnitType.CANNON and u.player_controlled:
                surface.blit(self.f_mini.render(f"Range: {u.atk_range} | CD: {u.atk_cd}", True, ORANGE), (px + 8, py + 80))
            if self.sandbox_mode:
                surface.blit(self.f_mini.render("N: Name this unit", True, CYAN), (px + 8, py + 94))
        else:
            ps = pygame.Surface((pw, 30), pygame.SRCALPHA)
            pygame.draw.rect(ps, (0, 0, 0, 120), (0, 0, pw, 30), border_radius=5)
            surface.blit(ps, (px, py + ph - 30))
            surface.blit(self.f_mini.render("Click unit, F=control | RMB drag=select", True, LIGHT_GRAY), (px + 6, py + ph - 24))

    def _draw_ui(self, surface):
        ps = pygame.Surface((SCREEN_WIDTH, 72), pygame.SRCALPHA)
        pygame.draw.rect(ps, (0, 0, 0, 185), (0, 0, SCREEN_WIDTH, 72))
        pygame.draw.line(ps, GOLD, (0, 71), (SCREEN_WIDTH, 71), 2)
        surface.blit(ps, (0, 0))

        ga = sum(1 for u in self.gold_units if u.alive)
        gs = sum(1 for u in self.gold_units if u.alive and u.unit_type == UnitType.SOLDIER)
        gp = next((u for u in self.gold_units if u.unit_type == UnitType.SULTAN and u.alive), None)
        gc = sum(1 for u in self.gold_units if u.alive and u.unit_type == UnitType.CANNON)
        gc_a = sum(1 for u in self.gold_units if u.alive and u.unit_type == UnitType.CANNON and u.has_crew())

        draw_star(surface, BRIGHT_GOLD, (22, 35), 13, 6, 5, self.frame * 0.02, DARK_GOLD, 2)
        surface.blit(self.f_med.render("YELLOW TEAM", True, GOLD), (42, 4))
        surface.blit(self.f_mini.render(f"Soldiers:{gs} Cannons:{gc_a}/{gc} Total:{ga}", True, YELLOW_LIGHT), (42, 27))
        if gp: surface.blit(self.f_mini.render(f"Sultan HP:{gp.hp}/{gp.max_hp}", True, GREEN), (42, 42))
        surface.blit(self.f_small.render(f"Kills:{self.kills_gold}", True, GOLD), (42, 55))

        ra = sum(1 for u in self.red_units if u.alive)
        rs = sum(1 for u in self.red_units if u.alive and u.unit_type == UnitType.SOLDIER)
        rp = next((u for u in self.red_units if u.unit_type == UnitType.SULTAN and u.alive), None)
        rc = sum(1 for u in self.red_units if u.alive and u.unit_type == UnitType.CANNON)
        rc_a = sum(1 for u in self.red_units if u.alive and u.unit_type == UnitType.CANNON and u.has_crew())

        draw_star(surface, BRIGHT_RED, (SCREEN_WIDTH - 22, 35), 13, 6, 5, self.frame * 0.02, DARK_RED, 2)
        t = self.f_med.render("RED TEAM", True, RED)
        surface.blit(t, (SCREEN_WIDTH - 42 - t.get_width(), 4))
        t2 = self.f_mini.render(f"Soldiers:{rs} Cannons:{rc_a}/{rc} Total:{ra}", True, RED_LIGHT)
        surface.blit(t2, (SCREEN_WIDTH - 42 - t2.get_width(), 27))
        if rp:
            t3 = self.f_mini.render(f"Sultan HP:{rp.hp}/{rp.max_hp}", True, RED_LIGHT)
            surface.blit(t3, (SCREEN_WIDTH - 42 - t3.get_width(), 42))
        kt = self.f_small.render(f"Kills:{self.kills_red}", True, RED)
        surface.blit(kt, (SCREEN_WIDTH - 42 - kt.get_width(), 55))

        if self.battle_paused:
            vs = self.f_large.render("PAUSED", True, ORANGE)
        elif self.battle_started:
            p = abs(math.sin(self.frame * 0.05))
            vs = self.f_large.render("BATTLE", True, (255, int(200 + p * 55), int(150 + p * 55)))
        else:
            vs = self.f_large.render("STRATEGY PHASE", True, CYAN)
        surface.blit(vs, vs.get_rect(center=(SCREEN_WIDTH // 2, 35)))

    def _draw_side_panel(self, surface):
        pw = 175; px = SCREEN_WIDTH - pw - 5; py = 78; ph = 260
        ps = pygame.Surface((pw, ph), pygame.SRCALPHA)
        pygame.draw.rect(ps, (0, 0, 0, 150), (0, 0, pw, ph), border_radius=8)
        pygame.draw.rect(ps, GOLD, (0, 0, pw, ph), 2, border_radius=8)
        surface.blit(ps, (px, py))
        surface.blit(self.f_tiny.render("CONTROLS", True, CYAN), (px + 8, py + 8))
        controls = ["RMB drag: Box select", "LMB: Send selected", "Click + F: Control",
                    "WASD: Move unit/cannon", "LMB: Fire cannon", "P: Pause/Resume",
                    "SPACE: Attack order", "Arrows: Scroll cam", "TAB: Focus ctrl unit",
                    "[ ]: Speed down/up", "ESC: Menu", "", "Cannons auto-advance!", "Cannons need crew!"]
        for i, c in enumerate(controls):
            col = LIGHT_GRAY
            if "cannon" in c.lower(): col = ORANGE
            if "pause" in c.lower(): col = CYAN
            if "speed" in c.lower(): col = YELLOW
            surface.blit(self.f_mini.render(c, True, col), (px + 8, py + 26 + i * 14))

    def _draw_sandbox_panel(self, surface):
        pw = 180; px = 5; py = 78; ph = 340
        ps = pygame.Surface((pw, ph), pygame.SRCALPHA)
        pygame.draw.rect(ps, (0, 0, 0, 170), (0, 0, pw, ph), border_radius=8)
        pygame.draw.rect(ps, CYAN, (0, 0, pw, ph), 2, border_radius=8)
        surface.blit(ps, (px, py))

        surface.blit(self.f_med.render("SANDBOX", True, CYAN), (px + 10, py + 6))
        surface.blit(self.f_tiny.render("Team:", True, WHITE), (px + 10, py + 32))
        gold_btn = pygame.Rect(px + 55, py + 30, 50, 20)
        red_btn = pygame.Rect(px + 110, py + 30, 50, 20)
        pygame.draw.rect(surface, BRIGHT_GOLD if self.sandbox_team == "gold" else DARK_GOLD, gold_btn, border_radius=4)
        pygame.draw.rect(surface, BRIGHT_RED if self.sandbox_team == "red" else DARK_RED, red_btn, border_radius=4)
        surface.blit(self.f_mini.render("Yellow", True, BLACK), self.f_mini.render("Yellow", True, BLACK).get_rect(center=gold_btn.center))
        surface.blit(self.f_mini.render("Red", True, WHITE), self.f_mini.render("Red", True, WHITE).get_rect(center=red_btn.center))
        self.sb_gold_btn = gold_btn; self.sb_red_btn = red_btn

        surface.blit(self.f_tiny.render("Place Unit:", True, WHITE), (px + 10, py + 58))
        unit_btns = []
        types = [("Sultan", UnitType.SULTAN, GOLD), ("Commander", UnitType.COMMANDER, GREEN),
                 ("Soldier", UnitType.SOLDIER, YELLOW), ("Cannon", UnitType.CANNON, GRAY)]
        for i, (name, ut, col) in enumerate(types):
            btn = pygame.Rect(px + 10, py + 78 + i * 28, pw - 20, 24)
            sel = self.sandbox_placing == ut
            pygame.draw.rect(surface, col if sel else (40, 40, 50), btn, border_radius=5)
            if sel: pygame.draw.rect(surface, WHITE, btn, 2, border_radius=5)
            tc2 = BLACK if sel else col
            surface.blit(self.f_mini.render(name, True, tc2), self.f_mini.render(name, True, tc2).get_rect(center=btn.center))
            unit_btns.append((ut, btn))
        self.sb_unit_btns = unit_btns

        cy = py + 200
        g_count = len([u for u in self.gold_units if u.alive])
        r_count = len([u for u in self.red_units if u.alive])
        surface.blit(self.f_tiny.render(f"Yellow: {g_count}", True, GOLD), (px + 10, cy))
        surface.blit(self.f_tiny.render(f"Red: {r_count}", True, RED), (px + 10, cy + 16))

        clear_g = pygame.Rect(px + 10, cy + 38, pw // 2 - 15, 22)
        clear_r = pygame.Rect(px + pw // 2 + 5, cy + 38, pw // 2 - 15, 22)
        clear_a = pygame.Rect(px + 10, cy + 64, pw - 20, 22)
        pygame.draw.rect(surface, DARK_GOLD, clear_g, border_radius=4)
        pygame.draw.rect(surface, DARK_RED, clear_r, border_radius=4)
        pygame.draw.rect(surface, DARK_GRAY, clear_a, border_radius=4)
        surface.blit(self.f_mini.render("Clear Y", True, WHITE), self.f_mini.render("Clear Y", True, WHITE).get_rect(center=clear_g.center))
        surface.blit(self.f_mini.render("Clear R", True, WHITE), self.f_mini.render("Clear R", True, WHITE).get_rect(center=clear_r.center))
        surface.blit(self.f_mini.render("Clear All", True, WHITE), self.f_mini.render("Clear All", True, WHITE).get_rect(center=clear_a.center))
        self.sb_clear_g = clear_g; self.sb_clear_r = clear_r; self.sb_clear_a = clear_a

        desel = pygame.Rect(px + 10, cy + 90, pw - 20, 22)
        pygame.draw.rect(surface, (60, 60, 80), desel, border_radius=4)
        surface.blit(self.f_mini.render("Deselect [X]", True, WHITE), self.f_mini.render("Deselect [X]", True, WHITE).get_rect(center=desel.center))
        self.sb_desel = desel

        surface.blit(self.f_mini.render("N: Name selected unit", True, CYAN), (px + 10, cy + 118))

    def _draw_minimap(self, surface):
        mw = 220; mh = 165
        mx2 = SCREEN_WIDTH - mw - 10; my2 = SCREEN_HEIGHT - mh - 10
        ms = pygame.Surface((mw, mh), pygame.SRCALPHA)
        pygame.draw.rect(ms, (0, 0, 0, 150), (0, 0, mw, mh), border_radius=5)
        surface.blit(ms, (mx2, my2))
        pygame.draw.rect(surface, LIGHT_GRAY, (mx2, my2, mw, mh), 2, border_radius=5)
        sx = WORLD_WIDTH / mw; sy2 = WORLD_HEIGHT / mh
        for u in self.gold_units:
            if u.alive:
                px3 = mx2 + int(u.x / sx); py3 = my2 + int(u.y / sy2)
                s = 3 if u.unit_type == UnitType.SULTAN else (2 if u.unit_type in (UnitType.COMMANDER, UnitType.CANNON) else 1)
                c = MAGENTA if u.player_controlled else (CANNON_GRAY if u.unit_type == UnitType.CANNON else (GREEN if u.unit_type == UnitType.COMMANDER else GOLD))
                pygame.draw.circle(surface, c, (px3, py3), s)
        for u in self.red_units:
            if u.alive:
                px3 = mx2 + int(u.x / sx); py3 = my2 + int(u.y / sy2)
                s = 3 if u.unit_type == UnitType.SULTAN else 1
                pygame.draw.circle(surface, RED, (px3, py3), s)
        cvx = mx2 + int(self.camera.x / sx); cvy = my2 + int(self.camera.y / sy2)
        cvw = int(SCREEN_WIDTH / sx); cvh = int(SCREEN_HEIGHT / sy2)
        pygame.draw.rect(surface, WHITE, (cvx, cvy, cvw, cvh), 1)
        surface.blit(self.f_mini.render("MINIMAP", True, WHITE), (mx2 + 5, my2 + 3))

    def draw_victory(self, surface):
        self.draw_battle(surface)
        ov = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(ov, (0, 0, 0, 180), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        surface.blit(ov, (0, 0))
        if self.winner == "GOLD":
            wc, sc2, bc2 = GOLD, BRIGHT_GOLD, DARK_GOLD; wt = "YELLOW TEAM WINS!"
        else:
            wc, sc2, bc2 = RED, BRIGHT_RED, DARK_RED; wt = "RED TEAM WINS!"
        draw_star(surface, sc2, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 140), 50, 22, 5, self.frame * 0.03, bc2, 3, True)
        t = self.f_title.render(wt, True, wc)
        surface.blit(t, t.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)))
        sy = SCREEN_HEIGHT // 2 + 20
        surface.blit(self.f_med.render(f"Yellow Kills: {self.kills_gold}", True, GOLD),
                     self.f_med.render(f"Yellow Kills: {self.kills_gold}", True, GOLD).get_rect(center=(SCREEN_WIDTH // 2, sy)))
        surface.blit(self.f_med.render(f"Red Kills: {self.kills_red}", True, RED),
                     self.f_med.render(f"Red Kills: {self.kills_red}", True, RED).get_rect(center=(SCREEN_WIDTH // 2, sy + 35)))
        bw3 = 260; bh3 = 48
        replay = pygame.Rect(SCREEN_WIDTH // 2 - bw3 // 2, sy + 80, bw3, bh3)
        h1 = replay.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(surface, BRIGHT_GREEN if h1 else GREEN, replay, border_radius=10)
        surface.blit(self.f_med.render("PLAY AGAIN", True, WHITE),
                     self.f_med.render("PLAY AGAIN", True, WHITE).get_rect(center=replay.center))
        menu = pygame.Rect(SCREEN_WIDTH // 2 - bw3 // 2, sy + 140, bw3, bh3)
        h2 = menu.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(surface, BRIGHT_GOLD if h2 else GOLD, menu, border_radius=10)
        surface.blit(self.f_med.render("MAIN MENU", True, BLACK),
                     self.f_med.render("MAIN MENU", True, BLACK).get_rect(center=menu.center))
        self.vic_btns = [replay, menu]

    def start_mode(self, mode, sandbox=False):
        self.map_mode = mode; self.sandbox_mode = sandbox
        self.game_map = GameMap(mode if not sandbox else "sandbox")
        self.setup_armies(); self.state = "BATTLE"
        if sandbox:
            self.battle_started = False
            self.camera.target_x = WORLD_WIDTH // 2 - SCREEN_WIDTH // 2
            self.camera.target_y = WORLD_HEIGHT // 2 - SCREEN_HEIGHT // 2

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False
                if event.type == pygame.VIDEORESIZE:
                    global SCREEN_WIDTH, SCREEN_HEIGHT
                    SCREEN_WIDTH = event.w; SCREEN_HEIGHT = event.h

                if self.naming_mode:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            if self.naming_unit: self.naming_unit.custom_name = self.naming_text
                            self.naming_mode = False; self.naming_unit = None; self.naming_text = ""
                        elif event.key == pygame.K_ESCAPE:
                            self.naming_mode = False; self.naming_unit = None; self.naming_text = ""
                        elif event.key == pygame.K_BACKSPACE:
                            self.naming_text = self.naming_text[:-1]
                        else:
                            if len(self.naming_text) < 20 and event.unicode.isprintable() and event.unicode:
                                self.naming_text += event.unicode
                    continue

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.state == "MENU":
                        for name, rect in self.menu_btns:
                            if rect.collidepoint(pos):
                                if name == "normal": self.start_mode("normal")
                                elif name == "eflak": self.start_mode("eflak")
                                elif name == "sandbox": self.start_mode("sandbox", sandbox=True)
                                elif name == "exit": running = False
                                elif name == "minus_s": self.soldier_count = max(5, self.soldier_count - 5)
                                elif name == "plus_s": self.soldier_count = min(80, self.soldier_count + 5)
                                elif name == "minus_c": self.commander_count = max(1, self.commander_count - 1)
                                elif name == "plus_c": self.commander_count = min(10, self.commander_count + 1)
                                elif name == "minus_t": self.cannon_count = max(0, self.cannon_count - 1)
                                elif name == "plus_t": self.cannon_count = min(10, self.cannon_count + 1)

                    elif self.state == "BATTLE":
                        # ===== HIZ BUTONLARI KONTROLÜ =====
                        speed_clicked = False
                        if event.button == 1:
                            for spd, btn_rect in self.speed_btn_rects:
                                if btn_rect.collidepoint(pos):
                                    self.set_speed(spd)
                                    speed_clicked = True
                                    break

                        if speed_clicked:
                            pass  # Hız butonu tıklandı, başka işlem yapma
                        elif event.button == 1:
                            ctrl = self.controlled_unit
                            if ctrl and ctrl.alive and ctrl.unit_type == UnitType.CANNON and ctrl.player_controlled and self.battle_started:
                                self.fire_controlled_cannon()
                            elif self.atk_btn and self.atk_btn.collidepoint(pos):
                                self.battle_started = True; self.cam_shake = 10
                            elif self.sandbox_mode:
                                handled = False
                                if hasattr(self, 'sb_gold_btn') and self.sb_gold_btn.collidepoint(pos):
                                    self.sandbox_team = "gold"; handled = True
                                elif hasattr(self, 'sb_red_btn') and self.sb_red_btn.collidepoint(pos):
                                    self.sandbox_team = "red"; handled = True
                                elif hasattr(self, 'sb_clear_g') and self.sb_clear_g.collidepoint(pos):
                                    self.gold_units.clear(); self.release_control(); self.clicked_unit = None; handled = True
                                elif hasattr(self, 'sb_clear_r') and self.sb_clear_r.collidepoint(pos):
                                    self.red_units.clear(); self.release_control(); self.clicked_unit = None; handled = True
                                elif hasattr(self, 'sb_clear_a') and self.sb_clear_a.collidepoint(pos):
                                    self.gold_units.clear(); self.red_units.clear(); self.release_control(); self.clicked_unit = None; handled = True
                                elif hasattr(self, 'sb_desel') and self.sb_desel.collidepoint(pos):
                                    self.sandbox_placing = None; handled = True
                                if hasattr(self, 'sb_unit_btns'):
                                    for ut, btn in self.sb_unit_btns:
                                        if btn.collidepoint(pos): self.sandbox_placing = ut; handled = True
                                if not handled and self.sandbox_placing and pos[1] > 75:
                                    if not (pos[0] < 190 and pos[1] < 400):
                                        wx, wy = self.camera.screen_to_world(pos[0], pos[1])
                                        self.sandbox_place(wx, wy)
                                elif not handled:
                                    if self.box_selected_units:
                                        wx, wy = self.camera.screen_to_world(pos[0], pos[1])
                                        self.send_selected_to(wx, wy)
                                        for u in self.box_selected_units: u.selected = False
                                        self.box_selected_units = []
                                    else:
                                        wx, wy = self.camera.screen_to_world(pos[0], pos[1])
                                        self.try_select_unit_at(wx, wy)
                            else:
                                if self.box_selected_units:
                                    wx, wy = self.camera.screen_to_world(pos[0], pos[1])
                                    self.send_selected_to(wx, wy)
                                    for u in self.box_selected_units: u.selected = False
                                    self.box_selected_units = []
                                else:
                                    wx, wy = self.camera.screen_to_world(pos[0], pos[1])
                                    self.try_select_unit_at(wx, wy)

                        elif event.button == 3:
                            self.box_selecting = True; self.box_start = pos; self.box_end = pos
                        elif event.button == 2:
                            self.camera.drag = True; self.camera.drag_start = pos
                            self.camera.drag_cam_start = (self.camera.target_x, self.camera.target_y)

                    elif self.state == "VICTORY":
                        if len(self.vic_btns) >= 2:
                            if self.vic_btns[0].collidepoint(pos): self.start_mode(self.map_mode, self.sandbox_mode)
                            elif self.vic_btns[1].collidepoint(pos): self.state = "MENU"

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 2: self.camera.drag = False
                    if event.button == 3 and self.state == "BATTLE":
                        if self.box_selecting:
                            self.box_selecting = False
                            self.box_end = pygame.mouse.get_pos()
                            if self.box_start:
                                dx = abs(self.box_end[0] - self.box_start[0])
                                dy = abs(self.box_end[1] - self.box_start[1])
                                if dx > 10 or dy > 10: self.select_units_in_box()
                                else:
                                    for u in self.box_selected_units: u.selected = False
                                    self.box_selected_units = []

                if event.type == pygame.MOUSEMOTION:
                    if self.camera.drag:
                        dx = event.pos[0] - self.camera.drag_start[0]
                        dy = event.pos[1] - self.camera.drag_start[1]
                        self.camera.target_x = self.camera.drag_cam_start[0] - dx
                        self.camera.target_y = self.camera.drag_cam_start[1] - dy
                    if self.box_selecting: self.box_end = event.pos

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.state == "BATTLE" and not self.battle_started:
                        self.battle_started = True; self.cam_shake = 10
                    elif event.key == pygame.K_p and self.state == "BATTLE" and self.battle_started:
                        self.battle_paused = not self.battle_paused
                    elif event.key == pygame.K_ESCAPE:
                        if self.state in ("BATTLE", "VICTORY"): self.state = "MENU"; self.release_control()
                    elif event.key == pygame.K_r and self.state == "VICTORY":
                        self.start_mode(self.map_mode, self.sandbox_mode)
                    elif event.key == pygame.K_x:
                        if self.sandbox_mode: self.sandbox_placing = None
                    elif event.key == pygame.K_f and self.state == "BATTLE":
                        self.toggle_control()
                    elif event.key == pygame.K_n and self.state == "BATTLE" and self.sandbox_mode:
                        self.start_naming()
                    elif event.key == pygame.K_TAB and self.state == "BATTLE":
                        ctrl = self.controlled_unit
                        if ctrl and ctrl.alive:
                            self.camera.target_x = ctrl.x - SCREEN_WIDTH // 2
                            self.camera.target_y = ctrl.y - SCREEN_HEIGHT // 2
                    # ===== HIZ KLAVYE KONTROLLERI =====
                    elif event.key == pygame.K_RIGHTBRACKET and self.state == "BATTLE":
                        self.cycle_speed_up()
                    elif event.key == pygame.K_LEFTBRACKET and self.state == "BATTLE":
                        self.cycle_speed_down()

            self.update()
            screen.fill(BLACK)
            if self.state == "MENU": self.draw_menu(screen)
            elif self.state == "BATTLE": self.draw_battle(screen)
            elif self.state == "VICTORY": self.draw_victory(screen)
            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit(); sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()