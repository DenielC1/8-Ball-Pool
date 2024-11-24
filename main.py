from cmu_graphics import *
import numpy as np
import math
import random

from ball import Ball
from settings import *

def onAppStart(app):
    app.stepsPerSecond = FPS
    app.paused = False

    app.table_cx = app.width/2
    app.table_cy = app.height/2-100

    app.cueBallStartX = app.width/2+168
    app.startingRackX = app.width/2-168

    app.other_cy = app.height/2+220
    
    app.cueStickAngle = 0
    app.cueStickPlaced = False

    app.powerMeterX = 336
    app.powerMeterY = 588
    app.powerMeterMinX = 336
    app.powerMeterMaxX = 543
    app.powerMeterLength = 300
    app.powerMeterHeight = 12

    app.centerPos = (121, 564)
    app.hitPos = app.centerPos

    app.prevX = None

    app.isDraggingPower = False
    app.isDraggingContactPoint = False
    app.balls_moving = False

    app.cueBall = None
    app.balls = []
    setupBalls(app)

    app.boundary_x = 72
    app.boundary_y = 90
    app.boundary_width = 657
    app.boundary_height = 321

def redrawAll(app):
    drawImage('graphics/Pool Table.png', app.table_cx, app.table_cy, align='center')
    
    for ball in app.balls:
        x, y = ball.pos
        drawImage(ball.currSprite, int(x)-12, int(y)-12, rotateAngle=ball.rotation)

    if not app.balls_moving:
        drawImage('graphics/cue stick.png', int(app.cueBall.pos[0])-250, int(app.cueBall.pos[1])-6, rotateAngle=-app.cueStickAngle)

    drawImage('graphics/other.png', app.table_cx, app.other_cy, align='center')
    drawImage('graphics/spin_selector.png', app.hitPos[0], app.hitPos[1])


    drawPowerMeter(app)

def drawPowerMeter(app):
    drawRect(app.powerMeterX, app.powerMeterY, app.powerMeterLength, app.powerMeterHeight) 
    drawImage('graphics/powermeter/other cue stick.png', app.powerMeterX, app.powerMeterY, align='left')
    drawImage('graphics/powermeter/cue ball.png', 282, 594, align='left')

def onKeyPress(app, key):
    if key == 'p':
        app.paused = not app.paused
    if key == 'enter':
        takeStep(app)
    if key == 'r':
        resetGame(app)
    if key == 'up':
        app.cueBall.pos = np.array([app.table_cx, app.table_cy-90])
        app.cueStickAngle = 90
        app.cueStickPlaced = True
    if key == 'down':
        app.cueBall.pos = np.array([app.table_cx, app.table_cy+90])
        app.cueStickAngle = 270
        app.cueStickPlaced = True
    if key == 'right':
        app.cueBall.pos = np.array([app.cueBallStartX, app.table_cy])
        app.cueStickAngle = 0
        app.cueStickPlaced = True
    if key == 'left':
        app.cueBall.pos = np.array([app.startingRackX, app.table_cy])
        app.cueStickAngle = 180
        app.cueStickPlaced = True

def resetGame(app):
    app.balls = []
    setupBalls(app)
    app.isDraggingPower = False
    app.isDraggingContactPoint = False
    app.balls_moving = False
    app.cueStickPlaced = False
    app.paused = False


def setupBalls(app):

    app.cueBall = Ball(0, np.array([app.cueBallStartX, app.table_cy]))
    app.balls.append(app.cueBall)

    #app.balls.append(Ball(15, np.array([app.table_cx, app.table_cy])))
    #app.balls.append(Ball(5, np.array([app.table_cx-45, app.table_cy])))

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
            app.balls.append(Ball(num, np.array([app.startingRackX-x_offset, app.table_cy-y_offset])))

def onMouseMove(app, mouseX, mouseY):
    if not app.cueStickPlaced:
        app.cueStickAngle = math.degrees(math.atan2(app.cueBall.pos[1]-mouseY, mouseX-app.cueBall.pos[0]))%360
    

def onMousePress(app, mouseX, mouseY):
    if not app.cueStickPlaced:
        app.cueStickPlaced = True
    else:
        if (app.powerMeterX <= mouseX <= app.powerMeterX+app.powerMeterLength and
            app.powerMeterY <= mouseY <= app.powerMeterY+app.powerMeterHeight):
            app.isDraggingPower = True
            app.prevX = mouseX
        if (app.hitPos[0] <= mouseX < app.hitPos[0]+12 and 
            app.hitPos[1] <= mouseY < app.hitPos[1]+12):
                app.isDraggingContactPoint = True

def onMouseDrag(app, mouseX, mouseY):
    if app.isDraggingPower:
        app.powerMeterX = app.powerMeterMinX+mouseX-app.prevX
        if app.powerMeterX  <= app.powerMeterMinX:
            app.powerMeterX  = app.powerMeterMinX
        elif app.powerMeterX >= app.powerMeterMaxX:
            app.powerMeterX  = app.powerMeterMaxX
    if app.isDraggingContactPoint:
        if distance(mouseX, mouseY, app.centerPos[0], app.centerPos[1]) < 63:
            app.hitPos = mouseX, mouseY
        else:
            degree =  angleTo(app.centerPos[0], app.centerPos[1], mouseX, mouseY)
            app.hitPos = getPointInDir(app.centerPos[0], app.centerPos[1], degree, 63)


def onMouseRelease(app, mouseX, mouseY):
    if app.isDraggingPower: 
        contactDirection = np.array([math.cos(math.radians(-app.cueStickAngle)), math.sin(math.radians(-app.cueStickAngle))])
        power = (app.powerMeterX-app.powerMeterMinX)/(app.powerMeterMaxX-app.powerMeterMinX)* 3000
        powerDirection = power * contactDirection 
        #print(f'Power: {powerDirection}')

        app.cueBall.update_rotation(power)
        app.cueBall.update_physics(-powerDirection)    
        app.cueBall.update_animation_state(contactDirection)
        app.powerMeterX = app.powerMeterMinX
        app.balls_moving = True
        app.isDraggingPower = False
        app.prevX = None
    
    if app.isDraggingContactPoint:
        app.cueBall.hitPos = app.centerPos[0]-app.hitPos[0],app.centerPos[1]- app.hitPos[1]
        app.isDraggingContactPoint = False

def onStep(app):
    if not app.paused:
        takeStep(app)

def takeStep(app):
    if app.balls_moving:
        for ball in app.balls:
            ball.apply_physics()
            ball.apply_friction()
            wall_collision(app)
            ball_collision(app)

            if ball.in_motion:
                ball.nextSprite()

        if not areBallsMoving(app):
            app.balls_moving = False
            app.hitPos = app.centerPos
            app.cueBall.hitPos = (0,0)
            app.cueStickPlaced = False

    else:
        for ball in app.balls:
            ball.notMoving()

def areBallsMoving(app):
    for ball in app.balls:
        if ball.in_motion:
            return True
    return False

def wall_collision(app):
    ball_radius = 13
    for ball in app.balls:
        if ball.pos[0]-ball_radius < app.boundary_x:
            ball.pos[0] = app.boundary_x + ball_radius
            ball.collidedWall('vertical_wall')
            ball.update_animation_state((ball.contactDir[0] * -1, ball.contactDir[1]))

        elif ball.pos[0]+ball_radius > app.boundary_x + app.boundary_width:
            ball.pos[0] = app.boundary_x + app.boundary_width - ball_radius
            ball.collidedWall('vertical_wall')
            ball.update_animation_state((ball.contactDir[0] * -1, ball.contactDir[1]))

        if ball.pos[1]-ball_radius < app.boundary_y:
            ball.pos[1] = app.boundary_y + ball_radius
            ball.collidedWall('horizontal_wall')
            ball.update_animation_state((ball.contactDir[0], ball.contactDir[1] * -1))

        elif ball.pos[1]+ball_radius > app.boundary_y + app.boundary_height:
            ball.pos[1] = app.boundary_y + app.boundary_height - ball_radius
            ball.collidedWall('horizontal_wall')
            ball.update_animation_state((ball.contactDir[0], ball.contactDir[1] * -1))

def ball_collision(app):
    ball_radius = 12
    for ball1 in app.balls:
        for ball2 in app.balls:
            if ball1 != ball2:
                dist = distance(ball1.pos[0], ball1.pos[1], ball2.pos[0], ball2.pos[1])
                if dist <= 2*ball_radius:
                    ball1.collidedBall(ball2)
                    ball1.update_animation_state((ball1.contactDir[0], ball1.contactDir[1] * -1))
                    ball2.update_animation_state((ball1.contactDir[0], ball1.contactDir[1] * -1))


def main():
    runApp(width=800, height=700)
main()