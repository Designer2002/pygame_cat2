from player import Player, TILE_SIZE
import pygame as pg
import generator
import tracemalloc
from camera import Camera
from pathlib import Path


BASE_DIR = Path(__file__).absolute().parent

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
WHITE = (255,255,255)

FPS = 60

def run():

    pg.init()
    screen_surface = pg.display.set_mode(SCREEN_SIZE)

    timer = pg.time.Clock()


    generator.run_generation(TILE_SIZE)
    img = pg.image.load(BASE_DIR / "resources" / "images" / "map.jpg").convert()
    img_rect = img.get_rect()

    entity_sprites = pg.sprite.Group()

    hero = Player(generator.start[0], generator.start[1])

    camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, screen_surface)

    entity_sprites.add(hero)

    screen_surface.fill(WHITE)

    caption = "Cat Adventure"
    pg.display.set_caption(caption)

    is_working = True
    print(generator.collision_points)
    print(generator.working_zone)
    print(generator.start)
    start = (generator.start[0], generator.start[1])

    #старт есть и в рабочей зоне и в коллизиях. надо пересмотреть это дело

    if start in generator.collision_points:
        print("wrong")
        print(len(generator.collision_points), "cp")
    if start in generator.working_zone:
        print("right")
        print(len(generator.working_zone), "wz")

    while is_working:

        pg.display.update()
        timer.tick(FPS)

        screen_surface.fill(WHITE)

        screen_surface.blit(img, camera.camera)

        #camera.update(hero)

        for sprite in entity_sprites:
            # Используем метод apply для смещения позиции спрайта
            screen_surface.blit(sprite.image, camera.apply(sprite))

        # Отрисовка героя с учетом камеры
        screen_surface.blit(hero.image, camera.apply(hero))

        for event in pg.event.get():


            if event.type == pg.KEYDOWN:
                if event.key == pg.K_g:
                    tracemalloc.start()
                    generator.run_generation(TILE_SIZE)
                    hero = Player(generator.start[0], generator.start[1])
                    print(tracemalloc.get_traced_memory(), " - all")
                    tracemalloc.stop()
                #if event.key == pg.K_r:
                    #open
                if event.key == pg.K_a:
                    hero.is_left = True
                if event.key == pg.K_d:
                    hero.is_right = True
                if event.key == pg.K_w:
                    hero.is_up = True
                if event.key == pg.K_s:
                    hero.is_down = True

            if event.type == pg.KEYUP:
                #print(hero.rect)
                if event.key == pg.K_a:
                    hero.is_left = False
                if event.key == pg.K_d:
                    hero.is_right = False
                if event.key == pg.K_w:
                    hero.is_up = False
                if event.key == pg.K_s:
                    hero.is_down = False

            if event.type == pg.QUIT:
                is_working = False

        hero.update(generator.collision_points, camera)


    pg.quit()

if __name__ == '__main__':
    run()