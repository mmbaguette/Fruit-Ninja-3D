import numpy as np
import cv2
import pygame
from calculations import blitRotateCenter

# fruit names that can appear, and details about them
fruit_names = [
    [
        "bomb", # name
        "images/bomb.png", # filepath
        0, # points when cut
        35, # velocity (pixels per frame)
        1/7, # rarity
        (200, 200) # size on screen
    ],
    [
        "orange", # name
        "images/orange.png", # filepath
        2, # points when cut
        60, # velocity (pixels per frame)
        1/3, # rarity
        (200, 200) # size on screen
    ],
    [
        "kiwi",
        "images/kiwi.png",
        2,
        60,
        1/3,
        (200, 160)
    ],
    [
        "pineapple",
        "images/pineapple.png",
        3,
        40,
        1/6,
        (250, 500) 
    ],
    [
        "watermelon",
        "images/watermelon.png",
        4,
        40,
        1/8,
        (240, 300)
    ]
]

class Fruit():
    x = 0
    y = 0
    rotation = 0
    going_up = True
    spawn_sound_played = False
    bomb_sound = None
    rotated_img = None

    def __init__(self, name, img_filepath, starting_point, size, velocity, points):
        self.name = name
        self.velocity = round(velocity)
        self.points = points

        # things that have a special kind of property assignment
        self.x = round(starting_point[0]) # in case not rounded already
        self.y = round(starting_point[1])
        self.rotation = 0
        self.pygame_surface = pygame.image.load(img_filepath).convert_alpha()
        self.pygame_surface = pygame.transform.scale(self.pygame_surface, size)
        self.rect = self.pygame_surface.get_rect()
        self.size = self.pygame_surface.get_width(), self.pygame_surface.get_height()
        self.cv2_image = cv2.imread(img_filepath, cv2.IMREAD_UNCHANGED)

    def slice(self, point1, point2) -> tuple:
        mask = np.zeros(self.cv2_image.shape, np.uint8)
        pts = np.array([[0, 0], point1, point2,[self.cv2_image.shape[0], 0]])
        cv2.drawContours(mask, np.int32([pts]), 0, 255, -1)

        img1 = self.cv2_image.copy()
        img2 = self.cv2_image.copy()
        img1[mask == 0] = 0
        img2[mask > 0] = 0
        return img1, img2

    def get_width(self) -> int:
        return self.pygame_surface.get_width()

    def get_height(self) -> int:
        return self.pygame_surface.get_height()

    def get_length(self) -> int:
        '''Returns longest side'''
        return max(self.get_height(), self.get_width())

    def get_centre(self) -> tuple:
        return (self.x + round(self.pygame_surface.get_width() / 2), 
                self.y + round(self.pygame_surface.get_height() / 2))

    def play_bomb_sound(self):
        self.bomb_sound = pygame.mixer.Sound("sounds/bomb.wav")
        self.bomb_sound.play()

    def stop_bomb_sound(self):
        if self.bomb_sound != None:
            self.bomb_sound.stop()
        
    def draw(self, screen: pygame.Surface):
        if self.rotation >= 360:
            self.rotation = 0
        
        # rotate image from its centre without distortion
        self.rect, self.rotated_img = blitRotateCenter(
            screen,
            self.pygame_surface,
            (self.x, self.y), 
            self.rotation)