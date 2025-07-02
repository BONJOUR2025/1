class DataFrame:
    def __init__(self, data=None):
        self.data = data

    def to_excel(self, *args, **kwargs):
        pass

    def to_dict(self, *args, **kwargs):
        return {}


def read_excel(*args, **kwargs):
    return DataFrame()


