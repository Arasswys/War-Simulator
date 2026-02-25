import pygame
import sys
import math
import random
from enum import Enum

pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Sultan Wars - Epic Battle")
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
CANNON_GRAY = (80, 80, 90)
SMOKE_COLOR = (160, 160, 160)
ORANGE = (255, 140, 0)
FIRE_RED = (255, 80, 20)
CYAN = (0, 200, 200)
MAGENTA = (255, 0, 255)
STEEL = (170, 175, 185)

WORLD_WIDTH = 8000
WORLD_HEIGHT = 6000

LANG_EN = {
    "title": "SULTAN WARS", "subtitle": "Epic Battle - Strategy & Tactics",
    "army_settings": "ARMY SETTINGS", "soldiers": "Soldiers", "commanders": "Commanders",
    "cannons": "Cannons", "normal_battle": "Normal Battle",
    "normal_desc": "Equal armies - Yellow vs Red", "wallachia": "Wallachia Campaign",
    "wallachia_desc": "Yellow has more troops, Red has NO cannons",
    "ankara": "War of Ankara",
    "ankara_desc": "1402 - Bayezid vs Timur | Scripted + Cutscene",
    "sandbox": "Sandbox Mode", "exit": "EXIT", "language": "Language",
    "attack_order": "ATTACK ORDER [SPACE]",
    "begin_ankara": "BEGIN BATTLE OF ANKARA [SPACE]",
    "paused": "PAUSED", "battle": "BATTLE", "battle_ankara": "BATTLE OF ANKARA",
    "strategy_phase": "STRATEGY PHASE", "ankara_1402": "ANKARA - 1402",
    "yellow_team": "YELLOW TEAM", "red_team": "RED TEAM",
    "bayezid_army": "BAYEZID'S ARMY", "timur_army": "TIMUR'S ARMY",
    "kills": "Kills", "sultan_hp": "Sultan HP", "total": "Total",
    "timur_in_tent": "Timur: In tent (waiting)", "controls": "CONTROLS",
    "ctrl_box_select": "RMB drag: Box select", "ctrl_send": "LMB: Send selected",
    "ctrl_control": "Click + F: Control", "ctrl_move": "WASD: Move unit",
    "ctrl_move_cannon": "WASD: Move unit/cannon", "ctrl_fire": "LMB: Fire cannon",
    "ctrl_pause": "P: Pause/Resume", "ctrl_start": "SPACE: Start battle",
    "ctrl_attack": "SPACE: Attack order", "ctrl_speed": "[ ]: Speed",
    "ctrl_scroll": "Arrows: Scroll cam", "ctrl_focus": "TAB: Focus ctrl unit",
    "ctrl_menu": "ESC: Menu", "ctrl_cannon_crew": "Cannons need crew!",
    "ankara_info_1": "=== ANKARA 1402 ===", "ankara_info_2": "Bayezid fights!",
    "ankara_info_3": "Timur waits in tent", "ankara_info_4": "10 vs 20 soldiers",
    "ankara_info_5": "Watch the story!",
    "units_selected": "units selected - Left click to send",
    "click_unit": "Click unit, F=control | RMB drag=select",
    "press_f": "Press F to control", "ctrl_wasd": "CTRL: WASD move, F release",
    "hp": "HP", "atk": "ATK", "spd": "SPD", "pos": "Pos",
    "minimap": "MINIMAP", "play_again": "PLAY AGAIN", "main_menu": "MAIN MENU",
    "yellow_wins": "YELLOW TEAM WINS!", "red_wins": "RED TEAM WINS!",
    "timur_wins": "TIMUR WINS!", "ankara_title_vic": "Battle of Ankara - 1402",
    "bayezid_captured": "Bayezid I was captured and imprisoned.",
    "interregnum": "The Ottoman Empire fell into an interregnum period.",
    "timur_kills": "Timur Kills", "bayezid_kills": "Bayezid Kills",
    "yellow_kills": "Yellow Kills", "red_kills": "Red Kills",
    "no_crew": "NO CREW", "has_crew": "Has crew",
    "cannon_crew": "Assigned as cannon crew", "ctrl_label": "CTRL",
    "sultan": "Sultan", "commander": "Commander", "soldier": "Soldier",
    "cannon": "Cannon", "yellow": "Yellow", "red": "Red",
    "name_unit": "Name your", "enter_confirm": "Enter: Confirm | Esc: Cancel",
    "name_selected": "N: Name selected unit", "sandbox_title": "SANDBOX",
    "team": "Team", "place_unit": "Place Unit:", "clear_y": "Clear Y",
    "clear_r": "Clear R", "clear_all": "Clear All", "deselect": "Deselect [X]",
    "prison": "PRISON", "timur_tent": "TIMUR'S TENT",
    "cutscene_alone": "THE BATTLE OF ANKARA - 1402 | Bayezid stands alone...",
    "cutscene_capture": "THE BATTLE OF ANKARA | Bayezid is being captured!",
    "cutscene_escort": "THE BATTLE OF ANKARA | Escorting to Timur's tent...",
    "cutscene_throne": "THE BATTLE OF ANKARA | Before the conqueror...",
    "cutscene_dialogue1": "THE BATTLE OF ANKARA | A historic conversation...",
    "cutscene_dialogue2": "THE BATTLE OF ANKARA | Timur responds...",
    "cutscene_prison": "THE BATTLE OF ANKARA | The sultan is imprisoned...",
    "cutscene_default": "THE BATTLE OF ANKARA - 1402",
    "enter_skip": "ENTER: skip",
    "bayezid_imprisoned": "Bayezid was imprisoned...",
    "bayezid_speaker": "BAYEZID (Yellow Sultan)",
    "timur_speaker": "TIMUR (Red Sultan)",
    "dialogue_1": "Laughing at someone whom God has afflicted with misfortune is unbecoming of a man like you, who claims to be a world conqueror.",
    "dialogue_2": "No, I don't mean to mock you, I'm just laughing that God left this world to a blind person like you and a lame person like me.",
    "press_p": "Press P to resume",
    "in_range": "IN RANGE", "out_range": "OUT OF RANGE", "ready": "READY",
    "info_1": "RMB drag: Box select | LMB: Send | Click+F: Control | WASD: Move",
    "info_2": "SPACE: Start | P: Pause | [ ]: Speed | ESC: Menu",
}

LANG_TR = {
    "title": "SULTAN SAVASLARI", "subtitle": "Destansi Savas - Strateji ve Taktik",
    "army_settings": "ORDU AYARLARI", "soldiers": "Askerler", "commanders": "Komutanlar",
    "cannons": "Toplar", "normal_battle": "Normal Savas",
    "normal_desc": "Esit ordular - Sari vs Kirmizi", "wallachia": "Eflak Seferi",
    "wallachia_desc": "Sari daha kalabalik, Kirmizida top YOK",
    "ankara": "Ankara Savasi",
    "ankara_desc": "1402 - Bayezid vs Timur | Senaryolu + Sahne",
    "sandbox": "Serbest Mod", "exit": "CIKIS", "language": "Dil",
    "attack_order": "SALDIRI EMRI [SPACE]",
    "begin_ankara": "ANKARA SAVASINI BASLAT [SPACE]",
    "paused": "DURAKLATILDI", "battle": "SAVAS", "battle_ankara": "ANKARA SAVASI",
    "strategy_phase": "STRATEJI ASAMASI", "ankara_1402": "ANKARA - 1402",
    "yellow_team": "SARI TAKIM", "red_team": "KIRMIZI TAKIM",
    "bayezid_army": "BAYEZID'IN ORDUSU", "timur_army": "TIMUR'UN ORDUSU",
    "kills": "Oldurme", "sultan_hp": "Sultan HP", "total": "Toplam",
    "timur_in_tent": "Timur: Cadirda (bekliyor)", "controls": "KONTROLLER",
    "ctrl_box_select": "Sag surukleme: Sec", "ctrl_send": "Sol tik: Gonder",
    "ctrl_control": "Tik + F: Kontrol et", "ctrl_move": "WASD: Hareket",
    "ctrl_move_cannon": "WASD: Birim/top hareket", "ctrl_fire": "Sol tik: Top ates",
    "ctrl_pause": "P: Duraklat/Devam", "ctrl_start": "SPACE: Savasi baslat",
    "ctrl_attack": "SPACE: Saldiri emri", "ctrl_speed": "[ ]: Hiz",
    "ctrl_scroll": "Oklar: Kamera kaydir", "ctrl_focus": "TAB: Birime odaklan",
    "ctrl_menu": "ESC: Menu", "ctrl_cannon_crew": "Toplarin mustahkeme ihtiyaci var!",
    "ankara_info_1": "=== ANKARA 1402 ===", "ankara_info_2": "Bayezid savasiyor!",
    "ankara_info_3": "Timur cadirda bekliyor", "ankara_info_4": "10'a karsi 20 asker",
    "ankara_info_5": "Hikayeyi izle!",
    "units_selected": "birim secildi - Sol tik ile gonder",
    "click_unit": "Birime tikla, F=kontrol | Sag surukleme=sec",
    "press_f": "Kontrol icin F'ye bas", "ctrl_wasd": "KONTROL: WASD hareket, F birak",
    "hp": "HP", "atk": "SLD", "spd": "HIZ", "pos": "Konum",
    "minimap": "MINIHARITA", "play_again": "TEKRAR OYNA", "main_menu": "ANA MENU",
    "yellow_wins": "SARI TAKIM KAZANDI!", "red_wins": "KIRMIZI TAKIM KAZANDI!",
    "timur_wins": "TIMUR KAZANDI!", "ankara_title_vic": "Ankara Savasi - 1402",
    "bayezid_captured": "I. Bayezid esir alinip hapsedildi.",
    "interregnum": "Osmanli Devleti fetret devrine girdi.",
    "timur_kills": "Timur Oldurme", "bayezid_kills": "Bayezid Oldurme",
    "yellow_kills": "Sari Oldurme", "red_kills": "Kirmizi Oldurme",
    "no_crew": "MUSTERI YOK", "has_crew": "Musterisi var",
    "cannon_crew": "Top musterisi olarak atandi", "ctrl_label": "KNTRL",
    "sultan": "Sultan", "commander": "Komutan", "soldier": "Asker",
    "cannon": "Top", "yellow": "Sari", "red": "Kirmizi",
    "name_unit": "Biriminizi adlandirin:", "enter_confirm": "Enter: Onayla | Esc: Iptal",
    "name_selected": "N: Secili birime ad ver", "sandbox_title": "SERBEST MOD",
    "team": "Takim", "place_unit": "Birim Yerlestir:", "clear_y": "Sari Temizle",
    "clear_r": "Kirmizi Temizle", "clear_all": "Hepsini Temizle",
    "deselect": "Secimi Kaldir [X]", "prison": "HAPISHANE",
    "timur_tent": "TIMUR'UN CADIRI",
    "cutscene_alone": "ANKARA SAVASI - 1402 | Bayezid tek basina kaldi...",
    "cutscene_capture": "ANKARA SAVASI | Bayezid esir aliniyor!",
    "cutscene_escort": "ANKARA SAVASI | Timur'un cadirina goturuluyor...",
    "cutscene_throne": "ANKARA SAVASI | Fatih'in huzurunda...",
    "cutscene_dialogue1": "ANKARA SAVASI | Tarihi bir konusma...",
    "cutscene_dialogue2": "ANKARA SAVASI | Timur cevap veriyor...",
    "cutscene_prison": "ANKARA SAVASI | Sultan hapsediliyor...",
    "cutscene_default": "ANKARA SAVASI - 1402",
    "enter_skip": "ENTER: atla",
    "bayezid_imprisoned": "Bayezid hapsedildi...",
    "bayezid_speaker": "BAYEZID (Sari Sultan)",
    "timur_speaker": "TIMUR (Kirmizi Sultan)",
    "dialogue_1": "Talihsizlige ugrayan birine gulmek, dunya fatihi oldugunu iddia eden senin gibi bir adama yakismaz.",
    "dialogue_2": "Hayir, seninle alay etmiyorum. Sadece Allah'in bu dunyayi senin gibi bir kore ve benim gibi bir topala birakmasina guluyorum.",
    "press_p": "Devam icin P'ye bas",
    "in_range": "MENZILDE", "out_range": "MENZIL DISI", "ready": "HAZIR",
    "info_1": "Sag surukleme: Sec | Sol tik: Gonder | Tik+F: Kontrol | WASD: Hareket",
    "info_2": "SPACE: Baslat | P: Duraklat | [ ]: Hiz | ESC: Menu",
}

LANGUAGES = {"EN": LANG_EN, "TR": LANG_TR}
current_lang = "EN"


def T(key):
    return LANGUAGES.get(current_lang, LANG_EN).get(key, LANG_EN.get(key, key))


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
        if mx < 20:
            self.target_x -= self.edge_scroll_speed
        if mx > SCREEN_WIDTH - 20:
            self.target_x += self.edge_scroll_speed
        if my < 20:
            self.target_y -= self.edge_scroll_speed
        if my > SCREEN_HEIGHT - 20:
            self.target_y += self.edge_scroll_speed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.target_x -= self.edge_scroll_speed
        if keys[pygame.K_RIGHT]:
            self.target_x += self.edge_scroll_speed
        if keys[pygame.K_UP]:
            self.target_y -= self.edge_scroll_speed
        if keys[pygame.K_DOWN]:
            self.target_y += self.edge_scroll_speed
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
        if border_c:
            pygame.draw.polygon(surface, border_c, pts, border_w)
        hc = (min(255, color[0] + 70), min(255, color[1] + 70), min(255, color[2] + 70))
        ip = []
        for i in range(points * 2):
            a = rot + (i * math.pi / points) - math.pi / 2
            r2 = (outer_r if i % 2 == 0 else inner_r) * 0.4
            ip.append((center[0] + r2 * math.cos(a) - 1, center[1] + r2 * math.sin(a) - 1))
        if len(ip) >= 3:
            pygame.draw.polygon(surface, hc, ip)


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
    pygame.draw.line(surface, DARK_BROWN,
                     (int(gx + math.cos(perp) * 4), int(gy + math.sin(perp) * 4)),
                     (int(gx - math.cos(perp) * 4), int(gy - math.sin(perp) * 4)), 2)
    pygame.draw.line(surface, BROWN, (cx, cy),
                     (int(cx - math.cos(sa) * 4), int(cy - math.sin(sa) * 4)), 3)
    if abs(swing) > 0.3:
        pygame.draw.circle(surface, WHITE, (int(tip_x), int(tip_y)), 2)


def draw_tent_at(surface, ix, iy, frame, label=""):
    pygame.draw.ellipse(surface, (20, 30, 15, 80), (ix - 90, iy - 8, 180, 20))
    tent_h = 100
    tent_w = 85
    tent_pts = [(ix, iy - tent_h), (ix - tent_w, iy), (ix + tent_w, iy)]
    pygame.draw.polygon(surface, (150, 30, 30), tent_pts)
    pygame.draw.polygon(surface, (190, 45, 45), tent_pts, 3)
    pygame.draw.line(surface, GOLD, (ix, iy - tent_h), (ix, iy), 2)
    pygame.draw.line(surface, GOLD, (ix - 42, iy - 38), (ix + 42, iy - 38), 1)
    pygame.draw.line(surface, GOLD, (ix - 62, iy - 15), (ix + 62, iy - 15), 1)
    door_pts = [(ix - 16, iy), (ix, iy - 35), (ix + 16, iy)]
    pygame.draw.polygon(surface, (110, 20, 20), door_pts)
    fx = ix
    fy = iy - tent_h
    pygame.draw.line(surface, BROWN, (fx, fy), (fx, fy - 28), 2)
    fw = math.sin(frame * 0.05) * 6
    fp = [(fx, fy - 28), (fx + 22 + fw, fy - 22), (fx + 20 + fw, fy - 12), (fx, fy - 14)]
    pygame.draw.polygon(surface, BRIGHT_RED, fp)
    draw_star(surface, GOLD, (int(fx + 11 + fw), int(fy - 20)), 4, 2, 5, frame * 0.03)
    if label:
        try:
            f = pygame.font.SysFont("Arial", 12, bold=True)
            t = f.render(label, True, RED_LIGHT)
            surface.blit(t, (ix - t.get_width() // 2, iy - tent_h - 35))
        except:
            pass


def draw_prison_at(surface, ix, iy):
    pygame.draw.rect(surface, (55, 55, 55), (ix - 45, iy - 35, 90, 70))
    pygame.draw.rect(surface, (35, 35, 35), (ix - 45, iy - 35, 90, 70), 3)
    for i in range(-38, 42, 10):
        pygame.draw.line(surface, (130, 130, 130), (ix + i, iy - 35), (ix + i, iy + 35), 2)
    pygame.draw.line(surface, (130, 130, 130), (ix - 45, iy - 12), (ix + 45, iy - 12), 2)
    pygame.draw.line(surface, (130, 130, 130), (ix - 45, iy + 12), (ix + 45, iy + 12), 2)
    pygame.draw.circle(surface, (80, 80, 80), (ix + 45, iy), 7)
    pygame.draw.circle(surface, DARK_GOLD, (ix + 45, iy), 4)


class Tree:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.trunk_h = random.randint(15, 30)
        self.trunk_w = random.randint(4, 7)
        self.canopy_r = random.randint(14, 24)
        self.canopy_layers = random.randint(2, 4)
        self.sway = random.uniform(0, math.pi * 2)
        self.sway_speed = random.uniform(0.005, 0.015)
        self.leaf_color_base = (random.randint(25, 45), random.randint(90, 130), random.randint(20, 40))

    def draw(self, surface, cam, frame):
        if not cam.on_screen(self.x, self.y, 80):
            return
        sx, sy = cam.world_to_screen(self.x, self.y)
        sway = math.sin(frame * self.sway_speed + self.sway) * 2
        pygame.draw.ellipse(surface, (25, 50, 18, 100),
                            (sx - self.canopy_r, sy + 4, self.canopy_r * 2, self.canopy_r // 2))
        trunk_pts = [(sx - self.trunk_w // 2, sy), (sx - self.trunk_w // 2 - 1, sy - self.trunk_h),
                     (sx + self.trunk_w // 2 + 1, sy - self.trunk_h), (sx + self.trunk_w // 2, sy)]
        pygame.draw.polygon(surface, DARK_BROWN, trunk_pts)
        for i in range(self.canopy_layers):
            ly = sy - self.trunk_h + 5 - i * (self.canopy_r // self.canopy_layers)
            lr = self.canopy_r - i * 2
            lx = sx + int(sway * (i + 1) * 0.3)
            shade = i * 12
            lc = (self.leaf_color_base[0] + shade, self.leaf_color_base[1] + shade,
                  self.leaf_color_base[2] + shade)
            pygame.draw.circle(surface, lc, (lx, ly), lr)
            pygame.draw.circle(surface, (lc[0] - 15, lc[1] - 15, lc[2] - 10), (lx, ly), lr, 1)


class Cannonball:
    def __init__(self, x, y, tx, ty, team, damage):
        self.x, self.y = float(x), float(y)
        self.sx, self.sy = float(x), float(y)
        self.tx, self.ty = float(tx), float(ty)
        self.team = team
        self.damage = damage
        self.alive = True
        self.speed = 4.0
        self.splash = 55
        self.trail = []
        self.progress = 0.0
        self.total_d = max(1, dist((x, y), (tx, ty)))
        self.arc_h = min(180, self.total_d * 0.25)

    def update(self):
        if not self.alive:
            return
        self.progress += self.speed / self.total_d
        self.x = self.sx + (self.tx - self.sx) * self.progress
        base_y = self.sy + (self.ty - self.sy) * self.progress
        arc = -4 * self.arc_h * self.progress * (self.progress - 1)
        self.y = base_y - arc
        self.trail.append((self.x, self.y))
        if len(self.trail) > 20:
            self.trail.pop(0)
        if self.progress >= 1.0:
            self.alive = False

    def draw(self, surface, cam):
        if not self.alive:
            return
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
                if d <= self.splash:
                    t.append((e, 1.0 - d / self.splash * 0.5))
        return t


class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.life = 35
        self.max_life = 35
        self.alive = True
        self.parts = []
        for _ in range(25):
            a = random.uniform(0, math.pi * 2)
            s = random.uniform(1, 6)
            self.parts.append({
                'x': x, 'y': y, 'vx': math.cos(a) * s, 'vy': math.sin(a) * s,
                'size': random.uniform(2, 7),
                'color': random.choice([ORANGE, FIRE_RED, YELLOW, WHITE, SMOKE_COLOR])
            })

    def update(self):
        self.life -= 1
        if self.life <= 0:
            self.alive = False
        for p in self.parts:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vx'] *= 0.94
            p['vy'] *= 0.94

    def draw(self, surface, cam):
        if not cam.on_screen(self.x, self.y, 60):
            return
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
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.life = life
        self.max_life = life
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.alive = True

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.94
        self.vy *= 0.94
        self.life -= 1
        if self.life <= 0:
            self.alive = False

    def draw(self, surface, cam):
        if not self.alive:
            return
        sp = cam.world_to_screen(self.x, self.y)
        s = max(1, int(self.size * (self.life / self.max_life)))
        pygame.draw.circle(surface, self.color, sp, s)


class Waypoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pulse = 0
        self.life = 180

    def draw(self, surface, cam):
        self.pulse += 0.06
        self.life -= 1
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
        self.x = float(x)
        self.y = float(y)
        self.team = team
        self.unit_type = unit_type
        self.alive = True
        self.rotation = random.uniform(0, math.pi * 2)
        self.rot_spd = random.uniform(0.004, 0.01)
        self.target = None
        self.atk_cd = 0
        self.anim_t = 0
        self.hit_flash = 0
        self.vx = 0
        self.vy = 0
        self.facing = 0
        self.move_target = None
        self.group_id = 0
        self.selected = False
        self.player_controlled = False
        self.operating_cannon = None
        self.cannon_target_override = None
        self.custom_name = ""
        self.sword_swing = 0.0
        self.sword_swing_dir = 1
        self.frozen = False
        self.in_tent = False
        if unit_type == UnitType.SULTAN:
            self.hp = 800
            self.max_hp = 800
            self.attack = 30
            self.speed = 1.8
            self.atk_range = 55
            self.size = 28
            self.atk_spd = 45
            self.engage_r = 200
        elif unit_type == UnitType.COMMANDER:
            self.hp = 350
            self.max_hp = 350
            self.attack = 22
            self.speed = 0.65
            self.atk_range = 45
            self.size = 20
            self.atk_spd = 35
            self.engage_r = 350
        elif unit_type == UnitType.SOLDIER:
            self.hp = 120
            self.max_hp = 120
            self.attack = 12
            self.speed = 0.7
            self.atk_range = 30
            self.size = 10
            self.atk_spd = 30
            self.engage_r = 600
        elif unit_type == UnitType.CANNON:
            self.hp = 200
            self.max_hp = 200
            self.attack = 60
            self.speed = 0.3
            self.atk_range = 550
            self.size = 18
            self.atk_spd = 160
            self.engage_r = 550
            self.cannon_angle = math.pi if team == "red" else 0
            self.fire_anim = 0
            self.crew = None

    def has_crew(self):
        if self.unit_type != UnitType.CANNON:
            return True
        if self.crew and self.crew.alive:
            return dist((self.x, self.y), (self.crew.x, self.crew.y)) < 80
        return False

    def find_target(self, enemies):
        valid = [e for e in enemies if e.alive and not e.frozen and not e.in_tent]
        if not valid:
            return None
        if self.unit_type == UnitType.CANNON:
            if not self.has_crew():
                return None
            best = None
            bd = float('inf')
            for e in valid:
                d = dist((self.x, self.y), (e.x, e.y))
                if d <= self.atk_range and d < bd:
                    bd = d
                    best = e
            return best
        if self.unit_type == UnitType.SULTAN:
            best = None
            bd = float('inf')
            for e in valid:
                d = dist((self.x, self.y), (e.x, e.y))
                if d <= self.engage_r and d < bd:
                    bd = d
                    best = e
            return best
        cands = []
        for e in valid:
            d = dist((self.x, self.y), (e.x, e.y))
            if self.unit_type == UnitType.SOLDIER:
                p = {UnitType.SOLDIER: 0.7, UnitType.COMMANDER: 1.0, UnitType.CANNON: 1.1,
                     UnitType.SULTAN: 2.5}.get(e.unit_type, 1.0)
            elif self.unit_type == UnitType.COMMANDER:
                p = {UnitType.SOLDIER: 0.8, UnitType.COMMANDER: 0.7, UnitType.CANNON: 0.9,
                     UnitType.SULTAN: 1.8}.get(e.unit_type, 1.0)
            else:
                p = 1.0
            cands.append((d * p, e))
        if not cands:
            return None
        cands.sort(key=lambda c: c[0])
        return cands[0][1]

    def find_nearest_enemy(self, enemies):
        best = None
        bd = float('inf')
        for e in enemies:
            if e.alive and not e.frozen and not e.in_tent:
                d = dist((self.x, self.y), (e.x, e.y))
                if d < bd:
                    bd = d
                    best = e
        return best, bd

    def update(self, enemies, allies, cannonballs=None, obstacles=None, battle_started=True):
        if not self.alive or self.frozen or self.in_tent:
            return
        self.anim_t += 1
        self.rotation += self.rot_spd
        if self.hit_flash > 0:
            self.hit_flash -= 1
        if self.atk_cd > 0:
            self.atk_cd -= 1
        if self.unit_type in (UnitType.SOLDIER, UnitType.COMMANDER, UnitType.SULTAN):
            if self.atk_cd > self.atk_spd - 8:
                self.sword_swing += 0.25 * self.sword_swing_dir
                if abs(self.sword_swing) > 1.2:
                    self.sword_swing_dir *= -1
            else:
                self.sword_swing *= 0.85
                if abs(self.sword_swing) < 0.05:
                    self.sword_swing = 0

        if self.player_controlled and self.unit_type != UnitType.CANNON:
            keys = pygame.key.get_pressed()
            dx = dy = 0
            if keys[pygame.K_w]:
                dy = -self.speed
            if keys[pygame.K_s]:
                dy = self.speed
            if keys[pygame.K_a]:
                dx = -self.speed
            if keys[pygame.K_d]:
                dx = self.speed
            if dx != 0 and dy != 0:
                dx *= 0.707
                dy *= 0.707
            if dx != 0 or dy != 0:
                self.facing = math.atan2(dy, dx)
            self.x += dx
            self.y += dy
            self.x = clamp(self.x, 30, WORLD_WIDTH - 30)
            self.y = clamp(self.y, 30, WORLD_HEIGHT - 30)
            if battle_started:
                if self.target is None or not self.target.alive:
                    self.target = self.find_target(enemies)
                if self.target and self.target.alive:
                    self.facing = ang_to((self.x, self.y), (self.target.x, self.target.y))
                    d = dist((self.x, self.y), (self.target.x, self.target.y))
                    if d <= self.atk_range and self.atk_cd <= 0:
                        self.target.hp -= self.attack + random.randint(-3, 5)
                        self.target.hit_flash = 8
                        self.sword_swing_dir = random.choice([-1, 1])
                        if self.target.hp <= 0:
                            self.target.alive = False
                            self.target = None
                        self.atk_cd = self.atk_spd
            return

        if self.player_controlled and self.unit_type == UnitType.CANNON:
            if hasattr(self, 'fire_anim') and self.fire_anim > 0:
                self.fire_anim -= 1
            keys = pygame.key.get_pressed()
            dx = dy = 0
            if keys[pygame.K_w]:
                dy = -self.speed
            if keys[pygame.K_s]:
                dy = self.speed
            if keys[pygame.K_a]:
                dx = -self.speed
            if keys[pygame.K_d]:
                dx = self.speed
            if dx != 0 and dy != 0:
                dx *= 0.707
                dy *= 0.707
            self.x += dx
            self.y += dy
            self.x = clamp(self.x, 30, WORLD_WIDTH - 30)
            self.y = clamp(self.y, 30, WORLD_HEIGHT - 30)
            if not battle_started or not self.has_crew():
                return
            if self.cannon_target_override:
                tx, ty = self.cannon_target_override
                self.cannon_angle = ang_to((self.x, self.y), (tx, ty))
                if dist((self.x, self.y), (tx, ty)) <= self.atk_range and self.atk_cd <= 0:
                    if cannonballs is not None:
                        cannonballs.append(Cannonball(self.x, self.y,
                                                     tx + random.randint(-25, 25),
                                                     ty + random.randint(-25, 25),
                                                     self.team, self.attack))
                    self.atk_cd = self.atk_spd
                    self.fire_anim = 15
                    self.cannon_target_override = None
            return

        if self.unit_type == UnitType.CANNON:
            if hasattr(self, 'fire_anim') and self.fire_anim > 0:
                self.fire_anim -= 1
            if not battle_started or not self.has_crew():
                return
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
                    self.vx *= 0.85
                    self.vy *= 0.85
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
                        self.vx += math.cos(pa) * pf
                        self.vy += math.sin(pa) * pf
            self.vx *= 0.93
            self.vy *= 0.93
            self.x += self.vx
            self.y += self.vy
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
                    self.atk_cd = self.atk_spd
                    self.fire_anim = 15
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
                if spd > ms:
                    self.vx = (self.vx / spd) * ms
                    self.vy = (self.vy / spd) * ms
            else:
                self.vx *= 0.5
                self.vy *= 0.5
            self.vx *= 0.91
            self.vy *= 0.91
            self.x += self.vx
            self.y += self.vy
            self.x = clamp(self.x, 30, WORLD_WIDTH - 30)
            self.y = clamp(self.y, 30, WORLD_HEIGHT - 30)
            if battle_started:
                for e in enemies:
                    if e.alive and not e.frozen and not e.in_tent:
                        ed = dist((self.x, self.y), (e.x, e.y))
                        if ed < 50 and self.atk_cd <= 0:
                            self.facing = ang_to((self.x, self.y), (e.x, e.y))
                            if ed <= self.atk_range:
                                e.hp -= self.attack + random.randint(-3, 5)
                                e.hit_flash = 8
                                self.sword_swing_dir = random.choice([-1, 1])
                                if e.hp <= 0:
                                    e.alive = False
                                self.atk_cd = self.atk_spd
                            break
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
                    if spd > self.speed:
                        self.vx = (self.vx / spd) * self.speed
                        self.vy = (self.vy / spd) * self.speed
                else:
                    self.move_target = None
                    self.vx *= 0.5
                    self.vy *= 0.5
            for a2 in allies:
                if a2 is not self and a2.alive:
                    ad = dist((self.x, self.y), (a2.x, a2.y))
                    md = (self.size + a2.size) * 1.6
                    if ad < md and ad > 0:
                        pa = ang_to((a2.x, a2.y), (self.x, self.y))
                        pf = (md - ad) * 0.04
                        self.vx += math.cos(pa) * pf
                        self.vy += math.sin(pa) * pf
            self.vx *= 0.91
            self.vy *= 0.91
            self.x += self.vx
            self.y += self.vy
            self.x = clamp(self.x, 30, WORLD_WIDTH - 30)
            self.y = clamp(self.y, 30, WORLD_HEIGHT - 30)
            return

        if self.move_target:
            d = dist((self.x, self.y), self.move_target)
            if d > 30:
                a = ang_to((self.x, self.y), self.move_target)
                self.facing = a
                self.vx += math.cos(a) * self.speed * 0.1
                self.vy += math.sin(a) * self.speed * 0.1
                spd = math.sqrt(self.vx ** 2 + self.vy ** 2)
                if spd > self.speed:
                    self.vx = (self.vx / spd) * self.speed
                    self.vy = (self.vy / spd) * self.speed
                for e in enemies:
                    if e.alive and not e.frozen and not e.in_tent:
                        ed = dist((self.x, self.y), (e.x, e.y))
                        if ed < self.atk_range and self.atk_cd <= 0:
                            self.facing = ang_to((self.x, self.y), (e.x, e.y))
                            e.hp -= self.attack + random.randint(-3, 5)
                            e.hit_flash = 8
                            self.sword_swing_dir = random.choice([-1, 1])
                            if e.hp <= 0:
                                e.alive = False
                            self.atk_cd = self.atk_spd
                            break
            else:
                self.move_target = None
        else:
            if self.target is None or not self.target.alive:
                self.target = self.find_target(enemies)
            if self.target and self.target.alive:
                d = dist((self.x, self.y), (self.target.x, self.target.y))
                self.facing = ang_to((self.x, self.y), (self.target.x, self.target.y))
                if d <= self.atk_range:
                    self.vx *= 0.5
                    self.vy *= 0.5
                    if self.atk_cd <= 0:
                        self.target.hp -= self.attack + random.randint(-3, 5)
                        self.target.hit_flash = 8
                        self.sword_swing_dir = random.choice([-1, 1])
                        if self.target.hp <= 0:
                            self.target.alive = False
                            self.target = None
                        self.atk_cd = self.atk_spd
                else:
                    a = ang_to((self.x, self.y), (self.target.x, self.target.y))
                    self.vx += math.cos(a) * self.speed * 0.1
                    self.vy += math.sin(a) * self.speed * 0.1
                    spd = math.sqrt(self.vx ** 2 + self.vy ** 2)
                    if spd > self.speed:
                        self.vx = (self.vx / spd) * self.speed
                        self.vy = (self.vy / spd) * self.speed
            else:
                self.vx *= 0.9
                self.vy *= 0.9

        for a2 in allies:
            if a2 is not self and a2.alive:
                ad = dist((self.x, self.y), (a2.x, a2.y))
                md = (self.size + a2.size) * 1.5
                if ad < md and ad > 0:
                    pa = ang_to((a2.x, a2.y), (self.x, self.y))
                    pf = (md - ad) * 0.05
                    self.vx += math.cos(pa) * pf
                    self.vy += math.sin(pa) * pf
        self.vx *= 0.92
        self.vy *= 0.92
        self.x += self.vx
        self.y += self.vy
        self.x = clamp(self.x, 30, WORLD_WIDTH - 30)
        self.y = clamp(self.y, 30, WORLD_HEIGHT - 30)

    def draw(self, surface, cam):
        if not self.alive or self.in_tent:
            return
        if not cam.on_screen(self.x, self.y, 50):
            return
        sp = cam.world_to_screen(self.x, self.y)
        ix, iy = sp
        if self.selected:
            pygame.draw.circle(surface, (0, 220, 0), (ix, iy), self.size + 14, 2)
        if self.player_controlled:
            pulse = abs(math.sin(self.anim_t * 0.07)) * 4
            pygame.draw.circle(surface, MAGENTA, (ix, iy), int(self.size + 18 + pulse), 3)
            try:
                cf = pygame.font.SysFont("Arial", 10)
                ct = cf.render(T("ctrl_label"), True, MAGENTA)
                surface.blit(ct, (ix - ct.get_width() // 2, iy + self.size + 8))
            except:
                pass
        if self.unit_type == UnitType.CANNON:
            self._draw_cannon(surface, ix, iy)
            return
        if self.unit_type in (UnitType.SOLDIER, UnitType.COMMANDER, UnitType.SULTAN):
            sl = 14 if self.unit_type == UnitType.SOLDIER else (
                20 if self.unit_type == UnitType.COMMANDER else 24)
            sx2 = ix + math.cos(self.facing + 0.5) * (self.size * 0.6)
            sy2 = iy + math.sin(self.facing + 0.5) * (self.size * 0.6)
            if not self.frozen:
                draw_sword(surface, int(sx2), int(sy2), self.facing, sl, self.sword_swing)
        if self.unit_type == UnitType.SULTAN:
            mc = BRIGHT_GOLD if self.team == "gold" else BRIGHT_RED
            if self.hit_flash > 0:
                mc = WHITE
            bc = DARK_GOLD if self.team == "gold" else DARK_RED
            gc = YELLOW if self.team == "gold" else RED
            draw_glow(surface, gc, (ix, iy), self.size + 10, 7)
            cp = math.sin(self.anim_t * 0.04) * 3
            pygame.draw.circle(surface, gc, (ix, iy), int(self.size + 15 + cp), 2)
            draw_star(surface, mc, (ix, iy), self.size, self.size * 0.45, 5, self.rotation, bc, 3, True)
            if self.frozen:
                pygame.draw.circle(surface, (150, 150, 255), (ix, iy), self.size + 8, 2)
        elif self.unit_type == UnitType.COMMANDER:
            if self.team == "gold":
                mc = BRIGHT_GREEN if self.hit_flash == 0 else WHITE
                bc = DARK_GREEN
                gc = GREEN
            else:
                mc = CRIMSON if self.hit_flash == 0 else WHITE
                bc = DARK_RED
                gc = RED
            draw_glow(surface, gc, (ix, iy), self.size + 5, 4)
            pygame.draw.circle(surface, gc, (ix, iy), self.size + 8, 2)
            draw_star(surface, mc, (ix, iy), self.size, self.size * 0.4, 5, self.rotation, bc, 2, True)
        else:
            if self.team == "gold":
                mc = BRIGHT_GOLD if self.hit_flash == 0 else WHITE
                bc = DARK_GOLD
                gc = YELLOW
            else:
                mc = BRIGHT_RED if self.hit_flash == 0 else WHITE
                bc = DARK_RED
                gc = RED
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
            except:
                pass
        if self.atk_cd > self.atk_spd - 5 and self.target and self.target.alive:
            ac = YELLOW if self.team == "gold" else RED_LIGHT
            tp = cam.world_to_screen(self.target.x, self.target.y)
            pygame.draw.line(surface, ac, (ix, iy), tp, 1)

    def _draw_cannon(self, surface, ix, iy):
        bc2 = (170, 150, 55) if self.team == "gold" else (150, 45, 45)
        if self.hit_flash > 0:
            bc2 = WHITE
        has_crew = self.has_crew()
        pygame.draw.ellipse(surface, (20, 35, 12), (ix - 20, iy + 10, 40, 12))
        pygame.draw.circle(surface, DARK_BROWN, (ix - 12, iy + 5), 8)
        pygame.draw.circle(surface, DARK_BROWN, (ix + 12, iy + 5), 8)
        pygame.draw.circle(surface, BROWN, (ix - 12, iy + 5), 4)
        pygame.draw.circle(surface, BROWN, (ix + 12, iy + 5), 4)
        pygame.draw.rect(surface, bc2, (ix - 14, iy - 8, 28, 16), border_radius=3)
        ca = self.cannon_angle if hasattr(self, 'cannon_angle') else 0
        bx = ix + math.cos(ca) * 25
        by = iy + math.sin(ca) * 25
        pygame.draw.line(surface, CANNON_GRAY, (ix, iy), (int(bx), int(by)), 6)
        pygame.draw.circle(surface, CANNON_GRAY, (int(bx), int(by)), 4)
        if not has_crew:
            try:
                cf = pygame.font.SysFont("Arial", 10)
                ct = cf.render(T("no_crew"), True, RED)
                surface.blit(ct, (ix - ct.get_width() // 2, iy - 32))
            except:
                pass
            pygame.draw.line(surface, RED, (ix - 15, iy - 15), (ix + 15, iy + 15), 2)
            pygame.draw.line(surface, RED, (ix + 15, iy - 15), (ix - 15, iy + 15), 2)
        if self.player_controlled:
            range_surf = pygame.Surface((self.atk_range * 2 + 4, self.atk_range * 2 + 4), pygame.SRCALPHA)
            pygame.draw.circle(range_surf, (255, 255, 0, 25),
                               (self.atk_range + 2, self.atk_range + 2), self.atk_range, 1)
            surface.blit(range_surf, (ix - self.atk_range - 2, iy - self.atk_range - 2))
        fa = self.fire_anim if hasattr(self, 'fire_anim') else 0
        if fa > 10:
            fs = (fa - 10) * 4
            pygame.draw.circle(surface, YELLOW, (int(bx), int(by)), fs)
            pygame.draw.circle(surface, ORANGE, (int(bx), int(by)), fs + 3)
            for _ in range(3):
                sx2 = bx + random.randint(-10, 10)
                sy2 = by + random.randint(-10, 10)
                pygame.draw.circle(surface, SMOKE_COLOR, (int(sx2), int(sy2)), random.randint(3, 7))
        elif fa > 0:
            for _ in range(2):
                sx2 = bx + random.randint(-12, 12)
                sy2 = by + random.randint(-15, 5)
                pygame.draw.circle(surface, SMOKE_COLOR, (int(sx2), int(sy2)), random.randint(3, 8))
        draw_hp_bar(surface, (ix, iy), self.hp, self.max_hp, w=36, h=4)
        if self.custom_name:
            try:
                nf = pygame.font.SysFont("Arial", 10)
                nt = nf.render(self.custom_name, True, WHITE)
                surface.blit(nt, (ix - nt.get_width() // 2, iy - 38))
            except:
                pass


class GameMap:
    def __init__(self, map_type="normal"):
        self.map_type = map_type
        self.trees = []
        self.ground_details = []
        self.generate()

    def generate(self):
        self.trees.clear()
        self.ground_details.clear()
        if self.map_type == "normal":
            for _ in range(200):
                x = random.randint(100, WORLD_WIDTH - 100)
                y = random.randint(100, WORLD_HEIGHT - 100)
                if abs(x - WORLD_WIDTH // 2) > 400 or abs(y - WORLD_HEIGHT // 2) > 500:
                    self.trees.append(Tree(x, y))
        elif self.map_type == "eflak":
            for _ in range(350):
                self.trees.append(
                    Tree(random.randint(50, WORLD_WIDTH - 50), random.randint(50, WORLD_HEIGHT - 50)))
        elif self.map_type == "sandbox":
            for _ in range(150):
                self.trees.append(
                    Tree(random.randint(100, WORLD_WIDTH - 100), random.randint(100, WORLD_HEIGHT - 100)))
        elif self.map_type == "ankara":
            for _ in range(60):
                x = random.randint(100, WORLD_WIDTH - 100)
                y = random.randint(100, WORLD_HEIGHT - 100)
                if abs(x - WORLD_WIDTH // 2) > 800:
                    self.trees.append(Tree(x, y))
        for _ in range(500):
            x = random.randint(0, WORLD_WIDTH)
            y = random.randint(0, WORLD_HEIGHT)
            if self.map_type == "ankara":
                c = random.choice(
                    [(130, 125, 60), (120, 115, 50), (140, 130, 65), (110, 105, 45)])
            else:
                c = random.choice(
                    [(70, 130, 45), (55, 115, 35), (80, 140, 55), (65, 120, 40)])
            self.ground_details.append((x, y, c, random.randint(8, 25)))

    def draw(self, surface, cam, frame):
        if self.map_type == "eflak":
            surface.fill((35, 75, 30))
        elif self.map_type == "sandbox":
            surface.fill((50, 100, 40))
        elif self.map_type == "ankara":
            surface.fill((110, 105, 60))
        else:
            surface.fill((45, 95, 35))
        for gx, gy, gc, gs in self.ground_details:
            if cam.on_screen(gx, gy, gs + 5):
                pygame.draw.circle(surface, gc, cam.world_to_screen(gx, gy), gs)
        if self.map_type == "normal":
            rx = WORLD_WIDTH // 2
            for y in range(0, WORLD_HEIGHT, 3):
                if cam.on_screen(rx, y, 50):
                    w = math.sin(y * 0.015 + frame * 0.02) * 20
                    wd = 30 + int(math.sin(y * 0.008) * 12)
                    sp = cam.world_to_screen(int(rx + w) - wd, y)
                    pygame.draw.rect(surface, WATER_BLUE, (sp[0], sp[1], wd * 2, 3))
        if self.map_type == "ankara":
            for i in range(8):
                dx2 = int(math.sin(frame * 0.002 + i * 2.1) * 400) + WORLD_WIDTH // 2
                dy2 = 300 + i * 700
                if cam.on_screen(dx2, dy2, 300):
                    sp = cam.world_to_screen(dx2, dy2)
                    ds = pygame.Surface((500, 100), pygame.SRCALPHA)
                    alpha = int(10 + math.sin(frame * 0.004 + i) * 6)
                    pygame.draw.ellipse(ds, (190, 175, 130, alpha), (0, 0, 500, 100))
                    surface.blit(ds, (sp[0] - 250, sp[1] - 50))
        for tree in self.trees:
            tree.draw(surface, cam, frame)


class AnkaraCutscenePhase(Enum):
    BATTLE = 0
    SULTAN_ALONE = 1
    SOLDIERS_APPROACH = 2
    ESCORT_TO_TENT = 3
    TENT_SCENE = 4
    DIALOGUE_1 = 5
    DIALOGUE_2 = 6
    PRISON = 7
    VICTORY = 8


class AnkaraCutscene:
    def __init__(self):
        self.phase = AnkaraCutscenePhase.BATTLE
        self.phase_timer = 0
        self.escort_soldiers = []
        self.tent_x = 0
        self.tent_y = 0
        self.gold_sultan = None
        self.red_sultan = None
        self.red_commander = None
        self.dialogue_text = ""
        self.dialogue_speaker = ""
        self.dialogue_char_index = 0
        self.dialogue_speed = 2
        self.dialogue_full_text = ""
        self.prison_x = 0
        self.prison_y = 0
        self.fade_alpha = 0
        self.cutscene_active = False
        self.skip_available = False

    def start_cutscene(self, gold_sultan, red_sultan, red_units, tent_x, tent_y):
        self.cutscene_active = True
        self.gold_sultan = gold_sultan
        self.red_sultan = red_sultan
        self.tent_x = tent_x
        self.tent_y = tent_y
        self.prison_x = tent_x + 200
        self.prison_y = tent_y + 50
        self.phase = AnkaraCutscenePhase.SULTAN_ALONE
        self.phase_timer = 0
        gold_sultan.frozen = True
        gold_sultan.target = None
        gold_sultan.vx = 0
        gold_sultan.vy = 0
        for u in red_units:
            if u.alive and u is not red_sultan:
                u.frozen = True
                u.target = None
                u.vx = 0
                u.vy = 0
        soldiers = [u for u in red_units if u.alive and u.unit_type == UnitType.SOLDIER]
        soldiers.sort(key=lambda s: dist((s.x, s.y), (gold_sultan.x, gold_sultan.y)))
        self.escort_soldiers = soldiers[:2]
        for s in self.escort_soldiers:
            s.frozen = False
        commanders = [u for u in red_units if u.alive and u.unit_type == UnitType.COMMANDER]
        self.red_commander = commanders[0] if commanders else None

    def update(self, cam, frame):
        if not self.cutscene_active:
            return False
        self.phase_timer += 1
        if self.phase == AnkaraCutscenePhase.SULTAN_ALONE:
            cam.update((self.gold_sultan.x, self.gold_sultan.y))
            if self.phase_timer > 150:
                self.phase = AnkaraCutscenePhase.SOLDIERS_APPROACH
                self.phase_timer = 0
        elif self.phase == AnkaraCutscenePhase.SOLDIERS_APPROACH:
            cam.update((self.gold_sultan.x, self.gold_sultan.y))
            all_arrived = True
            for i, s in enumerate(self.escort_soldiers):
                if not s.alive:
                    continue
                off_a = math.pi / 2 if i == 0 else -math.pi / 2
                tx = self.gold_sultan.x + math.cos(off_a) * 40
                ty = self.gold_sultan.y + math.sin(off_a) * 40
                d = dist((s.x, s.y), (tx, ty))
                if d > 12:
                    a = ang_to((s.x, s.y), (tx, ty))
                    s.x += math.cos(a) * 1.5
                    s.y += math.sin(a) * 1.5
                    s.facing = a
                    all_arrived = False
                else:
                    s.facing = ang_to((s.x, s.y), (self.gold_sultan.x, self.gold_sultan.y))
            if all_arrived and self.phase_timer > 80:
                self.phase = AnkaraCutscenePhase.ESCORT_TO_TENT
                self.phase_timer = 0
        elif self.phase == AnkaraCutscenePhase.ESCORT_TO_TENT:
            cam.update((self.gold_sultan.x, self.gold_sultan.y))
            d = dist((self.gold_sultan.x, self.gold_sultan.y), (self.tent_x, self.tent_y))
            if d > 50:
                a = ang_to((self.gold_sultan.x, self.gold_sultan.y), (self.tent_x, self.tent_y))
                self.gold_sultan.frozen = False
                self.gold_sultan.x += math.cos(a) * 1.2
                self.gold_sultan.y += math.sin(a) * 1.2
                self.gold_sultan.facing = a
                self.gold_sultan.anim_t += 1
                self.gold_sultan.rotation += self.gold_sultan.rot_spd
                for i, s in enumerate(self.escort_soldiers):
                    if not s.alive:
                        continue
                    off_a = math.pi / 2 if i == 0 else -math.pi / 2
                    ex = self.gold_sultan.x + math.cos(off_a) * 40
                    ey = self.gold_sultan.y + math.sin(off_a) * 40
                    if dist((s.x, s.y), (ex, ey)) > 8:
                        ea = ang_to((s.x, s.y), (ex, ey))
                        s.x += math.cos(ea) * 1.3
                        s.y += math.sin(ea) * 1.3
                        s.facing = a
                    s.anim_t += 1
                    s.rotation += s.rot_spd
            else:
                self.gold_sultan.frozen = True
                self.gold_sultan.vx = 0
                self.gold_sultan.vy = 0
                for s in self.escort_soldiers:
                    s.frozen = True
                self.phase = AnkaraCutscenePhase.TENT_SCENE
                self.phase_timer = 0
        elif self.phase == AnkaraCutscenePhase.TENT_SCENE:
            cam.update((self.tent_x, self.tent_y))
            self.gold_sultan.x = self.tent_x + 70
            self.gold_sultan.y = self.tent_y
            self.gold_sultan.facing = math.pi
            self.gold_sultan.anim_t += 1
            self.gold_sultan.rotation += self.gold_sultan.rot_spd
            self.red_sultan.facing = 0
            self.red_sultan.anim_t += 1
            self.red_sultan.rotation += self.red_sultan.rot_spd
            if self.red_commander and self.red_commander.alive:
                self.red_commander.x = self.tent_x - 90
                self.red_commander.y = self.tent_y - 50
                self.red_commander.facing = 0
                self.red_commander.anim_t += 1
            for i, s in enumerate(self.escort_soldiers):
                if not s.alive:
                    continue
                s.x = self.tent_x + 30 + i * 35
                s.y = self.tent_y + 40
                s.facing = -math.pi / 2
                s.anim_t += 1
            if self.phase_timer > 120:
                self.phase = AnkaraCutscenePhase.DIALOGUE_1
                self.phase_timer = 0
                self.dialogue_full_text = T("dialogue_1")
                self.dialogue_speaker = T("bayezid_speaker")
                self.dialogue_char_index = 0
                self.dialogue_text = ""
        elif self.phase == AnkaraCutscenePhase.DIALOGUE_1:
            cam.update((self.tent_x, self.tent_y))
            self.gold_sultan.anim_t += 1
            self.gold_sultan.rotation += self.gold_sultan.rot_spd
            self.red_sultan.anim_t += 1
            self.red_sultan.rotation += self.red_sultan.rot_spd
            if self.phase_timer % self.dialogue_speed == 0:
                if self.dialogue_char_index < len(self.dialogue_full_text):
                    self.dialogue_char_index += 1
                    self.dialogue_text = self.dialogue_full_text[:self.dialogue_char_index]
            self.skip_available = True
            if self.dialogue_char_index >= len(self.dialogue_full_text) and \
                    self.phase_timer > len(self.dialogue_full_text) * self.dialogue_speed + 300:
                self._go_dialogue2()
        elif self.phase == AnkaraCutscenePhase.DIALOGUE_2:
            cam.update((self.tent_x, self.tent_y))
            self.gold_sultan.anim_t += 1
            self.gold_sultan.rotation += self.gold_sultan.rot_spd
            self.red_sultan.anim_t += 1
            self.red_sultan.rotation += self.red_sultan.rot_spd
            if self.phase_timer % self.dialogue_speed == 0:
                if self.dialogue_char_index < len(self.dialogue_full_text):
                    self.dialogue_char_index += 1
                    self.dialogue_text = self.dialogue_full_text[:self.dialogue_char_index]
            self.skip_available = True
            if self.dialogue_char_index >= len(self.dialogue_full_text) and \
                    self.phase_timer > len(self.dialogue_full_text) * self.dialogue_speed + 300:
                self.phase = AnkaraCutscenePhase.PRISON
                self.phase_timer = 0
                self.dialogue_text = ""
                self.dialogue_speaker = ""
                self.skip_available = False
                for s in self.escort_soldiers:
                    if s.alive:
                        s.frozen = False
        elif self.phase == AnkaraCutscenePhase.PRISON:
            cam.update((self.gold_sultan.x, self.gold_sultan.y))
            pd = dist((self.gold_sultan.x, self.gold_sultan.y), (self.prison_x, self.prison_y))
            if pd > 25:
                self.gold_sultan.frozen = False
                a = ang_to((self.gold_sultan.x, self.gold_sultan.y), (self.prison_x, self.prison_y))
                self.gold_sultan.x += math.cos(a) * 1.0
                self.gold_sultan.y += math.sin(a) * 1.0
                self.gold_sultan.facing = a
                self.gold_sultan.anim_t += 1
                self.gold_sultan.rotation += self.gold_sultan.rot_spd
                for i, s in enumerate(self.escort_soldiers):
                    if not s.alive:
                        continue
                    off_a = math.pi / 2 if i == 0 else -math.pi / 2
                    ex = self.gold_sultan.x + math.cos(off_a) * 35
                    ey = self.gold_sultan.y + math.sin(off_a) * 35
                    ea = ang_to((s.x, s.y), (ex, ey))
                    s.x += math.cos(ea) * 1.1
                    s.y += math.sin(ea) * 1.1
                    s.facing = a
                    s.anim_t += 1
            else:
                self.gold_sultan.frozen = True
                for s in self.escort_soldiers:
                    if s.alive:
                        s.frozen = True
                self.fade_alpha = min(255, self.fade_alpha + 2)
                if self.fade_alpha >= 255 and self.phase_timer > 240:
                    self.phase = AnkaraCutscenePhase.VICTORY
                    self.phase_timer = 0
        elif self.phase == AnkaraCutscenePhase.VICTORY:
            return True
        return False

    def _go_dialogue2(self):
        self.phase = AnkaraCutscenePhase.DIALOGUE_2
        self.phase_timer = 0
        self.dialogue_full_text = T("dialogue_2")
        self.dialogue_speaker = T("timur_speaker")
        self.dialogue_char_index = 0
        self.dialogue_text = ""

    def draw(self, surface, cam, frame):
        if not self.cutscene_active:
            return
        self._draw_banner(surface, frame)
        if self.phase in (AnkaraCutscenePhase.DIALOGUE_1, AnkaraCutscenePhase.DIALOGUE_2):
            self._draw_dialogue(surface, frame)
        if self.fade_alpha > 0:
            fs = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            pygame.draw.rect(fs, (0, 0, 0, self.fade_alpha), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            surface.blit(fs, (0, 0))
            if self.fade_alpha > 200:
                try:
                    f = pygame.font.SysFont("Arial", 36, bold=True)
                    t = f.render(T("bayezid_imprisoned"), True, (200, 200, 200))
                    surface.blit(t, t.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
                except:
                    pass

    def _draw_banner(self, surface, frame):
        bh = 52
        bs = pygame.Surface((SCREEN_WIDTH, bh), pygame.SRCALPHA)
        pygame.draw.rect(bs, (0, 0, 0, 200), (0, 0, SCREEN_WIDTH, bh))
        surface.blit(bs, (0, 0))
        phase_keys = {
            AnkaraCutscenePhase.SULTAN_ALONE: "cutscene_alone",
            AnkaraCutscenePhase.SOLDIERS_APPROACH: "cutscene_capture",
            AnkaraCutscenePhase.ESCORT_TO_TENT: "cutscene_escort",
            AnkaraCutscenePhase.TENT_SCENE: "cutscene_throne",
            AnkaraCutscenePhase.DIALOGUE_1: "cutscene_dialogue1",
            AnkaraCutscenePhase.DIALOGUE_2: "cutscene_dialogue2",
            AnkaraCutscenePhase.PRISON: "cutscene_prison"
        }
        text = T(phase_keys.get(self.phase, "cutscene_default"))
        p = abs(math.sin(frame * 0.03))
        col = (255, int(180 + p * 55), int(80 + p * 120))
        try:
            f = pygame.font.SysFont("Arial", 21, bold=True)
            t = f.render(text, True, col)
            surface.blit(t, t.get_rect(center=(SCREEN_WIDTH // 2, 26)))
        except:
            pass
        if self.skip_available:
            try:
                sf = pygame.font.SysFont("Arial", 13)
                st = sf.render(T("enter_skip"), True, LIGHT_GRAY)
                surface.blit(st, (SCREEN_WIDTH - st.get_width() - 15, 34))
            except:
                pass

    def _draw_dialogue(self, surface, frame):
        dw = min(900, SCREEN_WIDTH - 100)
        dh = 160
        dx = SCREEN_WIDTH // 2 - dw // 2
        dy = SCREEN_HEIGHT - dh - 30
        ds = pygame.Surface((dw, dh), pygame.SRCALPHA)
        pygame.draw.rect(ds, (10, 10, 25, 230), (0, 0, dw, dh), border_radius=12)
        if self.phase == AnkaraCutscenePhase.DIALOGUE_1:
            bc = BRIGHT_GOLD
            sc = GOLD
            pc = BRIGHT_GOLD
            sdc = DARK_GOLD
        else:
            bc = BRIGHT_RED
            sc = RED
            pc = BRIGHT_RED
            sdc = DARK_RED
        pygame.draw.rect(ds, bc, (0, 0, dw, dh), 3, border_radius=12)
        surface.blit(ds, (dx, dy))
        px2 = dx + 55
        py2 = dy + dh // 2
        pygame.draw.circle(surface, (20, 20, 30), (px2, py2), 38)
        pygame.draw.circle(surface, bc, (px2, py2), 38, 3)
        sr = frame * 0.02 if self.phase == AnkaraCutscenePhase.DIALOGUE_1 else -frame * 0.02
        draw_star(surface, pc, (px2, py2), 25, 11, 5, sr, sdc, 2, True)
        try:
            nf = pygame.font.SysFont("Arial", 18, bold=True)
            nt = nf.render(self.dialogue_speaker, True, sc)
            surface.blit(nt, (dx + 105, dy + 12))
        except:
            pass
        try:
            tf = pygame.font.SysFont("Arial", 16)
            words = self.dialogue_text.split(' ')
            lines = []
            current_line = ""
            max_w = dw - 130
            for word in words:
                test_line = current_line + (" " if current_line else "") + word
                if tf.size(test_line)[0] > max_w and current_line:
                    lines.append(current_line)
                    current_line = word
                else:
                    current_line = test_line
            if current_line:
                lines.append(current_line)
            for i, line in enumerate(lines):
                surface.blit(tf.render(line, True, WHITE), (dx + 105, dy + 38 + i * 22))
            if self.dialogue_char_index < len(self.dialogue_full_text) and (frame // 15) % 2 == 0:
                if lines:
                    lw = tf.size(lines[-1])[0]
                    surface.blit(tf.render("|", True, WHITE),
                                 (dx + 105 + lw + 2, dy + 38 + (len(lines) - 1) * 22))
        except:
            pass

    def skip_dialogue(self):
        if self.phase == AnkaraCutscenePhase.DIALOGUE_1:
            if self.dialogue_char_index < len(self.dialogue_full_text):
                self.dialogue_char_index = len(self.dialogue_full_text)
                self.dialogue_text = self.dialogue_full_text
            else:
                self._go_dialogue2()
        elif self.phase == AnkaraCutscenePhase.DIALOGUE_2:
            if self.dialogue_char_index < len(self.dialogue_full_text):
                self.dialogue_char_index = len(self.dialogue_full_text)
                self.dialogue_text = self.dialogue_full_text
            else:
                self.phase = AnkaraCutscenePhase.PRISON
                self.phase_timer = 0
                self.dialogue_text = ""
                self.dialogue_speaker = ""
                self.skip_available = False
                for s in self.escort_soldiers:
                    if s.alive:
                        s.frozen = False


class Game:
    def __init__(self):
        self.state = "MENU"
        self.camera = Camera()
        self.game_map = GameMap()
        self.gold_units = []
        self.red_units = []
        self.cannonballs = []
        self.explosions = []
        self.particles = []
        self.waypoints = []
        self.battle_started = False
        self.battle_paused = False
        self.winner = None
        self.frame = 0
        self.cam_shake = 0
        self.kills_gold = 0
        self.kills_red = 0
        self.map_mode = "normal"
        self.soldier_count = 25
        self.commander_count = 3
        self.cannon_count = 3
        self.menu_btns = []
        self.atk_btn = None
        self.vic_btns = []
        self.sandbox_mode = False
        self.sandbox_placing = None
        self.sandbox_team = "gold"
        self.clicked_unit = None
        self.controlled_unit = None
        self.box_selecting = False
        self.box_start = None
        self.box_end = None
        self.box_selected_units = []
        self.naming_mode = False
        self.naming_unit = None
        self.naming_text = ""
        self.speed_options = [0.25, 0.5, 1.0, 2.0, 3.0, 5.0]
        self.battle_speed = 1.0
        self.speed_accumulator = 0.0
        self.speed_btn_rects = []
        self.ankara_mode = False
        self.ankara_cutscene = AnkaraCutscene()
        self.ankara_cutscene_triggered = False
        self.ankara_tent_x = 0
        self.ankara_tent_y = 0
        self.lang_btn_rects = []
        try:
            self.f_title = pygame.font.SysFont("Arial", 56, bold=True)
            self.f_large = pygame.font.SysFont("Arial", 36, bold=True)
            self.f_med = pygame.font.SysFont("Arial", 24, bold=True)
            self.f_small = pygame.font.SysFont("Arial", 17)
            self.f_tiny = pygame.font.SysFont("Arial", 14)
            self.f_mini = pygame.font.SysFont("Arial", 11)
        except:
            self.f_title = pygame.font.Font(None, 56)
            self.f_large = pygame.font.Font(None, 36)
            self.f_med = pygame.font.Font(None, 24)
            self.f_small = pygame.font.Font(None, 17)
            self.f_tiny = pygame.font.Font(None, 14)
            self.f_mini = pygame.font.Font(None, 11)

    def full_reset(self):
        self.gold_units.clear()
        self.red_units.clear()
        self.cannonballs.clear()
        self.explosions.clear()
        self.particles.clear()
        self.waypoints.clear()
        self.battle_started = False
        self.battle_paused = False
        self.winner = None
        self.kills_gold = 0
        self.kills_red = 0
        self.clicked_unit = None
        self.controlled_unit = None
        self.box_selected_units = []
        self.box_selecting = False
        self.box_start = None
        self.box_end = None
        self.naming_mode = False
        self.naming_unit = None
        self.naming_text = ""
        self.battle_speed = 1.0
        self.speed_accumulator = 0.0
        self.ankara_cutscene = AnkaraCutscene()
        self.ankara_cutscene_triggered = False
        self.ankara_mode = False
        self.sandbox_mode = False
        self.sandbox_placing = None
        self.atk_btn = None
        self.vic_btns = []
        self.camera = Camera()

    def go_to_menu(self):
        self.full_reset()
        self.state = "MENU"

    def cycle_speed_up(self):
        for i, s in enumerate(self.speed_options):
            if abs(s - self.battle_speed) < 0.01:
                if i < len(self.speed_options) - 1:
                    self.battle_speed = self.speed_options[i + 1]
                return

    def cycle_speed_down(self):
        for i, s in enumerate(self.speed_options):
            if abs(s - self.battle_speed) < 0.01:
                if i > 0:
                    self.battle_speed = self.speed_options[i - 1]
                return

    def set_speed(self, speed):
        self.battle_speed = speed

    def assign_cannon_crews(self, units):
        cannons = [u for u in units if u.unit_type == UnitType.CANNON and u.alive]
        available = [u for u in units if
                     u.unit_type == UnitType.SOLDIER and u.alive and u.operating_cannon is None]
        for cannon in cannons:
            if cannon.crew and cannon.crew.alive:
                continue
            cannon.crew = None
            if available:
                best = min(available, key=lambda s: dist((s.x, s.y), (cannon.x, cannon.y)))
                cannon.crew = best
                best.operating_cannon = cannon
                available.remove(best)

    def setup_armies(self):
        self.gold_units.clear()
        self.red_units.clear()
        self.cannonballs.clear()
        self.explosions.clear()
        self.particles.clear()
        self.waypoints.clear()
        self.battle_started = False
        self.battle_paused = False
        self.winner = None
        self.kills_gold = 0
        self.kills_red = 0
        self.clicked_unit = None
        self.controlled_unit = None
        self.box_selected_units = []
        self.naming_mode = False
        self.battle_speed = 1.0
        self.speed_accumulator = 0.0
        self.ankara_cutscene = AnkaraCutscene()
        self.ankara_cutscene_triggered = False
        if self.sandbox_mode:
            return
        mx = WORLD_WIDTH // 2
        my = WORLD_HEIGHT // 2
        left_base = mx - 1200
        right_base = mx + 1200
        if self.ankara_mode:
            self.ankara_tent_x = right_base + 400
            self.ankara_tent_y = my
            p = Unit(left_base, my, "gold", UnitType.SULTAN)
            p.custom_name = "Bayezid I"
            p.engage_r = 800
            p.speed = 1.5
            self.gold_units.append(p)
            for i in range(2):
                self.gold_units.append(
                    Unit(left_base + 150, my - 120 + i * 240, "gold", UnitType.COMMANDER))
            for i in range(10):
                r = i // 5
                c = i % 5
                self.gold_units.append(
                    Unit(left_base + 300 + r * 45, my - 160 + c * 75, "gold", UnitType.SOLDIER))
            rs = Unit(self.ankara_tent_x - 60, self.ankara_tent_y, "red", UnitType.SULTAN)
            rs.custom_name = "Timur"
            rs.frozen = True
            rs.in_tent = True
            self.red_units.append(rs)
            for i in range(3):
                self.red_units.append(
                    Unit(right_base - 150, my - 200 + i * 133, "red", UnitType.COMMANDER))
            for i in range(20):
                r = i // 5
                c = i % 5
                self.red_units.append(
                    Unit(right_base - 300 - r * 45, my - 200 + c * 90, "red", UnitType.SOLDIER))
        elif self.map_mode == "eflak":
            sc = self.soldier_count
            cc = self.commander_count
            tc = self.cannon_count
            gold_sc = int(sc * 1.5)
            gold_cc = cc + 2
            gold_tc = tc + 1
            red_sc = sc
            red_cc = cc
            self.gold_units.append(Unit(left_base, my, "gold", UnitType.SULTAN))
            for i in range(gold_tc):
                self.gold_units.append(
                    Unit(left_base + 80, my - 400 + i * (800 // max(1, gold_tc)), "gold", UnitType.CANNON))
            for i in range(gold_cc):
                self.gold_units.append(
                    Unit(left_base + 200, my - 300 + i * (600 // max(1, gold_cc)), "gold",
                         UnitType.COMMANDER))
            for i in range(gold_sc):
                r = i // 6
                c = i % 6
                self.gold_units.append(
                    Unit(left_base + 350 + r * 40, my - 200 + c * 72, "gold", UnitType.SOLDIER))
            self.red_units.append(Unit(right_base, my, "red", UnitType.SULTAN))
            for i in range(red_cc):
                self.red_units.append(
                    Unit(right_base - 200, my - 300 + i * (600 // max(1, red_cc)), "red",
                         UnitType.COMMANDER))
            for i in range(red_sc):
                r = i // 6
                c = i % 6
                self.red_units.append(
                    Unit(right_base - 350 - r * 40, my - 200 + c * 72, "red", UnitType.SOLDIER))
        else:
            sc = self.soldier_count
            cc = self.commander_count
            tc = self.cannon_count
            self.gold_units.append(Unit(left_base, my, "gold", UnitType.SULTAN))
            for i in range(tc):
                self.gold_units.append(
                    Unit(left_base + 80, my - 400 + i * (800 // max(1, tc)), "gold", UnitType.CANNON))
            for i in range(cc):
                self.gold_units.append(
                    Unit(left_base + 200, my - 300 + i * (600 // max(1, cc)), "gold", UnitType.COMMANDER))
            for i in range(sc):
                r = i // 6
                c = i % 6
                self.gold_units.append(
                    Unit(left_base + 350 + r * 40, my - 200 + c * 72, "gold", UnitType.SOLDIER))
            self.red_units.append(Unit(right_base, my, "red", UnitType.SULTAN))
            for i in range(tc):
                self.red_units.append(
                    Unit(right_base - 80, my - 400 + i * (800 // max(1, tc)), "red", UnitType.CANNON))
            for i in range(cc):
                self.red_units.append(
                    Unit(right_base - 200, my - 300 + i * (600 // max(1, cc)), "red", UnitType.COMMANDER))
            for i in range(sc):
                r = i // 6
                c = i % 6
                self.red_units.append(
                    Unit(right_base - 350 - r * 40, my - 200 + c * 72, "red", UnitType.SOLDIER))
        self.assign_cannon_crews(self.gold_units)
        self.assign_cannon_crews(self.red_units)
        self.camera.target_x = left_base - SCREEN_WIDTH // 2 + 200
        self.camera.target_y = my - SCREEN_HEIGHT // 2

    def sandbox_place(self, wx, wy):
        if self.sandbox_placing is None:
            return
        u = Unit(wx, wy, self.sandbox_team, self.sandbox_placing)
        if self.sandbox_team == "gold":
            self.gold_units.append(u)
            self.assign_cannon_crews(self.gold_units)
        else:
            self.red_units.append(u)
            self.assign_cannon_crews(self.red_units)

    def try_select_unit_at(self, wx, wy):
        best = None
        best_d = float('inf')
        for u in self.gold_units + self.red_units:
            if not u.alive or u.in_tent:
                continue
            d = dist((u.x, u.y), (wx, wy))
            if d < u.size + 12 and d < best_d:
                best_d = d
                best = u
        if self.clicked_unit:
            self.clicked_unit.selected = False
        self.clicked_unit = best
        if best:
            best.selected = True
        return best

    def toggle_control(self):
        if not self.clicked_unit or not self.clicked_unit.alive:
            return
        u = self.clicked_unit
        if u.player_controlled:
            u.player_controlled = False
            self.controlled_unit = None
            return
        if self.controlled_unit and self.controlled_unit.alive:
            self.controlled_unit.player_controlled = False
        u.player_controlled = True
        self.controlled_unit = u

    def release_control(self):
        if self.controlled_unit and self.controlled_unit.alive:
            self.controlled_unit.player_controlled = False
        self.controlled_unit = None

    def select_units_in_box(self):
        if not self.box_start or not self.box_end:
            return
        wx1, wy1 = self.camera.screen_to_world(*self.box_start)
        wx2, wy2 = self.camera.screen_to_world(*self.box_end)
        x1, y1, x2, y2 = min(wx1, wx2), min(wy1, wy2), max(wx1, wx2), max(wy1, wy2)
        for u in self.box_selected_units:
            u.selected = False
        self.box_selected_units = []
        for u in self.gold_units:
            if u.alive and not (
                    u.operating_cannon and u.operating_cannon.alive) and x1 <= u.x <= x2 and y1 <= u.y <= y2:
                u.selected = True
                self.box_selected_units.append(u)

    def send_selected_to(self, wx, wy):
        if not self.box_selected_units:
            return
        n = len(self.box_selected_units)
        cols = max(1, int(math.sqrt(n)))
        spacing = 35
        for i, u in enumerate(self.box_selected_units):
            r = i // cols
            c = i % cols
            u.move_target = (wx + (c - cols // 2) * spacing, wy + (r - (n // cols) // 2) * spacing)
        self.waypoints.append(Waypoint(wx, wy))

    def fire_controlled_cannon(self):
        ctrl = self.controlled_unit
        if not ctrl or not ctrl.alive or ctrl.unit_type != UnitType.CANNON or not ctrl.has_crew() or ctrl.atk_cd > 0:
            return
        mx2, my2 = pygame.mouse.get_pos()
        wx, wy = self.camera.screen_to_world(mx2, my2)
        if dist((ctrl.x, ctrl.y), (wx, wy)) <= ctrl.atk_range:
            ctrl.cannon_target_override = (wx, wy)

    def _do_one_sim_tick(self):
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
                    e.hp -= dmg
                    e.hit_flash = 10
                    if e.hp <= 0:
                        e.alive = False
        self.cannonballs = [b for b in self.cannonballs if b.alive]
        for e in self.explosions:
            e.update()
        self.explosions = [e for e in self.explosions if e.alive]
        for u in self.gold_units:
            if prev_g.get(id(u), False) and not u.alive:
                if self.ankara_mode and u.unit_type == UnitType.SULTAN and not self.ankara_cutscene_triggered:
                    u.alive = True
                    u.hp = max(1, u.hp)
                    continue
                for _ in range(12):
                    self.particles.append(
                        Particle(u.x, u.y, YELLOW, random.randint(2, 5), random.randint(20, 45)))
                self.kills_red += 1
                if u is self.controlled_unit:
                    self.controlled_unit = None
                if u is self.clicked_unit:
                    self.clicked_unit = None
        for u in self.red_units:
            if prev_r.get(id(u), False) and not u.alive:
                for _ in range(12):
                    self.particles.append(
                        Particle(u.x, u.y, RED, random.randint(2, 5), random.randint(20, 45)))
                self.kills_gold += 1
                if u is self.controlled_unit:
                    self.controlled_unit = None
                if u is self.clicked_unit:
                    self.clicked_unit = None

    def _check_ankara_cutscene(self):
        if not self.ankara_mode or self.ankara_cutscene_triggered or not self.battle_started:
            return
        gold_alive = [u for u in self.gold_units if u.alive]
        gold_sultan = None
        gold_others = 0
        for u in gold_alive:
            if u.unit_type == UnitType.SULTAN:
                gold_sultan = u
            else:
                gold_others += 1
        if gold_sultan and gold_others == 0:
            self.ankara_cutscene_triggered = True
            red_sultan = next(
                (u for u in self.red_units if u.alive and u.unit_type == UnitType.SULTAN), None)
            if red_sultan:
                red_sultan.in_tent = False
                red_sultan.frozen = True
                red_sultan.x = self.ankara_tent_x - 60
                red_sultan.y = self.ankara_tent_y
                self.ankara_cutscene.start_cutscene(gold_sultan, red_sultan, self.red_units,
                                                    self.ankara_tent_x, self.ankara_tent_y)
                self.release_control()
                if self.clicked_unit:
                    self.clicked_unit.selected = False
                    self.clicked_unit = None
                self.box_selected_units = []

    def update(self):
        self.frame += 1
        if self.cam_shake > 0:
            self.cam_shake -= 1
        if self.state == "BATTLE":
            if self.ankara_mode and self.ankara_cutscene.cutscene_active:
                result = self.ankara_cutscene.update(self.camera, self.frame)
                if result:
                    self.winner = "RED"
                    self.state = "VICTORY"
                for p in self.particles:
                    p.update()
                self.particles = [p for p in self.particles if p.alive]
                return
            ctrl = self.controlled_unit
            if ctrl and ctrl.alive:
                self.camera.update((ctrl.x, ctrl.y))
            else:
                self.camera.update()
            if ctrl and ctrl.alive and ctrl.unit_type == UnitType.CANNON and ctrl.player_controlled:
                mx2, my2 = pygame.mouse.get_pos()
                wx, wy = self.camera.screen_to_world(mx2, my2)
                ctrl.cannon_angle = ang_to((ctrl.x, ctrl.y), (wx, wy))
            if self.battle_paused:
                return
            self.speed_accumulator += self.battle_speed
            ticks = min(int(self.speed_accumulator), 10)
            self.speed_accumulator -= ticks
            for _ in range(ticks):
                self._do_one_sim_tick()
            if self.frame % max(30, int(120 / max(0.25, self.battle_speed))) == 0:
                self.assign_cannon_crews(self.gold_units)
                self.assign_cannon_crews(self.red_units)
            if self.ankara_mode:
                self._check_ankara_cutscene()
            if self.battle_started and not self.sandbox_mode and not self.ankara_mode:
                ga = sum(1 for u in self.gold_units if u.alive)
                ra = sum(1 for u in self.red_units if u.alive)
                if ga == 0:
                    self.winner = "RED"
                    self.state = "VICTORY"
                elif ra == 0:
                    self.winner = "GOLD"
                    self.state = "VICTORY"
        self.waypoints = [w for w in self.waypoints if w.life > 0]
        for p in self.particles:
            p.update()
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
        self.menu_btns = []
        self.lang_btn_rects = []
        cy = 35
        t = self.f_title.render(T("title"), True, GOLD)
        surface.blit(t, t.get_rect(center=(SCREEN_WIDTH // 2, cy)))
        cy += 38
        t = self.f_med.render(T("subtitle"), True, LIGHT_GRAY)
        surface.blit(t, t.get_rect(center=(SCREEN_WIDTH // 2, cy)))
        cy += 28
        t = self.f_small.render(T("language") + ":", True, WHITE)
        surface.blit(t, t.get_rect(center=(SCREEN_WIDTH // 2 - 60, cy)))
        for i, lc in enumerate(["EN", "TR"]):
            br = pygame.Rect(SCREEN_WIDTH // 2 + i * 55, cy - 12, 48, 24)
            active = current_lang == lc
            pygame.draw.rect(surface, CYAN if active else DARK_GRAY, br, border_radius=5)
            if active:
                pygame.draw.rect(surface, WHITE, br, 2, border_radius=5)
            lt = self.f_mini.render(lc, True, BLACK if active else LIGHT_GRAY)
            surface.blit(lt, lt.get_rect(center=br.center))
            self.lang_btn_rects.append((lc, br))
        cy += 28
        draw_star(surface, BRIGHT_GOLD, (SCREEN_WIDTH // 2 - 160, cy), 16, 7, 5, self.frame * 0.02,
                  DARK_GOLD, 2, True)
        draw_star(surface, BRIGHT_RED, (SCREEN_WIDTH // 2 + 160, cy), 16, 7, 5, -self.frame * 0.02,
                  DARK_RED, 2, True)
        t = self.f_large.render("VS", True, WHITE)
        surface.blit(t, t.get_rect(center=(SCREEN_WIDTH // 2, cy)))
        cy += 32
        panel = pygame.Rect(SCREEN_WIDTH // 2 - 260, cy, 520, 120)
        ps = pygame.Surface((520, 120), pygame.SRCALPHA)
        pygame.draw.rect(ps, (15, 15, 30, 200), (0, 0, 520, 120), border_radius=10)
        surface.blit(ps, (panel.x, panel.y))
        pygame.draw.rect(surface, GOLD, panel, 2, border_radius=10)
        t = self.f_med.render(T("army_settings"), True, GOLD)
        surface.blit(t, t.get_rect(center=(SCREEN_WIDTH // 2, cy + 14)))
        settings = [
            (f"{T('soldiers')}: {self.soldier_count}", cy + 34, "s"),
            (f"{T('commanders')}: {self.commander_count}", cy + 56, "c"),
            (f"{T('cannons')}: {self.cannon_count}", cy + 78, "t")
        ]
        for txt, sy2, key in settings:
            surface.blit(self.f_small.render(txt, True, WHITE), (SCREEN_WIDTH // 2 - 160, sy2))
            m = pygame.Rect(SCREEN_WIDTH // 2 + 70, sy2 - 2, 36, 20)
            p2 = pygame.Rect(SCREEN_WIDTH // 2 + 112, sy2 - 2, 36, 20)
            pygame.draw.rect(surface,
                             BRIGHT_RED if m.collidepoint(pygame.mouse.get_pos()) else RED, m,
                             border_radius=4)
            pygame.draw.rect(surface,
                             BRIGHT_GREEN if p2.collidepoint(pygame.mouse.get_pos()) else GREEN, p2,
                             border_radius=4)
            lbl = "-5" if key == "s" else "-1"
            lbl2 = "+5" if key == "s" else "+1"
            lt = self.f_mini.render(lbl, True, WHITE)
            surface.blit(lt, lt.get_rect(center=m.center))
            lt2 = self.f_mini.render(lbl2, True, WHITE)
            surface.blit(lt2, lt2.get_rect(center=p2.center))
            self.menu_btns.append(("minus_" + key, m))
            self.menu_btns.append(("plus_" + key, p2))
        cy2 = cy + 130
        bw = 250
        bh = 42
        mp = pygame.mouse.get_pos()
        buttons = [
            ("normal", T("normal_battle"), BRIGHT_GOLD, GOLD, BLACK, T("normal_desc"), LIGHT_GRAY),
            ("eflak", T("wallachia"), BRIGHT_GREEN, DARK_GREEN, WHITE, T("wallachia_desc"), LIGHT_GRAY),
            ("ankara", T("ankara"), (220, 110, 40), (180, 80, 20), WHITE, T("ankara_desc"), ORANGE),
            ("sandbox", T("sandbox"), CYAN, (0, 150, 150), WHITE, "", LIGHT_GRAY),
            ("exit", T("exit"), GRAY, DARK_GRAY, WHITE, "", LIGHT_GRAY)
        ]
        for name, label, hc, nc, tc2, desc, dc in buttons:
            btn = pygame.Rect(SCREEN_WIDTH // 2 - bw // 2, cy2, bw, bh)
            h = btn.collidepoint(mp)
            pygame.draw.rect(surface, hc if h else nc, btn, border_radius=9)
            if name == "ankara":
                pulse = abs(math.sin(self.frame * 0.04))
                pygame.draw.rect(surface,
                                 (int(200 + pulse * 55), int(150 + pulse * 50), int(pulse * 80)),
                                 btn, 3, border_radius=9)
            t = self.f_med.render(label, True, tc2)
            surface.blit(t, t.get_rect(center=btn.center))
            self.menu_btns.append((name, btn))
            if desc:
                dt = self.f_mini.render(desc, True, dc)
                surface.blit(dt, dt.get_rect(center=(SCREEN_WIDTH // 2, cy2 + bh + 5)))
                cy2 += bh + 18
            else:
                cy2 += bh + 8
        cy2 += 8
        for i, info in enumerate([T("info_1"), T("info_2")]):
            t = self.f_tiny.render(info, True, LIGHT_GRAY)
            surface.blit(t, t.get_rect(center=(SCREEN_WIDTH // 2, cy2 + i * 16)))

    def draw_battle(self, surface):
        sx = random.randint(-self.cam_shake, self.cam_shake) if self.cam_shake > 0 else 0
        sy = random.randint(-self.cam_shake, self.cam_shake) if self.cam_shake > 0 else 0
        bs = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.game_map.draw(bs, self.camera, self.frame)
        if self.ankara_mode:
            sp = self.camera.world_to_screen(self.ankara_tent_x, self.ankara_tent_y)
            draw_tent_at(bs, sp[0], sp[1], self.frame, T("timur_tent"))
            if self.ankara_cutscene.cutscene_active and \
                    self.ankara_cutscene.phase.value >= AnkaraCutscenePhase.PRISON.value:
                pp = self.camera.world_to_screen(self.ankara_cutscene.prison_x,
                                                 self.ankara_cutscene.prison_y)
                draw_prison_at(bs, pp[0], pp[1])
        for wp in self.waypoints:
            wp.draw(bs, self.camera)
        all_u = self.gold_units + self.red_units
        for layer in [UnitType.SOLDIER, UnitType.CANNON, UnitType.COMMANDER, UnitType.SULTAN]:
            for u in all_u:
                if u.unit_type == layer and u.alive:
                    u.draw(bs, self.camera)
        for b in self.cannonballs:
            b.draw(bs, self.camera)
        for e in self.explosions:
            e.draw(bs, self.camera)
        for p in self.particles:
            p.draw(bs, self.camera)
        ctrl = self.controlled_unit
        if ctrl and ctrl.alive and ctrl.unit_type == UnitType.CANNON and ctrl.player_controlled:
            mx2, my2 = pygame.mouse.get_pos()
            pygame.draw.line(bs, YELLOW, (mx2 - 15, my2), (mx2 + 15, my2), 1)
            pygame.draw.line(bs, YELLOW, (mx2, my2 - 15), (mx2, my2 + 15), 1)
            pygame.draw.circle(bs, YELLOW, (mx2, my2), 10, 1)
            pygame.draw.circle(bs, YELLOW, (mx2, my2), 3)
            wx, wy = self.camera.screen_to_world(mx2, my2)
            d = dist((ctrl.x, ctrl.y), (wx, wy))
            in_range = d <= ctrl.atk_range
            col = GREEN if in_range else RED
            ready = ctrl.atk_cd <= 0 and ctrl.has_crew()
            status = T("ready") if ready else f"CD:{ctrl.atk_cd}"
            range_txt = T("in_range") if in_range else T("out_range")
            try:
                cf = pygame.font.SysFont("Arial", 12)
                ct = cf.render(f"{range_txt} | {status}", True, col)
                bs.blit(ct, (mx2 + 15, my2 - 20))
            except:
                pass
        if self.box_selecting and self.box_start and self.box_end:
            bx1 = min(self.box_start[0], self.box_end[0])
            by1 = min(self.box_start[1], self.box_end[1])
            bx2 = max(self.box_start[0], self.box_end[0])
            by2 = max(self.box_start[1], self.box_end[1])
            w = max(1, bx2 - bx1)
            h = max(1, by2 - by1)
            sel_s = pygame.Surface((w, h), pygame.SRCALPHA)
            pygame.draw.rect(sel_s, (0, 255, 0, 40), (0, 0, w, h))
            bs.blit(sel_s, (bx1, by1))
            pygame.draw.rect(bs, (0, 255, 0), (bx1, by1, w, h), 2)
        surface.blit(bs, (sx, sy))
        cs_active = self.ankara_mode and self.ankara_cutscene.cutscene_active
        if cs_active:
            self.ankara_cutscene.draw(surface, self.camera, self.frame)
        else:
            self._draw_ui(surface)
            self._draw_speed_panel(surface)
            if self.sandbox_mode:
                self._draw_sandbox_panel(surface)
            else:
                self._draw_side_panel(surface)
            self._draw_control_info(surface)
        if not cs_active:
            self._draw_minimap(surface)
        if not self.battle_started and not cs_active:
            bw2 = 300
            bh2 = 50
            btn = pygame.Rect(SCREEN_WIDTH // 2 - bw2 // 2, SCREEN_HEIGHT - 75, bw2, bh2)
            h = btn.collidepoint(pygame.mouse.get_pos())
            pygame.draw.rect(surface, BRIGHT_RED if h else RED, btn, border_radius=12)
            txt = T("begin_ankara") if self.ankara_mode else T("attack_order")
            t = self.f_med.render(txt, True, WHITE)
            surface.blit(t, t.get_rect(center=btn.center))
            self.atk_btn = btn
        else:
            self.atk_btn = None
        if self.box_selected_units and not cs_active:
            gt = self.f_small.render(
                f"{len(self.box_selected_units)} {T('units_selected')}", True, (100, 255, 100))
            surface.blit(gt, gt.get_rect(center=(SCREEN_WIDTH // 2, 118)))
        if self.naming_mode:
            self._draw_naming_dialog(surface)
        if self.battle_paused and self.battle_started and not cs_active:
            pov = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            pygame.draw.rect(pov, (0, 0, 0, 80), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            surface.blit(pov, (0, 0))
            t = self.f_title.render(T("paused"), True, WHITE)
            surface.blit(t, t.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)))
            t2 = self.f_med.render(T("press_p"), True, LIGHT_GRAY)
            surface.blit(t2, t2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)))

    def _draw_ui(self, surface):
        ps = pygame.Surface((SCREEN_WIDTH, 72), pygame.SRCALPHA)
        pygame.draw.rect(ps, (0, 0, 0, 185), (0, 0, SCREEN_WIDTH, 72))
        pygame.draw.line(ps, GOLD, (0, 71), (SCREEN_WIDTH, 71), 2)
        surface.blit(ps, (0, 0))
        ga = sum(1 for u in self.gold_units if u.alive)
        gp = next((u for u in self.gold_units if u.unit_type == UnitType.SULTAN and u.alive), None)
        sng = T("bayezid_army") if self.ankara_mode else T("yellow_team")
        snr = T("timur_army") if self.ankara_mode else T("red_team")
        draw_star(surface, BRIGHT_GOLD, (22, 35), 13, 6, 5, self.frame * 0.02, DARK_GOLD, 2)
        surface.blit(self.f_med.render(sng, True, GOLD), (42, 4))
        surface.blit(self.f_mini.render(f"{T('total')}:{ga}", True, YELLOW_LIGHT), (42, 27))
        if gp:
            surface.blit(self.f_mini.render(f"{T('sultan_hp')}:{gp.hp}/{gp.max_hp}", True, GREEN),
                          (42, 42))
        surface.blit(self.f_small.render(f"{T('kills')}:{self.kills_gold}", True, GOLD), (42, 55))
        ra = sum(1 for u in self.red_units if u.alive and not u.in_tent)
        rp = next((u for u in self.red_units if u.unit_type == UnitType.SULTAN and u.alive), None)
        draw_star(surface, BRIGHT_RED, (SCREEN_WIDTH - 22, 35), 13, 6, 5, self.frame * 0.02, DARK_RED,
                  2)
        t = self.f_med.render(snr, True, RED)
        surface.blit(t, (SCREEN_WIDTH - 42 - t.get_width(), 4))
        t2 = self.f_mini.render(f"{T('total')}:{ra}", True, RED_LIGHT)
        surface.blit(t2, (SCREEN_WIDTH - 42 - t2.get_width(), 27))
        if rp and not rp.in_tent:
            t3 = self.f_mini.render(f"{T('sultan_hp')}:{rp.hp}/{rp.max_hp}", True, RED_LIGHT)
            surface.blit(t3, (SCREEN_WIDTH - 42 - t3.get_width(), 42))
        elif self.ankara_mode:
            t3 = self.f_mini.render(T("timur_in_tent"), True, ORANGE)
            surface.blit(t3, (SCREEN_WIDTH - 42 - t3.get_width(), 42))
        kt = self.f_small.render(f"{T('kills')}:{self.kills_red}", True, RED)
        surface.blit(kt, (SCREEN_WIDTH - 42 - kt.get_width(), 55))
        if self.battle_paused:
            vs = self.f_large.render(T("paused"), True, ORANGE)
        elif self.battle_started:
            p = abs(math.sin(self.frame * 0.05))
            if self.ankara_mode:
                vs = self.f_large.render(T("battle_ankara"), True,
                                         (255, int(150 + p * 55), int(50 + p * 100)))
            else:
                vs = self.f_large.render(T("battle"), True,
                                         (255, int(200 + p * 55), int(150 + p * 55)))
        else:
            vs = self.f_large.render(
                T("ankara_1402") if self.ankara_mode else T("strategy_phase"), True,
                ORANGE if self.ankara_mode else CYAN)
        surface.blit(vs, vs.get_rect(center=(SCREEN_WIDTH // 2, 35)))

    def _draw_speed_panel(self, surface):
        pw = 320
        ph = 38
        px = SCREEN_WIDTH // 2 - pw // 2
        py = 74
        ps = pygame.Surface((pw, ph), pygame.SRCALPHA)
        pygame.draw.rect(ps, (0, 0, 0, 180), (0, 0, pw, ph), border_radius=8)
        surface.blit(ps, (px, py))
        sc2 = WHITE
        if self.battle_speed < 1.0:
            sc2 = (100, 180, 255)
        elif self.battle_speed >= 3.0:
            sc2 = FIRE_RED
        elif self.battle_speed > 1.0:
            sc2 = ORANGE
        surface.blit(self.f_small.render(f"{self.battle_speed:.2g}x", True, sc2), (px + 8, py + 10))
        self.speed_btn_rects = []
        bw2 = 36
        bh2 = 24
        by2 = py + 7
        sx2 = px + 60
        mp = pygame.mouse.get_pos()
        for i, spd in enumerate(self.speed_options):
            bx = sx2 + i * (bw2 + 3)
            br = pygame.Rect(bx, by2, bw2, bh2)
            act = abs(self.battle_speed - spd) < 0.01
            hov = br.collidepoint(mp)
            if act:
                if spd < 1.0:
                    bc2 = (40, 120, 200)
                elif spd == 1.0:
                    bc2 = (40, 160, 60)
                elif spd <= 2.0:
                    bc2 = (200, 120, 20)
                else:
                    bc2 = (200, 40, 40)
            elif hov:
                bc2 = (70, 70, 90)
            else:
                bc2 = (45, 45, 60)
            pygame.draw.rect(surface, bc2, br, border_radius=4)
            if act:
                pygame.draw.rect(surface, WHITE, br, 2, border_radius=4)
            t = self.f_mini.render(f"{spd:.2g}x", True, WHITE if act else (130, 130, 140))
            surface.blit(t, t.get_rect(center=br.center))
            self.speed_btn_rects.append((spd, br))

    def _draw_side_panel(self, surface):
        pw = 180
        px = SCREEN_WIDTH - pw - 5
        py = 78
        ph = 270
        ps = pygame.Surface((pw, ph), pygame.SRCALPHA)
        pygame.draw.rect(ps, (0, 0, 0, 150), (0, 0, pw, ph), border_radius=8)
        pygame.draw.rect(ps, GOLD, (0, 0, pw, ph), 2, border_radius=8)
        surface.blit(ps, (px, py))
        surface.blit(self.f_tiny.render(T("controls"), True, CYAN), (px + 8, py + 8))
        if self.ankara_mode:
            controls = [T("ctrl_box_select"), T("ctrl_send"), T("ctrl_control"), T("ctrl_move"),
                        T("ctrl_pause"),
                        T("ctrl_start"), T("ctrl_speed"), T("ctrl_scroll"), T("ctrl_focus"),
                        T("ctrl_menu"), "",
                        T("ankara_info_1"), T("ankara_info_2"), T("ankara_info_3"),
                        T("ankara_info_4"), T("ankara_info_5")]
        else:
            controls = [T("ctrl_box_select"), T("ctrl_send"), T("ctrl_control"),
                        T("ctrl_move_cannon"), T("ctrl_fire"),
                        T("ctrl_pause"), T("ctrl_attack"), T("ctrl_speed"), T("ctrl_scroll"),
                        T("ctrl_focus"),
                        T("ctrl_menu"), "", T("ctrl_cannon_crew")]
        for i, c in enumerate(controls):
            col = LIGHT_GRAY
            cl = c.lower()
            if any(w in cl for w in ["cannon", "top", "toplar"]):
                col = ORANGE
            if any(w in cl for w in ["pause", "duraklat"]):
                col = CYAN
            if any(w in cl for w in ["speed", "hiz"]):
                col = YELLOW
            if any(w in cl for w in ["ankara", "bayezid", "timur"]):
                col = ORANGE
            if "===" in c:
                col = GOLD
            surface.blit(self.f_mini.render(c, True, col), (px + 8, py + 26 + i * 14))

    def _draw_sandbox_panel(self, surface):
        pw = 180
        px = 5
        py = 78
        ph = 340
        ps = pygame.Surface((pw, ph), pygame.SRCALPHA)
        pygame.draw.rect(ps, (0, 0, 0, 170), (0, 0, pw, ph), border_radius=8)
        pygame.draw.rect(ps, CYAN, (0, 0, pw, ph), 2, border_radius=8)
        surface.blit(ps, (px, py))
        surface.blit(self.f_med.render(T("sandbox_title"), True, CYAN), (px + 10, py + 6))
        surface.blit(self.f_tiny.render(T("team") + ":", True, WHITE), (px + 10, py + 32))
        gold_btn = pygame.Rect(px + 55, py + 30, 50, 20)
        red_btn = pygame.Rect(px + 110, py + 30, 50, 20)
        pygame.draw.rect(surface,
                         BRIGHT_GOLD if self.sandbox_team == "gold" else DARK_GOLD, gold_btn,
                         border_radius=4)
        pygame.draw.rect(surface,
                         BRIGHT_RED if self.sandbox_team == "red" else DARK_RED, red_btn,
                         border_radius=4)
        t = self.f_mini.render(T("yellow"), True, BLACK)
        surface.blit(t, t.get_rect(center=gold_btn.center))
        t = self.f_mini.render(T("red"), True, WHITE)
        surface.blit(t, t.get_rect(center=red_btn.center))
        self.sb_gold_btn = gold_btn
        self.sb_red_btn = red_btn
        surface.blit(self.f_tiny.render(T("place_unit"), True, WHITE), (px + 10, py + 58))
        unit_btns = []
        types = [(T("sultan"), UnitType.SULTAN, GOLD), (T("commander"), UnitType.COMMANDER, GREEN),
                 (T("soldier"), UnitType.SOLDIER, YELLOW), (T("cannon"), UnitType.CANNON, GRAY)]
        for i, (name, ut, col) in enumerate(types):
            btn = pygame.Rect(px + 10, py + 78 + i * 28, pw - 20, 24)
            sel = self.sandbox_placing == ut
            pygame.draw.rect(surface, col if sel else (40, 40, 50), btn, border_radius=5)
            if sel:
                pygame.draw.rect(surface, WHITE, btn, 2, border_radius=5)
            tc2 = BLACK if sel else col
            t = self.f_mini.render(name, True, tc2)
            surface.blit(t, t.get_rect(center=btn.center))
            unit_btns.append((ut, btn))
        self.sb_unit_btns = unit_btns
        cy = py + 200
        surface.blit(self.f_tiny.render(
            f"{T('yellow')}: {len([u for u in self.gold_units if u.alive])}", True, GOLD),
            (px + 10, cy))
        surface.blit(self.f_tiny.render(
            f"{T('red')}: {len([u for u in self.red_units if u.alive])}", True, RED),
            (px + 10, cy + 16))
        clear_g = pygame.Rect(px + 10, cy + 38, pw // 2 - 15, 22)
        clear_r = pygame.Rect(px + pw // 2 + 5, cy + 38, pw // 2 - 15, 22)
        clear_a = pygame.Rect(px + 10, cy + 64, pw - 20, 22)
        pygame.draw.rect(surface, DARK_GOLD, clear_g, border_radius=4)
        pygame.draw.rect(surface, DARK_RED, clear_r, border_radius=4)
        pygame.draw.rect(surface, DARK_GRAY, clear_a, border_radius=4)
        t = self.f_mini.render(T("clear_y"), True, WHITE)
        surface.blit(t, t.get_rect(center=clear_g.center))
        t = self.f_mini.render(T("clear_r"), True, WHITE)
        surface.blit(t, t.get_rect(center=clear_r.center))
        t = self.f_mini.render(T("clear_all"), True, WHITE)
        surface.blit(t, t.get_rect(center=clear_a.center))
        self.sb_clear_g = clear_g
        self.sb_clear_r = clear_r
        self.sb_clear_a = clear_a
        desel = pygame.Rect(px + 10, cy + 90, pw - 20, 22)
        pygame.draw.rect(surface, (60, 60, 80), desel, border_radius=4)
        t = self.f_mini.render(T("deselect"), True, WHITE)
        surface.blit(t, t.get_rect(center=desel.center))
        self.sb_desel = desel
        surface.blit(self.f_mini.render(T("name_selected"), True, CYAN), (px + 10, cy + 118))

    def _draw_control_info(self, surface):
        pw = 260
        ph = 115
        px = 5
        py = SCREEN_HEIGHT - ph - 10
        if self.clicked_unit and self.clicked_unit.alive:
            u = self.clicked_unit
            ps = pygame.Surface((pw, ph), pygame.SRCALPHA)
            pygame.draw.rect(ps, (0, 0, 0, 170), (0, 0, pw, ph), border_radius=8)
            border_c = MAGENTA if u.player_controlled else (0, 220, 0)
            pygame.draw.rect(ps, border_c, (0, 0, pw, ph), 2, border_radius=8)
            surface.blit(ps, (px, py))
            type_names = {UnitType.SULTAN: T("sultan"), UnitType.COMMANDER: T("commander"),
                          UnitType.SOLDIER: T("soldier"), UnitType.CANNON: T("cannon")}
            tn = T("yellow") if u.team == "gold" else T("red")
            tc2 = GOLD if u.team == "gold" else RED
            ns = f' "{u.custom_name}"' if u.custom_name else ""
            surface.blit(self.f_small.render(
                f"{type_names[u.unit_type]}{ns} ({tn})", True, tc2), (px + 8, py + 6))
            surface.blit(self.f_mini.render(
                f"{T('hp')}:{max(0, u.hp)}/{u.max_hp} {T('atk')}:{u.attack} {T('spd')}:{u.speed}",
                True, WHITE), (px + 8, py + 26))
            if u.player_controlled:
                if u.unit_type == UnitType.CANNON:
                    surface.blit(self.f_small.render(
                        T("ctrl_wasd") + " + LMB fire", True, MAGENTA), (px + 8, py + 44))
                else:
                    surface.blit(self.f_small.render(
                        T("ctrl_wasd"), True, MAGENTA), (px + 8, py + 44))
            elif u.unit_type == UnitType.CANNON:
                crew_txt = T("has_crew") if u.has_crew() else T("no_crew") + "!"
                crew_c = GREEN if u.has_crew() else RED
                surface.blit(self.f_small.render(
                    f"{T('cannon')} - {crew_txt}", True, crew_c), (px + 8, py + 44))
            else:
                surface.blit(self.f_small.render(
                    T("press_f"), True, (100, 255, 100)), (px + 8, py + 44))
            if u.operating_cannon and u.operating_cannon.alive:
                surface.blit(self.f_mini.render(
                    T("cannon_crew"), True, CANNON_GRAY), (px + 8, py + 64))
            else:
                surface.blit(self.f_mini.render(
                    f"{T('pos')}: ({int(u.x)}, {int(u.y)})", True, LIGHT_GRAY), (px + 8, py + 64))
            if u.unit_type == UnitType.CANNON and u.player_controlled:
                surface.blit(self.f_mini.render(
                    f"Range:{u.atk_range} | CD:{u.atk_cd}", True, ORANGE), (px + 8, py + 80))
            if self.sandbox_mode:
                surface.blit(self.f_mini.render(
                    T("name_selected"), True, CYAN), (px + 8, py + 96))
        else:
            ps = pygame.Surface((pw, 28), pygame.SRCALPHA)
            pygame.draw.rect(ps, (0, 0, 0, 120), (0, 0, pw, 28), border_radius=5)
            surface.blit(ps, (px, py + ph - 28))
            surface.blit(self.f_mini.render(
                T("click_unit"), True, LIGHT_GRAY), (px + 6, py + ph - 22))

    def _draw_naming_dialog(self, surface):
        dw = 400
        dh = 120
        dx = SCREEN_WIDTH // 2 - dw // 2
        dy = SCREEN_HEIGHT // 2 - dh // 2
        ds = pygame.Surface((dw, dh), pygame.SRCALPHA)
        pygame.draw.rect(ds, (10, 10, 30, 230), (0, 0, dw, dh), border_radius=12)
        pygame.draw.rect(ds, CYAN, (0, 0, dw, dh), 3, border_radius=12)
        surface.blit(ds, (dx, dy))
        type_names = {UnitType.SULTAN: T("sultan"), UnitType.COMMANDER: T("commander"),
                      UnitType.SOLDIER: T("soldier"), UnitType.CANNON: T("cannon")}
        uname = type_names.get(self.naming_unit.unit_type, "Unit") if self.naming_unit else "Unit"
        t = self.f_med.render(f"{T('name_unit')} {uname}", True, CYAN)
        surface.blit(t, t.get_rect(center=(SCREEN_WIDTH // 2, dy + 20)))
        ib = pygame.Rect(dx + 30, dy + 48, dw - 60, 30)
        pygame.draw.rect(surface, (30, 30, 50), ib, border_radius=5)
        pygame.draw.rect(surface, WHITE, ib, 2, border_radius=5)
        cursor = "|" if (self.frame // 30) % 2 == 0 else ""
        surface.blit(self.f_small.render(self.naming_text + cursor, True, WHITE), (ib.x + 8, ib.y + 6))
        t = self.f_tiny.render(T("enter_confirm"), True, LIGHT_GRAY)
        surface.blit(t, t.get_rect(center=(SCREEN_WIDTH // 2, dy + 100)))

    def _draw_minimap(self, surface):
        mw = 200
        mh = 150
        mx2 = SCREEN_WIDTH - mw - 10
        my2 = SCREEN_HEIGHT - mh - 10
        ms = pygame.Surface((mw, mh), pygame.SRCALPHA)
        pygame.draw.rect(ms, (0, 0, 0, 150), (0, 0, mw, mh), border_radius=5)
        surface.blit(ms, (mx2, my2))
        pygame.draw.rect(surface, LIGHT_GRAY, (mx2, my2, mw, mh), 2, border_radius=5)
        sx2 = WORLD_WIDTH / mw
        sy2 = WORLD_HEIGHT / mh
        for u in self.gold_units:
            if u.alive:
                pygame.draw.circle(surface,
                                   MAGENTA if u.player_controlled else GOLD,
                                   (mx2 + int(u.x / sx2), my2 + int(u.y / sy2)),
                                   2 if u.unit_type == UnitType.SULTAN else 1)
        for u in self.red_units:
            if u.alive and not u.in_tent:
                pygame.draw.circle(surface, RED,
                                   (mx2 + int(u.x / sx2), my2 + int(u.y / sy2)),
                                   2 if u.unit_type == UnitType.SULTAN else 1)
        if self.ankara_mode:
            tx = mx2 + int(self.ankara_tent_x / sx2)
            ty = my2 + int(self.ankara_tent_y / sy2)
            pygame.draw.rect(surface, ORANGE, (tx - 3, ty - 3, 6, 6))
        cvx = mx2 + int(self.camera.x / sx2)
        cvy = my2 + int(self.camera.y / sy2)
        cvw = int(SCREEN_WIDTH / sx2)
        cvh = int(SCREEN_HEIGHT / sy2)
        pygame.draw.rect(surface, WHITE, (cvx, cvy, cvw, cvh), 1)
        surface.blit(self.f_mini.render(T("minimap"), True, WHITE), (mx2 + 5, my2 + 3))

    def draw_victory(self, surface):
        self.draw_battle(surface)
        ov = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(ov, (0, 0, 0, 180), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        surface.blit(ov, (0, 0))
        if self.ankara_mode and self.winner == "RED":
            draw_star(surface, BRIGHT_RED, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 180), 50, 22, 5,
                      self.frame * 0.03, DARK_RED, 3, True)
            t = self.f_title.render(T("timur_wins"), True, RED)
            surface.blit(t, t.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80)))
            t = self.f_large.render(T("ankara_title_vic"), True, ORANGE)
            surface.blit(t, t.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)))
            sy3 = SCREEN_HEIGHT // 2 + 10
            t = self.f_med.render(T("bayezid_captured"), True, GOLD)
            surface.blit(t, t.get_rect(center=(SCREEN_WIDTH // 2, sy3)))
            t = self.f_small.render(T("interregnum"), True, LIGHT_GRAY)
            surface.blit(t, t.get_rect(center=(SCREEN_WIDTH // 2, sy3 + 28)))
        else:
            wt = T("yellow_wins") if self.winner == "GOLD" else T("red_wins")
            wc = GOLD if self.winner == "GOLD" else RED
            sc2 = BRIGHT_GOLD if self.winner == "GOLD" else BRIGHT_RED
            bc3 = DARK_GOLD if self.winner == "GOLD" else DARK_RED
            draw_star(surface, sc2, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 140), 50, 22, 5,
                      self.frame * 0.03, bc3, 3, True)
            t = self.f_title.render(wt, True, wc)
            surface.blit(t, t.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)))
            sy3 = SCREEN_HEIGHT // 2 + 20
            t = self.f_med.render(f"{T('yellow_kills')}: {self.kills_gold}", True, GOLD)
            surface.blit(t, t.get_rect(center=(SCREEN_WIDTH // 2, sy3)))
            t = self.f_med.render(f"{T('red_kills')}: {self.kills_red}", True, RED)
            surface.blit(t, t.get_rect(center=(SCREEN_WIDTH // 2, sy3 + 35)))
        bw3 = 260
        bh3 = 48
        sy_btn = SCREEN_HEIGHT // 2 + (110 if self.ankara_mode else 100)
        replay = pygame.Rect(SCREEN_WIDTH // 2 - bw3 // 2, sy_btn, bw3, bh3)
        pygame.draw.rect(surface,
                         BRIGHT_GREEN if replay.collidepoint(pygame.mouse.get_pos()) else GREEN,
                         replay, border_radius=10)
        t = self.f_med.render(T("play_again"), True, WHITE)
        surface.blit(t, t.get_rect(center=replay.center))
        menu = pygame.Rect(SCREEN_WIDTH // 2 - bw3 // 2, sy_btn + 60, bw3, bh3)
        pygame.draw.rect(surface,
                         BRIGHT_GOLD if menu.collidepoint(pygame.mouse.get_pos()) else GOLD,
                         menu, border_radius=10)
        t = self.f_med.render(T("main_menu"), True, BLACK)
        surface.blit(t, t.get_rect(center=menu.center))
        self.vic_btns = [replay, menu]

    def start_mode(self, mode, sandbox=False, ankara=False):
        self.map_mode = mode
        self.sandbox_mode = sandbox
        self.ankara_mode = ankara
        if ankara:
            self.game_map = GameMap("ankara")
        elif sandbox:
            self.game_map = GameMap("sandbox")
        else:
            self.game_map = GameMap(mode)
        self.setup_armies()
        self.state = "BATTLE"
        if sandbox:
            self.battle_started = False
            self.camera.target_x = WORLD_WIDTH // 2 - SCREEN_WIDTH // 2
            self.camera.target_y = WORLD_HEIGHT // 2 - SCREEN_HEIGHT // 2

    def run(self):
        global current_lang
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.VIDEORESIZE:
                    global SCREEN_WIDTH, SCREEN_HEIGHT
                    SCREEN_WIDTH = event.w
                    SCREEN_HEIGHT = event.h
                if self.naming_mode:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            if self.naming_unit:
                                self.naming_unit.custom_name = self.naming_text
                            self.naming_mode = False
                        elif event.key == pygame.K_ESCAPE:
                            self.naming_mode = False
                        elif event.key == pygame.K_BACKSPACE:
                            self.naming_text = self.naming_text[:-1]
                        elif len(self.naming_text) < 20 and event.unicode.isprintable() and event.unicode:
                            self.naming_text += event.unicode
                    continue
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if self.state in ("BATTLE", "VICTORY"):
                        self.go_to_menu()
                        continue
                if self.ankara_mode and self.ankara_cutscene.cutscene_active and self.state == "BATTLE":
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        self.ankara_cutscene.skip_dialogue()
                    continue
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.state == "MENU":
                        for lc, br in self.lang_btn_rects:
                            if br.collidepoint(pos):
                                current_lang = lc
                        for name, rect in self.menu_btns:
                            if rect.collidepoint(pos):
                                if name == "normal":
                                    self.start_mode("normal")
                                elif name == "eflak":
                                    self.start_mode("eflak")
                                elif name == "ankara":
                                    self.start_mode("ankara", ankara=True)
                                elif name == "sandbox":
                                    self.start_mode("sandbox", sandbox=True)
                                elif name == "exit":
                                    running = False
                                elif name == "minus_s":
                                    self.soldier_count = max(5, self.soldier_count - 5)
                                elif name == "plus_s":
                                    self.soldier_count = min(80, self.soldier_count + 5)
                                elif name == "minus_c":
                                    self.commander_count = max(1, self.commander_count - 1)
                                elif name == "plus_c":
                                    self.commander_count = min(10, self.commander_count + 1)
                                elif name == "minus_t":
                                    self.cannon_count = max(0, self.cannon_count - 1)
                                elif name == "plus_t":
                                    self.cannon_count = min(10, self.cannon_count + 1)
                    elif self.state == "BATTLE":
                        speed_clicked = False
                        if event.button == 1:
                            for spd, br in self.speed_btn_rects:
                                if br.collidepoint(pos):
                                    self.set_speed(spd)
                                    speed_clicked = True
                                    break
                        if speed_clicked:
                            pass
                        elif event.button == 1:
                            ctrl = self.controlled_unit
                            if ctrl and ctrl.alive and ctrl.unit_type == UnitType.CANNON and \
                                    ctrl.player_controlled and self.battle_started:
                                self.fire_controlled_cannon()
                            elif self.atk_btn and self.atk_btn.collidepoint(pos):
                                self.battle_started = True
                                self.cam_shake = 10
                            elif self.sandbox_mode:
                                handled = False
                                if hasattr(self, 'sb_gold_btn') and self.sb_gold_btn.collidepoint(pos):
                                    self.sandbox_team = "gold"
                                    handled = True
                                elif hasattr(self, 'sb_red_btn') and self.sb_red_btn.collidepoint(pos):
                                    self.sandbox_team = "red"
                                    handled = True
                                elif hasattr(self, 'sb_clear_g') and self.sb_clear_g.collidepoint(pos):
                                    self.gold_units.clear()
                                    handled = True
                                elif hasattr(self, 'sb_clear_r') and self.sb_clear_r.collidepoint(pos):
                                    self.red_units.clear()
                                    handled = True
                                elif hasattr(self, 'sb_clear_a') and self.sb_clear_a.collidepoint(pos):
                                    self.gold_units.clear()
                                    self.red_units.clear()
                                    handled = True
                                elif hasattr(self, 'sb_desel') and self.sb_desel.collidepoint(pos):
                                    self.sandbox_placing = None
                                    handled = True
                                if hasattr(self, 'sb_unit_btns'):
                                    for ut, btn in self.sb_unit_btns:
                                        if btn.collidepoint(pos):
                                            self.sandbox_placing = ut
                                            handled = True
                                if not handled and self.sandbox_placing and pos[1] > 75 and not (
                                        pos[0] < 190 and pos[1] < 400):
                                    wx, wy = self.camera.screen_to_world(*pos)
                                    self.sandbox_place(wx, wy)
                                elif not handled:
                                    if self.box_selected_units:
                                        wx, wy = self.camera.screen_to_world(*pos)
                                        self.send_selected_to(wx, wy)
                                        for u in self.box_selected_units:
                                            u.selected = False
                                        self.box_selected_units = []
                                    else:
                                        self.try_select_unit_at(
                                            *self.camera.screen_to_world(*pos))
                            else:
                                if self.box_selected_units:
                                    wx, wy = self.camera.screen_to_world(*pos)
                                    self.send_selected_to(wx, wy)
                                    for u in self.box_selected_units:
                                        u.selected = False
                                    self.box_selected_units = []
                                else:
                                    self.try_select_unit_at(
                                        *self.camera.screen_to_world(*pos))
                        elif event.button == 3:
                            self.box_selecting = True
                            self.box_start = pos
                            self.box_end = pos
                        elif event.button == 2:
                            self.camera.drag = True
                            self.camera.drag_start = pos
                            self.camera.drag_cam_start = (self.camera.target_x, self.camera.target_y)
                    elif self.state == "VICTORY":
                        if len(self.vic_btns) >= 2:
                            if self.vic_btns[0].collidepoint(pos):
                                self.start_mode(self.map_mode, self.sandbox_mode, self.ankara_mode)
                            elif self.vic_btns[1].collidepoint(pos):
                                self.go_to_menu()
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 2:
                        self.camera.drag = False
                    if event.button == 3 and self.state == "BATTLE":
                        if self.box_selecting:
                            self.box_selecting = False
                            self.box_end = pygame.mouse.get_pos()
                            if self.box_start:
                                if abs(self.box_end[0] - self.box_start[0]) > 10 or \
                                        abs(self.box_end[1] - self.box_start[1]) > 10:
                                    self.select_units_in_box()
                                else:
                                    for u in self.box_selected_units:
                                        u.selected = False
                                    self.box_selected_units = []
                if event.type == pygame.MOUSEMOTION:
                    if self.camera.drag:
                        self.camera.target_x = self.camera.drag_cam_start[0] - (
                                event.pos[0] - self.camera.drag_start[0])
                        self.camera.target_y = self.camera.drag_cam_start[1] - (
                                event.pos[1] - self.camera.drag_start[1])
                    if self.box_selecting:
                        self.box_end = event.pos
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.state == "BATTLE" and not self.battle_started:
                        self.battle_started = True
                        self.cam_shake = 10
                    elif event.key == pygame.K_p and self.state == "BATTLE" and self.battle_started:
                        self.battle_paused = not self.battle_paused
                    elif event.key == pygame.K_r and self.state == "VICTORY":
                        self.start_mode(self.map_mode, self.sandbox_mode, self.ankara_mode)
                    elif event.key == pygame.K_x and self.sandbox_mode:
                        self.sandbox_placing = None
                    elif event.key == pygame.K_f and self.state == "BATTLE":
                        self.toggle_control()
                    elif event.key == pygame.K_n and self.state == "BATTLE" and self.sandbox_mode:
                        if self.clicked_unit and self.clicked_unit.alive:
                            self.naming_mode = True
                            self.naming_unit = self.clicked_unit
                            self.naming_text = self.clicked_unit.custom_name
                    elif event.key == pygame.K_TAB and self.state == "BATTLE":
                        if self.controlled_unit and self.controlled_unit.alive:
                            self.camera.target_x = self.controlled_unit.x - SCREEN_WIDTH // 2
                            self.camera.target_y = self.controlled_unit.y - SCREEN_HEIGHT // 2
                    elif event.key == pygame.K_RIGHTBRACKET and self.state == "BATTLE":
                        self.cycle_speed_up()
                    elif event.key == pygame.K_LEFTBRACKET and self.state == "BATTLE":
                        self.cycle_speed_down()
            self.update()
            screen.fill(BLACK)
            if self.state == "MENU":
                self.draw_menu(screen)
            elif self.state == "BATTLE":
                self.draw_battle(screen)
            elif self.state == "VICTORY":
                self.draw_victory(screen)
            pygame.display.flip()
            clock.tick(FPS)
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()