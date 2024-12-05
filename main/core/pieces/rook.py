from .piece import Piece
from ..square import Square
from ..move import Move

class Rook(Piece):
    def __init__(self, color):
        super().__init__('rook', color, 5.0)  # Xe có giá trị 5.0

    def calc_moves(self, row, col, board, game_logic, validate=True):
        """
        Tính toán các nước đi hợp lệ cho quân Xe.
        :param row: Hàng hiện tại.
        :param col: Cột hiện tại.
        :param board: Đối tượng bàn cờ.
        :param game_logic: Đối tượng GameLogic để kiểm tra logic trò chơi.
        :param validate: Có kiểm tra trạng thái "chiếu" hay không.
        """
        directions = [
            (1, 0),   # Xuống
            (-1, 0),  # Lên
            (0, 1),   # Phải
            (0, -1)   # Trái
        ]

        for row_dir, col_dir in directions:
            self._add_straight_line_moves(row, col, row_dir, col_dir, board, game_logic, validate)

    def _add_straight_line_moves(self, row, col, row_dir, col_dir, board, game_logic, validate):
        """
        Xử lý di chuyển theo một hướng cho quân Xe.
        :param row: Hàng hiện tại.
        :param col: Cột hiện tại.
        :param row_dir: Hướng di chuyển hàng.
        :param col_dir: Hướng di chuyển cột.
        :param board: Bàn cờ.
        :param game_logic: Logic trò chơi.
        :param validate: Có kiểm tra trạng thái "chiếu" hay không.
        """
        current_row, current_col = row + row_dir, col + col_dir
        initial_square = Square(row, col)

        while Square.in_range(current_row, current_col):
            final_square = board.squares[current_row][current_col]
            move = Move(initial_square, Square(current_row, current_col, final_square.piece))

            if final_square.isempty():
                self._try_add_move(move, game_logic, validate)
            elif final_square.has_enemy_piece(self.color):
                self._try_add_move(move, game_logic, validate)
                break  # Không thể đi xa hơn khi gặp quân địch
            else:
                break  # Gặp quân đồng minh, không thể đi xa hơn

            # Tăng tọa độ để tiếp tục kiểm tra
            current_row += row_dir
            current_col += col_dir

    
