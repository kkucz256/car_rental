from kivy.uix.textinput import TextInput
from kivy.graphics import Color, RoundedRectangle


class CustomTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.multiline = False
        self.size_hint = (None, None)
        self.width, self.height = 200, 30
        self.background_color = (8 / 255, 32 / 255, 50 / 255, 1)
        self.foreground_color = (1, 1, 1, 1)
        self.highlight_color = (104/255, 109/255, 118/255, 1)


