import sys
import os
import pygame

class Player(pygame.sprite. Sprite):
    def __init__(self):
        super().__init__()

        # FOR ANIMATING
        self.isAnimating = False

        self.sprites = []
        self.sprites.append(pygame.image.load(os.path.join("Ochitwa_Reese_Tuesday_Final_Project",'images', 'fish1.png')))
        self.sprites.append(pygame.image.load(os.path.join('Ochitwa_Reese_Tuesday_Final_Project','images', 'fish2.png')))
        self.current_sprite = 0    
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()

        self.y_speed = 0
        self.x_speed = 5
        self.rect.x = 300
        self.rect.y = 550
        self.rect.height = 60
        self.rect.width = 80
        
        self.jump_cooldown = 0  # The player can jump right away!

    def animate(self):
        self.isAnimating = True

    def update(self, keys_pressed, mouse_buttons, mouse_pos):
        GRAVITY = 0.4
        JUMP_VELOCITY = 13

        teleport = False  # Must reset to False, or else the player will keep teleporting to the cursor after the first click
        direction = [0, 0]  # Reset direction so that the player stops moving when keys not pressed

        if keys_pressed[pygame.K_UP]:
            direction[1] = -1  # y direction goes up
            self.animate()
        if keys_pressed[pygame.K_DOWN]:
            direction[1] = 1  # y direction goes down
            self.animate()
        if keys_pressed[pygame.K_LEFT]:
            direction[0] = -1  # x direction goes left
            self.animate()
        if keys_pressed[pygame.K_RIGHT]:
            direction[0] = 1  # x direction goes right
            self.animate()

        # Handle jump events
        if keys_pressed[pygame.K_UP] and self.y_speed == 0:
            # This will run if SPACE is pressed
            if self.jump_cooldown == 0:  # This will run if jump_cooldown is 0
                self.jump_cooldown = 30  # Reset the cooldown to 30 frames
                self.y_speed -= JUMP_VELOCITY  # Add velocity for the jump (must be greater than gravity to work properly)
        
        if mouse_buttons[0]:  # If left mouse pressed
            teleport = True  
        if mouse_buttons[2]:  # If right mouse pressed
            teleport = True

        if teleport:
            self.teleport(mouse_pos) # if True, teleport to mouse position

        self.rect.x += direction[0] * self.x_speed

        self.y_speed += GRAVITY  # Add gravity to y_speed
        self.rect.y += self.y_speed  # Add speed to position

        if self.jump_cooldown > 0:
            self.jump_cooldown -= 1

        if self.y_speed > 20:
            self.y_speed == 20
        
        #ANIMATE PLAYER
        if self.isAnimating == True:
            self.current_sprite += 0.17

            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
                self.isAnimating = False
        
        self.image = self.sprites[int(self.current_sprite)]
            
    #TELEPORT PLAYER TO MOUSE position 
    def teleport(self, mousepos):
        x = mousepos[0]
        y = mousepos[1]
        self.rect.x = x
        self.rect.y = y
