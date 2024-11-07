from cmu_graphics import *
from PIL import Image
from ball import Ball

def onAppStart(app):
    app.stepsPerSecond = 50

    app.table_cx = app.width/2
    app.table_cy = app.height/2
    
    app.ballTypeSetup = [[0],
                         [1, 0],
                         [0,8,1],
                         [1,0,1,0],
                         [0,1,1,0,1]
                        ]
    
    app.ball1 = Ball(14, app.table_cx, app.table_cy)
    app.ball2 = Ball(2, app.table_cx, app.table_cy)

def redrawAll(app):
    drawImage('graphics/Pool Table.png', app.table_cx, app.table_cy, align='center')

    drawImage(app.ball1.currSprite, app.ball1.x, app.ball1.y)
    drawImage(app.ball2.currSprite, app.ball2.x+24, app.ball2.y)

def onKeyPress(app, key):
    pass

def main():
    runApp(width=800, height=500)
main()