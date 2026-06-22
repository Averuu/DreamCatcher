import pygame
import sys
from src.controllers.scene_manager import SceneManager
from src.views.menu_screen import render_menu
from src.views.game_screen import render_game_select, get_clicked_game
from src.views.victory_screen import render_victory_screen
from src.views.hud import HUD
from src.views.mini_game_views.gardener_view import GardenerView
from src.views.mini_game_views.delivery_view import DeliveryView
from src.views.mini_game_views.analyst_view import AnalystView
from src.controllers.mini_game_controllers.gardener_controller import GardenerController
from src.controllers.mini_game_controllers.delivery_controller import DeliveryController
from src.controllers.mini_game_controllers.analyst_controller import AnalystController
from src.models.player_resume import PlayerResume
from src.utils.serialization import save_game, load_game


class DreamCatcherApp:

    MINI_GAME_SCENES = ("GARDENER", "DELIVERY", "ANALYST")
    BG_COLOR = (30, 220, 255)
    GRID_OFFSET_X = 20
    GRID_OFFSET_Y = 80

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("DreamCatcher")
        self.clock = pygame.time.Clock()

        try:
            self.font_large = pygame.font.Font("./src/assets/fonts/comic.ttf", 36)
        except Exception:
            self.font_large = pygame.font.Font(None, 36)
        self.smol_font = pygame.font.Font(None, 24)

        try:
            pygame.mixer.init()
            self.startup_sound = pygame.mixer.Sound("./src/assets/sounds/dogcheck.ogg")
        except Exception:
            self.startup_sound = None

        self.scene_manager = SceneManager()
        saved_data = load_game()
        if saved_data:
            self.player = PlayerResume.from_dict(saved_data)
        else:
            self.player = PlayerResume()

        self.gardener_view = GardenerView(cell_size=40)
        self.gardener_controller = GardenerController(self.gardener_view)

        self.delivery_view = DeliveryView(cell_size=40)
        self.delivery_controller = DeliveryController(self.delivery_view)

        self.analyst_view = AnalystView(cell_size=40)
        self.analyst_controller = AnalystController(self.analyst_view)

        self.hud = HUD(self.smol_font)
        self._controller_ready = False

        if self.startup_sound:
            self.startup_sound.play(-1)

    def run(self):
        while True:
            delta_time = self.clock.tick(60) / 1000.0
            self._update(delta_time)
            self._handle_events()
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
                    elif self.scene_manager.current_scene == "GAME_SELECT":
                        self.scene_manager.switch_to("MENU")
                    elif self.scene_manager.current_scene == "VICTORY":
                        self.scene_manager.switch_to("MENU")
                    else:
                        self.scene_manager.switch_to("GAME_SELECT")
                        self._controller_ready = False

                if event.key == pygame.K_SPACE and self.scene_manager.current_scene == "MENU":
                    self.scene_manager.switch_to("GAME_SELECT")

                if event.key == pygame.K_h and self.scene_manager.current_scene in self.MINI_GAME_SCENES:
                    controller = self.scene_manager.active_controller
                    if controller and hasattr(controller, "get_hint"):
                        controller.get_hint()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.scene_manager.current_scene == "GAME_SELECT":
                    self._handle_game_select_click(event.pos[0], event.pos[1])

            if self.scene_manager.active_controller:
                self.scene_manager.active_controller.handle_event(event)

    def _handle_game_select_click(self, mouse_x, mouse_y):
        picked_game = get_clicked_game(
            mouse_x,
            mouse_y,
            self.screen.get_width(),
            self.screen.get_height()
        )
        if picked_game is None:
            return
        if picked_game == "final":
            if self.player.total_score >= 1000:
                self.scene_manager.switch_to("VICTORY")
                self._controller_ready = False
            return

        if picked_game not in self.player.unlocked_games:
            return

        if picked_game == "gardener":
            self.scene_manager.switch_to("GARDENER", self.gardener_controller)
            self.gardener_view.set_offset(self.GRID_OFFSET_X, self.GRID_OFFSET_Y)
            self._controller_ready = False
        elif picked_game == "delivery":
            self.scene_manager.switch_to("DELIVERY", self.delivery_controller)
            self.delivery_view.set_offset(self.GRID_OFFSET_X, self.GRID_OFFSET_Y)
            self._controller_ready = False
        elif picked_game == "analyst":
            self.scene_manager.switch_to("ANALYST", self.analyst_controller)
            self.analyst_view.set_offset(self.GRID_OFFSET_X, self.GRID_OFFSET_Y)
            self._controller_ready = False

    def _update(self, delta_time):
        if self.scene_manager.current_scene not in self.MINI_GAME_SCENES:
            return

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
        current_scene = self.scene_manager.current_scene

        if current_scene == "MENU":
            render_menu(self.screen, self.font_large, self.player.total_score, self.smol_font)
            return

        if current_scene == "GAME_SELECT":
            render_game_select(self.screen, self.font_large, self.smol_font, self.player)
            return

        if current_scene == "GARDENER":
            self._render_gardener()
            return

        if current_scene == "DELIVERY":
            self._render_delivery()
            return

        if current_scene == "ANALYST":
            self._render_analyst()
            return

        if current_scene == "VICTORY":
            render_victory_screen(self.screen, self.font_large, self.smol_font)

    def _render_gardener(self):
        self.screen.fill(self.BG_COLOR)
        controller = self.scene_manager.active_controller
        if not controller:
            return

        self.gardener_view.set_offset(self.GRID_OFFSET_X, self.GRID_OFFSET_Y)
        self.gardener_view.render(self.screen, hint=controller.hint)
        self.hud.render(
            self.screen,
            game_title=controller.game_title,
            score=controller.get_score(),
            progress_text=controller.progress_text,
            message=self._make_gardener_message(controller)
        )

    def _render_delivery(self):
        self.screen.fill(self.BG_COLOR)
        controller = self.scene_manager.active_controller
        if not controller:
            return

        self.delivery_view.set_offset(self.GRID_OFFSET_X, self.GRID_OFFSET_Y)
        self.delivery_view.render(
            self.screen,
            hint=controller.hint,
            player_path=controller.player_path
        )
        self.hud.render(
            self.screen,
            game_title=controller.game_title,
            score=controller.get_score(),
            progress_text=controller.progress_text,
            message=self._make_delivery_message(controller)
        )

    def _render_analyst(self):
        self.screen.fill(self.BG_COLOR)
        controller = self.scene_manager.active_controller
        if not controller:
            return

        self.analyst_view.set_offset(self.GRID_OFFSET_X, self.GRID_OFFSET_Y)
        self.analyst_view.render(
            self.screen,
            hint=controller.hint,
            player_path=controller.player_path
        )
        self.hud.render(
            self.screen,
            game_title=controller.game_title,
            score=controller.get_score(),
            progress_text=controller.progress_text,
            message=self._make_analyst_message(controller)
        )

    def _make_analyst_message(self, controller):
        if controller.is_finished():
            if controller.hint_was_used:
                return "Маршрут найден. Подсказка была — 0 очков"
            return "Анализ завершён! Нажмите ESC в меню"
        if controller.hint_was_used:
            return "Подсказка включена — за этот маршрут будет 0 очков"
        return "Кликайте соседние клетки. H — подсказка"

    def _make_gardener_message(self, controller):
        if controller.is_finished():
            return "Уровень пройден! Нажмите ESC в меню"
        return "Нажмите H для подсказки"

    def _make_delivery_message(self, controller):
        if controller.is_finished():
            if controller.hint_was_used:
                return "Маршрут готов. Подсказка была — 0 очков"
            return "Доставка завершена! Нажмите ESC в меню"
        if controller.hint_was_used:
            return "Подсказка включена — за этот маршрут будет 0 очков"
        return "Кликайте соседние клетки. H — подсказка"

    def _quit(self):
        save_game(self.player.to_dict())
        pygame.quit()
        sys.exit()
