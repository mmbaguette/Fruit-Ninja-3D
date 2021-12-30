import pygame
import numpy as np
import cv2
import mediapipe as mp
import math
import time

MP_DRAWING = mp.solutions.drawing_utils
MP_DRAWING_STYLES = mp.solutions.drawing_styles
MP_POSE = mp.solutions.pose

def easeOutQuad(x: float) -> float:
    return 1 - (1 - x) * (1 - x)

def blitRotateCenter(surf, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)
    surf.blit(rotated_image, new_rect)
    return new_rect, rotated_image

def knife_trail(srf, color, start, end, radius=1):
    points = []
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = max(abs(dx), abs(dy))

    # draw a bunch of circles next to each other to form a rounded line
    for i in range(distance):
        x = int(start[0] + float(i) / distance * dx)
        y = int(start[1] + float(i) / distance * dy)
        pygame.draw.circle(srf, color, (x, y), radius)
        points.append((x, y))
    return points

def add_webcam_feed(image_to_display, frame):
    # show webcam feed at bottom right corner
    mini_cam = cv2.resize(
        frame,
        (round(frame.shape[1] / 4), round(frame.shape[0] / 4)))
    overlay_image(
        image_to_display, 
        mini_cam,
        0,
        image_to_display.shape[0] - mini_cam.shape[0])

def overlay_image(l_img, s_img, x_offset, y_offset):
	l_img[y_offset:y_offset+s_img.shape[0], x_offset:x_offset+s_img.shape[1]] = s_img

def distance_2D(point1: tuple, point2: tuple):
    return math.hypot(point2[0] - point1[0], point2[1] - point1[1])

def midpoint(point1: tuple, point2: tuple, rounding = False) -> tuple:
    x1, y1 = point1
    x2, y2 = point2
    return (int(round((x1 + x2) / 2)), int(round((y1 + y2) / 2))) if rounding else ((x1 + x2) / 2, (y1 + y2) / 2)

def sub(u, v):
    return [u[i]-v[i] for i in range(len(u))]

def colliding_fruit(point1: tuple, fruit):
    try: # get_at returns IndexError if the point is NOT on the surface
        mask = pygame.mask.from_surface(fruit.rotated_img)
        rel_point = sub(point1, (fruit.x, fruit.y))

        if mask.get_at(rel_point): # if fruit touching left hand            
            return True
    except IndexError: # outside fruit_surface
        return False

# add left and right index and pinky pose landmarks if they exist
def knife_trails_and_find_hands(
    results, 
    left_knife_trail, 
    right_knife_trail,
    width, 
    height) -> tuple:
    left_hand_is_visible = True
    right_hand_is_visible = True

    if results.pose_landmarks:
        left_pinky = results.pose_landmarks.landmark[17]
        left_index = results.pose_landmarks.landmark[19]
        right_pinky = results.pose_landmarks.landmark[18]
        right_index = results.pose_landmarks.landmark[20]

        if left_pinky.visibility >= 1 and left_index.visibility >= 1:
            left_hand_is_visible = True

        if right_pinky.visibility >= 1 and right_index.visibility >= 1:
            right_hand_is_visible = True
            
        left_hand = midpoint(
            (width - left_pinky.x * width, left_pinky.y * height), 
            (width - left_index.x * width, left_index.y * height), rounding = True)
        left_knife_trail.append((left_hand, time.time()))

        right_hand = midpoint(
            (width - right_pinky.x * width, right_pinky.y * height), 
            (width - right_index.x * width, right_index.y * height), rounding = True)
        right_knife_trail.append((right_hand, time.time()))
        return (
            left_hand if left_hand_is_visible else None, 
            right_hand if right_hand_is_visible else None) # coords of hands that are cutting fruit
    else:
        return None, None

def find_and_draw_pose(pose, frame, background) -> tuple:
    background = background.copy()

    # used for mediapipe to detect pose
    image_to_process = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # improve performance by optionally marking image as not writeable
    image_to_process.flags.writeable = False
    results = pose.process(image_to_process)

    # draw pose
    MP_DRAWING.draw_landmarks(
        background,
        results.pose_landmarks,
        MP_POSE.POSE_CONNECTIONS,
        landmark_drawing_spec=MP_DRAWING_STYLES.get_default_pose_landmarks_style())
    return results, background

def array_img_to_pygame(img, width, height):
    # image needs to be rotated in pygame (weird bug)
    img = np.rot90(img)
    
    # CV2 uses BGR colors and PyGame needs RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (height, width), interpolation=cv2.INTER_LINEAR)
    pygame_img = pygame.surfarray.make_surface(img)
    return pygame_img