class GemModel:
    """class that retains characteristics of item"""

    def __init__(self, type: int, row: int, column: int):
        self.type = type
        self.row = row
        self.column = column

    def set_row_and_column(self, row: int, column: int):
        self.row = row
        self.column = column

    def set_type(self, type: int):
        self.type = type
