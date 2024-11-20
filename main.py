from cmu_graphics import *
import numpy as np
import math

from ball import Ball
from settings import *

def onAppStart(app):
    app.stepsPerSecond = FPS

    app.table_cx = app.width/2
    app.table_cy = app.height/2-100

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

    app.cueBall = Ball(12, np.array([app.table_cx, app.table_cy], dtype=int))

    app.balls = [app.cueBall]

    app.boundary_x = 73
    app.boundary_y = 90
    app.boundary_width = 655
    app.boundary_height = 318

def redrawAll(app):
    drawImage('graphics/Pool Table.png', app.table_cx, app.table_cy, align='center')
    
    x, y = app.cueBall.pos
    drawImage(app.cueBall.currSprite, int(x)-12, int(y)-12, rotateAngle=app.cueBall.rotation)
    if not app.balls_moving:
        drawImage('graphics/cue stick.png', int(x)-250, int(y)-6, rotateAngle=-app.cueStickAngle)

    drawImage('graphics/other.png', app.table_cx, app.other_cy, align='center')
    
    drawImage('graphics/spin_selector.png', app.hitPos[0], app.hitPos[1])


    drawPowerMeter(app)

def drawPowerMeter(app):
    #hitbox
    drawRect(app.powerMeterX, app.powerMeterY, app.powerMeterLength, app.powerMeterHeight) 
    
    #cue stick sprite
    drawImage('graphics/powermeter/other cue stick.png', app.powerMeterX, app.powerMeterY, align='left')
    
    #ball sprite
    drawImage('graphics/powermeter/cue ball.png', 282, 594, align='left')

def onKeyPress(app, key):
    pass

def onMouseMove(app, mouseX, mouseY):
    #print(mouseX, mouseY)
    
    if not app.cueStickPlaced:
        app.cueStickAngle = math.degrees(math.atan2(app.cueBall.pos[1]-mouseY, mouseX-app.cueBall.pos[0]))%360
        #print(app.cueStickAngle)
    

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
        power = (app.powerMeterX-app.powerMeterMinX)/(app.powerMeterMaxX-app.powerMeterMinX)* 1000 * contactDirection 
        #print(f'Power: {power}')

        app.cueBall.update_rotation((app.powerMeterX-app.powerMeterMinX)/(app.powerMeterMaxX-app.powerMeterMinX)* 1000)
        app.cueBall.update_physics(-power)    
        app.cueBall.update_animation_state(contactDirection)
        app.powerMeterX = app.powerMeterMinX
        app.balls_moving = True
        app.isDraggingPower = False
        app.prevX = None
    
    if app.isDraggingContactPoint:
        app.cueBall.hitPos = app.centerPos[0]-app.hitPos[0],app.centerPos[1]- app.hitPos[1]
        app.isDraggingContactPoint = False

def onStep(app):
    if app.balls_moving:
        app.cueBall.apply_physics()
        app.cueBall.apply_friction()
        wall_collision(app)

        app.cueBall.nextSprite()

        if not app.cueBall.in_motion:
            
            app.balls_moving = False
            app.hitPos = app.centerPos
            app.cueBall.hitPos = (0,0)
            app.cueStickPlaced = False

    else:
        for ball in app.balls:
            ball.notMoving()

def wall_collision(app):
    ball_radius = 13
    for ball in app.balls:
        if (ball.pos[0]-ball_radius < app.boundary_x or 
            ball.pos[0]+ball_radius > app.boundary_x + app.boundary_width):
            ball.collided('vertical_wall')
            ball.update_animation_state((ball.contactDir[0] * -1, ball.contactDir[1]))

        elif (ball.pos[1]-ball_radius < app.boundary_y or 
            ball.pos[1]+ball_radius > app.boundary_y + app.boundary_height):
            ball.collided('horizontal_wall')
            ball.update_animation_state((ball.contactDir[0], ball.contactDir[1] * -1))

def main():
    runApp(width=800, height=700)
main()