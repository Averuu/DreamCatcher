import pygame

def render_game(screen, font):
    screen.fill((20, 255, 220))
    text = font.render("Игра. ESC для выхода", True, (0, 0, 0))
    text_rect = text.get_rect(center=(screen.get_width()//2,
                                      screen.get_height()//2))
    screen.blit(text, text_rect)