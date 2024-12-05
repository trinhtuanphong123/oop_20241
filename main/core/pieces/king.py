from .piece import Piece
from ..square import Square
from ..move import Move
from .rook import Rook

class King(Piece):  # Kế thừa từ lớp Piece
    def __init__(self, color):
        super().__init__('king', color, 100.0)  # Giá trị quân Vua rất cao
        self.left_rook = None  # Biến lưu trữ Xe trái
        self.right_rook = None  # Biến lưu trữ Xe phải

    def calc_moves(self, row, col, board, game_logic, validate=True):
        """
        Tính toán các nước đi hợp lệ cho quân Vua.
        :param row: Hàng hiện tại.
        :param col: Cột hiện tại.
        :param board: Đối tượng bàn cờ.
        :param game_logic: Đối tượng GameLogic để kiểm tra logic trò chơi.
        :param validate: Có kiểm tra trạng thái "chiếu" hay không.
        """
        directions = [
            (-1, 1), (-1, -1), (1, 1), (1, -1),  # Chéo
            (0, 1), (0, -1), (-1, 0), (1, 0)    # Thẳng
        ]

        for row_dir, col_dir in directions:
            self._add_king_move(row, col, row_dir, col_dir, board, game_logic, validate)

        # Xử lý nhập thành nếu Vua chưa di chuyển
        if not self.moved:
            self._add_castling_moves(row, col, board, game_logic, validate)

    def _add_king_move(self, row, col, row_dir, col_dir, board, game_logic, validate):
        """
        Tính toán nước đi cơ bản của quân Vua.
        """
        target_row, target_col = row + row_dir, col + col_dir

        if Square.in_range(target_row, target_col):
            target_square = board.squares[target_row][target_col]

            if target_square.isempty_or_enemy(self.color):
                initial_square = Square(row, col)
                final_square = Square(target_row, target_col, target_square.piece)
                move = Move(initial_square, final_square)

                self._try_add_move(move, game_logic, validate)

    def _add_castling_moves(self, row, col, board, game_logic, validate):
        """
        Xử lý nước đi nhập thành cho Vua.
        """
        # Nhập thành trái
        self._add_castling_move(row, col, board, game_logic, 0, 3, 2, "left", validate)
        # Nhập thành phải
        self._add_castling_move(row, col, board, game_logic, 7, 5, 6, "right", validate)

    def _add_castling_move(self, row, col, board, game_logic, rook_col, rook_target_col, king_target_col, side, validate):
        """
        Kiểm tra và thêm nước đi nhập thành cho một phía.
        """
        rook = board.squares[row][rook_col].piece
        if isinstance(rook, Rook) and not rook.moved:
            if all(board.squares[row][c].isempty() for c in range(min(col, rook_col) + 1, max(col, rook_col))):
                # Nếu các ô giữa Vua và Xe đều trống
                initial_square = Square(row, col)
                final_square = Square(row, king_target_col)
                king_move = Move(initial_square, final_square)

                if not validate or not game_logic.in_check(self.color, king_move):  # Kiểm tra trạng thái "chiếu"
                    self.add_move(king_move)

                rook_initial = Square(row, rook_col)
                rook_final = Square(row, rook_target_col)
                rook_move = Move(rook_initial, rook_final)

                if not validate or not game_logic.in_check(self.color, rook_move):  # Kiểm tra trạng thái "chiếu"
                    rook.add_move(rook_move)

                # Gán Xe tương ứng cho nhập thành
                if side == "left":
                    self.left_rook = rook
                elif side == "right":
                    self.right_rook = rook

    def _try_add_move(self, move, game_logic, validate):
        """
        Kiểm tra và thêm nước đi vào danh sách.
        """
        if not validate or not game_logic.in_check(self.color, move):
            self.add_move(move)

    def move_of_piece(self, board, move, testing=False):
        """
        Thực hiện nước đi cho quân Vua.
        """
        super().move_of_piece(board, move, testing)
        initial, final = move.initial, move.final

        if self.castling(initial, final) and not testing:  # Nếu thực hiện nhập thành
            diff = final.col - initial.col
            rook = self.left_rook if diff < 0 else self.right_rook
            rook_move = rook.moves[-1]  # Lấy nước đi của Xe trong nhập thành
            rook.move_of_piece(board, rook_move)  # Di chuyển quân Xe khi nhập thành

    def castling(self, initial, final):
        """
        Kiểm tra xem nước đi có phải nhập thành không.
        """
        return abs(initial.col - final.col) == 2
