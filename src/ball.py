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
        self.count = 0
        self.frameDelay = 1

        self.pos = pos
        self.rotation = 0
        self.hitpos = (0, 0)
        self.contactDir = np.array([0, 0])
        self.v = np.array([0.0,0.0])
        self.contactPoint = None
  
        self.in_motion = False
        self.near_pocket = False
        self.is_in_pocket = False
        self.pocket = None

    def __lt__(self, other):
        return (self.num < other.num)
    
    def drawStaticBall(self, player):
        num = self.num%8

        if self.is_in_pocket:
            sprite_opacity = 10
        else:
            sprite_opacity = 100

        if player == 'Player 2':
            offset = 580
        else:
            offset = 55

        drawImage(self.main_sprite, 30*num+offset, 58, opacity=sprite_opacity)

    def updateRotation(self, power):
        torque = (self.hitpos[0] * self.hitpos[1]) * power
        self.rotation += torque * .01
    
    def updatePhysics(self, v):
        self.v = v

    def applyPhysics(self, dt):
        if abs(self.v[0]) > self.stop_threshold or abs(self.v[1]) > self.stop_threshold:
            self.in_motion = True
            self.pos = self.pos + (self.v * dt)
        else:
            self.in_motion = False
            self.v = np.array([0,0])

    def applyFriction(self):
        self.v = self.v * self.friction_coefficient

    def applyRotation(self):
        self.rotation *= .9

    def updateAnimationState(self, contactDir):
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
            self.animationState = 'horizontal'

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
        if collision_type == 'left' or collision_type == 'right' :
            self.v[0] *= -.8
            self.updateAnimationState((self.contactDir[0] * -1, self.contactDir[1]))
        elif collision_type == 'top' or collision_type == 'bottom':
            self.v[1] *= - .8
            self.updateAnimationState((self.contactDir[0], self.contactDir[1] * -1))
        elif collision_type == 'diagonal':
            contact_angle = np.arctan2(self.pos[1]-self.contactPoint[1], self.pos[0]-self.contactPoint[0])
            rotation_matrix = np.array([[np.cos(contact_angle), np.sin(contact_angle)], 
                                        [-np.sin(contact_angle), np.cos(contact_angle)]])
            inverse_rotation_matrix = np.array([[np.cos(contact_angle), -np.sin(contact_angle)],
                                            [np.sin(contact_angle), np.cos(contact_angle)]])
            
            self.v = self.v @ rotation_matrix

            self.v *= -.8

            self.v = self.v @ inverse_rotation_matrix





    def collidedBall(self, other, dist):
        impactVector = np.subtract(other.pos, self.pos)
        
        overlap = dist - (self.radius + other.radius)
        direction = impactVector / np.linalg.norm(impactVector) * (overlap * 0.5)
        self.pos += direction
        other.pos -= direction

        dist = self.radius + other.radius
        impactVector = impactVector / np.linalg.norm(impactVector) * dist
        velocityVector = np.subtract(other.v, self.v)

        num = np.dot(velocityVector, impactVector)
        den = dist * dist

        delta_v = np.dot(impactVector, num/den)

        self.v += delta_v
        other.v += -delta_v

    def nearPocket(self):
        self.near_pocket = True

    def inPocket(self, pocket):
        self.is_in_pocket = True
        self.pocket = pocket
    
    def collidePocketWalls(self):
        if self.pocket != None:

            if self.pocket.check_collision_with_circle(self):

                dx, dy = self.pos[0] - self.pocket.cx, self.pos[1] - self.pocket.cy

                dist = distance(self.pos[0], self.pos[1], self.pocket.cx, self.pocket.cy)

                overlap = (dist + self.radius) - self.pocket.radius
                if overlap > 0:
                    self.pos[0] -= (dx/dist) * overlap
                    self.pos[1] -= (dy/dist) * overlap
                
                normal_x = dx / dist
                normal_y = dy / dist

                normal = np.array([dx/dist, dy/dist])

                velocityVector = np.dot(self.v, normal)
                
                self.v[0] -= 2 * velocityVector * normal[0]
                self.v[1] -= 2 * velocityVector * normal[1]

        
