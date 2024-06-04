from kivy.uix.label import Label


class CustomLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (200, 50)


