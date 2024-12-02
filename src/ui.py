from cmu_graphics import *
import numpy as np

class Button:

    font_style = 'Edit Undo BRK'
    normal_font_size = 30
    hover_font_size = 33
    
    sound_fx = {'click_sound' : Sound('../music/menu/Menu_Select2.wav'), 
                'release_sound' : Sound('../music/menu/release.wav')}
    
    def __init__ (self, text, x, y, button_width, button_height, line_x1, line_x2):
        self.text = text
        self.x = x
        self.y = y 
        self.button_width = button_width
        self.button_height = button_height
        self.line_x1 = line_x1
        self.line_x2 = line_x2
        
        self.font_size = self.normal_font_size

        self.is_hovering = False
        self.is_clicked = False

    def draw(self):
        drawLabel(self.text, self.x, self.y + self.button_height/2, font=self.font_style, size=self.font_size)
        if self.is_hovering:
            drawLine(self.line_x1, self.y+self.button_height, self.line_x2, self.y+self.button_height)

        #debug
        #drawRect(self.x, self.y+self.button_height/2, self.button_width, self.button_height, opacity=50, align='center')

    def onHover(self, mouseX, mouseY):
        if (self.x - self.button_width/2 < mouseX < self.x + self.button_width/2 and 
            self.y < mouseY < self.y + self.button_height):
            self.is_hovering = True
            self.font_size = self.hover_font_size
        else:
            self.is_hovering = False
            self.font_size = self.normal_font_size

    def click(self):
        self.is_clicked = True
        self.sound_fx['click_sound'].play()
        
    def release(self):
        self.is_clicked = False
        self.is_hovering = False        

class Slider(Button):
    def __init__(self, text, x, y , width, height, lineWidth):
        super().__init__(text, x, y, width, height, x-width/2, x-width/2+lineWidth)
        self.max_x = x+width/2
        self.min_x = x-width/2
        self.offset = 0

    def draw(self):
        drawLabel(self.text, self.x-self.button_width/2, self.y-self.button_height/2-20, font=self.font_style, align='left', size=18)
        drawLine(self.line_x1, self.y-self.button_height/2-10, self.line_x2, self.y-self.button_height/2-10)

        drawRect(self.x, self.y, self.button_width, self.button_height, opacity=40, align='center')
        drawRect(self.x-self.offset/2, self.y, self.button_width-self.offset, self.button_height, align='center', fill=rgb(6, 24, 31))
        drawRect(self.x+self.button_width/2-self.offset, self.y, 10, 35, align='center')

    def onHover(self, mouseX, mouseY):
        if (self.x+self.button_width/2-self.offset-5 < mouseX < self.x+self.button_width/2-self.offset+5 and
            self.y-self.button_height/2 < mouseY < self.y + self.button_height/2):
            self.is_hovering = True
        else:
            self.is_hovering = False
    
    def release(self):
        self.is_clicked = False
        self.sound_fx['release_sound'].play()

    def isDragging(self, mouseX):
        self.offset = self.max_x-mouseX
        if self.offset >= self.button_width:
            self.offset = self.button_width-1
        elif self.offset < 0:
            self.offset = 0

    def getVolumeLevel(self):
        volume_level = (self.max_x-self.offset-self.min_x)/(self.max_x-self.min_x)
        return volume_level
    
class Toggle(Button):
    def __init__(self, text, x, y , width, height, lineWidth):
        super().__init__(text, x, y, width, height, x-width/2, x-width/2+lineWidth)
        self.select_x = self.x+self.button_width/2 - height/2
        self.select_width = self.button_height - 5
        self.select_height = self.button_height - 5

        self.active = False

    def draw(self):
        drawLabel(self.text, self.x-self.button_width/2+10, self.y, font=self.font_style, align='left', size=18)
        drawRect(self.x, self.y, self.button_width, self.button_height, opacity=40, align='center')
        drawRect(self.select_x, self.y, self.select_width, self.select_height, align='center', opacity=30, border='black')

        if self.active:
            drawLine(self.select_x-10, self.y, self.select_x, self.y+10)
            drawLine(self.select_x, self.y+10, self.select_x+17, self.y-10)

    def onHover(self, mouseX, mouseY):
        if (self.select_x - self.select_width/2 < mouseX < self.select_x + self.select_width/2 and
            self.y-self.select_height/2 < mouseY < self.y + self.select_height/2):
            self.is_hovering = True
        else:
            self.is_hovering = False

    def click(self):
        self.active = not self.active
        self.is_clicked = True
        self.sound_fx['click_sound'].play()

