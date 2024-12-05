from core.pieces.queen import Queen



class Move:
    """
    Đại diện cho một nước đi trên bàn cờ, bao gồm xử lý các quy tắc đặc biệt.
    """
    def __init__(self, initial, final, captured_piece=None, special_rule=None):
        self.initial = initial
        self.final = final
        self.captured_piece = captured_piece
        self.special_rule = special_rule

    def apply(self, board):
        """
        Áp dụng nước đi trên bàn cờ.
        """
        piece = board.squares[self.initial.row][self.initial.col].piece

        if self.special_rule == 'castling':
            self._apply_castling(board)
        elif self.special_rule == 'en_passant':
            self._apply_en_passant(board)
        elif self.special_rule == 'promotion':
            self._apply_promotion(board, piece)
        else:
            self._apply_normal_move(board, piece)

    def _apply_castling(self, board):
        """
        Xử lý nước đi nhập thành.
        """
        king = board.squares[self.initial.row][self.initial.col].piece
        if self.final.col > self.initial.col:  # Nhập thành cánh vua
            rook_start = (self.initial.row, 7)
            rook_end = (self.initial.row, 5)
        else:  # Nhập thành cánh hậu
            rook_start = (self.initial.row, 0)
            rook_end = (self.initial.row, 3)

        rook = board.get_piece_at(rook_start)
        board.squares[self.final.row][self.final.col].piece = king
        king.position = (self.final.row, self.final.col)
        board.squares[self.initial.row][self.initial.col].piece = None

        # Di chuyển Rook
        board.squares[rook_end[0]][rook_end[1]].piece = rook
        rook.position = rook_end
        board.squares[rook_start[0]][rook_start[1]].piece = None

    def _apply_en_passant(self, board):
        """
        Xử lý nước đi bắt chốt qua đường.
        """
        pawn = board.squares[self.initial.row][self.initial.col].piece
        board.squares[self.final.row][self.final.col].piece = pawn
        pawn.position = (self.final.row, self.final.col)
        board.squares[self.initial.row][self.initial.col].piece = None

        # Xóa quân tốt bị bắt
        capture_row = self.initial.row
        capture_col = self.final.col
        board.squares[capture_row][capture_col].piece = None

    def _apply_promotion(self, board, piece):
        """
        Xử lý phong cấp.
        """
        board.squares[self.final.row][self.final.col].piece = Queen(piece.color)
        board.squares[self.initial.row][self.initial.col].piece = None

    def _apply_normal_move(self, board, piece):
        """
        Áp dụng một nước đi thông thường.
        """
        board.squares[self.final.row][self.final.col].piece = piece
        piece.position = (self.final.row, self.final.col)
        board.squares[self.initial.row][self.initial.col].piece = None

    def undo(self, board):
        """
        Hoàn tác nước đi trên bàn cờ.
        """
        piece = board.squares[self.final.row][self.final.col].piece

        # Hoàn tác bắt chốt qua đường
        if self.special_rule == 'en_passant':
            capture_row = self.initial.row
            capture_col = self.final.col
            board.squares[capture_row][capture_col].piece = self.captured_piece

        # Hoàn tác nhập thành
        elif self.special_rule == 'castling':
            if self.final.col > self.initial.col:  # Nhập thành cánh vua
                rook_start = (self.initial.row, 7)
                rook_end = (self.initial.row, 5)
            else:  # Nhập thành cánh hậu
                rook_start = (self.initial.row, 0)
                rook_end = (self.initial.row, 3)

            rook = board.get_piece_at(rook_end)
            board.squares[rook_start[0]][rook_start[1]].piece = rook
            rook.position = rook_start
            board.squares[rook_end[0]][rook_end[1]].piece = None

        # Hoàn tác nước đi thông thường
        board.squares[self.initial.row][self.initial.col].piece = piece
        board.squares[self.final.row][self.final.col].piece = self.captured_piece
        piece.position = (self.initial.row, self.initial.col)
