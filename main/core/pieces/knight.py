from ..square import Square
from .piece import Piece
from ..move import Move

class Knight(Piece):  # Kế thừa từ lớp Piece
    def __init__(self, color):
        super().__init__('knight', color, 3.0)  # Giá trị quân Mã là 3.0

    def calc_moves(self, row, col, board, game_logic, validate=True):
        """
        Tính toán các nước đi hợp lệ cho quân Mã.
        :param row: Hàng hiện tại.
        :param col: Cột hiện tại.
        :param board: Đối tượng bàn cờ.
        :param game_logic: Đối tượng GameLogic để kiểm tra logic trò chơi.
        :param validate: Có kiểm tra trạng thái "chiếu" hay không.
        """
        knight_moves = [
            (-2, 1), (-2, -1), (2, 1), (2, -1),  # Di chuyển dọc
            (1, 2), (1, -2), (-1, 2), (-1, -2)   # Di chuyển ngang
        ]

        for row_dir, col_dir in knight_moves:
            self._add_knight_move(row, col, row_dir, col_dir, board, game_logic, validate)

    def _add_knight_move(self, row, col, row_dir, col_dir, board, game_logic, validate):
        """
        Thêm một nước đi hợp lệ cho quân Mã.
        :param row: Hàng hiện tại.
        :param col: Cột hiện tại.
        :param row_dir: Hướng di chuyển hàng.
        :param col_dir: Hướng di chuyển cột.
        :param board: Đối tượng bàn cờ.
        :param game_logic: Đối tượng GameLogic để kiểm tra trạng thái "chiếu".
        :param validate: Có kiểm tra trạng thái "chiếu" hay không.
        """
        new_row, new_col = row + row_dir, col + col_dir

        if Square.in_range(new_row, new_col):
            target_square = board.squares[new_row][new_col]

            if target_square.isempty_or_enemy(self.color):
                initial_square = Square(row, col)
                final_square = Square(new_row, new_col, target_square.piece)
                move = Move(initial_square, final_square)

                self._try_add_move(move, game_logic, validate)

    def _try_add_move(self, move, game_logic, validate):
        """
        Kiểm tra và thêm nước đi vào danh sách.
        :param move: Nước đi cần kiểm tra.
        :param game_logic: Đối tượng GameLogic để kiểm tra trạng thái "chiếu".
        :param validate: Có kiểm tra trạng thái "chiếu" hay không.
        """
        if not validate or not game_logic.in_check(self.color, move):
            self.add_move(move)
