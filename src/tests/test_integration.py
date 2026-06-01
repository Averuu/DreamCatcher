import pygame
import sys

pygame.init()

scene = "MENU"

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DreamCatcher")
clock = pygame.time.Clock()
running = True

font = pygame.font.Font("comicsansms", 36)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.K_SPACE:
            scene = "GAME"
        if event.type == pygame.K_ESCAPE:
            scene = "MENU"
        
        if scene == "MENU":
            text = font.render("Нажмите пробел для начала", True, (0, 0, 0))
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGTH//2))
        
        if scene == "GAME":
            text = font.render("ESC для выхода", True, (0, 0, 0))
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGTH//2))

    screen.fill((20, 233, 254))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()