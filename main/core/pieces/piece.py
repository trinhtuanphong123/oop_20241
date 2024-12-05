import os
from typing import Optional
from abc import ABC, abstractmethod

class Piece(ABC):  # Lớp trừu tượng đại diện quân cờ
    __slots__ = ('name', 'color', 'value', 'moves', 'moved', 'texture', 'texture_rect')
    
    def __init__(self, name: str, color: str, value: int, texture: Optional[str] = None, texture_rect=None):
        self.name = name  # Tên quân cờ
        self.color = color  # Màu sắc
        self.value = value * (1 if color == 'white' else -1)  # Giá trị
        self.moves = []  # Nước đi hợp lệ
        self.moved = False  # Đã di chuyển hay chưa
        self.texture = texture  # Hình ảnh
        self.texture_rect = texture_rect  # Vị trí trên giao diện
        self.set_texture()  # Thiết lập texture
    
    @abstractmethod
    def calc_moves(self, row, col, board, bool_check=True):
        pass  # Phương thức tính nước đi (lớp con phải cài đặt)

    def set_texture(self, size=80):
        if not self.texture:  # Thiết lập hình ảnh theo kích thước
            self.texture = os.path.join(
                f'project/assets/images/imgs-{size}/{self.color}-{self.name}.png'
            )
    
    def add_move(self, move):
        self.moves.append(move)  # Thêm nước đi hợp lệ
            
    def move_of_piece(self, board, move, testing=False):
        initial = move.initial
        final = move.final

        # Thực hiện di chuyển quân cờ
        board.squares[initial.row][initial.col].piece = None
        board.squares[final.row][final.col].piece = self

        self.clear_moves()  # Xóa nước đi
        board.last_move = move  # Lưu nước đi cuối
        self.moved = True  # Đánh dấu đã di chuyển
        
    def is_valid_move(self, move):
        return move in self.moves  # Kiểm tra nước đi hợp lệ
        
    def clear_moves(self):
        self.moves.clear()  # Xóa nước đi hợp lệ

    def __repr__(self):
        return f"{self.color.capitalize()} {self.name.capitalize()}"  # Chuỗi mô tả
