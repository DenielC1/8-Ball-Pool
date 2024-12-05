from cmu_graphics import *
from random import randint
import numpy as np
from ball import Ball
from settings import *
from wall import Wall
from pocket import Pocket
from ui import *

class Game:
    font_style = 'Edit Undo BRK'
    
    offset_x = 159
    offset_y = 140

    top_y = offset_y
    bottom_y = offset_y+321
    left_x = offset_x-38
    right_x = offset_x-38+657

    collidables = [Wall((offset_x, offset_y), (offset_x+258, offset_y), 'top'), 
                Wall((offset_x+258+66, offset_y), (offset_x+66+2*258, offset_y), 'top'),
                Wall((offset_x, offset_y+321), (offset_x+258, offset_y+321), 'bottom'),
                Wall((offset_x+258+66, offset_y+321), (offset_x+66+2*258, offset_y+321), 'bottom'),
                Wall((offset_x-38, offset_y+37), (offset_x-38, offset_y+37+246), 'left'),
                Wall((offset_x-38+657, offset_y+37), (offset_x-38+657, offset_y+37+246), 'right'),
                Wall((offset_x, offset_y), (133, 107), 'diagonal'),
                Wall((offset_x+258, offset_y), (428, 107), 'diagonal'),
                Wall((offset_x+258+66, offset_y), (474, 107), 'diagonal'),
                Wall((offset_x+66+2*258, offset_y), (767, 107), 'diagonal'),
                Wall((offset_x-38+657, offset_y+37), (809, 151), 'diagonal'),
                Wall((offset_x-38+657, offset_y+37+246), (809, 449), 'diagonal'),
                Wall((offset_x+66+2*258, offset_y+321), (766, 491), 'diagonal'),
                Wall((offset_x+258+66, offset_y+321), (472, 495), 'diagonal'),
                Wall((offset_x+258, offset_y+321), (429, 495), 'diagonal'),
                Wall((offset_x, offset_y+321), (133, 491), 'diagonal'),
                Wall((offset_x-38, offset_y+37+246), (88, 453), 'diagonal'),
                Wall((offset_x-38, offset_y+37), (89, 148), 'diagonal')]
    
        
    pockets_entrance = [Wall((118, 169), (152, 135), 'top_left'), 
               Wall((118+666,169), (82+666, 135), 'top_right'),
               Wall((82+666, 169+294), (118+666, 135+294), 'bottom_right'),
               Wall((152, 169+294), (118, 135+294), 'bottom_left'),
               Wall((offset_x+261, offset_y-3), (offset_x+60+261, offset_y-3), 'top_middle'),
               Wall((offset_x+261, offset_y+324), (offset_x+60+261, offset_y+324), 'bottom_middle')]
    
    pockets = [Pocket(116, 133, 28, (-3,-3)),
            Pocket(116, 465, 28, (-3, 3)),
            Pocket(785, 133, 28, (3, -3)),
            Pocket(450, 122, 24, (0, -7)),
            Pocket(450, 476, 24, (0, 7)),
            Pocket(785, 465, 28, (3, 3))]
    
    cueball_start_x = WIDTH/2+168
    starting_rack_x = WIDTH/2-168
    table_cx = WIDTH/2
    table_cy = HEIGHT/2-101
    other_cy = HEIGHT/2+220

    power_meter_y = 638
    power_meter_min_x = 386
    power_meter_max_x = 593
    power_meter_length = 300
    power_meter_height = 12

    boundary_x = 123
    boundary_y = 140
    boundary_width = 654
    boundary_height = 318

    def __init__ (self):
    
        self.player_balls = {'Player 1':[],
                             'Player 2':[]}

        self.current_turn = 'Player 1'
        self.waiting = 'Player 2'

        self.cueball = None
        self.balls = []
        self.solid_balls = []
        self.stripe_balls = []
        self.balls_in_pocket = []
        self.setupBalls()

        self.cuestick_angle = 0

        self.power_meter_x = 386

        self.center_pos = (171, 615)
        self.hitpos = self.center_pos

        self.cuestick_placed = False        
        self.is_dragging_powermeter = False
        self.is_dragging_hitpos = False
        self.is_dragging_cueball = False
        self.is_placing_cueball = True
        self.is_break_shot = True
        self.balls_moving = False
        
        self.game_started = True
        self.end_of_turn = True
        self.game_over =  False

        self.selecting_pocket = False
        self.selected_pocket = None
        self.winner = None

        self.player_hit_ball = False
        self.player_scratched = True
        self.no_balls_in = True

        self.found_collision = False

        self.player_blinking_timer = 0
        self.cueball_blinking_timer = 0
        self.cueball_blinking_timer = 0
        self.text_timer= 0

    def drawGame(self):
        drawImage('graphics/Pool Table.png', self.table_cx, self.table_cy, align='center')
    
        if not self.end_of_turn and self.is_break_shot and self.is_placing_cueball:
            drawLine(self.cueball_start_x, 141, self.cueball_start_x, 458, fill=rgb(203,203,203), dashes=(8, 6))

        for ball in self.balls:
            x, y = ball.pos
            if ball.type == 'cueball' and self.is_placing_cueball:
                if not self.end_of_turn and not self.balls_moving and not self.selecting_pocket:
                    drawImage('graphics/cueball indicator.png', int(x) -12, int(y)-12)
                    if self.cueball_blinking_timer <5:
                        drawImage(ball.currSprite, int(x)-12, int(y)-12, rotateAngle=ball.rotation)
                    elif self.cueball_blinking_timer >10:
                        self.cueball_blinking_timer = 0   
            else:
                drawImage(ball.currSprite, int(x)-12, int(y)-12, rotateAngle=ball.rotation)

        if not self.end_of_turn and not self.balls_moving and not self.player_scratched and not self.selecting_pocket:
            drawImage('graphics/cue stick.png', int(self.cueball.pos[0])-250, int(self.cueball.pos[1])-6, rotateAngle=-self.cuestick_angle)

        drawImage('graphics/other.png', self.table_cx, self.other_cy, align='center')
        drawImage('graphics/spin_selector.png', self.hitpos[0], self.hitpos[1])

        self.drawScoreboard()
        self.drawPowerMeter()
        
        if not self.no_balls_in and self.ballsLeft(self.current_turn) == 0 and self.selecting_pocket and not self.game_over:
            self.drawPocketSelection()
        
        if self.end_of_turn:
            self.drawAnimations()

        # for wall in self.collidables:
        #     drawLine(wall.wall_start[0], wall.wall_start[1], wall.wall_end[0],  wall.wall_end[1], fill=wall.color)
        # # for wall in self.pockets:
        # #    drawLine(wall.wall_start[0], wall.wall_start[1], wall.wall_end[0],  wall.wall_end[1], fill=wall.color)
        # for wall in self.pockets_entrance:
        #     drawLine(wall.wall_start[0], wall.wall_start[1], wall.wall_end[0],  wall.wall_end[1], fill=wall.color)

        # drawRect(self.boundary_x, self.boundary_y, self.boundary_width, self.boundary_height, fill='red', opacity= 20)

    def drawScoreboard(self):
        if self.current_turn == 'Player 1':
            if self.player_blinking_timer < 20:
                drawLabel('Player 1', 150, 30, font=self.font_style, size=36)
            elif self.player_blinking_timer > 40:
                self.player_blinking_timer = 0
        else:
            drawLabel('Player 1', 150, 30, font=self.font_style, size=36)
        drawLine(80, 50, 297, 50)

        if self.current_turn == 'Player 2':
            if self.player_blinking_timer < 20:
                drawLabel('Player 2', 748, 30, font=self.font_style, size=36)
            elif self.player_blinking_timer > 40:
                self.player_blinking_timer = 0
        else:
            drawLabel('Player 2', 748, 30, font=self.font_style, size=36)
        drawLine(605, 50, 823, 50)

        if self.no_balls_in == False:
            for ball in self.player_balls['Player 1']:
                ball.drawStaticBall('Player 1')
            for ball in self.player_balls['Player 2']:
                ball.drawStaticBall('Player 2')
    
    def drawPowerMeter(self):
        drawRect(self.power_meter_x, self.power_meter_y, self.power_meter_length, self.power_meter_height) 
        drawImage('graphics/powermeter/other cue stick.png', self.power_meter_x, self.power_meter_y, align='left')
        drawImage('graphics/powermeter/cue ball.png', 316, 644, align='left')

    def drawBallPath(self):
        temp_distance = 1000        
        direction = np.array([np.cos(np.radians(180-self.cuestick_angle)), np.sin(np.radians(180-self.cuestick_angle))]) 
        direction = direction * temp_distance

        x1, y1 = int(self.cueball.pos[0]), int(self.cueball.pos[1])
        x2, y2 = x1 + int(direction[0]), y1 + int(direction[1])

        closest_ball = None
        closest_t = 2
        for ball in self.balls:
            if ball.type != 'cueball':
                cx, cy = ball.pos[0], ball.pos[1]  
                r = self.cueball.radius + ball.radius 

                dx, dy = x2 - x1, y2 - y1
                cdx, cdy = x1 - cx, y1 - cy

                a = dx**2 + dy**2
                b = 2 * (cdx * dx + cdy * dy)
                c = cdx**2 + cdy**2 - r**2

                discriminant = b**2 - 4 * a * c
                if discriminant >= 0: 
                    sqrt_discriminant = discriminant**0.5
                    t1 = (-b - sqrt_discriminant) / (2 * a)
                    t2 = (-b + sqrt_discriminant) / (2 * a)

                    for t in (t1, t2):
                        if 0 <= t <= 1:
                            if t < closest_t:
                                closest_ball = ball
                                closest_t = t
        if closest_t != 2:
            self.found_collision = True
                             
            new_x, new_y = int(x1 + closest_t * dx), int(y1 + closest_t * dy)

            temp_ball = Ball(0, (new_x, new_y))

            contactDirection = np.array([np.cos(np.radians(-self.cuestick_angle)), np.sin(np.radians(-self.cuestick_angle))])
            temp_ball.v = contactDirection
            
            cueball_line = closest_ball.getDeltaV(temp_ball) * 25
            collision_ball_line = closest_ball.getDeltaV(temp_ball) * 50

            drawLine(new_x, new_y, new_x-int(cueball_line[0]), new_y-int(cueball_line[1]), fill='white', lineWidth=3)
            drawLine(new_x, new_y, new_x-int(collision_ball_line[0]), new_y+int(collision_ball_line[1]), fill='white', lineWidth=3)

            drawLine(x1, y1, new_x, new_y, fill='white', lineWidth=3)
            drawImage('graphics/ball_location.png', new_x-self.cueball.radius, new_y-self.cueball.radius)
        else:
            self.found_collision = False
        
        if not self.found_collision:
            for wall in self.collidables:
                if wall.type != 'top_middle' and wall.type != 'top_bottom':
                    offset_x = 0
                    offset_y = 0

                    if wall.type == 'top':
                        offset_y = self.cueball.radius
                    elif wall.type == 'bottom':
                        offset_y = -self.cueball.radius
                    elif wall.type == 'left':
                        offset_x = self.cueball.radius
                    elif wall.type == 'right':
                        offset_x = -self.cueball.radius

                    x3, y3 = wall.wall_start[0] + offset_x, wall.wall_start[1] + offset_y
                    x4, y4 = wall.wall_end[0] + offset_x, wall.wall_end[1] + offset_y

                    den = (x1-x2) * (y3-y4) - (y1-y2) * (x3-x4)

                    if den != 0:
                        t = ((x1-x3) * (y3-y4) - (y1-y3) * (x3-x4)) / den
                        u = - ((x1-x2) * (y1-y3) - (y1-y2) * (x1-x3)) / den

                        if 0<=t<=1 and 0<=u<=1:
                            new_x, new_y = int(x1 + t * (x2-x1)), int(y1 + t *(y2-y1))
                            self.found_collision = True
                            drawLine(x1, y1, new_x, new_y, fill='white')
                            drawImage('graphics/ball_location.png', new_x-self.cueball.radius, new_y-self.cueball.radius)
                            break
            
        if not self.found_collision:
                furthest_t = -1
                for pocket in self.pockets:
                    cx, cy = pocket.cx, pocket.cy  
                    r = self.cueball.radius + pocket.radius

                    dx, dy = x2 - x1, y2 - y1 
                    cdx, cdy = x1 - cx, y1 - cy

                    a = dx**2 + dy**2
                    b = 2 * (cdx * dx + cdy * dy)
                    c = cdx**2 + cdy**2 - r**2

                    discriminant = b**2 - 4 * a * c
                    if discriminant >= 0: 
                        sqrt_discriminant = discriminant**0.5
                        t1 = (-b - sqrt_discriminant) / (2 * a)
                        t2 = (-b + sqrt_discriminant) / (2 * a)

                        for t in (t1, t2):
                            if 0 <= t <= 1:
                                if t > furthest_t:
                                    furthest_t = t
                if furthest_t != -1:
                    self.found_collision = True
                                    
                    new_x, new_y = int(x1 + furthest_t * dx), int(y1 + furthest_t * dy)

                    drawLine(x1, y1, new_x, new_y, fill='white')
                    drawImage('graphics/ball_location.png', new_x-self.cueball.radius, new_y-self.cueball.radius)
                else:
                    self.found_collision = False
    
    def drawPocketSelection(self):
        drawLabel('Select a pocket', self.table_cx,75, font=self.font_style, size=24)
        for pocket in self.pockets:
            drawCircle(pocket.cx, pocket.cy, pocket.radius, fill=None, opacity=70, border='white', borderWidth=4)


    def drawAnimations(self):
        if not self.game_over:
            if self.game_started:
                text = "Game Start"
            elif self.player_scratched:
                text = 'SCRATCHED'
            else:
                text = 'NEXT TURN'
        
            drawLabel(text, self.table_cx, self.table_cy, font=self.font_style, size=72)

    def animate(self):
        self.player_blinking_timer += 1
        if self.end_of_turn:
            self.text_timer += 1
            if self.text_timer > 60:
                self.text_timer = 0
                self.end_of_turn = False
                if self.game_started:
                    self.game_started = False
        elif self.is_placing_cueball:
            self.cueball_blinking_timer += 1

    def setupBalls(self):

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
                    index = randint(0, len(solids)-1)
                    num = solids.pop(index)
                elif ballTypeSetup[i][j] == 1:
                    index = randint(0, len(stripes)-1)
                    num = stripes.pop(index)
                elif ballTypeSetup[i][j] == 8:
                    num = 8
                x_offset = i*21
                y_offset = j*24-(len(ballTypeSetup[i])-1)*12
                
                ball = Ball(num, np.array([self.starting_rack_x-x_offset, self.table_cy-y_offset]))
                if ball.type == 'solids':
                    self.solid_balls.append(ball)
                elif ball.type == 'stripes':
                    self.stripe_balls.append(ball)
                self.balls.append(ball)      

        self.cueball = Ball(0, np.array([self.cueball_start_x, self.table_cy]))
        self.balls.append(self.cueball)

        # ball =  Ball(1, np.array([self.cueball_start_x-300, self.table_cy]))
        # self.balls.append(ball)
        # self.stripe_balls.append(ball)

        # ball = Ball(2, np.array([self.cueball_start_x-300, self.table_cy-30]))
        # self.balls.append(ball)
        # self.solid_balls.append(ball)
        
        # ball = Ball(3, np.array([self.cueball_start_x-300, self.table_cy+30]))
        # self.balls.append(ball)


    def selectingDirection(self, mouseX, mouseY):
        self.cuestick_angle = int(np.degrees(np.atan2(self.cueball.pos[1]-mouseY, mouseX-self.cueball.pos[0]))%360)
    
    def placeCuestick(self):
        self.cuestick_placed = True

    def clickedPowermeter(self, mouseX, mouseY):
        if (self.power_meter_x <= mouseX <= self.power_meter_x+self.power_meter_length and
            self.power_meter_y <= mouseY <= self.power_meter_y+self.power_meter_height):
            self.is_dragging_powermeter = True
            self.prevX = mouseX
    
    def draggingPowermeter(self, mouseX):
        self.power_meter_x = self.power_meter_min_x+mouseX-self.prevX
        if self.power_meter_x  <= self.power_meter_min_x:
            self.power_meter_x  = self.power_meter_min_x
        elif self.power_meter_x >= self.power_meter_max_x:
            self.power_meter_x  = self.power_meter_max_x

    def releasePowermeter(self):
        contactDirection = np.array([np.cos(np.radians(-self.cuestick_angle)), np.sin(np.radians(-self.cuestick_angle))])
        power = (self.power_meter_x-self.power_meter_min_x)/(self.power_meter_max_x-self.power_meter_min_x)* 2000
        powerDirection = power * contactDirection 

        self.cueball.updatePhysics(-powerDirection)    
        self.cueball.updateAnimationState(contactDirection)
        self.power_meter_x = self.power_meter_min_x
        self.balls_moving = True
        self.is_dragging_powermeter = False
        self.prevX = None

    def clickedHitpos(self, mouseX, mouseY):
        if (self.hitpos[0] <= mouseX < self.hitpos[0]+12 and 
            self.hitpos[1] <= mouseY < self.hitpos[1]+12):
            self.is_dragging_hitpos = True

    def draggingHitpos(self, mouseX, mouseY):
        if distance(mouseX, mouseY, self.center_pos[0], self.center_pos[1]) < 63:
            self.hitpos = mouseX, mouseY
        else:
            degree =  angleTo(self.center_pos[0], self.center_pos[1], mouseX, mouseY)
            self.hitpos = getPointInDir(self.center_pos[0], self.center_pos[1], degree, 63)

    def releaseHitpos(self):
        self.cueball.setUpdate((self.center_pos[0]-self.hitpos[0], self.center_pos[1]- self.hitpos[1]))
        self.cueball.updateSpin()
        self.is_dragging_hitpos = False

    def clickedCueball(self, mouseX, mouseY):
        dist = distance(self.cueball.pos[0], self.cueball.pos[1], mouseX, mouseY)
        if dist <= self.cueball.radius:
            self.is_dragging_cueball = True
    
    def draggingCueball(self, mouseX, mouseY):
        self.cueball.pos = np.array([mouseX, mouseY])

        if self.is_break_shot:
            if mouseX < self.cueball_start_x: 
                self.cueball.pos[0] = self.cueball_start_x
            elif mouseX+self.cueball.radius >  self.boundary_x + self.boundary_width:
                self.cueball.pos[0] =  self.boundary_x + self.boundary_width - self.cueball.radius
        else:
            if mouseX-self.cueball.radius < self.boundary_x:
                self.cueball.pos[0] = self.boundary_x + self.cueball.radius
            elif mouseX+self.cueball.radius > self.boundary_x + self.boundary_width:
                self.cueball.pos[0] = self.boundary_x + self.boundary_width - self.cueball.radius
        if mouseY-self.cueball.radius < self.boundary_y:
            self.cueball.pos[1] = self.boundary_y + self.cueball.radius
        elif mouseY+self.cueball.radius > self.boundary_y + self.boundary_height:
            self.cueball.pos[1] = self.boundary_y + self.boundary_height - self.cueball.radius
            
    def releaseCueball(self):
        self.is_dragging_cueball = False

    def clickedPocket(self, mouseX, mouseY):
        for pocket in self.pockets:
            dist = distance(pocket.cx, pocket.cy, mouseX, mouseY)
            if dist <= pocket.radius:
                self.selected_pocket = pocket
                self.selecting_pocket = False

    def run(self):
        if not self.end_of_turn:
            if not self.selecting_pocket:
                if self.balls_moving:
                    for ball in self.balls:
                        ball.applyPhysics(1/FPS)
                        ball.applyFriction()

                        self.ballCollision()
                        self.wallCollision()
                        self.pocketCollision()

                        if ball.is_in_pocket and not ball.in_motion:
                            if ball.type == 'cueball':
                                self.drawNewCueball()
                            self.balls.remove(ball)

                        if ball.in_motion:
                            ball.nextSprite() 
                            
                    if not self.areBallsMoving():
                        self.balls_moving = False
                        self.hitpos = self.center_pos
                        self.cuestick_placed = False

                        self.end()

                else:
                    for ball in self.balls:
                        ball.notMoving()
        self.animate()
            
    def areBallsMoving(self):
        for ball in self.balls:
            if ball.in_motion:
                return True
        return False
    
    def wallCollision(self):
        for ball in self.balls:
            if ball.in_motion:
                    ball.pos = self.updatedBallPos(ball)
                    for wall in self.collidables:
                        if wall.checkCollision(ball):
                            wall.fixBallPosition(ball)
                            ball.collidedWall(wall.type)

    def updatedBallPos(self, ball):
        if (ball.pos[0] > 486 or ball.pos[0] < 420) or ball.near_pocket:
            offset = 0
            if ball.near_pocket:
                offset = 40
            if ball.pos[0] - ball.radius < self.left_x - offset:
                ball.pos[0] = self.left_x + ball.radius - offset
            if ball.pos[0] + ball.radius > self.right_x + offset:
                ball.pos[0] = self.right_x - ball.radius + offset
            if ball.pos[1] - ball.radius < self.top_y - offset:
                ball.pos[1] = self.top_y + ball.radius - offset
            if ball.pos[1] + ball.radius > self.bottom_y + offset:
                ball.pos[1] = self.bottom_y - ball.radius + offset
        return ball.pos
    
    def pocketCollision(self):
        for ball in self.balls:
            for wall in self.pockets_entrance:
                if wall.checkCollision(ball):
                    ball.near_pocket = True
                    
            for pocket in self.pockets:
                if not ball.is_in_pocket and pocket.isBallInPocket(ball):
                    ball.inPocket(pocket)
                    self.balls_in_pocket.append(ball)
            if ball.is_in_pocket:
                ball.collidePocketWalls()

    def ballCollision(self):
        for ball1 in self.balls:
            if ball1.in_motion and not ball1.is_in_pocket:
                for ball2 in self.balls:
                    if not ball2.is_in_pocket:
                        if ball1 != ball2:
                            dist = distance(ball1.pos[0], ball1.pos[1], ball2.pos[0], ball2.pos[1])
                            if dist <= ball1.radius + ball2.radius:
                                self.ballHit(ball1, ball2)
                                ball1.updateAnimationState((ball2.contactDir[0], ball2.contactDir[1] * -1))
                                ball2.updateAnimationState((ball1.contactDir[0], ball1.contactDir[1] * -1))
                                ball1.collidedBall(ball2, dist)
        
    def scratched(self):
        self.player_scratched = True

    def assignPlayerBalls(self, ball_type):
        self.no_balls_in = False

        if ball_type == 'solids':
            self.player_balls[self.current_turn] = self.solid_balls
            self.player_balls[self.waiting] = self.stripe_balls
        else:
            self.player_balls[self.current_turn] = self.stripe_balls
            self.player_balls[self.waiting] = self.solid_balls

        self.player_balls[self.current_turn].sort()
        self.player_balls[self.waiting].sort()

    def ballHit(self, ball1, ball2):
        if ball1.type == 'cueball' and self.player_hit_ball == False:
            self.player_hit_ball = True
            if not self.isValidHit(ball2.type):
                self.scratched()

    def drawNewCueball(self):
        self.cueball = Ball(0, np.array([self.cueball_start_x, self.table_cy]))
        self.balls.append(self.cueball)
        self.is_placing_cueball = True

    def cueballPlaced(self):
        if self.canPlaceCueball():
            self.is_placing_cueball = False
            self.player_scratched = False

    def canPlaceCueball(self):
        for ball in self.balls:
            if ball.type != 'cueball':
                dist = distance(self.cueball.pos[0], self.cueball.pos[1], ball.pos[0], ball.pos[1])
                if dist <= self.cueball.radius + ball.radius:
                    return False
        return True

    def checkPockets(self):
        if self.balls_in_pocket == []:
            return False
        for i in range(len(self.balls_in_pocket)):
            ball = self.balls_in_pocket[i]
            if ball.type == '8ball':
                if ball.pocket == self.selected_pocket:
                    self.winner = self.current_turn
                else:
                    self.winner = self.waiting
                self.game_over = True
            elif ball.type == 'cueball':
                self.scratched()
            else:
                if len(self.balls_in_pocket) > 1:
                    ball_type = self.balls_in_pocket[0].type
                    for i in range(1, len(self.balls_in_pocket)):
                        if self.balls_in_pocket[i].type != ball_type:
                            return False
                    if not self.no_balls_in:
                        if self.balls_in_pocket[0].type != self.player_balls[self.current_turn][0].type:
                            return False
                if self.no_balls_in:
                    self.assignPlayerBalls(self.balls_in_pocket[0].type)
        return True

    def isValidHit(self, ball_type):
        if self.player_hit_ball:
            if self.is_break_shot:
                self.is_break_shot = False

            if ball_type == '8ball':
                if self.no_balls_in == False:
                    if self.ballsLeft(self.current_turn) == 0:
                        return True

            if self.no_balls_in or (ball_type == self.player_balls[self.current_turn][0].type):
                return True
            
        return False

    def ballsLeft(self, player):
        count = len(self.stripe_balls)
        for ball in self.player_balls[player]:
            if ball.is_in_pocket:
                count -= 1
        return count

    def end(self):
        if not self.player_hit_ball:
            self.scratched()

        if not self.checkPockets() or self.player_scratched:
            self.end_of_turn = True
        
        if self.player_scratched:
            self.balls.remove(self.cueball)
            self.drawNewCueball()

        if not self.game_over and self.end_of_turn:
            self.current_turn, self.waiting = self.waiting, self.current_turn

        if not self.no_balls_in and self.ballsLeft(self.current_turn) == 0:
            self.selecting_pocket = True
        
        self.selected_pocket = None
        self.balls_in_pocket = []
        self.player_hit_ball = False

    def getWinner(self):
        return self.winner
    

class PracticeGame(Game):
    def __init__(self):
        super().__init__()
        
        self.sliders = {'ball_count_slider' : Slider('# of balls', 75, 50, 100, 25, 90, 'fixed', 5),
                        'power_slider' : Slider('power scale', 200, 50, 100, 25, 102)}

        self.buttons = {}

    def drawGame(self):
        drawImage('graphics/Pool Table.png', self.table_cx, self.table_cy, align='center')

        self.drawPracticeUI()
    
        for ball in self.balls:
            x, y = ball.pos
            if ball.type == 'cueball' and self.is_placing_cueball:
                if not self.end_of_turn and not self.balls_moving and not self.selecting_pocket:
                    drawImage('graphics/cueball indicator.png', int(x) -12, int(y)-12)
                    if self.cueball_blinking_timer <5:
                        drawImage(ball.currSprite, int(x)-12, int(y)-12, rotateAngle=ball.rotation)
                    elif self.cueball_blinking_timer >10:
                        self.cueball_blinking_timer = 0   
            else:
                drawImage(ball.currSprite, int(x)-12, int(y)-12, rotateAngle=ball.rotation)

        if not self.end_of_turn and not self.balls_moving and not self.player_scratched and not self.selecting_pocket:
            drawImage('graphics/cue stick.png', int(self.cueball.pos[0])-250, int(self.cueball.pos[1])-6, rotateAngle=-self.cuestick_angle)

        drawImage('graphics/other.png', self.table_cx, self.other_cy, align='center')
        drawImage('graphics/spin_selector.png', self.hitpos[0], self.hitpos[1])

        self.drawPowerMeter()
        
        if self.end_of_turn:
            self.drawAnimations()

    def drawPracticeUI(self):
        for name in self.sliders:
            self.sliders[name].draw()

    def onPracticeUIHover(self, mouseX, mouseY):
        for name in self.sliders:
            self.sliders[name].onHover(mouseX, mouseY)

    def onPracticeUIClick(self):
        for name in self.sliders:
            if self.sliders[name].is_hovering:
                self.sliders[name].click()

    def onPracticeUIDrag(self, mouseX):
        for name in self.sliders:
            if self.sliders[name].is_clicked:
                self.sliders[name].isDragging(mouseX)

    def onPracticeUIRelease(self):
        for name in self.sliders:
            if self.sliders[name].is_clicked:
                self.sliders[name].release()


    def setupBalls(self):

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
                    index = randint(0, len(solids)-1)
                    num = solids.pop(index)
                elif ballTypeSetup[i][j] == 1:
                    index = randint(0, len(stripes)-1)
                    num = stripes.pop(index)
                elif ballTypeSetup[i][j] == 8:
                    num = 8
                x_offset = i*21
                y_offset = j*24-(len(ballTypeSetup[i])-1)*12
                
                ball = Ball(num, np.array([self.starting_rack_x-x_offset, self.table_cy-y_offset]))
                if ball.type == 'solids':
                    self.solid_balls.append(ball)
                elif ball.type == 'stripes':
                    self.stripe_balls.append(ball)
                self.balls.append(ball)      

        self.cueball = Ball(0, np.array([self.cueball_start_x, self.table_cy]))
        self.balls.append(self.cueball)