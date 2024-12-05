import pygame
from const import *

class Dragger:
    def __init__(self):
        self._mouse_pos = (0, 0)  # Lưu vị trí chuột (x, y)
        self._initial_pos = (0, 0)  # Lưu vị trí ban đầu (row, col)
        self._piece = None  # Quân cờ đang được kéo
        self._dragging = False  # Trạng thái kéo

    # Property cho vị trí chuột
    @property
    def mouse_pos(self):
        return self._mouse_pos

    @mouse_pos.setter
    def mouse_pos(self, pos):
        if not isinstance(pos, (tuple, list)) or len(pos) != 2:
            raise ValueError("mouse_pos must be a tuple/list with two elements (x, y)")
        self._mouse_pos = pos

    # Property cho vị trí ban đầu
    @property
    def initial_position(self):
        return self._initial_pos

    @initial_position.setter
    def initial_position(self, pos):
        if not isinstance(pos, (tuple, list)) or len(pos) != 2:
            raise ValueError("initial_position must be a tuple/list with two elements (x, y)")
        row = pos[1] // SQ_SIZE
        col = pos[0] // SQ_SIZE
        self._initial_pos = (row, col)

    # Property cho quân cờ
    @property
    def piece(self):
        return self._piece

    @piece.setter
    def piece(self, value):
        self._piece = value

    # Property cho trạng thái kéo
    @property
    def dragging(self):
        return self._dragging

    @dragging.setter
    def dragging(self, value):
        if not isinstance(value, bool):
            raise ValueError("Dragging must be a boolean value")
        self._dragging = value

    # Phương thức cập nhật và vẽ quân cờ
    def update_blit(self, surface, size=128):
        if self.piece:
            self.piece.set_texture(size=size)
            img = pygame.image.load(self.piece.texture)
            img_center = self.mouse_pos
            self.piece.texture_rect = img.get_rect(center=img_center)
            surface.blit(img, self.piece.texture_rect)

    # Bắt đầu kéo quân cờ
    def drag_piece(self, piece, pos):
        self.piece = piece
        self.initial_position = pos
        self.dragging = True

    # Kết thúc kéo quân cờ
    def undrag_piece(self):
        self.piece = None
        self.dragging = False
