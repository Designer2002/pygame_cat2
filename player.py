import pygame as pg
from pathlib import Path

TILE_SIZE = (64, 64)
PLAYER_WIDTH = 32
PLAYER_HEIGHT = 32
PLAYER_SIZE = (PLAYER_WIDTH,PLAYER_HEIGHT)
PLAYER_COLOR = (255,0,0)
PLAYER_MOTION_SPEED = 3
BASE_DIR = Path(__file__).absolute().parent

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, rect_size_x, rect_size_y):
        pg.sprite.Sprite.__init__(self)
        self.image = None
        self.rect = pg.Rect(x, y, rect_size_x, rect_size_y)

class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.x_velocity = 0
        self.y_velocity = 0
        self.start_x = x
        self.start_y = y
        self.is_left = False
        self.is_right = False
        self.is_up = False
        self.is_down = False
        
        self.images = {
            'sit': [self.load_pair(BASE_DIR / "resources" / "images" / "cat" / "idle" / f"cat_idle{i}.png") for i in range(1, 9)],
            'walk': [self.load_pair(BASE_DIR / "resources" / "images" / "cat" / "walk" / f"cat_walk{i}.png") for i in range(1, 8)]
        }
        self.current_animation = 'sit'
        self.frame_index = 0
        self.image = self.images[self.current_animation][self.frame_index][self.get_direction()]
        self.rect = pg.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)

        self.animation_speed = 0.1  # Скорость анимации
        self.last_update = pg.time.get_ticks()

    def load_pair(self, path):
        return pg.transform.scale(pg.transform.flip(pg.image.load(path).convert_alpha(), True, False), (PLAYER_HEIGHT*2, PLAYER_WIDTH*2)), pg.transform.scale(pg.image.load(path).convert_alpha(), (PLAYER_HEIGHT*2, PLAYER_WIDTH*2))
    def get_direction(self):
        if self.is_left:
            return 0
        else:
            return 1
    def update(self, c_points, camera):
        pos_x= camera.camera.x
        pos_y = camera.camera.y

        self.animate()
        
        if self.is_left:
            self.x_velocity = -PLAYER_MOTION_SPEED
            pos_x += PLAYER_MOTION_SPEED
            self.current_animation = 'walk'

        elif self.is_right:
            self.x_velocity = PLAYER_MOTION_SPEED
            pos_x-= PLAYER_MOTION_SPEED
            self.current_animation = 'walk'

        elif self.is_up:
            self.y_velocity = -PLAYER_MOTION_SPEED
            pos_y += PLAYER_MOTION_SPEED

        elif self.is_down:
            self.y_velocity = PLAYER_MOTION_SPEED
            pos_y -= PLAYER_MOTION_SPEED

        if not (self.is_left or self.is_right):
            self.x_velocity = 0

            self.current_animation = 'sit'

        if not (self.is_up or self.is_down):
            self.y_velocity = 0



        self.rect.x += self.x_velocity
        self.rect.y += self.y_velocity
        camera.camera.x = pos_x
        camera.camera.y = pos_y
        self.collide(self.x_velocity, self.y_velocity, c_points)



    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 100:  # Задержка между кадрами анимации
            self.last_update = now
            if self.current_animation == 'walk':
                self.frame_index = (self.frame_index + 1) % len(self.images['walk'])
                self.image = self.images['walk'][self.frame_index][self.get_direction()]
            else:
                self.frame_index = (self.frame_index + 1) % len(self.images['sit'])
                self.image = self.images['sit'][self.frame_index][self.get_direction()]



    def collide(self, x_velocity, y_velocity, c_points):
        for point in c_points:
            p = Platform(point[0]*TILE_SIZE[0], point[1]*TILE_SIZE[1], TILE_SIZE[0], TILE_SIZE[1])
            if pg.sprite.collide_rect(self, p):
                if x_velocity > 0:
                    #print("collide right")
                    #print(p.rect)
                    self.rect.right = p.rect.left - TILE_SIZE[0] // 4
                elif x_velocity < 0:
                    #print("collide left")
                    self.rect.left = p.rect.right + TILE_SIZE[0] // 4
                elif y_velocity > 0:
                    #print("collide down")
                    self.rect.bottom = p.rect.top - TILE_SIZE[0] // 4
                elif y_velocity < 0:
                    #print("collide up")
                    self.rect.top = p.rect.bottom + TILE_SIZE[0] // 4
            else:
                self.x_velocity = 0
                self.y_velocity = 0
        self.rect.x += self.x_velocity
        self.rect.y += self.y_velocity

