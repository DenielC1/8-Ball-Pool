from cmu_graphics import *

class Pocket:
    def __init__(self, cx, cy, radius, offset_pos):
        self.cx = cx
        self.cy = cy
        self.radius = radius
        self.offset_pos = offset_pos

        #debug
        self.color = 'red'

    def isBallInPocket(self, ball):
        dist = distance(self.cx + self.offset_pos[0], self.cy + self.offset_pos[1], ball.pos[0], ball.pos[1])
        if dist + ball.radius < 35:
            return True
        return False
        
    def check_collision_with_circle(self, ball):
        dist = distance(self.cx, self.cy, ball.pos[0], ball.pos[1])
        
        if dist + ball.radius > self.radius:
            return True
        return False
    

            

    
    