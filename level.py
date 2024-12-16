from pathlib import Path
import pygame as pg
class Level():
    def __init__(self,display_surface, player):
        # Basic setup
        self.setup_level(player)
        self.display_surface = display_surface
    def setup_level(self, player):
        BASE_DIR = Path(__file__).absolute().parent
        self.img = pg.image.load(BASE_DIR / "resources" / "images" / "map.jpg").convert()
        self.player = player
    def run(self, collision_points):
        self.player.update(collision_points)

        # Определяем границы карты
        map_left = 0
        map_right = self.img.get_rect().width
        map_top = 0
        map_bottom = self.img.get_rect().height

        # Вычисляем смещение камеры
        camera_x = -self.player.rect.centerx + self.display_surface.get_rect().centerx
        camera_y = -self.player.rect.centery + self.display_surface.get_rect().centery

        # Ограничиваем камеру по границам карты
        if self.player.rect.centerx < map_left + self.display_surface.get_rect().centerx:
            camera_x = -map_left
        if self.player.rect.centerx > map_right - self.display_surface.get_rect().centerx:
            camera_x = -(map_right - self.display_surface.get_rect().width)

        if self.player.rect.centery < map_top + self.display_surface.get_rect().centery:
            camera_y = -map_top
        if self.player.rect.centery > map_bottom - self.display_surface.get_rect().centery:
            camera_y = -(map_bottom - self.display_surface.get_rect().height)

        camera = (camera_x, camera_y)

        # Очищаем экран
        self.display_surface.fill((0, 0, 0))  # Заполняем черным цветом

        # Отрисовываем карту и игрока с учетом смещения камеры
        self.display_surface.blit(self.img, self.img.get_rect().move(camera))
        self.display_surface.blit(self.player.image, self.player.rect.move(camera))

