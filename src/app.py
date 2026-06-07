import pygame
import sys
from src.controllers.scene_manager import SceneManager
from src.views.menu_screen import render_menu
from src.views.game_screen import render_game_select, get_clicked_game
from src.views.hud import HUD
from src.models.mini_game_grid import Grid
from src.views.mini_game_views.gardener_view import GardenerView
from src.controllers.mini_game_controllers.gardener_controller import GardenerController
from src.models.player_resume import PlayerResume


class DreamCatcherApp:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("DreamCatcher")
        self.clock = pygame.time.Clock()

        try:
            self.font_large = pygame.font.Font("./src/assets/fonts/comic.ttf", 36)
        except (FileNotFoundError, pygame.error):
            self.font_large = pygame.font.Font(None, 36)
        self.smol_font = pygame.font.Font(None, 24)

        self.scene_manager = SceneManager()
        self.player = PlayerResume()

        self.grid = Grid(10, 10)
        self.gardener_view = GardenerView(self.grid, cell_size=40)
        self.gardener_controller = GardenerController(self.grid, self.gardener_view)
        self.hud = HUD(self.smol_font)

        self._controller_ready = False

    def run(self):
        while True:
            delta_time = self.clock.tick(60) / 1000.0
            self._handle_events()
            self._update(delta_time)
            self._render()
            pygame.display.flip()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.scene_manager.current_scene == "MENU":
                        self._quit()
                    else:
                        self.scene_manager.switch_to("MENU")
                        self._controller_ready = False

                if event.key == pygame.K_SPACE and self.scene_manager.current_scene == "MENU":
                    self.scene_manager.switch_to("GAME_SELECT")

                if event.key == pygame.K_h and self.scene_manager.current_scene == "GARDENER":
                    controller = self.scene_manager.active_controller
                    if controller and hasattr(controller, "get_hint"):
                        controller.get_hint()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.scene_manager.current_scene == "GAME_SELECT":
                    picked_game = get_clicked_game(
                        event.pos[0],
                        event.pos[1],
                        self.screen.get_width(),
                        self.screen.get_height()
                    )
                    if picked_game == "gardener":
                        self.scene_manager.switch_to("GARDENER", self.gardener_controller)
                        self.gardener_view.set_offset(20, 80)
                        self._controller_ready = False

            if self.scene_manager.active_controller:
                self.scene_manager.active_controller.handle_event(event)

    def _update(self, delta_time):
        if self.scene_manager.current_scene == "GARDENER":
            controller = self.scene_manager.active_controller
            if controller and not self._controller_ready:
                controller.setup()
                self._controller_ready = True

            if controller and controller.is_finished() and not controller.was_score_added():
                self.player.add_score(controller.get_score())
                controller.mark_score_added()

            if controller:
                controller.update(delta_time)

    def _render(self):
        if self.scene_manager.current_scene == "MENU":
            render_menu(self.screen, self.font_large, self.player.total_score, self.smol_font)

        elif self.scene_manager.current_scene == "GAME_SELECT":
            render_game_select(self.screen, self.font_large, self.smol_font, self.player)

        elif self.scene_manager.current_scene == "GARDENER":
            self.screen.fill((50, 50, 50))
            controller = self.scene_manager.active_controller
            if controller:
                offset_x, offset_y = 20, 80
                self.gardener_view.set_offset(offset_x, offset_y)
                self.gardener_view.render(self.screen, hint=controller.hint)
                self.hud.render(
                    self.screen,
                    game_title=controller.game_title,
                    score=controller.get_score(),
                    progress_text=controller.progress_text,
                    message=("Нажмите H для подсказки" if not controller.is_finished()
                             else "Уровень пройден! Нажмите ESC в меню")
                )

    @staticmethod
    def _quit():
        pygame.quit()
        sys.exit()
