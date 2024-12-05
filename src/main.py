from cmu_graphics import *
from game import *
from ui import *
from settings import *

def onAppStart(app):
    app.stepsPerSecond = FPS
    app.paused = False

    app.game_type = None

    app.cx = app.width/2
    app.cy = app.height/2

    app.background_color = rgb(16, 70, 87)
    app.background_color2 = rgb(16, 60, 76)
    app.font_style = 'Edit Undo BRK'
    app.heading_size = 80

    app.on_base_menu = True
    app.on_selection_menu = False
    app.on_settings_menu = False

    app.game_started = False

    app.volume_changed = False

    app.assisted_path_on = False

    app.buttons = {'new_game_button' : Button('new game', app.cx, 325, 150, 50, 375, 525),
                   'settings_button' : Button('settings', app.cx, 375, 140, 50, 380, 520),
                   'quit_button' : Button('quit', app.cx, 425, 80, 50, 410, 490),
                   'eight_ball_pool_button' : Button('eight-ball pool', app.cx, 275, 250, 50, 325, 575),
                   'practice_button': Button('practice', app.cx, 325, 140, 50, 380, 520),
                   'back_button': Button('back', app.cx, 490, 80, 50, 410, 490),
                   'play_again_button': Button('play again', app.cx, 275, 170, 50, 360, 540),
                'resume_button' : Button('resume', app.cx, 225, 120, 50, 390, 510),
                   'restart_button' : Button('restart', app.cx, 275, 130, 50, 385, 515),
                   'return_to_menu_button' : Button('return to menu', app.cx, 325, 220, 50, 340, 560),
                   }
    
    app.sliders = {'master_volume_slider' : Slider('master volume', app.cx, 300, 350, 25, 122),
                   'background_volume_slider' : Slider('background volume', app.cx, 360, 350, 25, 156),
                   'sound_fx_volume_slider' : Slider('sound fx volume', app.cx, 420, 350, 25, 138)}
    
    app.toggles = {'assisted_path_toggle' : Toggle('assisted path', app.cx, 460, 350, 30, 112)} 

    app.toggles['assisted_path_toggle'].active = False

    app.game = Game()
    
    app.volume = {'master_volume_slider' : 1,
                  'background_volume_slider' : 1,
                  'sound_fx_volume_slider' :1}

    app.main_music = Sound('../music/menu/Action 5 Looped Pure.wav')
    app.main_music.play(loop=True)        
    app.main_music.setVolume(0)

def redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill=app.background_color)
    if not app.game_started:
        if app.on_base_menu:
            drawBaseMenu(app)
        elif app.on_selection_menu:
            drawSelectionMenu(app)
        elif app.on_settings_menu:
            drawSettingsMenu(app)
    else: 
        app.game.drawGame()

        if ((not app.game.end_of_turn and not app.game.balls_moving) and 
        ((not app.game.player_scratched and not app.game.selecting_pocket) or 
        (app.game_type == 'practice' and not app.game.dragging_balls))):
            if app.assisted_path_on:
                app.game.drawBallPath()

        if app.paused:
            drawRect(0, 0, app.width, app.height, opacity=50)
            if app.on_settings_menu:
                drawSettingsMenu(app)
            else:
                drawPauseMenu(app)

        elif app.game.game_over:
            drawGameOverMenu(app)

def drawBaseMenu(app):
    drawLabel("8 Ball Pool", app.cx, 200, font=app.font_style, size=app.heading_size)
    drawLine(210, 240, 680, 240)

    app.buttons['new_game_button'].draw()
    app.buttons['settings_button'].draw()
    app.buttons['quit_button'].draw()

def drawSelectionMenu(app):
    drawLabel("Choose a gamemode", app.cx, 200, font=app.font_style, size=app.heading_size)
    drawLine(100, 240, 800, 240)

    app.buttons['eight_ball_pool_button'].draw()
    app.buttons['practice_button'].draw()
    app.buttons['back_button'].draw()

def drawSettingsMenu(app):
    drawLabel("Settings", app.cx, 200, font=app.font_style, size=app.heading_size)
    drawLine(280, 240, 600, 240)

    drawRect(app.cx, 400, 400, 300, fill=app.background_color2, border='black',align='center')

    app.buttons['back_button'].draw()

    for name in app.sliders:
        app.sliders[name].draw()

    for name in app.toggles:
        app.toggles[name].draw()

def drawGameOverMenu(app):
    text = app.game.getWinner()
    drawLabel(f'{text} won', app.cx, 200, font=app.font_style, size=app.heading_size)
    drawLine(200, 240, 700, 240)

    app.buttons['play_again_button'].draw()
    app.buttons['return_to_menu_button'].draw()

def drawPauseMenu(app):
    drawRect(app.cx, app.cy-50, 300, 300, align='center', fill=app.background_color2, border='black')

    app.buttons['resume_button'].draw()
    app.buttons['restart_button'].draw()
    app.buttons['return_to_menu_button'].draw()
    app.buttons['settings_button'].draw()
    app.buttons['quit_button'].draw()
    
def onStep(app):
    if not app.paused and not app.game.game_over:
        takeStep(app)

    if app.volume_changed:
        app.volume_changed = False

        for name in Button.sound_fx:
            Button.sound_fx[name].setVolume(app.volume['master_volume_slider'] * app.volume['sound_fx_volume_slider'])

        app.main_music.setVolume(app.volume['master_volume_slider'] * app.volume['background_volume_slider'])

def takeStep(app):
    if app.game_started:
        app.game.run()
    
def onMouseMove(app, mouseX, mouseY):

    for name in app.buttons:
        app.buttons[name].onHover(mouseX, mouseY)

    for name in app.sliders:
        app.sliders[name].onHover(mouseX, mouseY)

    for name in app.toggles:
        app.toggles[name].onHover(mouseX, mouseY)


    if app.game_started and not app.paused:

        if type(app.game) == PracticeGame:
            app.game.onPracticeUIHover(mouseX, mouseY)

        if app.game.balls_moving == False:
            if not app.game.cuestick_placed:
                app.game.selectingDirection(mouseX, mouseY)
    
def settings_menu_click(app):
    if app.buttons['back_button'].is_hovering:
        app.buttons['back_button'].click()
    
    for name in app.sliders:
        if app.sliders[name].is_hovering:
            app.sliders[name].click()
    
    for name in app.toggles:
        if app.toggles[name].is_hovering:
            app.toggles[name].click()

def settings_menu_release(app):

    for name in app.sliders:
        if app.sliders[name].is_clicked:
            app.sliders[name].release()
            app.volume[name] = app.sliders[name].getVolumeLevel()
            app.volume_changed = True

    if app.buttons['back_button'].is_clicked:
        app.buttons['back_button'].release()
        if not app.game_started:
            app.on_base_menu = True
        app.on_settings_menu = False
    
    if app.toggles['assisted_path_toggle'].is_clicked:
        app.toggles['assisted_path_toggle'].release()
        app.assisted_path_on = not app.assisted_path_on

def onMousePress(app, mouseX, mouseY):
    if app.paused:
        if app.on_settings_menu:
            settings_menu_click(app)
        elif app.buttons['resume_button'].is_hovering:
            app.buttons['resume_button'].click()
        elif app.buttons['restart_button'].is_hovering:
            app.buttons['restart_button'].click()
        elif app.buttons['return_to_menu_button'].is_hovering:
            app.buttons['return_to_menu_button'].click()
        elif app.buttons['settings_button'].is_hovering:
            app.buttons['settings_button'].click()
        elif app.buttons['quit_button'].is_hovering:
            app.buttons['quit_button'].click()

    elif app.on_base_menu:
        if app.buttons['new_game_button'].is_hovering:
            app.buttons['new_game_button'].click()
        elif app.buttons['settings_button'].is_hovering:
            app.buttons['settings_button'].click()
        elif app.buttons['quit_button'].is_hovering:
            app.buttons['quit_button'].click()

    elif app.on_selection_menu:
        if app.buttons['eight_ball_pool_button'].is_hovering:
            app.buttons['eight_ball_pool_button'].click()
        elif app.buttons['practice_button'].is_hovering:
            app.buttons['practice_button'].click()
        elif app.buttons['back_button'].is_hovering:
            app.buttons['back_button'].click()

    elif app.on_settings_menu:
        settings_menu_click(app)

    elif app.game.game_over:
        if app.buttons['play_again_button'].is_hovering:
            app.buttons['play_again_button'].click()
        elif app.buttons['return_to_menu_button'].is_hovering:
            app.buttons['return_to_menu_button'].click()            

    if app.game_started and not app.game.game_over and not app.game.end_of_turn and not app.paused:
        
        if type(app.game) == PracticeGame:
            if app.game.onPracticeUIClick():
                pass

            elif app.game.dragging_balls:
                app.game.clickedBall(mouseX, mouseY)
            elif not app.game.cuestick_placed:
                    app.game.placeCuestick()
            elif not app.game.balls_moving:
                app.game.clickedPowermeter(mouseX, mouseY)
                app.game.clickedHitpos(mouseX, mouseY)

        else:
            if app.game.selecting_pocket:
                app.game.clickedPocket(mouseX, mouseY)
            else:
                if app.game.player_scratched:
                    if app.game.is_placing_cueball:
                        app.game.clickedCueball(mouseX, mouseY)
                elif not app.game.cuestick_placed:
                    app.game.placeCuestick()
                elif not app.game.balls_moving:
                    app.game.clickedPowermeter(mouseX, mouseY)
                    app.game.clickedHitpos(mouseX, mouseY)

def onMouseDrag(app, mouseX, mouseY):

    for name in app.sliders:
        if app.sliders[name].is_clicked:
            app.sliders[name].isDragging(mouseX)

    if app.game_started:

        if type(app.game) == PracticeGame:
            app.game.onPracticeUIDrag(mouseX)
            if app.game.is_dragging_ball:
                app.game.draggingBall(mouseX, mouseY)
        else:
            if app.game.is_dragging_cueball:
                app.game.draggingCueball(mouseX, mouseY)

        if app.game.is_dragging_powermeter:
            app.game.draggingPowermeter(mouseX)
        if app.game.is_dragging_hitpos:
            app.game.draggingHitpos(mouseX, mouseY)

def onMouseRelease(app, mouseX, mouseY):
    if app.paused:
        if app.on_settings_menu:
            settings_menu_release(app)
        elif app.buttons['resume_button'].is_clicked:
            app.buttons['resume_button'].release()
            app.paused = not app.paused
        elif app.buttons['restart_button'].is_clicked:
            app.buttons['restart_button'].release()
            app.paused = not app.paused
            resetGame(app)
        elif app.buttons['return_to_menu_button'].is_clicked:
            app.buttons['return_to_menu_button'].release()
            app.on_base_menu = True
            app.game_started = False
            app.paused = not app.paused
        elif app.buttons['settings_button'].is_clicked:
            app.buttons['settings_button'].release()
            app.on_settings_menu = True
        elif app.buttons['quit_button'].is_clicked:
            app.buttons['quit_button'].release()
            app.quit()

    elif app.on_base_menu:
        if app.buttons['new_game_button'].is_clicked:
            app.buttons['new_game_button'].release()
            app.on_selection_menu = True
            app.on_base_menu = False
        elif app.buttons['settings_button'].is_clicked:
            app.buttons['settings_button'].release()
            app.on_settings_menu = True
            app.on_base_menu = False
        elif app.buttons['quit_button'].is_clicked:
            app.buttons['quit_button'].release()
            
            app.quit()

    elif app.on_selection_menu:
        if app.buttons['eight_ball_pool_button'].is_clicked:
            app.buttons['eight_ball_pool_button'].release()
            app.game_type = 'eight_ball'
            gamemodeSelected(app)
        elif app.buttons['practice_button'].is_clicked:
            app.buttons['practice_button'].release()
            app.game_type = 'practice'
            gamemodeSelected(app)
        elif app.buttons['back_button'].is_clicked:
            app.buttons['back_button'].release()
            app.on_base_menu = True
            app.on_selection_menu = False

    elif app.game.game_over:
        if app.buttons['play_again_button'].is_clicked:
            app.buttons['play_again_button'].release()
            resetGame(app)
        elif app.buttons['return_to_menu_button'].is_clicked:
            app.buttons['return_to_menu_button'].release()
            resetGame(app)
            app.on_base_menu = True
            app.game_started = False
    
    elif app.on_settings_menu:
        settings_menu_release(app)

    if app.game_started:

        if type(app.game) == PracticeGame:
            app.game.onPracticeUIRelease()
            if app.game.is_dragging_ball:
                app.game.releaseBall()
        else:
            if app.game.is_dragging_cueball:
                app.game.releaseCueball()
                app.game.cueballPlaced()

        if app.game.is_dragging_powermeter:
            app.game.releasePowermeter()
        if app.game.is_dragging_hitpos:
            app.game.releaseHitpos()

def onKeyPress(app, key):
    if key == 'enter':
        takeStep(app)
    if app.game_started:
        if key == 'escape':
            if app.paused and app.on_settings_menu:
                app.on_settings_menu = False
            else:
                app.paused = not app.paused

def gamemodeSelected(app):
    resetGame(app)
    app.game_started = True
    app.on_selection_menu = False

def resetGame(app):
    if app.game_type == 'eight_ball':
        app.game = Game()
    else:
        app.game = PracticeGame()

def main():
    runApp(width=WIDTH, height=HEIGHT)

main()