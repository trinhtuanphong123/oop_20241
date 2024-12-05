from ..square import Square
from ..move import Move
from .piece import Piece
from .queen import Queen


class Pawn(Piece):  # Kế thừa từ lớp Piece
    def __init__(self, color):
        self.dir = -1 if color == 'white' else 1  # Hướng di chuyển dựa trên màu sắc
        self.en_passant = False  # Biến theo dõi nước đi "en passant"
        super().__init__('pawn', color, 1.0)  # Gọi hàm khởi tạo của lớp cha

    def calc_moves(self, row, col, board, game_logic, validate=True):
        """
        Tính toán các nước đi hợp lệ cho quân tốt.
        :param row: Hàng hiện tại.
        :param col: Cột hiện tại.
        :param board: Bàn cờ hiện tại.
        :param game_logic: Logic trò chơi.
        :param validate: Có kiểm tra trạng thái "chiếu" hay không.
        """
        self.moves = []
        initial_square = Square(row, col)

        # 1. Tính nước đi thẳng
        self._add_pawn_forward_moves(row, col, board, game_logic, initial_square, validate)

        # 2. Tính nước đi chéo (ăn quân)
        self._add_pawn_diagonal_moves(row, col, board, game_logic, initial_square, validate)

        # 3. Xử lý nước đi "en passant"
        self._add_en_passant_moves(row, col, board, game_logic, initial_square, validate)

    def _add_pawn_forward_moves(self, row, col, board, game_logic, initial_square, validate):
        """
        Tính toán các nước đi thẳng cho quân tốt.
        :param row: Hàng hiện tại.
        :param col: Cột hiện tại.
        :param board: Bàn cờ hiện tại.
        :param game_logic: Logic trò chơi.
        :param initial_square: Ô hiện tại của quân tốt.
        :param validate: Có kiểm tra trạng thái "chiếu" hay không.
        """
        max_steps = 2 if not self.moved else 1
        for step in range(1, max_steps + 1):
            target_row = row + step * self.dir
            if Square.in_range(target_row) and board.squares[target_row][col].isempty():
                move = Move(initial_square, Square(target_row, col))
                self._try_add_move(move, game_logic, validate)
            else:
                break  # Ngừng kiểm tra nếu gặp vật cản

    def _add_pawn_diagonal_moves(self, row, col, board, game_logic, initial_square, validate):
        """
        Tính toán các nước đi chéo (ăn quân) cho quân tốt.
        :param row: Hàng hiện tại.
        :param col: Cột hiện tại.
        :param board: Bàn cờ hiện tại.
        :param game_logic: Logic trò chơi.
        :param initial_square: Ô hiện tại của quân tốt.
        :param validate: Có kiểm tra trạng thái "chiếu" hay không.
        """
        for delta_col in [-1, 1]:
            target_row, target_col = row + self.dir, col + delta_col
            if Square.in_range(target_row, target_col) and board.squares[target_row][target_col].has_enemy_piece(self.color):
                target_square = Square(target_row, target_col, board.squares[target_row][target_col].piece)
                move = Move(initial_square, target_square)
                self._try_add_move(move, game_logic, validate)

    def _add_en_passant_moves(self, row, col, board, game_logic, initial_square, validate):
        """
        Tính toán các nước đi "en passant" cho quân tốt.
        :param row: Hàng hiện tại.
        :param col: Cột hiện tại.
        :param board: Bàn cờ hiện tại.
        :param game_logic: Logic trò chơi.
        :param initial_square: Ô hiện tại của quân tốt.
        :param validate: Có kiểm tra trạng thái "chiếu" hay không.
        """
        en_passant_row = 3 if self.color == 'white' else 4  # Hàng en passant
        target_row = 2 if self.color == 'white' else 5  # Hàng kết thúc của en passant
        if row == en_passant_row:
            for delta_col in [-1, 1]:
                adjacent_col = col + delta_col
                if Square.in_range(adjacent_col):
                    adjacent_piece = board.squares[row][adjacent_col].piece
                    if (
                        board.squares[row][adjacent_col].has_enemy_piece(self.color)
                        and isinstance(adjacent_piece, Pawn)
                        and adjacent_piece.en_passant
                    ):
                        move = Move(initial_square, Square(target_row, adjacent_col))
                        self._try_add_move(move, game_logic, validate)

    def _try_add_move(self, move, game_logic, validate):
        """
        Kiểm tra và thêm nước đi vào danh sách.
        :param move: Nước đi cần kiểm tra.
        :param game_logic: Logic trò chơi.
        :param validate: Có kiểm tra trạng thái "chiếu" hay không.
        """
        if not validate or not game_logic.in_check(self.color, move):
            self.add_move(move)\
            
    def en_passant_check(self, initial, final):
        """
        Kiểm tra nếu quân tốt vừa thực hiện nước đi 2 ô.
        :param initial: Vị trí ban đầu.
        :param final: Vị trí cuối cùng.
        :return: True nếu nước đi là 2 ô, False nếu không.
        """
        return abs(initial.row - final.row) == 2
    
    def move_of_piece(self, board, move, testing=False):
        """
        Thực hiện nước đi cho quân tốt.
        :param board: Bàn cờ hiện tại.
        :param move: Nước đi cần thực hiện.
        :param testing: Có phải chế độ thử nghiệm không.
        """
        super().move_of_piece(board, move)  # Gọi hàm di chuyển từ lớp cha
        initial, final = move.initial, move.final

        # Nếu quân tốt di chuyển 2 ô, bật trạng thái en passant
        self.en_passant = self.en_passant_check(initial, final)

        # Nếu quân tốt đến hàng cuối, phong cấp thành Hậu (không phải trong chế độ thử nghiệm)
        if (final.row == 0 or final.row == 7) and not testing:
            board.squares[final.row][final.col].piece = Queen(self.color)

    
