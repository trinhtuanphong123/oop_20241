from .piece import Piece
from ..square import Square
from ..move import Move

class Bishop(Piece):  # Kế thừa từ lớp Piece
    def __init__(self, color):
        super().__init__('bishop', color, 3.0)  # Giá trị quân Tượng là 3.0

    def calc_moves(self, row, col, board, game_logic, validate=True):
        """
        Tính toán các nước đi hợp lệ cho quân Tượng.
        :param row: Hàng hiện tại.
        :param col: Cột hiện tại.
        :param board: Đối tượng bàn cờ.
        :param game_logic: Đối tượng GameLogic để kiểm tra logic trò chơi.
        :param validate: Có kiểm tra trạng thái "chiếu" hay không.
        """
        directions = [
            (-1, 1), (-1, -1),  # Trên phải, trên trái
            (1, 1), (1, -1)     # Dưới phải, dưới trái
        ]

        # Tính toán nước đi trong từng hướng
        for row_dir, col_dir in directions:
            self._add_diagonal_moves(row, col, row_dir, col_dir, board, game_logic, validate)

    def _add_diagonal_moves(self, row, col, row_dir, col_dir, board, game_logic, validate):
        """
        Xử lý di chuyển theo một hướng chéo.
        :param row: Hàng hiện tại.
        :param col: Cột hiện tại.
        :param row_dir: Hướng di chuyển hàng.
        :param col_dir: Hướng di chuyển cột.
        :param board: Đối tượng bàn cờ.
        :param game_logic: Đối tượng GameLogic để kiểm tra trạng thái trò chơi.
        :param validate: Có kiểm tra trạng thái "chiếu" hay không.
        """
        current_row, current_col = row + row_dir, col + col_dir
        initial_square = Square(row, col)

        while Square.in_range(current_row, current_col):
            target_square = board.squares[current_row][current_col]
            move = Move(initial_square, Square(current_row, current_col, target_square.piece))

            if target_square.isempty():
                self._try_add_move(move, game_logic, validate)
            elif target_square.has_enemy_piece(self.color):
                self._try_add_move(move, game_logic, validate)
                break  # Dừng lại vì không thể đi xa hơn
            else:
                break  # Gặp quân đồng minh, không thể đi xa hơn

            # Tiếp tục kiểm tra nước đi trong cùng một hướng
            current_row += row_dir
            current_col += col_dir

    def _try_add_move(self, move, game_logic, validate):
        """
        Kiểm tra và thêm nước đi vào danh sách.
        :param move: Nước đi cần kiểm tra.
        :param game_logic: Đối tượng GameLogic để kiểm tra trạng thái "chiếu".
        :param validate: Có kiểm tra trạng thái "chiếu" hay không.
        """
        if not validate or not game_logic.in_check(self.color, move):
            self.add_move(move)
