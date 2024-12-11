import pygame
class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target, w, h):
        x = -target.rect.centerx + int(w / 2)
        y = -target.rect.centery + int(h / 2)

        x = min(0, x)  # ограничиваем движение камеры по X
        y = min(0, y)  # ограничиваем движение камеры по Y
        x = max(-(self.width - w), x)  # ограничиваем движение камеры по X
        y = max(-(self.height - h), y)  # ограничиваем движение камеры по Y

        self.camera = pygame.Rect(x, y, self.width, self.height)