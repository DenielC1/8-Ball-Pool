from cmu_graphics import *
from game import Game

from settings import *

def onAppStart(app):
    app.stepsPerSecond = FPS
    app.paused = False

    app.game = Game()
    
def redrawAll(app):
    app.game.setupTable()

def onStep(app):
    if not app.paused:
        takeStep(app)

def takeStep(app):
    app.game.ball_movement()

def onMouseMove(app, mouseX, mouseY):
    if app.game.ballsMoving == False:
        if app.game.playerScratched: 
            app.game.placing_cueball(mouseX, mouseY)
        elif not app.game.cuestickPlaced:
            app.game.selecting_direction(mouseX, mouseY)
    


def onMousePress(app, mouseX, mouseY):
    if app.game.playerScratched:
        app.game.playerScratched = False
        app.game.cueball_placed()

    elif not app.game.cuestickPlaced:
        app.game.place_cuestick()
    else:
        app.game.has_clicked_powermeter(mouseX, mouseY)
        app.game.has_clicked_hit_pos(mouseX, mouseY)

def onMouseDrag(app, mouseX, mouseY):
    if app.game.isDraggingPowermeter:
        app.game.dragging_powermeter(mouseX)
    if app.game.isDraggingHitpos:
        app.game.dragging_hit_pos(mouseX, mouseY)

def onMouseRelease(app, mouseX, mouseY):
    if app.game.isDraggingPowermeter:
        app.game.release_powermeter()
    if app.game.isDraggingHitpos:
        app.game.release_hit_pos()

def onKeyPress(app, key):
    if key == 'r':
        resetGame(app)
    if key == 'p':
        app.paused = not app.paused
    if key == 'enter':
        takeStep(app)

def resetGame(app):
    app.game = Game()

def main():
    runApp(width=WIDTH, height=HEIGHT)

main()