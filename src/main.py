from cmu_graphics import *
from game import Game
from button import Button
from settings import *

def onAppStart(app):
    app.stepsPerSecond = FPS
    app.paused = False

    app.cx = app.width/2

    app.background_color = rgb(16, 70, 87)
    app.font_style = 'Edit Undo BRK'
    app.heading_size = 80

    app.on_base_menu = False
    app.on_selection_menu = False
    app.on_game_settings_menu = False
    app.on_settings_menu = False

    app.game_started = True

    app.aim_assistance_on = True


    app.buttons = {'new_game_button' : Button('new game', app.cx, 335, 360, 180, 375, 525),
                   'settings_button' : Button('settings', app.cx, 400, 360, 180, 375, 525),
                   'eight_ball_pool_button' : Button('eight-ball pool', app.cx, 300, 295, 305, 310, 595),
                   'snooker_button': Button('snooker', app.cx, 350, 360, 180, 380, 520),
                   'back_button': Button('back', app.cx, 700, 400, 100, 410, 490),
                   'single_player_button': Button('single player', app.cx, 300, 315, 275, 325, 575),
                   'play_again_button': Button('play again', app.cx, 325, 365, 170, 360, 540),
                   'return_to_menu_button': Button('return to menu', app.cx, 375, 325, 250, 325, 575)}
    

    app.game = Game(app.aim_assistance_on)
    
def redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill=app.background_color)
    if not app.game_started:
        if app.on_base_menu:
            drawBaseMenu(app)
        elif app.on_selection_menu:
            drawSelectionMenu(app)
        elif app.on_settings_menu:
            drawSettingsMenu(app)
        elif app.on_game_settings_menu:
            drawGameSettingsMenu(app)
    else: 
        app.game.drawGame()
        if app.game.game_over:
            drawGameOverMenu(app)

def drawBaseMenu(app):
    drawLabel("Billards", app.cx, 200, font=app.font_style, size=app.heading_size)
    drawLine(280, 240, 610, 240)

    app.buttons['new_game_button'].draw()
    app.buttons['settings_button'].draw()

def drawSelectionMenu(app):
    drawLabel("Choose a gamemode", app.cx, 200, font=app.font_style, size=app.heading_size)
    drawLine(100, 240, 800, 240)

    app.buttons['eight_ball_pool_button'].draw()
    app.buttons['snooker_button'].draw()
    app.buttons['back_button'].draw()

def drawSettingsMenu(app):
    drawLabel("Settings", app.cx, 200, font=app.font_style, size=app.heading_size)
    drawLine(300, 240, 600, 240)
    
    app.buttons['back_button'].draw()

def drawGameSettingsMenu(app):
    drawLabel("Game Settings", app.cx, 200, font=app.font_style, size=app.heading_size)
    drawLine(200, 240, 700, 240)

    app.buttons['single_player_button'].draw()
    app.buttons['back_button'].draw()

def drawGameOverMenu(app):
    text = app.game.getWinner()
    drawLabel(f'{text} won', app.cx, 200, font=app.font_style, size=app.heading_size)
    drawLine(200, 240, 700, 240)

    app.buttons['play_again_button'].draw()
    app.buttons['return_to_menu_button'].draw()

def onStep(app):
    if not app.paused and not app.game.game_over:
        takeStep(app)

def takeStep(app):
    if app.game_started:
        app.game.run()

def onMouseMove(app, mouseX, mouseY):
    if app.on_base_menu:
        app.buttons['new_game_button'].on_hover(mouseX, mouseY)
        app.buttons['settings_button'].on_hover(mouseX, mouseY)
    
    elif app.on_selection_menu:
        app.buttons['eight_ball_pool_button'].on_hover(mouseX, mouseY)
        app.buttons['snooker_button'].on_hover(mouseX, mouseY)
        app.buttons['back_button'].on_hover(mouseX, mouseY)

    elif app.on_settings_menu:
        app.buttons['back_button'].on_hover(mouseX, mouseY)

    elif app.on_game_settings_menu:
        app.buttons['single_player_button'].on_hover(mouseX, mouseY)
        app.buttons['back_button'].on_hover(mouseX, mouseY)

    elif app.game.game_over:
        app.buttons['play_again_button'].on_hover(mouseX, mouseY)
        app.buttons['return_to_menu_button'].on_hover(mouseX, mouseY)

    if app.game_started:
        if app.game.balls_moving == False:
            if not app.game.cuestick_placed:
                app.game.selectingDirection(mouseX, mouseY)
    
def onMousePress(app, mouseX, mouseY):
    if app.on_base_menu:
        if app.buttons['new_game_button'].is_hovering:
            app.on_selection_menu = True
            app.on_base_menu = False
        elif app.buttons['settings_button'].is_hovering:
            app.on_settings_menu = True
            app.on_base_menu = False

    elif app.on_selection_menu:
        if (app.buttons['eight_ball_pool_button'].is_hovering or
            app.buttons['snooker_button'].is_hovering):
            app.on_game_settings_menu = True
            app.on_selection_menu = False
        elif app.buttons['back_button'].is_hovering:
            app.on_base_menu = True
            app.on_selection_menu = False

    elif app.on_settings_menu:
        if app.buttons['back_button'].is_hovering:
            app.on_base_menu = True
            app.on_settings_menu = False

    elif app.on_game_settings_menu:
        if app.buttons['single_player_button'].is_hovering:
            app.game_started = True
            app.on_game_setting_menu = False
        elif app.buttons['back_button'].is_hovering:
            app.on_selection_menu = True
            app.on_game_setting_menu = False

    elif app.game.game_over:
        if app.buttons['play_again_button'].is_hovering:
            resetGame(app)
        elif app.buttons['return_to_menu_button'].is_hovering:
            resetGame(app)
            app.on_base_menu = True
            app.game_started = False

    if app.game_started and not app.game.game_over:
        if app.game.player_scratched:
            if app.game.is_placing_cueball:
                app.game.clickedCueball(mouseX, mouseY)
        elif not app.game.cuestick_placed:
            app.game.placeCuestick()
        elif not app.game.balls_moving:
            app.game.clickedPowermeter(mouseX, mouseY)
            app.game.clickedHitpos(mouseX, mouseY)

def onMouseDrag(app, mouseX, mouseY):
    if app.game_started:
        if app.game.is_dragging_powermeter:
            app.game.draggingPowermeter(mouseX)
        if app.game.is_dragging_hitpos:
            app.game.draggingHitpos(mouseX, mouseY)
        if app.game.is_dragging_cueball:
            app.game.draggingCueball(mouseX, mouseY)

def onMouseRelease(app, mouseX, mouseY):
    if app.game_started:
        if app.game.is_dragging_powermeter:
            app.game.releasePowermeter()
        if app.game.is_dragging_hitpos:
            app.game.releaseHitpos()
        if app.game.is_dragging_cueball:
            app.game.releaseCueball()
            app.game.cueballPlaced()

def onKeyPress(app, key):
    if key == 'r':
        resetGame(app)
    if key == 'p':
        app.paused = not app.paused
    if key == 'enter':
        takeStep(app)

def resetGame(app):
    app.game = Game(app.aim_assistance_on)

def main():
    runApp(width=WIDTH, height=HEIGHT)

main()