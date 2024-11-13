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
    app.powerMeterLength = 207
    app.powerMeterHeight = 12
    app.prevX = None

    app.isDraggingPower = False
    app.balls_moving = False

    app.cueBall = Ball(0, np.array([app.table_cx, app.table_cy], dtype=int))

def redrawAll(app):
    drawImage('graphics/Pool Table.png', app.table_cx, app.table_cy, align='center')
    
    x, y = app.cueBall.pos
    drawImage(app.cueBall.currSprite, int(x)-12, int(y)-12)
    if not app.balls_moving:
        drawImage('graphics/cue stick.png', int(x)-250, int(y)-6, rotateAngle=-app.cueStickAngle)

    drawImage('graphics/other.png', app.table_cx, app.other_cy, align='center')

    drawPowerMeter(app)

def drawPowerMeter(app):
    #hitbox
    drawRect(app.powerMeterX, app.powerMeterY, app.powerMeterLength, app.powerMeterHeight) 
    
    #cue stick sprite
    drawImage('graphics/powermeter/other cue stick.png', app.powerMeterX, app.powerMeterY, align='left')
    
    #ball sprite
    drawImage('graphics/powermeter/cue ball.png', 282, 594, align='left')
    

def drawBoundaries(app):
    #top
    t1 = drawPolygon(102, 79, 369, 79, 363, 88, 108, 88, fill='red')
    t2 = drawPolygon(429, 79, 699, 79, 693, 88, 435, 88, fill='red')
    
    #bottom
    b1 = drawPolygon(102, 415, 369, 415, 366, 407, 111, 407, fill='red')
    b2 = drawPolygon(429, 415, 699, 415, 693, 407, 435, 407, fill='red')

    #left
    l1 = drawPolygon(64, 111,64, 381, 73, 366, 73, 126, fill='red')

    #right
    r1 = drawPolygon(738, 111,738, 381, 729, 366, 729, 126, fill='red')    
    

def drawPockets(app):
    pass

def onKeyPress(app, key):
    pass

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

def onMouseDrag(app, mouseX, mouseY):
    if app.isDraggingPower:
        app.powerMeterX = app.powerMeterMinX+mouseX-app.prevX
        if app.powerMeterX  <= app.powerMeterMinX:
            app.powerMeterX  = app.powerMeterMinX
        elif app.powerMeterX >= app.powerMeterMaxX:
            app.powerMeterX  = app.powerMeterMaxX

def onMouseRelease(app, mouseX, mouseY):
    if app.isDraggingPower: 
        contactDirection = np.array([math.cos(math.radians(-app.cueStickAngle)), math.sin(math.radians(-app.cueStickAngle))])
        power = (app.powerMeterX-app.powerMeterMinX)/(app.powerMeterMaxX-app.powerMeterMinX)* 1000 * contactDirection 
        #print(f'Power: {power}')

        app.cueBall.update_physics(-power)    
        app.cueBall.setState('horizontal')
        app.powerMeterX = app.powerMeterMinX
        app.balls_moving = True
        app.isDraggingPower = False
        app.prevX = None

def onStep(app):
    if app.balls_moving:
        app.cueBall.apply_physics()
        app.cueBall.apply_friction()

        #temp
        app.cueBall.nextSprite()

        if not app.cueBall.in_motion:
            app.balls_moving = False
            app.cueStickPlaced = False

def main():
    runApp(width=800, height=700)
main()