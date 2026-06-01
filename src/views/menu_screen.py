import pygame

def render_menu(screen: pygame.Surface, font):
    screen.fill((20, 233, 254))
    text = font.render("Нажмите пробел для начала", True, (0, 0, 0))
    text_rect = text.get_rect(center=(screen.get_width()//2,
                                      screen.get_height()//2))
    screen.blit(text, text_rect)