from bearlibterminal import terminal
from renderer import render_starchart
from intro import Intro

import time

def input_listener(self):
    render_rate = 0
    anim = True
    while True:
        start_time = time.time()
        key = None
        if terminal.has_input() or self.pause == True:
            key = terminal.read()
        ###################
        ## Mouse catcher ## need to catch all mouse input or pause doesn't work
        ###################
        if (key == terminal.TK_MOUSE_SCROLL):
            print('mouse')
            self.tile_size -= int(terminal.state(terminal.TK_MOUSE_WHEEL))
            terminal.set(f"font: MegaFont.ttf, size={self.tile_size}")
            key = None
            continue
        if (key == terminal.TK_MOUSE_RIGHT):
            key = None
            continue

        if self.input_state == 'main':
            self.pause = True
            if (key == terminal.TK_MOUSE_LEFT):
                self.main_menu(0, terminal.state(terminal.TK_MOUSE_X), terminal.state(terminal.TK_MOUSE_Y), True, False)
            if (key == terminal.TK_MOUSE_MOVE):
                self.main_menu(0, terminal.state(terminal.TK_MOUSE_X), terminal.state(terminal.TK_MOUSE_Y), False, False)
                key = None
            if (key == terminal.TK_UP or key == terminal.TK_KP_8):
                self.main_menu(-1, 0, 0, False, False)
            if (key == terminal.TK_DOWN or key == terminal.TK_KP_2):
                self.main_menu(1, 0, 0, False, False)
            if (key == terminal.TK_ENTER):
                self.main_menu(0, 0, 0, False, True)
            if (key == terminal.TK_ESCAPE) and self.coords != []:
                self.input_state = 'sector'
                key = None
        if self.input_state == 'intro':
            Intro.play_intro(self, 1)
            if (key == terminal.TK_ENTER) or (key == terminal.TK_ESCAPE) or (key == terminal.TK_MOUSE_LEFT):
                self.main_menu(0, 0, 0, False, False)
        if self.input_state == 'sector loaded':
            print('loaded')
            if (key == terminal.TK_ENTER) or (key == terminal.TK_ESCAPE) or (key == terminal.TK_MOUSE_LEFT):
                self.input_state = 'sector'
                terminal.clear()
                key = None
        if self.input_state == 'sector':
            if (key == terminal.TK_LEFT or key == terminal.TK_KP_4 or key == terminal.TK_KP_7 or key == terminal.TK_KP_1):
                self.move_character(0,-1,0)
            if (key == terminal.TK_RIGHT or key == terminal.TK_KP_6  or key == terminal.TK_KP_3 or key == terminal.TK_KP_9):
                self.move_character(0,1,0)
            if (key == terminal.TK_UP or key == terminal.TK_KP_8 or key == terminal.TK_KP_9 or key == terminal.TK_KP_7):
                self.move_character(0,0,-1)
            if (key == terminal.TK_DOWN or key == terminal.TK_KP_2 or key == terminal.TK_KP_1 or key == terminal.TK_KP_3):
                self.move_character(0,0,1)
            if (key == terminal.TK_W or key == terminal.TK_KP_MINUS):
                self.move_character(-1,0,0)
            if (key == terminal.TK_S or key == terminal.TK_KP_PLUS):
                self.move_character(1,0,0)
            if (key == terminal.TK_SPACE):
                self.pause = not self.pause
            if self.pause:
                self.dev_console("[color=yellow]PAUSED  ", 0)
            else:
                self.dev_console("[color=dark red]realtime", 0)
            ########################
            ## animation modifier ##
            ########################
            render_rate += 1
            if render_rate >= 15:
                render_rate = 0
                anim = True
            render_starchart(self, anim)
            if (key == terminal.TK_ESCAPE):
                self.main_menu(0, 0, 0, False, False)
        # always active
        if(key == terminal.TK_CLOSE):
            break
        if (key == terminal.TK_RESIZED):
            print('hello')
        anim = False

        ##########################
        # mainloop frame counter #
        ##########################
        delta = int(time.time()* 1000 - start_time * 1000)
        target_framerate = 15
        if delta < target_framerate:
            terminal.delay(target_framerate - delta)
        if self.input_state != 'intro' and self.input_state != 'main' and self.dev_mode == True:
            # main loop time in milliseconds
            self.dev_console("Loop: " + str(delta), 2)
            # current frames per second (not averaged)
            self.dev_console("FPS: " + str(int(1.0 / (time.time() - start_time))), 3)
