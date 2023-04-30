import sys
import os
import pygame
import math

from player import Player
from platform2 import Platform
from lava import Lava
from enemy import Enemy
from rainbow import Rainbow

class Level: 
    def __init__(self, platforms_list, enemies_list, rainbows_list):
       self.platforms = pygame.sprite.Group(platforms_list)
       self.enemies = pygame.sprite.Group(enemies_list)
       self.rainbows = pygame.sprite.Group(rainbows_list)

    def update(self):
        self.enemies.draw(screen)
        self.platforms.draw(screen)
        self.rainbows.draw(screen)
        self.enemies.update()

#Formats backgrounds       
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT))
      
#Changes current level to next level
def next_level(level, levels):
    new_level_index = levels.index(level) + 1
    new_level = levels[new_level_index]
    return new_level        

"""
SETUP section - preparing everything before the main loop runs
"""
pygame.init()

# Global constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
FRAME_RATE = 60

GRAVITY = 0.4
JUMP_VELOCITY = 15
score = 0

font = pygame.font.Font(None, 36)

start_ticks = pygame.time.get_ticks()

# Useful colors 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

    
# Creating the screen and the clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.set_alpha(0)  # Make alpha bits transparent
clock = pygame.time.Clock()

# Create platfroms, enemies and points for 4 levels
levels = [ 
    Level( [Platform(70, 400, 250, 50),
            Platform(300,650,400,50),
            Platform(600,300,300,50),
            Platform(150,60,300,50)], 
            [Enemy(170, 350)],
            [Rainbow(720, 255),
            Rainbow(250, 15)]),
    Level( [Platform(250,730,500,50),
            Platform(100,500,200,50),
            Platform(600,400,400,50),
            Platform(150,100,500,50)], 
            [Enemy(160, 455),
             Enemy(400, 55)],
            [Rainbow(160, 450),
            Rainbow(760, 350)]),
    Level( [Platform(300,730,400,50),
            Platform(30,450,200,50),
            Platform(500,300,450,50),
            Platform(200,75,400,50)],
            [Enemy(90, 415),
             Enemy(700, 265),
             Enemy(300, 35)],
            [Rainbow(145, 400),
            Rainbow(750, 255),
            Rainbow(400, 30) ]  ),
    Level( [Platform(300,730,400,50),
            Platform(30,450,300,50),
            Platform(670,450,300,50),
            Platform(250,150,450,50)],
            [Enemy(100, 410),
             Enemy(700, 410),
             Enemy(360, 690)],
            [Rainbow(280, 105),
            Rainbow(380, 105),
            Rainbow(480, 105),
            Rainbow(580, 105)] )
]

#set initial level
level = levels[0]

#CREATE AND GROUP LAVA
lava = Lava(0, 750, 1000,50)
lavas = pygame.sprite.Group()
lavas.add(lava)

# CREATE AND GROUP PLAYER
player = Player()
players = pygame.sprite.Group()
players.add(player)

# CREATE AND GROUP BACKGROUND, Set to clouds
background = Background(("Ochitwa_Reese_Tuesday_Final_Project/images/clouds.webp"), [0,0])
backgrounds = pygame.sprite.Group()
backgrounds.add(background)

play_game = True

while play_game:
    """
    EVENTS section - how the code reacts when users do things
    """
    seconds = (pygame.time.get_ticks()-start_ticks)/1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # When user clicks the 'x' on the window, close our game
            pygame.quit()
            sys.exit()

    keys_pressed = pygame.key.get_pressed()
    
    #RESET PLAYER TO FIRST LEVEL IF THEY FALL IN LAVA
    if pygame.sprite.collide_rect(player, lava):
        level = levels[0]
        player.rect.x = 300
        player.rect.y = 550

    # Mouse events
    mouse_pos = pygame.mouse.get_pos()  # Get position of mouse as a tuple representing the
    # (x, y) coordinate

    mouse_buttons = pygame.mouse.get_pressed()

    """
    UPDATE section - manipulate everything on the screen
    """
     # Stop the player if they hit a platform!
    for platform in level.platforms:
        if pygame.sprite.collide_rect(player, platform):
            player.y_speed = 0  # Change their y speed to 0
            player.rect.y = platform.rect.y - player.rect.height  # Make sure they aren't "stuck" in a platform

    # Player/Enemy collisions
    for enemy in level.enemies:
        if pygame.sprite.collide_rect(player, enemy):
            # If the player landed on top of the enemy, squash em
            if player.rect.y + player.rect.height <= enemy.rect.y + enemy.rect.height:
                enemy.kill()
            else:
                # Player hit the enemy from below or the side, reset to first level
                level = levels[0]
                player.rect.x = 300
                player.rect.y = 550
                
    # Player/ rainbow collions
    for rainbow in level.rainbows:
        if pygame.sprite.collide_rect(player, rainbow):
            #Kill rainbow/ add one point to score
            rainbow.kill()
            score += 1
    
    #When the player goes above screen, switch to next level and reset player to bottom
    if player.rect.y + player.rect.height < 0 and levels.index(level) < 3:
        player.rect.y = SCREEN_HEIGHT - player.rect.height - 50
        level = next_level(level, levels)

        """
        DRAW section - make everything show up on screen
        """
    #If all the rainbows havent been collected
    if score < 11:  
    
        backgrounds.draw(screen)#Draw background of clouds

        # Update the player
        player.update(keys_pressed, mouse_buttons, mouse_pos)

        #PLAYER, LAVA draw
        players.draw(screen)
        lavas.draw(screen)

        #Update level
        level.update()

        #SET FONT, SIZE
        font = pygame.font.Font("freesansbold.ttf", 32)

        #RENDER SCORE AND LEVEL NUMBER
        score_text = font.render(f'Score: {score}', True, (0, 0, 0))
        screen.blit(score_text, (10, 50))

        level_number = font.render(f'Level: {levels.index(level) + 1}', True, (0, 0, 0))
        screen.blit(level_number, (10, 10))
    
    #IF ALL RAINBOWS COLLECTED
    else:  
        #CHANGE BACKGROUND TO FISH
        background = Background(("Ochitwa_Reese_Tuesday_Final_Project/images/fish_back.jpg"), [0,0])
        backgrounds.add(background)
        backgrounds.draw(screen)
        
        #RENDER CONGRATULATION MESSAGE
        font = pygame.font.Font("freesansbold.ttf", 60)
        congrats_message = font.render(f'Congratulations', True, (255, 255, 255))
        congrats_message2 = font.render(f'You Won', True, (255, 255, 255))
        screen.blit(congrats_message, (275, 300))
        screen.blit(congrats_message2, (400, 450))

    pygame.display.flip()  # Pygame uses a double-buffer, without this we see half-completed frames
    clock.tick(FRAME_RATE)  # Pause the clock to always maintain FRAME_RATE frames per second



