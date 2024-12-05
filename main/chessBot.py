from abc import ABC, abstractmethod


class AIStrategy(ABC):
    @abstractmethod
    def select_move(self, game_logic, depth):
        """Chọn nước đi tốt nhất dựa trên chiến lược AI"""
        pass


class MinimaxStrategy(AIStrategy):
    def __init__(self, evaluator):
        self.evaluator = evaluator  # Hàm đánh giá trạng thái bàn cờ

    def minimax(self, game_logic, depth, maximizing):
        """
        Hàm Minimax để tính nước đi tốt nhất.
        :param game_logic: Lớp logic quản lý trò chơi.
        :param depth: Độ sâu tìm kiếm.
        :param maximizing: True nếu đang tìm nước đi tốt nhất cho người chơi chính.
        :return: Giá trị đánh giá trạng thái tốt nhất.
        """
        if depth == 0 or game_logic.is_checkmate('white') or game_logic.is_checkmate('black'):
            return self.evaluator.evaluate(game_logic.board, game_logic)

        if maximizing:
            max_eval = float('-inf')
            for move in game_logic.generate_moves('white'):
                with game_logic.simulate_move_in_place(game_logic.board, move):
                    eval = self.minimax(game_logic, depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in game_logic.generate_moves('black'):
                with game_logic.simulate_move_in_place(game_logic.board, move):
                    eval = self.minimax(game_logic, depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval

    def select_move(self, game_logic, depth):
        """
        Chọn nước đi tốt nhất dựa trên thuật toán Minimax.
        :param game_logic: Lớp logic quản lý trò chơi.
        :param depth: Độ sâu tìm kiếm.
        :return: Nước đi tốt nhất.
        """
        best_move = None
        max_eval = float('-inf')

        for move in game_logic.generate_moves('white'):
            with game_logic.simulate_move_in_place(game_logic.board, move):
                eval = self.minimax(game_logic, depth - 1, False)
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return best_move


class NegamaxAlphaBetaStrategy(AIStrategy):
    def __init__(self, evaluator):
        self.evaluator = evaluator  # Hàm đánh giá trạng thái bàn cờ

    def negamax(self, game_logic, depth, alpha, beta, color):
        """
        Thuật toán NegaMax với cắt tỉa Alpha-Beta.
        :param game_logic: Lớp logic quản lý trò chơi.
        :param depth: Độ sâu tìm kiếm.
        :param alpha: Giá trị alpha (cắt tỉa).
        :param beta: Giá trị beta (cắt tỉa).
        :param color: 1 nếu là người chơi chính, -1 nếu là đối thủ.
        :return: Giá trị đánh giá tốt nhất.
        """
        if depth == 0 or game_logic.is_checkmate('white') or game_logic.is_checkmate('black'):
            return color * self.evaluator.evaluate(game_logic.board, game_logic)

        max_eval = float('-inf')
        for move in game_logic.generate_moves('white' if color == 1 else 'black'):
            with game_logic.simulate_move_in_place(game_logic.board, move):
                eval = -self.negamax(game_logic, depth - 1, -beta, -alpha, -color)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if alpha >= beta:
                break  # Cắt tỉa
        return max_eval

    def select_move(self, game_logic, depth):
        """
        Chọn nước đi tốt nhất dựa trên thuật toán Negamax Alpha-Beta.
        :param game_logic: Lớp logic quản lý trò chơi.
        :param depth: Độ sâu tìm kiếm.
        :return: Nước đi tốt nhất.
        """
        best_move = None
        max_eval = float('-inf')
        alpha, beta = float('-inf'), float('inf')

        for move in game_logic.generate_moves('white'):
            with game_logic.simulate_move_in_place(game_logic.board, move):
                eval = -self.negamax(game_logic, depth - 1, -beta, -alpha, -1)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
        return best_move


class AIPlayer:
    def __init__(self, strategy):
        self.strategy = strategy  # Chiến lược AI

    def set_strategy(self, strategy):
        """Thay đổi chiến lược AI."""
        self.strategy = strategy

    def select_move(self, game_logic, depth=3):
        """Chọn nước đi tốt nhất dựa trên chiến lược."""
        return self.strategy.select_move(game_logic, depth)


class Evaluator:
    def __init__(self):
        # Bảng giá trị quân cờ
        self.piece_values = {
            'king': 0,  # Vua không có giá trị cụ thể, được tính qua điểm an toàn
            'queen': 9,
            'rook': 5,
            'bishop': 3,
            'knight': 3,
            'pawn': 1
        }

        # Bảng điểm vị trí cho từng loại quân (tạm thời chỉ có cho một số quân cờ)
        self.position_tables = {
            'pawn': [ ... ],  # Như đã mô tả ở trên
            'knight': [ ... ],
            'bishop': [ ... ],
            'rook': [ ... ],
            'queen': [ ... ]
        }

    def evaluate(self, board, Game_Logic):
        """Đánh giá trạng thái bàn cờ."""
        score = 0

        for row in board.squares:
            for square in row:
                if square.has_piece():
                    piece = square.piece
                    piece_value = self.piece_values.get(piece.name, 0)
                    pos_table = self.position_tables.get(piece.name, [[0] * 8 for _ in range(8)])

                    # Giá trị quân cờ
                    base_score = piece_value if piece.color == 'white' else -piece_value

                    # Điểm vị trí
                    row_idx = piece.row if piece.color == 'white' else 7 - piece.row
                    col_idx = piece.col
                    position_score = pos_table[row_idx][col_idx] if piece.color == 'white' else -pos_table[row_idx][col_idx]

                    # Điểm kiểm soát
                    control_score = len(piece.moves) * 0.1 if piece.color == 'white' else -len(piece.moves) * 0.1

                    # Cộng dồn
                    score += base_score + position_score + control_score

        # Điểm an toàn của vua
        score += self.king_safety(board, 'white') - self.king_safety(board, 'black')

        return score

    def king_safety(self, board, color):
        """Tính toán điểm an toàn của vua."""
        king_square = board.get_king(color)
        if not king_square:
            return -float('inf') if color == 'white' else float('inf')  # Không có vua là trạng thái lỗi

        king_safety_score = 0
        for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            neighbor_row, neighbor_col = king_square.row + dx, king_square.col + dy
            if board.is_valid(neighbor_row, neighbor_col):
                square = board.squares[neighbor_row][neighbor_col]
                if square.has_team_piece(color):
                    king_safety_score += 1
        return king_safety_score
