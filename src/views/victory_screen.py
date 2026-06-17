import pygame


def render_victory_screen(screen, font_large, smol_font):
    screen.fill((40, 44, 52))

    title = font_large.render("Вы победили!", True, (255, 215, 0))
    title_rect = title.get_rect(center=(screen.get_width() // 2, 200))
    screen.blit(title, title_rect)

    text = font_large.render("Вы получили оффер от Сбера!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen.get_width() // 2, 280))
    screen.blit(text, text_rect)

    esc_text = smol_font.render("ESC — в главное меню", True, (200, 200, 200))
    esc_rect = esc_text.get_rect(center=(screen.get_width() // 2, screen.get_height() - 50))
    screen.blit(esc_text, esc_rect)
