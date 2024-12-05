import sys
import pygame
from const import WIDTH, HEIGHT, SQ_SIZE  # Import constants
from core.board import Board  # Chessboard management
from core.game_rule import GameRule  # Game logic
from player import Player  # Player management
from interface.dragger import Dragger
from core.square import Square
from core.move import Move


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')

        # Tạo các thành phần chính
        self.board = Board()
        self.dragger = Dragger()  # Đối tượng Dragger để xử lý kéo quân cờ
        self.game_logic = GameRule(self.board)

        # Khởi tạo người chơi
        self.white_player = Player("Player 1", "white")
        self.black_player = Player("Player 2", "black")

        # Lượt chơi ban đầu
        self.current_player = self.white_player

        # Trạng thái
        self.running = True
        self.valid_moves = []  # Danh sách nước đi hợp lệ của quân cờ được nhấn giữ

    def main_loop(self):
        """Main game loop."""
        while self.running:
            self._handle_events()
            self._render_screen()
            pygame.display.update()

    def _handle_events(self):
        """Xử lý các sự kiện từ người chơi."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit_game()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self._on_mouse_down(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self._on_mouse_up(event)
            elif event.type == pygame.MOUSEMOTION:
                self.dragger.mouse_pos = event.pos  # Cập nhật vị trí chuột

    def _on_mouse_down(self, event):
        """Xử lý khi nhấn chuột."""
        row, col = self._get_square_from_mouse(event.pos)
        square = self.board.squares[row][col]

        if square.has_piece() and square.piece.color == self.current_player.color:
            # Chọn quân cờ và bắt đầu kéo
            self.dragger.drag_piece(square.piece, event.pos)

            # Tính toán các nước đi hợp lệ
            self.game_logic.calculate_all_moves(self.current_player.color)
            self.valid_moves = square.piece.moves  # Lưu trữ các nước đi hợp lệ trong danh sách
            for a in range(len(self.valid_moves)):

                self.board.highlight_moves(a)  # Hiển thị các nước đi hợp lệ

    def _on_mouse_up(self, event):
        """Xử lý khi thả chuột."""
        if self.dragger.dragging:
            # Lấy tọa độ ô đích
            row, col = self._get_square_from_mouse(event.pos)

            # Lấy các ô ban đầu và cuối
            initial_square = self.board.squares[self.dragger.initial_position[0]][self.dragger.initial_position[1]]
            final_square = self.board.squares[row][col]

            # Tạo nước đi
            move = Move(initial_square, final_square)

            # Kiểm tra tính hợp lệ của nước đi
            if move in self.valid_moves:
                # Thực hiện nước đi
                self.dragger.piece.move_of_piece(self.board, move)
                self.game_logic.last_move = move  # Lưu nước đi cuối cùng

                # Kiểm tra trạng thái trò chơi
                self._check_game_status()

            # Làm rỗng danh sách nước đi hợp lệ
            self.valid_moves = []
            self.board.clear_highlights()  # Xóa màu của các ô hợp lệ

            # Kết thúc kéo
            self.dragger.undrag_piece()



    def _get_square_from_mouse(self, mouse_pos):
        """Chuyển đổi vị trí chuột sang tọa độ bàn cờ."""
        return mouse_pos[1] // SQ_SIZE, mouse_pos[0] // SQ_SIZE

    def _check_game_status(self):
        """Kiểm tra trạng thái trò chơi."""
        if self.game_logic.is_checkmate(self.current_player.color):
            print(f"Checkmate! {self.current_player.color} loses!")
            self.running = False
        elif self.game_logic.is_stalemate(self.current_player.color):
            print("Stalemate! It's a draw!")
            self.running = False
        else:
            self._switch_turn()

    def _switch_turn(self):
        """Chuyển đổi lượt chơi."""
        self.current_player = (
            self.black_player if self.current_player == self.white_player else self.white_player
        )
        self.game_logic.next_turn()

    def _render_screen(self):
        """Hiển thị giao diện trò chơi."""
        self.board.show_background(self.screen)  # Hiển thị nền bàn cờ
        self.board.show_pieces(self.screen, self.dragger)  # Hiển thị quân cờ
        if self.valid_moves:
            self.board.highlight_moves(self.valid_moves)  # Hiển thị các ô hợp lệ
        if self.game_logic.last_move:
            self.board.show_last_move(self.screen)  # Hiển thị nước đi cuối cùng
        if self.dragger.dragging:
            self.dragger.update_blit(self.screen)  # Hiển thị quân cờ đang kéo

    def _quit_game(self):
        """Thoát trò chơi."""
        self.running = False
        pygame.quit()
        sys.exit()


# Entry point
if __name__ == "__main__":
    game = Main()
    game.main_loop()
