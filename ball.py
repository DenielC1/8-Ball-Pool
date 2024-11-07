from cmu_graphics import *
from PIL import Image

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

    def __init__(self, index, x, y):
        self.spritesheet = loadSpritePilImages(self.CueBallSpritesheets, 27, 27, 9, 4, index)   
        length = int(len(self.spritesheet)/4)

        self.main_sprite = CMUImage(self.spritesheet[0])

        self.animation_sprites = {'horizontal' : [CMUImage(self.spritesheet[i]) for i in range(1, length+1)],
                                  'diagonal_right' : [CMUImage(self.spritesheet[i]) for i in range(length+1, length*2+1)],
                                  'vertical' : [CMUImage(self.spritesheet[i]) for i in range(length*2+1, length*3+1)],
                                  'diagonal_left' : [CMUImage(self.spritesheet[i]) for i in range(length*3+1, length*4+1)]
                                }

        self.currSprite = self.main_sprite
        self.animationState = None

        self.index = 0
        self.x = x
        self.y = y

    def setState(self, state):
        self.animationState = state

    def nextSprite(self):
        animation_sprites = self.animation_sprites.get(self.animationState)
        if self.index == len(animation_sprites)-1:
            self.index = 0
        else:
            self.index += 1
        self.currSprite = animation_sprites[self.index]





