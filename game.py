from cmu_graphics import *
import random
import numpy as np
from ball import Ball
from settings import *
import time 

class Game:
    #Constants
    cueballStartX = WIDTH/2+168
    startingRackX = WIDTH/2-168
    table_cx = WIDTH/2
    table_cy = HEIGHT/2-101
    other_cy = HEIGHT/2+220

    powerMeterY = 588
    powerMeterMinX = 336
    powerMeterMaxX = 543
    powerMeterLength = 300
    powerMeterHeight = 12

    boundary_x = 72
    boundary_y = 90
    boundary_width = 654
    boundary_height = 318

    wall_y = 123
    wall_height = 258
    wall_x1 = 105
    wall_x2 = 432
    wall_width = 264

    wait_time = 2

    def __init__ (self):

        self.player_balls = {'player1':[],
                             'player2':[]}

        self.current_turn = 'player1'
        self.waiting = 'player2'

        self.any_balls_in = False

        #Balls
        self.cueball = None
        self.balls = []
        self.solid_balls = []
        self.stripe_balls = []
        self.setupBalls()

        #Cue stick
        self.cuestick_angle = 0

        #Powermeter
        self.powerMeterX = 336
        #Rotation Thing
        self.center_pos = (121, 564)
        self.hit_pos = self.center_pos

        #booleans
        self.cuestickPlaced = False        
        self.isDraggingPowermeter = False
        self.isDraggingHitpos = False
        self.ballsMoving = False
        self.hitBall = False
        self.playerScratched = True

    def setupTable(self):
        drawImage('graphics/Pool Table.png', self.table_cx, self.table_cy, align='center')
        drawImage('graphics/other.png', self.table_cx, self.other_cy, align='center')
        drawImage('graphics/spin_selector.png', self.hit_pos[0], self.hit_pos[1])

        for ball in self.balls:
            x, y = ball.pos
            drawImage(ball.currSprite, int(x)-12, int(y)-12, rotateAngle=ball.rotation)

        if not self.ballsMoving and not self.playerScratched:
            drawImage('graphics/cue stick.png', int(self.cueball.pos[0])-250, int(self.cueball.pos[1])-6, rotateAngle=-self.cuestick_angle)

        self.drawPowerMeter()

        if self.any_balls_in:
            player1_type = self.player_balls['player1'][0].type
            player2_type = self.player_balls['player2'][0].type
            player1_balls_left = len(self.player_balls['player1'])
            player2_balls_left = len(self.player_balls['player2'])
            drawLabel(f'Player 1: {player1_type} | Balls Left: {player1_balls_left}', 10, 10, align='left')
            drawLabel(f'Player 2: {player2_type} | Balls Left: {player2_balls_left}', 10, 20, align='left')

        drawLabel(f'Current Turn: {self.current_turn}', self.table_cx, 10)

    def drawPowerMeter(self):
        drawRect(self.powerMeterX, self.powerMeterY, self.powerMeterLength, self.powerMeterHeight) 
        drawImage('graphics/powermeter/other cue stick.png', self.powerMeterX, self.powerMeterY, align='left')
        drawImage('graphics/powermeter/cue ball.png', 282, 594, align='left')

    def setupBalls(self):
        self.cueball = Ball(0, np.array([self.cueballStartX, self.table_cy]))
        self.balls.append(self.cueball)

        ballTypeSetup = [[0],
                        [1,0],
                        [0,8,1],
                        [1,0,1,0],
                        [0,1,1,0,1]
                        ]
        
        solids = [1, 2, 3, 4, 5, 6, 7]
        stripes = [9, 10, 11, 12, 13, 14, 15]
        
        for i in range(len(ballTypeSetup)):
            for j in range(len(ballTypeSetup[i])):
                if ballTypeSetup[i][j] == 0:
                    index = random.randint(0, len(solids)-1)
                    num = solids.pop(index)
                elif ballTypeSetup[i][j] == 1:
                    index = random.randint(0, len(stripes)-1)
                    num = stripes.pop(index)
                elif ballTypeSetup[i][j] == 8:
                    num = 8
                x_offset = i*21
                y_offset = j*24-(len(ballTypeSetup[i])-1)*12
                
                ball = Ball(num, np.array([self.startingRackX-x_offset, self.table_cy-y_offset]))
                if ball.type == 'solids':
                    self.solid_balls.append(ball)
                elif ball.type == 'stripes':
                    self.stripe_balls.append(ball)
                self.balls.append(ball)        

    def selecting_direction(self, mouseX, mouseY):
        self.cuestick_angle = int(np.degrees(np.atan2(self.cueball.pos[1]-mouseY, mouseX-self.cueball.pos[0]))%360)
    
    def place_cuestick(self):
        self.cuestickPlaced = True

    def has_clicked_powermeter(self, mouseX, mouseY):
        if (self.powerMeterX <= mouseX <= self.powerMeterX+self.powerMeterLength and
            self.powerMeterY <= mouseY <= self.powerMeterY+self.powerMeterHeight):
            self.isDraggingPowermeter = True
            self.prevX = mouseX

    def dragging_powermeter(self, mouseX):
        self.powerMeterX = self.powerMeterMinX+mouseX-self.prevX
        if self.powerMeterX  <= self.powerMeterMinX:
            self.powerMeterX  = self.powerMeterMinX
        elif self.powerMeterX >= self.powerMeterMaxX:
            self.powerMeterX  = self.powerMeterMaxX

    def release_powermeter(self):
        contactDirection = np.array([np.cos(np.radians(-self.cuestick_angle)), np.sin(np.radians(-self.cuestick_angle))])
        power = (self.powerMeterX-self.powerMeterMinX)/(self.powerMeterMaxX-self.powerMeterMinX)* 3000
        powerDirection = power * contactDirection 
        #print(f'Power: {powerDirection}')

        self.cueball.update_rotation(power)
        self.cueball.update_physics(-powerDirection)    
        self.cueball.update_animation_state(contactDirection)
        self.powerMeterX = self.powerMeterMinX
        self.ballsMoving = True
        self.isDraggingPowermeter = False
        self.prevX = None

    def has_clicked_hit_pos(self, mouseX, mouseY):
        if (self.hit_pos[0] <= mouseX < self.hit_pos[0]+12 and 
            self.hit_pos[1] <= mouseY < self.hit_pos[1]+12):
            self.isDraggingHitpos = True

    def dragging_hit_pos(self, mouseX, mouseY):
        if distance(mouseX, mouseY, self.center_pos[0], self.center_pos[1]) < 63:
            self.hit_pos = mouseX, mouseY
        else:
            degree =  angleTo(self.center_pos[0], self.center_pos[1], mouseX, mouseY)
            self.hit_pos = getPointInDir(self.center_pos[0], self.center_pos[1], degree, 63)

    def release_hit_pos(self):
        self.cueball.hit_pos = (self.center_pos[0]-self.hit_pos[0], self.center_pos[1]- self.hit_pos[1])
        self.isDraggingHitpos = False

    def ball_movement(self):
        if self.ballsMoving:
            for ball in self.balls:
                ball.apply_physics(1/FPS)
                ball.apply_friction()

                self.ball_collision()
                self.wall_collision()

                if ball.in_motion:
                    ball.nextSprite()

            if not self.areBallsMoving():
                self.ballsMoving = False
                self.hitPos = self.center_pos
                self.cueball.hitPos = (0,0)
                self.cuestickPlaced = False
                self.end()
        else:
            for ball in self.balls:
                ball.notMoving()
            

    def areBallsMoving(self):
        for ball in self.balls:
            if ball.in_motion:
                return True
        return False
    
    def wall_collision(self):
        for ball in self.balls:
            if self.wall_y < ball.pos[1] < self.wall_y + self.wall_height:
                if ball.pos[0]-ball.radius < self.boundary_x:
                    ball.pos[0] = self.boundary_x + ball.radius
                    ball.collidedWall('vertical_wall')
                    ball.update_animation_state((ball.contactDir[0] * -1, ball.contactDir[1]))
                elif ball.pos[0]+ball.radius > self.boundary_x + self.boundary_width:
                    ball.pos[0] = self.boundary_x + self.boundary_width - ball.radius
                    ball.collidedWall('vertical_wall')
                    ball.update_animation_state((ball.contactDir[0] * -1, ball.contactDir[1]))
            elif (self.wall_x1 < ball.pos[0]< self.wall_x1 + self.wall_width or self.wall_x2 < ball.pos[0]< self.wall_x2 + self.wall_width):
                if ball.pos[1]-ball.radius < self.boundary_y:
                    ball.pos[1] = self.boundary_y + ball.radius
                    ball.collidedWall('horizontal_wall')
                    ball.update_animation_state((ball.contactDir[0], ball.contactDir[1] * -1))
                elif ball.pos[1]+ball.radius > self.boundary_y + self.boundary_height:
                    ball.pos[1] = self.boundary_y + self.boundary_height - ball.radius
                    ball.collidedWall('horizontal_wall')
                    ball.update_animation_state((ball.contactDir[0], ball.contactDir[1] * -1))
            elif (ball.pos[0]< self.boundary_x - ball.radius or
              ball.pos[0] > self.boundary_x + self.boundary_width + ball.radius or 
              (ball.pos[1] < self.boundary_y - ball.radius or
              ball.pos[1] > self.boundary_y + self.boundary_height + ball.radius)):    
                
                if ball.type == 'cueball':
                    self.scratched()
                    self.cueball = Ball(0, np.array([self.cueballStartX, self.table_cy]))
                    self.balls.append(self.cueball)
                elif ball.type == '8ball':
                    self.eight_ball_in()
                elif self.any_balls_in == False:
                    self.assign_player_balls(ball)

                self.ball_in_pocket(ball)
                self.balls.remove(ball)
    
    def ball_collision(self):
        for ball1 in self.balls:
            for ball2 in self.balls:
                if ball1 != ball2:
                    dist = distance(ball1.pos[0], ball1.pos[1], ball2.pos[0], ball2.pos[1])
                    if dist <= ball1.radius + ball2.radius:
                        self.has_player_hit_ball(ball1, ball2)
                        ball1.update_animation_state((ball1.contactDir[0], ball1.contactDir[1] * -1))
                        ball2.update_animation_state((ball1.contactDir[0], ball1.contactDir[1] * -1))
                        ball1.collidedBall(ball2)


    def ball_in_pocket(self, ball):
        for player in self.player_balls:
            player_balls = self.player_balls[player]
            if ball in player_balls:
                player_balls.remove(ball)

    def scratched(self):
        print('scratched')
        self.playerScratched = True

    def eight_ball_in(self):
        if self.player_balls[self.current_turn] == []:
            print(f'{self.current_turn} won')
        else:
            print('game end')

    def assign_player_balls(self, ball):
        self.any_balls_in =  True
        if ball.type == 'solids':
            self.player_balls[self.current_turn] = self.solid_balls
            self.player_balls[self.waiting] = self.stripe_balls
        else:
            self.player_balls[self.current_turn] = self.stripe_balls
            self.player_balls[self.waiting] = self.solid_balls

    def has_player_hit_ball(self, ball1, ball2):
        if ball1.type == 'cueball' and self.hitBall == False:
            self.hitBall = True
            if (self.any_balls_in and ball2.type != self.player_balls[self.current_turn][0].type) or ball2.type == '8ball':
                self.scratched()

    def placing_cueball(self, mouseX, mouseY):
        self.cueball.pos = np.array([mouseX, mouseY])
        if mouseX-self.cueball.radius < self.cueballStartX: 
            self.cueball.pos[0] = self.cueballStartX
        elif mouseX+self.cueball.radius >  self.boundary_x + self.boundary_width:
            self.cueball.pos[0] =  self.boundary_x + self.boundary_width - self.cueball.radius
        if mouseY < self.boundary_y:
            self.cueball.pos[1] = self.boundary_y + self.cueball.radius
        elif mouseY+self.cueball.radius > self.boundary_y + self.boundary_height:
            self.cueball.pos[1] = self.boundary_y + self.boundary_height - self.cueball.radius
            
    def cueball_placed(self):
        self.playerScratched = False

    def end(self):
        if self.hitBall == False:
            self.scratched()
        else:
            self.hitBall = False
        self.current_turn, self.waiting = self.waiting, self.current_turn
        self.turn_ended = True

