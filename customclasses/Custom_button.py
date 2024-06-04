from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle


class CustomButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (1, 76 / 255, 41 / 256, 1)
        self.size_hint = (None, None)
        self.size = (200, 50)
        self.border = (10, 10, 10, 10)
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[10])

    def update_canvas(self, *args):
        self.rect.size = (208, 58)
        self.rect.pos = (self.center_x - self.rect.size[0] / 2, self.center_y - self.rect.size[1] / 2)
