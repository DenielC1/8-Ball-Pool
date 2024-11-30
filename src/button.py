from cmu_graphics import *

class Button:

    font_style = 'Edit Undo BRK'
    normal_font_size = 30
    hover_font_size = 33
    
    button_height = 50

    def __init__ (self, text, x, y, button_x, button_width, line_x1, line_x2):
        self.text = text
        self.x = x
        self.y = y 
        self.button_x = button_x
        self.button_width = button_width
        self.line_x1 = line_x1
        self.line_x2 = line_x2
        

        self.font_size = self.normal_font_size

        self.is_hovering = False

    def draw(self):
        drawLabel(self.text, self.x, self.y + self.button_height/2, font=self.font_style, size=self.font_size)
        if self.is_hovering:
            drawLine(self.line_x1, self.y+self.button_height, self.line_x2, self.y+self.button_height)

        #debug
        #drawRect(self.button_x, self.y, self.button_width, self.button_height, opacity=50) 
    def on_hover(self, mouseX, mouseY):
        if (self.button_x < mouseX < self.button_x + self.button_width and 
            self.y < mouseY < self.y + self.button_height):
            self.is_hovering = True
            self.font_size = self.hover_font_size
        else:
            self.is_hovering = False
            self.font_size = self.normal_font_size
    