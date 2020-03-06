from bearlibterminal import terminal

class Intro():
    frame = 0
    page_count = 0
    page = ['T               ',
            'Th              ',
            'Thi             ',
            'This            ',
            'This            ',
            'This i          ',
            'This is         ',
            'This is.        ',
            'This is..       ',
            'This is...      ',
            'This is... [color=red]Space',
            'This is... [color=red]Space',
            'This is... [color=red]Space',
            'This is... [color=red]Space',
            'This is... [color=red]Space',
            '           [color=red]Space',
            '           [color=dark red]Space',
            '           [color=dark red]Space',
            '           [color=darkest red]Space',
            '                ',
            '                ',
            '                ',
            '[color=red]Space[/color]          ',
            '[color=red]Space[/color]          ',
            '[color=red]Space[/color] is       ',
            '[color=red]Space[/color] is       ',
            '[color=red]Space[/color] is [color=orange]Vast  ',
            '[color=red]Space[/color] is [color=orange]Vast  ',
            '[color=red]Space[/color] is [color=orange]Vast  ',
            '         [color=dark orange]Vast  ',
            '         [color=darker orange]Vast  ',
            '         [color=darkest orange]Vast  ',
            '           ',
            '           ',
            'The           ',
            'The           ',
            'The Star      ',
            'The Star      ',
            'The Star Drive',
            'The Star Drive',
            '[color=yellow] Success   ',
            '[color=yellow] Success   ',
            '[color=red] Failure   ',
            '[color=red] Failure   ',
            '[color=orange]Unexpected ',
            '[color=orange]Unexpected ',
            '[color=dark red]Catastrophe',
            '[color=dark red]Catastrophe',
            '[color=dark red]Catastrophe',
            '[color=darker red]Catastrophe',
            '[color=darkest red]Catastrophe',
            '              ',
            '              ',
            '              ',
            'You           ',
            'You           ',
            'You are       ',
            'You are       ',
            'You are [color=yellow]Lost  ',
            'You are [color=yellow]Lost  ',
            'You are [color=orange]Alone ',
            'You are [color=orange]Alone ',
            'You are [color=red]Afraid',
            'You are [color=red]Afraid',
            '        [color=red]Afraid',
            '        [color=dark red]Afraid',
            '        [color=dark red]Afraid',
            '        [color=darker red]Afraid',
            '        [color=darker red]Afraid',
            '        [color=darkest red]Afraid',
            '        [color=darkest red]Afraid',
            '                  ',
            '                  ',
            '                  ',
            '                  ',
            '                  ',
            '                  ',
            '                  ',
            '                  ',
            '                  ',
            '                  ',
            '',
            ]

    def play_intro(self, count):
        if count == 0:
            Intro.frame = 0
        Intro.frame += count
        #print(Intro.frame)
        if Intro.frame == 25:
            Intro.frame = 0
            terminal.clear()
            terminal.printf(self.center_text(Intro.page[Intro.page_count]), 11, Intro.page[Intro.page_count])
            if Intro.page_count + 1 < len(Intro.page):
                Intro.page_count += 1
            if Intro.page_count + 5 >= len(Intro.page):
                terminal.printf(self.center_text('This is [color=red]Space '), 11, 'This is [color=red]Space ')
            if Intro.page_count + 1 == len(Intro.page):
                self.main_menu(0, 0, 0, False, False)
            terminal.refresh()
