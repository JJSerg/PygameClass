from random import randrange

import pygame


def load_image(image_name):
    image = pygame.image.load(f'{image_name}').convert_alpha()
    return image


# for now this only loads horizontal ships
def load_ships():
    ship2 = load_image('images/ship_h_two.png')
    ship3 = load_image('images/ship_h_three.png')
    ship4 = load_image('images/ship_h_four.png')
    ship5 = load_image('images/ship_h_five.png')
    return ship2, ship3, ship4, ship5


class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image('images/ship_h_five.png')
        self.rect = self.image.get_rect(midbottom=(400, 400))

    def move_ship(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= 2
            if self.rect.left < 0:
                self.rect.left = 0
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += 2
            if self.rect.right > 700:
                self.rect.right = 700
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= 2
            if self.rect.top < 50:
                self.rect.top = 50
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += 2
            if self.rect.bottom > 600:
                self.rect.bottom = 600

    def update(self):
        self.move_ship()


class Missile(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image('images/Missile_1_Flying_000.png')
        self.image = pygame.transform.rotate(self.image, 270)
        self.image = pygame.transform.scale(self.image, (150, 45))
        self.rect = self.image.get_rect(topleft=(0, randrange(50, 600)))

    def fire_missile(self):
        self.rect.x += 1

    def update(self):
        self.fire_missile()
        self.destroy()

    def destroy(self):
        if self.rect.right > 701:
            self.kill()


def collision():
    if pygame.sprite.spritecollide(ship.sprite, missiles.sprites(), False):
        return False
    else:
        return True


pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Battleship Game')
clock = pygame.time.Clock()
game_active = True
background = load_image('images/BG.png')
header_font = pygame.font.SysFont('blackadderitc', 25)
side_font = pygame.font.SysFont('timesnewroman', 10)
# Create a variable to edit the header area text
game_name = header_font.render('A battleship game', False, (0, 0, 0))
game_name_rect = game_name.get_rect(center=(400, 25))
# create a variable to hold the right side display text
side_display_text = side_font.render('Remaining ships', False, (0, 0, 0))
side_display_text_rect = side_display_text.get_rect(center=(750, 105))
# Ship variables
h_ship_two, h_ship_three, h_ship_four, h_ship_five = load_ships()
ship = pygame.sprite.GroupSingle()
ship.add(Ship())
missiles = pygame.sprite.Group()
missiles.add(Missile())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if game_active:
        screen.blit(background, (0, 0))
        screen.blit(game_name, game_name_rect)
        screen.blit(side_display_text, side_display_text_rect)
        ship.draw(screen)
        ship.update()
        missiles.draw(screen)
        missiles.update()
        game_active = collision()

    pygame.display.update()
    clock.tick(60)
