import pygame as pg
import generator
import tracemalloc
from pathlib import Path

BASE_DIR = Path(__file__).absolute().parent

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
WHITE = (255,255,255)

def run():

    pg.init()

    screen_surface = pg.display.set_mode(SCREEN_SIZE)

    #tmp!!!
    temporary_player = pg.Rect(50, 50, 25, 25)
    is_moving = False

    screen_surface.fill(WHITE)

    caption = "Cat Adventure"
    pg.display.set_caption(caption)

    img = pg.image.load(BASE_DIR / "resources" / "images" / "map.png").convert()

    is_working = True
    offset = [0,0]


    while is_working:

        pg.display.update()

        screen_surface.fill(WHITE)
        generator.run_generation_from_memory(screen_surface, img, offset)


        pg.draw.rect(screen_surface, (255, 0, 0), temporary_player)

        for event in pg.event.get():

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_g:
                    tracemalloc.start()
                    generator.run_generation(screen_surface, img, (0,0))
                    print(tracemalloc.get_traced_memory(), " - all")
                    tracemalloc.stop()
                if event.key == pg.K_r:
                    generator.run_generation_from_memory(screen_surface, img, (0,0))


            if event.type == pg.MOUSEBUTTONDOWN:
                if temporary_player.collidepoint(event.pos):
                    is_moving = True
            elif event.type == pg.MOUSEBUTTONUP:
                is_moving = False
            elif event.type == pg.MOUSEMOTION and is_moving:
                temporary_player.move_ip(event.rel)
                if temporary_player.x >= SCREEN_WIDTH - temporary_player.width:
                    offset[0] += 3
                elif temporary_player.x <= 0 + temporary_player.width:
                    offset[0] -= 3
                elif temporary_player.y >= SCREEN_WIDTH - temporary_player.height:
                    offset[0] += 3
                elif temporary_player.y <= 0 + temporary_player.height:
                    offset[0] -= 3
                else:
                    offset = [pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]]


            if event.type == pg.QUIT:
                is_working = False



    pg.quit()

if __name__ == '__main__':
    run()