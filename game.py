import pygame

from player import Player
from monster import Monster, Mummy, Alien
from comet_event import CometFallEvent
from sounds import SoundManager


class Game:
    def __init__(self):
        self.is_playing = False
        self.all_players = pygame.sprite.Group()
        self.player = Player(self)
        self.all_players.add(self.player)
        self.pressed = {}
        self.all_monsters = pygame.sprite.Group()
        self.comet_event = CometFallEvent(self)
        self.font = pygame.font.Font('assets/kode.ttf', 25)
        self.score = 0
        self.sound_manager = SoundManager()

    def start(self):
        self.is_playing = True
        self.spawn_monster(Mummy)
        self.spawn_monster(Mummy)
        self.spawn_monster(Alien)

    def game_over(self):
        self.all_monsters = pygame.sprite.Group()
        self.comet_event.all_comets = pygame.sprite.Group()
        self.comet_event.reset_percent()
        self.player.health = self.player.max_health
        self.is_playing = False
        self.score = 0
        self.sound_manager.play('game_over')

    def spawn_monster(self, monster_class_name):
        self.all_monsters.add(monster_class_name.__call__(self))

    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    def update(self, screen):
        # afficher le joueur
        screen.blit(self.player.image, self.player.rect)

        # afficher le score
        score_text = self.font.render(f"Score : {self.score}", 1, (0, 0, 0))
        screen.blit(score_text, (20, 20))

        self.player.update_health_bar(screen)
        self.player.update_animation()

        self.comet_event.update_bar(screen)

        self.comet_event.all_comets.draw(screen)
        for comet in self.comet_event.all_comets:
            comet.fall()

        # recup les projs et y appliquer move
        for projectile in self.player.all_projectiles:
            projectile.move()

        # afficher les projs
        self.player.all_projectiles.draw(screen)

        # afficher les monstres
        self.all_monsters.draw(screen)
        for monster in self.all_monsters:
            monster.forward()
            monster.update_health_bar(screen)
            monster.update_animation()

        # verifier les touches de mouvement
        if self.pressed.get(pygame.K_RIGHT) and self.player.rect.x + self.player.rect.width < screen.get_width():
            self.player.move_right()
        elif self.pressed.get(pygame.K_LEFT) and self.player.rect.x > 0:
            self.player.move_left()

        # update screen
        pygame.display.flip()

        # si le joueur ferme la fenetre
        for event in pygame.event.get():
            # evenement de fermeture
            if event.type == pygame.QUIT:
                running = False
                print('Fermeture...')
                pygame.quit()
            # evenement pour les touches de clavier
            elif event.type == pygame.KEYDOWN:
                self.pressed[event.key] = True
                # touche espace pour tier
                if event.key == pygame.K_SPACE:
                    self.player.lauch_projectile()
            elif event.type == pygame.KEYUP:
                self.pressed[event.key] = False
