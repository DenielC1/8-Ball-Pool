import numpy as np

class Wall:
    def __init__(self, wall_start, wall_end, type):
        self.wall_start = wall_start
        self.wall_end = wall_end    
        self.type = type

        #debug
        self.color = 'green'

    def checkCollision(self, ball_pos, ball_radius):
        wall_vector = np.array(self.wall_end) - np.array(self.wall_start)
        ball_vector = np.array(ball_pos) - np.array(self.wall_start)

        t = np.dot(ball_vector, wall_vector) / np.dot(wall_vector, wall_vector)

        if 0 <= t <= 1:
            closest_point = np.array(self.wall_start) + t * wall_vector
            distance = np.linalg.norm(np.array(ball_pos) - closest_point)
            return distance <= ball_radius
    
    def fixBallPosition(self, ball_pos):
        if self.type == 'right':
            ball_pos[0] -= 1
        elif self.type == 'left':
            ball_pos[0] += 1
        elif self.type == 'top':
            ball_pos[1] += 1
        elif self.type == 'bottom':
            ball_pos[1] -= 1
        return ball_pos