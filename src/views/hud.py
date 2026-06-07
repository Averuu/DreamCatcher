"""
Универсальный HUD, отображающий информацию о текущей игре.
"""
import pygame

class HUD:
    def __init__(self, font):
        self.font = font

    def render(self, screen, game_title: str, score: int,
               progress_text: str = "", message: str = "") -> None:
        """
        Отрисовывает панель информации.
        game_title   – название игры
        score        – текущий счёт
        progress_text – дополнительная строка прогресса (например, "Сорняков: 5/20")
        message      – вспомогательное сообщение (подсказка, статус)
        """
        y = 10
        title_surf = self.font.render(game_title, True, (255, 255, 255))
        screen.blit(title_surf, (10, y))
        y += 40

        score_surf = self.font.render(f"Очки: {score}", True, (255, 255, 255))
        screen.blit(score_surf, (10, y))
        y += 40

        if progress_text:
            prog_surf = self.font.render(progress_text, True, (255, 255, 255))
            screen.blit(prog_surf, (10, y))
            y += 40

        if message:
            msg_surf = self.font.render(message, True, (255, 255, 0))
            screen.blit(msg_surf, (10, y))