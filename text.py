import pygame


class Text:
    def __init__(self, text, font_size, color, x_pos, y_pos):
        self.text = text
        self.font_size = font_size
        self.color = color
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.font = pygame.font.Font(None, self.font_size)

    def render(self, surface):
        text = self.font.render(self.text, True, self.color)
        surface.blit(text, (self.x_pos, self.y_pos))

    def find_center_position(self, window_width):
        text_width, _ = self.font.size(self.text)
        self.x_pos = (window_width - text_width) // 2
