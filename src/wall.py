import numpy as np
from cmu_graphics import distance

class Wall:
    def __init__(self, wall_start, wall_end, type):
        self.wall_start = wall_start
        self.wall_end = wall_end    
        self.type = type


        #debug
        self.color = 'green'

    def checkCollision(self, ball):
        wall_vector = np.array(self.wall_end) - np.array(self.wall_start)
        ball_vector = np.array(ball.pos) - np.array(self.wall_start)

        t = np.dot(ball_vector, wall_vector) / np.dot(wall_vector, wall_vector)

        if 0 <= t <= 1:
            closest_point = np.array(self.wall_start) + t * wall_vector
            ball.contactPoint = closest_point
            distance = np.linalg.norm(np.array(ball.pos) - closest_point)
            return distance <= ball.radius
    
    def fixBallPosition(self, ball):
        direction = np.subtract(ball.pos, ball.contactPoint)
        mag = np.linalg.norm(direction)
        if mag != 0:
            direction = direction / mag
            ball.pos += direction
        
    
