from cmu_graphics import *
from PIL import Image
from settings import *
import numpy as np

def loadSpritePilImages(url, width, height, row, col, index=None):
    if isinstance(url, str):
        spritesheet = Image.open(url)
    else:
        spritesheet = url[index].image

    spritePilImages = []

    for i in range(col):
        for j in range(row):
            spriteImage = spritesheet.crop((width*j, height*i, width+width*j, height+height*i))
            alpha_channel = spriteImage.split()[3]
            if alpha_channel.getextrema()[1] > 0:
                spritePilImages.append(spriteImage)
    return spritePilImages

class Ball():
    spritesheetPilImage = loadSpritePilImages('graphics/Pool Balls.png', 243, 108, 4, 4)
    CueBallSpritesheets = [CMUImage(pilImage) for pilImage in spritesheetPilImage]
    friction_coefficient = .98
    stop_threshold = 20

    def __init__(self, num, pos):
        self.spritesheet = loadSpritePilImages(self.CueBallSpritesheets, 27, 27, 9, 4, num)   
        length = int(len(self.spritesheet)/4)

        self.main_sprite = CMUImage(self.spritesheet[0])

        self.animation_sprites = {'horizontal' : [CMUImage(self.spritesheet[i]) for i in range(1, length+1)],
                                  'diagonal_right' : [CMUImage(self.spritesheet[i]) for i in range(length+1, length*2+1)],
                                  'vertical' : [CMUImage(self.spritesheet[i]) for i in range(length*2+1, length*3+1)],
                                  'diagonal_left' : [CMUImage(self.spritesheet[i]) for i in range(length*3+1, length*4+1)]
                                }

        self.num = num
        self.type = "cueball" if num == 0 else '8ball' if num == 8 else 'solids' if 0<num<8 else 'stripes'
        self.radius = 12

        self.currSprite = self.main_sprite
        self.animationState = None
        self.index = 0
        self.frameDelay = 1
        self.count = 0
        
        self.pos = pos
        self.rotation = 0
        self.hit_pos = (0, 0)
        self.contactDir = np.array([0, 0])
        self.v = np.array([0,0], dtype=float)
  
        self.in_motion = False

    def update_rotation(self, power):
        torque = (self.hit_pos[0] * self.hit_pos[1]) * power
        self.rotation += torque * .01
    
    def update_physics(self, v):
        self.v = v

    def apply_physics(self, dt):
        if abs(self.v[0]) > self.stop_threshold or abs(self.v[1]) > self.stop_threshold:
            self.in_motion = True
            self.pos = self.pos + (self.v*dt)
        else:
            self.in_motion = False
            self.v = np.array([0,0])

    def apply_friction(self):
        self.v = self.v * self.friction_coefficient

    def apply_rotation(self):
        self.rotation *= .9

    def update_animation_state(self, contactDir):
        self.contactDir = contactDir
        x, y = contactDir[0], contactDir[1]
        if -0.5 < x < 0.05 and (y < 0 or y > 0):
            self.animationState = 'vertical'
        elif -0.05 < y < 0.05 and (x < 0 or x > 0):
            self.animationState = 'horizontal'
        elif (x > 0 and y < 0) or (x < 0 and y > 0):
            self.animationState = 'diagonal_right'
        elif (x > 0 and y > 0) or (x<0 and y < 0):
            self.animationState = 'diagonal_left'
        else:
            print(x, y)


    def nextSprite(self):
        if self.in_motion:
            if self.count == self.frameDelay: 
                animation_sprites = self.animation_sprites.get(self.animationState)
                if self.index == len(animation_sprites)-1:
                    self.index = 0
                else:
                    self.index += 1
                self.currSprite = animation_sprites[self.index]
                self.frameDelay += 4
            self.count += 1

    def notMoving(self):
        self.currSprite = self.main_sprite

    def collidedWall(self, collision_type):
        self.rotation *= 1.1
        if collision_type == 'vertical_wall':
            self.v[0] *= -.8
        elif collision_type == 'horizontal_wall':
            self.v[1] *= -.8

    def collidedBall(self, other):
        contact_angle = np.arctan2(self.pos[1]-other.pos[1], self.pos[0]-other.pos[0])

        rotation_matrix = np.array([[np.cos(contact_angle), np.sin(contact_angle)], 
                                    [-np.sin(contact_angle), np.cos(contact_angle)]])

        inverse_rotation_matrix = np.array([[np.cos(contact_angle), -np.sin(contact_angle)],
                                           [np.sin(contact_angle), np.cos(contact_angle)]])

        self.v = self.v @ rotation_matrix
        other.v = other.v @ rotation_matrix

        self.v[0], other.v[0] = other.v[0], self.v[0]

        self.v = self.v @ inverse_rotation_matrix
        other.v = other.v @ inverse_rotation_matrix

        dist = distance(self.pos[0], self.pos[1], other.pos[0], other.pos[1])
        overlap = 2 * self.radius - dist
        if overlap > 0:
            correction = overlap / 2
            direction = (other.pos - self.pos) / dist  
            self.pos -= correction * direction
            other.pos += correction * direction
