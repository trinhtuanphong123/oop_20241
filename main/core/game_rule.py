import copy
from const import ROWS, COLS
from core.pieces.pawn import Pawn
from core.pieces.king import King
from core.pieces.rook import Rook
from .square import Square
from contextlib import contextmanager


class GameRule:
    def __init__(self, board):
        self.board = board  # Bàn cờ
        self.next_player = 'white'  # Lượt chơi tiếp theo
        self.last_move = None  # Nước đi cuối cùng

    def _is_correct_turn(self, piece):
        """
        Kiểm tra xem quân cờ có thuộc lượt chơi hiện tại không.

        Args:
            piece (Piece): Quân cờ cần kiểm tra.

        Returns:
            bool: True nếu quân cờ thuộc lượt, ngược lại False.
        """
        # Giả định current_player_color có thể truy cập từ board
        current_player_color = self.board.current_player_color
        return piece.color == current_player_color
    

    def set_en_passant(self, move):
        """Cập nhật trạng thái en passant cho quân Tốt."""
        for row in range(ROWS):
            for col in range(COLS):
                square = self.board.squares[row][col]
                if isinstance(square.piece, Pawn):
                    square.piece.en_passant = False

        # Nếu quân Tốt đi 2 ô, bật trạng thái en passant
        piece = self.board.squares[move.initial.row][move.initial.col].piece
        if isinstance(piece, Pawn) and abs(move.final.row - move.initial.row) == 2:
            piece.en_passant = True

    def in_check(self, color, move=None):
        """
        Kiểm tra xem vua của người chơi có bị chiếu không.
        :param color: Màu của người chơi.
        :param move: Nước đi để kiểm tra (nếu có).
        :return: True nếu bị chiếu, ngược lại False.
        """
        with self.simulate_move_in_place(move):
            king_position = self.get_king_position(color)

            if king_position is None:
                raise ValueError(f"King for color '{color}' not found on the board.")

            # Kiểm tra xem có quân nào tấn công vua
            for row in range(ROWS):
                for col in range(COLS):
                    square = self.board.squares[row][col]
                    if square.has_enemy_piece(color):
                        piece = square.piece
                        piece.calc_moves(row, col, self.board, self, validate=False)
                        if any(
                            m.final.row == king_position[0] and m.final.col == king_position[1]
                            for m in piece.moves
                        ):
                            return True
        return False

    def get_king_position(self, color):
        """Tìm vị trí của quân vua."""
        for row in range(ROWS):
            for col in range(COLS):
                square = self.board.squares[row][col]
                if square.has_piece() and isinstance(square.piece, King) and square.piece.color == color:
                    return square.row, square.col
        return None

    def calculate_all_moves(self, color, validate=True):
        """
        Tính toán tất cả các nước đi cho người chơi.
        :param color: Màu sắc của người chơi.
        :param validate: Kiểm tra tính hợp lệ của nước đi.
        :return: Danh sách các nước đi hợp lệ.
        """
        moves = []
        for row in range(ROWS):
            for col in range(COLS):
                square = self.board.squares[row][col]
                if square.has_team_piece(color):
                    piece = square.piece
                    piece.clear_moves()
                    piece.calc_moves(row, col, self.board, self)

                    if validate:
                        piece.moves = [
                            move for move in piece.moves if not self.in_check(color, move)
                        ]
                    moves.extend(piece.moves)
        return moves
    
    def _is_within_bounds(self, position):
        """
        Kiểm tra xem vị trí có nằm trong bàn cờ không.

        Args:
            position (tuple): Vị trí (row, col).

        Returns:
            bool: True nếu nằm trong bàn cờ, ngược lại False.
        """
        row, col = position
        return 0 <= row < 8 and 0 <= col < 8
    
    def _is_self_check(self, piece, start, end):
        """
        Kiểm tra xem nước đi có dẫn đến tự chiếu không.

        Args:
            piece (Piece): Quân cờ cần di chuyển.
            start (tuple): Vị trí bắt đầu (row, col).
            end (tuple): Vị trí kết thúc (row, col).

        Returns:
            bool: True nếu tự chiếu, ngược lại False.
        """
        original_position = piece.position
        target_square = self.board.get_square(end)
        captured_piece = target_square.piece

        # Thử nước đi
        self.board.move_piece(start, end)
        king_position = self._find_king(piece.color)
        in_check = self._is_in_check(piece.color, king_position)

        # Hoàn tác nước đi
        self.board.get_square(start).place_piece(piece)
        self.board.get_square(end).place_piece(captured_piece)
        piece.position = original_position

        return in_check

    def _is_in_check(self, color, king_position):
        """
        Kiểm tra xem vua của màu `color` có bị chiếu không.

        Args:
            color (str): Màu của vua cần kiểm tra.
            king_position (tuple): Vị trí của vua.

        Returns:
            bool: True nếu vua bị chiếu, ngược lại False.
        """
        for row in self.board.grid:
            for square in row:
                piece = square.piece
                if piece and piece.color != color:
                    if king_position in piece.get_valid_moves(self.board):
                        return True
        return False
    
    def is_en_passant(self, piece, start, end):
        """
        Kiểm tra nước đi bắt chốt qua đường.
        """
        if isinstance(piece, Pawn):
            x_start, y_start = start
            x_end, y_end = end

            # Kiểm tra nước đi chéo 1 ô
            if abs(y_start - y_end) == 1 and (x_end - x_start) == (-1 if piece.color == 'white' else 1):
                # Lấy quân chốt đối thủ
                opponent_pawn = self.board.get_piece_at((x_start, y_end))
                if isinstance(opponent_pawn, Pawn) and opponent_pawn.color != piece.color:
                    # Kiểm tra nước đi trước đó của đối thủ
                    if self.last_move and self.last_move.piece == opponent_pawn:
                        if abs(self.last_move.start_pos[0] - self.last_move.end_pos[0]) == 2:
                            return True
        return False

    def is_castling(self, king, start, end):
        """
        Kiểm tra nhập thành.
        """
        if isinstance(king, King):
            x_start, y_start = start
            x_end, y_end = end

            # Kiểm tra điều kiện cơ bản
            if abs(y_end - y_start) == 2 and x_start == x_end:
                # Xác định hướng nhập thành
                rook_pos = (x_start, 0) if y_end < y_start else (x_start, 7)
                rook = self.board.get_piece_at(rook_pos)

                if rook and isinstance(rook, Rook) and not king.has_moved and not rook.has_moved:
                    # Kiểm tra đường đi không bị cản trở
                    step = 1 if y_end > y_start else -1
                    for y in range(y_start + step, y_end, step):
                        if self.board.get_piece_at((x_start, y)):
                            return False

                    # Kiểm tra không bị chiếu
                    if not self.is_in_check(king.color, (x_start, y_start)) and \
                       not self.is_in_check(king.color, (x_start, y_start + step)):
                        return True
        return False

    def is_valid_move(self, piece, start, end):
        """
        Kiểm tra xem nước đi từ start đến end có hợp lệ không.

        Args:
            piece (Piece): Quân cờ cần di chuyển.
            start (tuple): Vị trí bắt đầu (row, col).
            end (tuple): Vị trí kết thúc (row, col).

        Returns:
            bool: True nếu nước đi hợp lệ, ngược lại False.
        """
        if not self._is_within_bounds(start) or not self._is_within_bounds(end):
            return False

        if piece is None:
            return False

        if not self._is_correct_turn(piece):
            return False

        if end not in piece.get_valid_moves(self.board):
            return False

        if not self._is_path_clear(piece, start, end):
            return False

        if self._is_self_check(piece, start, end):
            return False

        return True
    