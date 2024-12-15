import pygame as pg
class Camera:
    def __init__(self, width, height, surface):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.surface = surface

    def apply(self, entity):
        # Смещаем объект относительно камеры
        return entity.rect.move(-self.camera.x, -self.camera.y)

    def update(self, target):
        x = -target.rect.centerx + int(self.width / 2)
        y = -target.rect.centery + int(self.height / 2)

        # Ограничиваем движение камеры, чтобы она не выходила за пределы уровня
        x = min(0, x)  # Не даем камере уходить влево
        x = max(-(self.surface.get_width() - self.width), x)  # Не даем камере уходить вправо
        y = min(0, y)  # Не даем камере уходить вверх
        y = max(-(self.surface.get_height() - self.height), y)  # Не даем камере уходить вниз

        self.camera = pg.Rect(x, y, self.width, self.height)
