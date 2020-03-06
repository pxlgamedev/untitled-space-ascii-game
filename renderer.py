from bearlibterminal import terminal
import random
import time

def render_starchart(self, anim):
    message = ''
    start_time = time.time()
    scanner = True
    center_screen = self.window_center - int(self.render_range[1] / 2)
    z_start = max(0, int(self.chr_pos[0] - self.render_range[0]/ 2))
    y_start = max(0, int(self.chr_pos[1] - self.render_range[1]/ 2))
    x_start = max(0, int(self.chr_pos[2] - self.render_range[2]/ 2))
    z_range = (z_start + self.render_range[0])
    y_range = (y_start + self.render_range[1])
    x_range = (x_start + self.render_range[2])
    if z_range >= self.map_depth:
        z_range = self.map_depth
        z_start = self.map_depth - self.render_range[0]
    if y_range > self.map_size:
        y_range = self.map_size
        y_start = self.map_size - self.render_range[1]
    if x_range > self.map_size:
        x_range = self.map_size
        x_start = self.map_size - self.render_range[2]
    for z in range(z_start, z_range):
        terminal.layer(z - z_start)
        terminal.clear_area(center_screen, 0, self.render_range[1], self.render_range[2])
        for y in range(y_start, y_range):
            for x in range(x_start, x_range):
                tile = self.coords[z][y][x]
                if tile.char != ' ':
                    offset_z = z - (self.chr_pos[0] - self.render_range[0])
                    dist = z - self.chr_pos[0]
                    if tile.multitile == False:
                        z_color = '[color='+ self.color_range[max(0, min(z - z_start, len(self.color_range) -1))] + 'white' + ']'
                    if tile.multitile == True:
                        z_color = '[color='+tile.color+']'
                    if anim and tile.anim != '':
                        tile.char = random.choice(tile.anim)
                    offset = '[offset=' + str((y - self.chr_pos[1]) * offset_z) + ',' + str((x - self.chr_pos[2]) * offset_z) + ']' + z_color + tile.char
                    if tile.solid == True:
                        #TODO add scanner range to ship stats
                        s_range = 2
                        if scanner == True and z - self.chr_pos[0] > -s_range and z - self.chr_pos[0] < s_range and y - self.chr_pos[1] > -s_range and y - self.chr_pos[1] < s_range and x - self.chr_pos[2] > -s_range and x - self.chr_pos[2] < s_range:
                            # only scan the nearest body, will be
                            scanner = False
                            offset = '[color='+tile.color +']'+ tile.char
                            r = ' '
                            if dist < 0:
                                r = 'scan:   (-)'
                            if dist > 0:
                                r = 'scan:   (+)'
                            terminal.layer(self.map_depth + 1)
                            terminal.printf((y -y_start + 2) + center_screen, (x - x_start + -1), tile.name)
                            terminal.printf((y -y_start - 6) + center_screen, (x - x_start + 1), r)
                            terminal.layer(self.map_depth + 1)
                            message = 'Approaching Stellar Mass'
                            if tile.scan != '' and dist == 0:
                                terminal.printf((y -y_start - 6) + center_screen, (x - x_start + 1), 'scan:   ' + tile.type)
                                terminal.printf((y -y_start + 2) + center_screen, (x - x_start + 2), tile.scan)
                            terminal.layer(0)
                            terminal.printf((y -y_start) + center_screen, x - x_start, '[bkcolor=darkest grey] ')
                    terminal.layer(z  - z_start)
                    terminal.printf((y -y_start) + center_screen, x - x_start, offset)
    self.message_console(message, 0)
    terminal.layer(self.chr_pos[0]   - z_start)
    terminal.printf((self.chr_pos[1] - y_start) + center_screen, self.chr_pos[2] - x_start, '@')
    self.ship_console(("LOC: " + str(self.chr_pos[0]) + str(self.chr_pos[1]) + str(self.chr_pos[2])), 0)
    terminal.refresh()
    terminal.layer(self.map_depth + 1)
    terminal.clear_area(0, 0, self.window_width, self.window_height)
    frame = int(time.time()* 1000 - start_time * 1000)
    self.dev_console("Render: " + str(frame), 1)
