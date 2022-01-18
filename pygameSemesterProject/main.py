import random
from random import randrange

import pygame


# Loads an image with a less wordy function
def load_image(image_name):
    image = pygame.image.load(f'{image_name}').convert_alpha()
    return image


# Used to detect if ship and missile sprites are colliding.
def collision():
    if pygame.sprite.spritecollide(ship.sprite, missiles.sprites(), False):
        return False
    else:
        return True


# Displays the amount of missiles that have been spawned to track player score.
def display_missiles_spawned(missiles_spawned):
    side_display_text = side_font.render(f'Missiles dodged {missiles_spawned}', True, (0, 0, 0))
    side_display_text_rect = side_display_text.get_rect(center=(750, 105))
    screen.blit(side_display_text, side_display_text_rect)


# Main shi class
class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load ship image. Change to 2, 3, 4, or 5 to get a different ship size
        self.image = load_image('images/ship_h_2.png')
        # Places the ship on the right side of the play area
        self.rect = self.image.get_rect(midbottom=(400, 400))

    # Basic logic for moving the ship and getting user input
    def move_ship(self):
        keys = pygame.key.get_pressed()
        # This loops through to check if a player is pressing a certain key
        # If they are, move the ship in that direction.
        # This also includes bound checking to make sure the ship stayin in the play area.
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= 4
            if self.rect.left < 0:
                self.rect.left = 0
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += 4
            if self.rect.right > 700:
                self.rect.right = 700
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= 4
            if self.rect.top < 50:
                self.rect.top = 50
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += 4
            if self.rect.bottom > 600:
                self.rect.bottom = 600

    # Main way of updating the ship location in the main game loop
    def update(self):
        self.move_ship()

# Missile base class
class Missile(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Loads the image
        self.image = load_image('images/Missile_1_Flying_000.png')
        # Transforming the missile image to face the correct direction
        self.image = pygame.transform.rotate(self.image, 270)
        # Transforming the size of the missile to fit the play area better
        self.image = pygame.transform.scale(self.image, (100, 30))
        self.rect = self.image.get_rect(topleft=(0, randrange(50, 600)))

    # Default method of determining the speed the missile travels.
    def fire_missile(self):
        self.rect.x += random.randint(1, 10)

    # Default update method for moving the missiles
    # And removing them once they go out of bounds.
    def update(self):
        self.fire_missile()
        self.destroy()

    # Removes any missile that has gone off the play area.
    def destroy(self):
        if self.rect.right > 701:
            self.kill()


pygame.init()
screen = pygame.display.set_mode((800, 600))
missiles_spawned = 0
pygame.display.set_caption('Battleship Game')
clock = pygame.time.Clock()
game_active = False
background = load_image('images/BG.png')
header_font = pygame.font.SysFont('blackadderitc', 25)
side_font = pygame.font.SysFont('timesnewroman', 10)
# Create a variable to edit the header area text
game_name = header_font.render('A battleship game', True, (0, 0, 0))
game_name_rect = game_name.get_rect(center=(400, 25))
# Ship variables
ship = pygame.sprite.GroupSingle()
ship.add(Ship())
# Creating missiles, then adding them to a sprite group.
missiles = pygame.sprite.Group()
missiles.add(Missile())
# Setting up a UI to get user input for difficulty
menu_text = header_font.render('Press space bar to start the game.', True, (0, 0, 0))
menu_text_rect = menu_text.get_rect(center=(400, 300))


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                missiles_spawned = 0

    if game_active:
        screen.blit(background, (0, 0))
        screen.blit(game_name, game_name_rect)
        display_missiles_spawned(missiles_spawned)
        ship.draw(screen)
        ship.update()
        if int(len(missiles)) < 10:
            missiles.add(Missile())
            missiles_spawned += 1
        missiles.draw(screen)
        missiles.update()
        game_active = collision()
    else:
        screen.fill((255, 255, 255))
        screen.blit(menu_text, menu_text_rect)
        display_missiles_spawned(missiles_spawned)
        missiles.remove(missiles)

    pygame.display.update()
    clock.tick(60)
