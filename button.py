import pygame

# Define the color BLACK
BLACK = (0, 0, 0)

class Button:
    def __init__(self, text, font, text_color, hover_color, x, y, width, height):
        self.text = text
        self.font = font
        self.text_color = text_color
        self.hover_color = hover_color
        self.rect = pygame.Rect(x, y, width, height)
        self.hovered = False  # Track if the button is hovered

    def draw(self, screen):
        # Change text color if hovered
        color = self.hover_color if self.hovered else self.text_color
        text_surface = self.font.render(self.text, True, color)
        screen.blit(text_surface, (self.rect.x + (self.rect.width - text_surface.get_width()) // 2,
                                   self.rect.y + (self.rect.height - text_surface.get_height()) // 2))

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)