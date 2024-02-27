import pygame
import math
from game import Game

pygame.init()

# Generer la fenetre
pygame.display.set_caption('21 Games')
screen = pygame.display.set_mode((1080, 720))

# ajouter un bg
background = pygame.image.load('assets/bg.jpg')

banner = pygame.image.load('assets/banner.png')
banner = pygame.transform.scale(banner, (500, 500))
banner_rect = banner.get_rect()
banner_rect.x = math.ceil(screen.get_width() / 4)

play_button = pygame.image.load('assets/button.png')
play_button = pygame.transform.scale(play_button, (400, 150))
play_button_rect = play_button.get_rect()
play_button_rect.x = math.ceil(screen.get_width()/3.33)
play_button_rect.y = math.ceil(screen.get_height()/1.5)


# charger le jeu
game = Game()

running = True
clock = pygame.time.Clock()

# boucle tant que running
while running:
    clock.tick(60)
    # applique le bg
    screen.blit(background, (0, -200))
    if game.is_playing:
        game.update(screen)
    else:
        screen.blit(banner, banner_rect)
        screen.blit(play_button, play_button_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    game.start()
                    game.sound_manager.play('click')
    pygame.display.flip()
