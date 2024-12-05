from core.move import Move
from core.square import Square


class Player:
    def __init__(self, username, color):
        """
        Khởi tạo đối tượng Player.
        :param username: Tên người chơi.
        :param color: Màu quân cờ của người chơi ('white' hoặc 'black').
        """
        self.username = username
        self.color = color
        self.selected_square = None  # Ô vuông được chọn (nếu có)
        self.moves = []  # Danh sách các nước đi hợp lệ
        self.score = 0  # Điểm số của người chơi

    def update_moves(self, game_logic):
        """
        Cập nhật danh sách các nước đi hợp lệ.
        :param game_logic: Đối tượng GameLogic quản lý logic trò chơi.
        """
        self.moves = game_logic.generate_moves(self.color)

    def make_move(self, move, game_logic):
        """
        Thực hiện nước đi cho người chơi.
        :param move: Nước đi cần thực hiện.
        :param game_logic: Đối tượng GameLogic quản lý logic trò chơi.
        :return: True nếu nước đi hợp lệ, False nếu không.
        """
        if move in self.moves:
            piece = game_logic.board.squares[move.initial.row][move.initial.col].piece

            if piece:
                # Thực hiện nước đi
                piece.move_of_piece(game_logic.board, move)
                # Cập nhật trạng thái logic
                game_logic.set_true_en_passant(move)
                game_logic.last_move = move
                game_logic.next_turn()
                return True
        return False

    def increment_score(self, amount=1):
        """
        Tăng điểm số cho người chơi.
        :param amount: Số điểm cần tăng (mặc định là 1).
        """
        self.score += amount

    def reset_score(self):
        """Đặt lại điểm số của người chơi."""
        self.score = 0

    def __repr__(self):
        return f"Player(username={self.username}, color={self.color}, score={self.score})"


class AIPlayer(Player):
    def __init__(self, ai_strategy, color="black", username="AI Bot"):
        """
        Khởi tạo đối tượng AI Player.
        :param ai_strategy: Chiến lược AI được sử dụng (lớp AIStrategy).
        :param color: Màu quân cờ của AI ('white' hoặc 'black').
        :param username: Tên người chơi AI (mặc định là 'AI Bot').
        """
        super().__init__(username, color)
        self.ai_strategy = ai_strategy

    def select_move(self, game_logic, depth=3):
        """
        Chọn nước đi tối ưu dựa trên chiến lược AI.
        :param game_logic: Đối tượng GameLogic để quản lý logic trò chơi.
        :param depth: Độ sâu tìm kiếm của thuật toán AI.
        :return: Nước đi được chọn hoặc None nếu không có nước đi.
        """
        return self.ai_strategy.select_move(game_logic, depth)

    def make_move(self, game_logic, depth=3):
        """
        Thực hiện nước đi bằng AI.
        :param game_logic: Đối tượng GameLogic để quản lý logic trò chơi.
        :param depth: Độ sâu tìm kiếm của thuật toán AI.
        :return: Nước đi được thực hiện.
        """
        best_move = self.select_move(game_logic, depth)
        if best_move:
            piece = game_logic.board.squares[best_move.initial.row][best_move.initial.col].piece
            if piece:
                # Thực hiện di chuyển quân cờ
                piece.move_of_piece(game_logic.board, best_move)

                # Cập nhật logic trò chơi
                game_logic.set_true_en_passant(best_move)
                game_logic.last_move = best_move
                game_logic.next_turn()
        return best_move

    def __repr__(self):
        return f"AIPlayer(username={self.username}, color={self.color}, strategy={self.ai_strategy})"
