import pygame
import sys

from src.controllers.scene_manager import SceneManager
from src.views.menu_screen import render_menu
from src.views.game_screen import render_game

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DreamCatcher")
clock = pygame.time.Clock()

try:
    font = pygame.font.Font("./src/assets/fonts/comic.ttf", 36)
except:
    font = pygame.font.Font(None, 36)

scene_manager = SceneManager()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if scene_manager.current_scene != "GAME":
                    scene_manager.switch_to("GAME")

            if event.key == pygame.K_ESCAPE:
                if scene_manager.current_scene != "MENU":
                    scene_manager.switch_to("MENU")
                else:
                    running = False

    if scene_manager.current_scene == "MENU":
        render_menu(screen, font)
    elif scene_manager.current_scene == "GAME":
        render_game(screen, font)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
