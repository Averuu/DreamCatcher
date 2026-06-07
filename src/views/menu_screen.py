"""
Отрисовка главного меню.
"""
import pygame

def render_menu(screen, font_large, total_score, font_small):
    screen.fill((20, 233, 254))

    title = font_large.render("DreamCatcher", True, (0, 0, 0))
    title_rect = title.get_rect(center=(screen.get_width() // 2, 100))
    screen.blit(title, title_rect)

    text = font_large.render("Нажмите ПРОБЕЛ для выбора работы", True, (0, 0, 0))
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(text, text_rect)

    score_text = font_small.render(f"Всего очков: {total_score}", True, (0, 0, 0))
    screen.blit(score_text, (10, screen.get_height() - 40))

    exit_text = font_small.render("ESC для выхода", True, (0, 0, 0))
    exit_rect = exit_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 60))
    screen.blit(exit_text, exit_rect)