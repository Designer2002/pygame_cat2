class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Container:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.center = Point(
            int(self.x + (self.w/2)),
            int(self.y + (self.h/2))
        )

