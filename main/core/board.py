import pygame
import copy
from const import *
from core.pieces import King, Queen, Bishop, Rook, Knight, Pawn
from .move import Move
from .square import Square

class Board:
    """
    Quản lý trạng thái bàn cờ và các thao tác liên quan.
    """
    def __init__(self):
        self.squares = []  # Mảng 2D đại diện cho các ô vuông
        self.selected_square = None  # Ô được chọn
        self.hovered_sqr = None  # Ô đang được di chuột qua
        self.last_move = None  # Lưu nước đi cuối cùng
        self.highlighted_moves = []  # Lưu các ô được tô sáng (nước đi hợp lệ)
        self._create_squares()  # Tạo các ô vuông
        self._add_pieces('white')  # Thêm quân trắng
        self._add_pieces('black')  # Thêm quân đen

    def _create_squares(self):
        """
        Tạo mảng 2D 8x8 đại diện cho các ô vuông.
        """
        self.squares = [[Square(row, col) for col in range(COLS)] for row in range(ROWS)]

    def move_piece(self, move):
        """
        Di chuyển quân cờ từ ô bắt đầu đến ô kết thúc.
        """
        initial_square = self.squares[move.initial.row][move.initial.col]
        final_square = self.squares[move.final.row][move.final.col]

        piece = initial_square.piece
        if piece:
            move.apply(self)  # Gọi phương thức apply của Move
            self.last_move = move  # Lưu nước đi cuối cùng

    def highlight_selected_square(self, row, col):
        """
        Tô sáng ô được chọn và hiển thị các nước đi hợp lệ.
        """
        self.selected_square = self.squares[row][col]  # Lưu đối tượng Square được chọn
        piece = self.selected_square.piece
        if piece:
            self.highlighted_moves = piece.moves  # Lưu danh sách nước đi hợp lệ

    def clear_highlights(self):
        """
        Xóa tất cả các ô được tô sáng và ô được chọn.
        """
        self.highlighted_moves = []
        self.selected_square = None

    def show_background(self, surface):
        """
        Hiển thị nền bàn cờ.
        """
        for row in range(ROWS):
            for col in range(COLS):
                square = self.squares[row][col]
                color = (234, 235, 200) if (row + col) % 2 == 0 else (119, 154, 86)

                # Tô sáng ô được chọn
                if self.selected_square == square:
                    color = (246, 246, 105)  # Vàng nhạt

                rect = (col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                pygame.draw.rect(surface, color, rect)

    def show_pieces(self, surface, dragger=None):
        """
        Hiển thị các quân cờ trên bàn cờ.
        """
        for row in range(ROWS):
            for col in range(COLS):
                square = self.squares[row][col]
                if square.has_piece():
                    piece = square.piece

                    # Bỏ qua quân cờ đang được kéo
                    if dragger and dragger.dragging and dragger.piece == piece:
                        continue

                    # Hiển thị quân cờ
                    piece.set_texture(size=80)
                    img = pygame.image.load(piece.texture)
                    img_center = (col * SQ_SIZE + SQ_SIZE // 2, row * SQ_SIZE + SQ_SIZE // 2)
                    piece.texture_rect = img.get_rect(center=img_center)
                    surface.blit(img, piece.texture_rect)

    def show_valid_moves(self, surface):
        """
        Hiển thị các nước đi hợp lệ dưới dạng chấm tròn.
        """
        for move in self.highlighted_moves:
            center = (move.final.col * SQ_SIZE + SQ_SIZE // 2, move.final.row * SQ_SIZE + SQ_SIZE // 2)
            pygame.draw.circle(surface, (0, 0, 0), center, 10)

    def show_last_move(self, surface):
        """
        Hiển thị nước đi cuối cùng.
        """
        if self.last_move:
            for square in [self.last_move.initial, self.last_move.final]:
                color = (244, 247, 116) if (square.row + square.col) % 2 == 0 else (172, 195, 51)
                rect = (square.col * SQ_SIZE, square.row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        """
        Hiển thị ô được di chuột qua.
        """
        if self.hovered_sqr:
            color = (180, 180, 180)
            rect = (self.hovered_sqr.col * SQ_SIZE, self.hovered_sqr.row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            pygame.draw.rect(surface, color, rect, width=4)

    def _add_pieces(self, color):
        """
        Thêm quân cờ vào bàn cờ.
        """
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        # Thêm quân Tốt
        for col in range(COLS):
            self.squares[row_pawn][col].piece = Pawn(color)

        # Thêm các quân chính
        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for col, piece_cls in enumerate(piece_order):
            self.squares[row_other][col].piece = piece_cls(color)

    def copy(self):
        """
        Tạo bản sao bàn cờ.
        """
        new_board = Board()
        new_board.squares = copy.deepcopy(self.squares)
        new_board.last_move = copy.deepcopy(self.last_move)
        return new_board
