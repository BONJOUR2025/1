class Workbook:
    def __init__(self):
        self.sheetnames = []
    def __getitem__(self, key):
        return Sheet()

class Sheet:
    merged_cells = type('mc', (), {'ranges': []})()
    def cell(self, row=1, column=1, value=None):
        class Cell:
            comment = None
            value = value
        return Cell()


def load_workbook(*args, **kwargs):
    return Workbook()

