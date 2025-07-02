class Image:
    @classmethod
    def new(cls, *args, **kwargs):
        return cls()

class ImageDraw:
    class Draw:
        def __init__(self, *args, **kwargs):
            pass
        def text(self, *args, **kwargs):
            pass

class ImageFont:
    @staticmethod
    def truetype(*args, **kwargs):
        return None
    @staticmethod
    def load_default():
        return None

