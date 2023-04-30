import pygame
import os

class Rainbow(pygame.sprite.Sprite):
    def __init__(self, x, y):
            super().__init__()

            # The default enemy.png image is the same as the walking_right_image
            # Make the image point to the walking_right_image and make walking_left_image a flipped copy of the walking_right_image
            image_location = os.path.join("images", "rainbow.png")
            self.image = pygame.image.load(image_location).convert_alpha()

            self.rect = self.image.get_rect()

            self.rect.x = x
            self.rect.y = y
            self.rect.height = 35
            self.rect.width = 55