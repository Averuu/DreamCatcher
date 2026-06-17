import pygame

BUTTON_WIDTH = 220
BUTTON_HEIGHT = 200
BUTTON_GAP = 20

COLOR_GARDENER = (34, 139, 34)
COLOR_DELIVERY = (65, 105, 225)
COLOR_ANALYST = (148, 0, 211)

COLOR_DELIVERY_LOCKED = (25, 40, 80)
COLOR_ANALYST_LOCKED = (45, 0, 60)

COLOR_FINAL_LOCKED = (100, 100, 100)
COLOR_FINAL = (255, 215, 0)
FINAL_BUTTON_WIDTH = 300
FINAL_BUTTON_HEIGHT = 60

GAME_NAMES = ["gardener", "delivery", "analyst", "final"]
GAME_LABELS = ["Садовник", "Доставщик", "Аналитик", "Финальный оффер"]


def _make_button_rects(screen_width, screen_height):
    total_width = BUTTON_WIDTH * 3 + BUTTON_GAP * 2
    start_x = (screen_width - total_width) // 2
    start_y = (screen_height - BUTTON_HEIGHT) // 2 + 20
    rects = []
    for index in range(3):
        x = start_x + index * (BUTTON_WIDTH + BUTTON_GAP)
        rects.append(pygame.Rect(x, start_y, BUTTON_WIDTH, BUTTON_HEIGHT))
    return rects


def _make_final_button_rect(screen_width, screen_height):
    start_y = (screen_height - BUTTON_HEIGHT) // 2 + 20 + BUTTON_HEIGHT + 30
    x = (screen_width - FINAL_BUTTON_WIDTH) // 2
    return pygame.Rect(x, start_y, FINAL_BUTTON_WIDTH, FINAL_BUTTON_HEIGHT)


def _pick_button_color(game_name, player):
    if game_name == "gardener":
        return COLOR_GARDENER
    if game_name == "delivery":
        if game_name in player.unlocked_games:
            return COLOR_DELIVERY
        return COLOR_DELIVERY_LOCKED
    if game_name in player.unlocked_games:
        return COLOR_ANALYST
    return COLOR_ANALYST_LOCKED


def _pick_final_button_color(player):
    if player.total_score >= 1000:
        return COLOR_FINAL
    return COLOR_FINAL_LOCKED


def render_game_select(screen, font_large, smol_font, player):
    screen.fill((40, 44, 52))

    title = font_large.render("Выберите работу", True, (255, 255, 255))
    title_rect = title.get_rect(center=(screen.get_width() // 2, 70))
    screen.blit(title, title_rect)

    button_rects = _make_button_rects(screen.get_width(), screen.get_height())

    for index in range(3):
        game_name = GAME_NAMES[index]
        button_color = _pick_button_color(game_name, player)
        pygame.draw.rect(screen, button_color, button_rects[index])
        pygame.draw.rect(screen, (0, 0, 0), button_rects[index], 2)

        label = font_large.render(GAME_LABELS[index], True, (255, 255, 255))
        label_rect = label.get_rect(center=button_rects[index].center)
        screen.blit(label, label_rect)

    final_rect = _make_final_button_rect(screen.get_width(), screen.get_height())
    final_color = _pick_final_button_color(player)
    pygame.draw.rect(screen, final_color, final_rect)
    pygame.draw.rect(screen, (0, 0, 0), final_rect, 2)

    final_label = smol_font.render(GAME_LABELS[3], True, (255, 255, 255))
    final_label_rect = final_label.get_rect(center=final_rect.center)
    screen.blit(final_label, final_label_rect)

    score_line = smol_font.render(f"Всего очков: {player.total_score}", True, (200, 200, 200))
    screen.blit(score_line, (10, screen.get_height() - 35))

    back_line = smol_font.render("ESC — назад в меню", True, (200, 200, 200))
    back_rect = back_line.get_rect(center=(screen.get_width() // 2, screen.get_height() - 35))
    screen.blit(back_line, back_rect)


def get_clicked_game(mouse_x, mouse_y, screen_width, screen_height):
    button_rects = _make_button_rects(screen_width, screen_height)
    for index in range(3):
        if button_rects[index].collidepoint(mouse_x, mouse_y):
            return GAME_NAMES[index]
    final_rect = _make_final_button_rect(screen_width, screen_height)
    if final_rect.collidepoint(mouse_x, mouse_y):
        return "final"
    return None
