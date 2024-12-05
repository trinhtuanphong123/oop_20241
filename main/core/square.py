class Square:
    """
    Đại diện cho một ô trên bàn cờ.
    """
    __slots__ = ('row', 'col', 'piece')

    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece

    def __eq__(self, other):
        return isinstance(other, Square) and self.row == other.row and self.col == other.col

    def has_piece(self):
        return self.piece is not None

    def isempty(self):
        return not self.has_piece()

    def has_team_piece(self, color):
        return self.has_piece() and self.piece.color == color

    def has_enemy_piece(self, color):
        return self.has_piece() and self.piece.color != color

    @staticmethod
    def in_range(*args):
        return all(0 <= arg < 8 for arg in args)
