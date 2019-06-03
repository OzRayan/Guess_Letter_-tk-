#!/usr/bin/env python3
import setup as st
import record as rc

from time import strftime, sleep
from tkinter import (Tk, Label, Button, Frame, StringVar, IntVar,
                     DISABLED, NORMAL, SUNKEN, SOLID,
                     RIGHT, LEFT, TOP, BOTTOM, BOTH, CENTER)


class Hangman:
    """Hangman class,
    made in tkinter GUInterface"""
    def __init__(self, master=None):
        """Constructor"""
        self.master = master
        self.screen()
        self.build_frame()
        self.build_grid()

        self.banner_text = StringVar()
        self.banner_text.set('')
        self.banner_text.trace('w', self.build_title_label)

        self.counter = StringVar()
        self.counter.trace('w', self.build_countdown)

        self.clock_text = StringVar()
        self.clock_text.set('Clock')
        self.clock_text.trace('w', self.build_clock_label)

        self.word_text = StringVar()
        self.word_text.set('Choose your category')
        self.word_text.trace('w', self.build_word_label)

        self.secret_word = StringVar()
        self.prompt = StringVar()
        self.prompt.set('random')

        self.timer_text = StringVar()
        self.timer_text.set(strftime("%H:%M"))
        self.timer_text.trace('w', self.build_timer)

        self.time_left = IntVar()
        self.time_left.set(st.DEFAULT_GAP)
        self.time_left.trace('w', self.alert)

        self.score_text = IntVar()
        self.score_text.set('0\n0')
        self.score_text.trace('w', self.build_score_label)

        self.sorted = ''
        self.char = ''
        # self.lang = 'FRA'
        self.level_status = 1
        self.total = 0
        self.abc = []
        self.category = []
        self.level = []
        self.misses = []
        self.guesses = []
        self.s_w_list = []
        self.first_last = []
        self.a = {}
        self.running = False
        self.rem = self.master.winfo_screenwidth()
        self.w = self.master.winfo_screenwidth() / 5
        self.h = self.master.winfo_screenheight() * 2 / 7

        self.build_title_label()
        self.build_word_label()
        self.build_countdown()
        self.build_welcome_label()
        self.build_score_label()
        self.build_timer()
        self.build_clock_label()

        self.buttons()
        self.category_buttons()
        self.abc_buttons()

        self.update()

    def screen(self):
        """Main window
        Minimal size 1024 / 600
        The window goes full screen if the width it's lower than 1440"""
        self.master.minsize(1024, 600)
        if self.master.winfo_screenwidth() <= 1440:
                # and self.master.winfo_screenheight() <= 720:
            self.master.overrideredirect(True)
            self.master.geometry('{0}x{1}+0+0'.format(
                self.master.winfo_screenwidth(),
                self.master.winfo_screenheight()))
        # elif 1024 < self.master.winfo_screenwidth() < 1920 \
        #         and 720 < self.master.winfo_screenheight() < 1080:
        #     a = int(float(70) * float(self.master.winfo_screenwidth()) / 100)
        #     b = int(float(70) * float(self.master.winfo_screenheight()) / 100)
        #     self.master.overrideredirect(True)
        #     self.master.geometry('{}x{}+{}+{}'.format(
        #         a, b, (self.master.winfo_screenwidth() // 2 - a // 2),
        #         (self.master.winfo_screenheight() // 2 - b // 2)))
        else:
            self.master.overrideredirect(True)
            x = int(float(65) * float(self.master.winfo_screenwidth()) / 100)
            y = int(float(75) * float(self.master.winfo_screenheight()) / 100)
            self.master.maxsize(x, y)
            self.master.geometry('{}x{}+{}+{}'.format(
                x, y, (self.master.winfo_screenwidth() // 2 - x // 2),
                (self.master.winfo_screenheight() // 2 - y // 2)))
        self.master.update_idletasks()

    def mini_screen(self):
        """Secondary window for result information"""
        # noinspection PyAttributeOutsideInit
        self.master_2 = Tk()
        # noinspection PyAttributeOutsideInit
        frame = Frame(self.master_2, bg=st.color['fg'],
                      highlightbackground=st.color['fg_enter'],
                      highlightcolor=st.color['fg_enter'],
                      highlightthickness=3)
        if self.rem < 1440:
            x, y = 400, 500
        else:
            x, y = 700, 900
        self.master_2.geometry(
            '{}x{}+{}+{}'.
            format(x, y,
                   int(self.master.winfo_screenwidth() // 2 - x / 2),
                   int(self.master.winfo_screenheight() // 2 - y / 2)
                   ))
        self.master_2.overrideredirect(True)
        self.master_2.update_idletasks()
        frame.pack(fill=BOTH, expand=True)
        niv = None
        if self.level_status == 1:
            niv = st.L_EN[2]
        if self.level_status == 2:
            niv = st.L_EN[1]
        if self.level_status == 3:
            niv = st.L_EN[0]
        text = st.P_EN['won'].format(
            niv.capitalize(), self.secret_word.get(), self.total, ''
        )
        fg = 'green'
        bg = st.color['fg']
        if len(self.misses) == 7 or not self.time_left.get():
            text = st.P_EN['lose']
            fg = 'red'
        # noinspection PyAttributeOutsideInit
        label = Label(
            frame, text=text,
            bg=bg, fg=fg, justify=LEFT,
            font=st.font(self.rem, 5)
        )
        ok = Button(
            frame, bg=st.color['fg'],
            bd=0, fg=st.color['fg_enter'], font=st.font(self.rem, 3),
            text='Ok', command=lambda: self.master_2.destroy(),
            activeforeground='black', activebackground=st.color['fg'],
            width=2
        )
        label.pack(fill=BOTH, expand=True)
        ok.place(relx=0.5, rely=0.96, anchor='s')

    def score_screen(self):
        """Score screen"""
        # noinspection PyAttributeOutsideInit
        self.master_3 = Tk()
        # noinspection PyAttributeOutsideInit
        self.frame = Frame(self.master_3, bg=st.color['fg'],
                           highlightbackground=st.color['fg_enter'],
                           highlightcolor=st.color['fg_enter'],
                           highlightthickness=3)
        if self.rem < 1440:
            x, y = 600, 500
        else:
            x, y = 600, 800
        self.master_3.geometry(
            '{}x{}+{}+{}'.
            format(x, y,
                   int(self.master.winfo_screenwidth() // 2 - x / 2),
                   int(self.master.winfo_screenheight() // 2 - y / 2)))
        self.master_3.overrideredirect(True)
        self.master_3.update_idletasks()
        self.frame.pack(fill=BOTH, expand=True)
        text = 'Level \t  Points\t\tTime\n' + 37 * '_' + '\n'
        for item in rc.search():
            text += '{}\t   {}     {}\n'.format(
                item.level, item.points,
                item.timestamp.strftime(' %B %d, %Y %I:%M %p')
            )
        label = Label(
            self.frame, text=text,
            bg=st.color['bg'], fg=st.color['fg'], justify=LEFT,
            font=st.font(self.rem, 0)
        )
        ok = Button(
            self.frame, bg=st.color['bg'],
            bd=0, fg=st.color['fg_enter'], font=st.font(self.rem, 3),
            text='Ok', command=lambda: self.master_3.destroy(),
            activeforeground='black', activebackground=st.color['fg'],
            width=2
        )
        label.pack(fill=BOTH, expand=True)
        ok.place(relx=0.5, rely=0.96, anchor='s')

    def create_frame(self, frame, code):
        """Creates frames for the main window"""
        wa, wb, ha, hb = None, None, None, None
        if code is 'm':
            wa, wb, ha, hb = 1, 1, 1, 1
        elif code is 'r2':
            wa, wb, ha, hb = 1, 1, 3, 5
        elif code in ['r0', 'r1', 'r3']:
            wa, wb, ha, hb = 1, 1, 1, 5
        return Frame(frame, bg=st.color['bg'],
                     width=self.master.winfo_width()*wa//wb,
                     height=self.master.winfo_height()*ha//hb
                     )

    def create_button(self, frame, text):
        """General buttons creator"""
        font = None
        command = self.set_command(text)
        state = None
        bg, fg, abg, afg, dfg = st.set_buttons_color(text)
        button = Button(
            frame, text=text.capitalize(), bg=bg, fg=fg, font=font, bd=0,
            command=command, justify='center', overrelief=SUNKEN,
            anchor=CENTER, state=state, disabledforeground=dfg,
            activeforeground=afg, activebackground=abg, image=None
        )
        return button

    def build_frame(self):
        """All the frames for the main window"""
        # noinspection PyAttributeOutsideInit
        self.welcome = self.create_frame(self.master, 'm')
        self.welcome.config(highlightbackground=st.color['fg'],
                            highlightcolor=st.color['fg'],
                            highlightthickness=2)
        self.welcome.pack(fill=BOTH, expand=True)

        # noinspection PyAttributeOutsideInit
        self.mainframe = self.create_frame(self.master, 'm')
        self.mainframe.config(highlightbackground='black',
                              highlightcolor='black',
                              highlightthickness=2)
        self.mainframe.pack(fill=BOTH, expand=True)
        self.mainframe.pack_forget()
        # Row 0
        # noinspection PyAttributeOutsideInit
        self.row_0_grid = self.create_frame(self.mainframe, 'r0')
        self.row_0_grid.grid(row=0, column=0, sticky='news', pady=10)
        # Row 0 Column 1
        # noinspection PyAttributeOutsideInit
        self.row_0_column_1 = Frame(self.row_0_grid, bg=st.color['bg'])
        self.row_0_column_1.config(highlightbackground=st.color['fg'],
                                   highlightcolor=st.color['bg_start'],
                                   highlightthickness=2)
        self.row_0_column_1.grid(row=0, column=1, rowspan=2,
                                 sticky='news', pady=7)
        # Row 0 Column 2
        # noinspection PyAttributeOutsideInit
        self.row_0_column_2 = Frame(self.row_0_grid, bg=st.color['bg'])
        self.row_0_column_2.config(highlightbackground=st.color['fg'],
                                   highlightcolor=st.color['bg_start'],
                                   highlightthickness=2)
        self.row_0_column_2.grid(row=0, column=2, rowspan=2,
                                 sticky='news', padx=20, pady=6)
        # Row 0 Column 3
        # noinspection PyAttributeOutsideInit
        self.row_0_column_3 = Frame(self.row_0_grid, bg=st.color['bg'])
        self.row_0_column_3.grid(row=0, column=3, rowspan=2, columnspan=2,
                                 sticky='news', padx=3, pady=4)
        # Row 1
        # noinspection PyAttributeOutsideInit
        self.row_1_grid = self.create_frame(self.mainframe, 'r1')
        self.row_1_grid.grid(row=1, column=0, sticky='news', padx=13)
        # Row 2
        # noinspection PyAttributeOutsideInit
        self.row_2_grid = self.create_frame(self.mainframe, 'r2')
        self.row_2_grid.grid(row=2, column=0, sticky='news')
        # Row 3
        # noinspection PyAttributeOutsideInit
        self.row_3_grid = self.create_frame(self.mainframe, 'r3')
        self.row_3_grid.grid(row=3, column=0, sticky='news', padx=5, pady=5)

    def build_grid(self):
        """Grid layout for all the frames"""
        u, u2 = None, None
        # Main Frame
        self.mainframe.columnconfigure(0, weight=1, uniform=u)
        for m in range(0, 4):
            self.mainframe.rowconfigure(m, weight=1, uniform=u2)
        # Row 0
        for y in range(15):
            self.row_0_grid.columnconfigure(y, weight=1, uniform=u)
        self.row_0_grid.rowconfigure(0, weight=1, uniform=u2)
        self.row_0_grid.rowconfigure(1, weight=1, uniform=u2)
        # Row 0 Column 1
        self.row_0_column_1.columnconfigure(0, weight=1, uniform=u)
        for c in range(6):
            self.row_0_column_1.rowconfigure(c, weight=1, uniform=u2)
        # Row 0 Column 2
        self.row_0_column_2.columnconfigure(0, weight=1, uniform=u)
        for c2 in range(3):
            self.row_0_column_2.rowconfigure(c2, weight=1, uniform=u2)
        # Row 0 Column 3
        self.row_0_column_3.columnconfigure(0, weight=1, uniform=u)
        for c3 in range(3):
            self.row_0_column_3.rowconfigure(c3, weight=1, uniform=u2)
        # Row 1
        for x in range(13):
            self.row_1_grid.columnconfigure(x, weight=1, uniform=u)
        self.row_1_grid.rowconfigure(0, weight=1, uniform=u2)
        self.row_1_grid.rowconfigure(1, weight=1, uniform=u2)
        # Row 2
        self.row_2_grid.columnconfigure(0, weight=1, uniform=u)
        self.row_2_grid.columnconfigure(1, weight=1, uniform=u)
        self.row_2_grid.rowconfigure(0, weight=1, uniform=u2)
        # Row 3
        for n in range(0, 4):
            self.row_3_grid.columnconfigure(n, weight=1, uniform=u)
        self.row_3_grid.rowconfigure(0, weight=1, uniform=u2)
        self.row_3_grid.rowconfigure(1, weight=1, uniform=u2)

    # noinspection PyUnusedLocal
    def build_score_label(self, *args):
        """Word categories label"""
        bg, fg = st.set_buttons_color('points', 1)
        points = Label(
            self.row_0_column_1, text='Points:',
            bg=bg, fg=fg,
            font=st.font(self.rem, -4, style='normal'),
            bd=0,
            width=2
        )
        points.grid(row=0, column=0, sticky='news', padx=0, pady=0)
        b, f = st.set_buttons_color('score', 1)
        score = Label(
            self.row_0_column_1, textvariable=self.score_text,
            bg=b, fg=f,
            font=st.font(self.rem, 0),
            justify=CENTER,
            bd=0,
            width=2
        )
        score.grid(row=1, column=0, sticky='news', padx=0, pady=0)

    # noinspection PyUnusedLocal
    def build_welcome_label(self, *args):
        """Word categories label"""
        bg, fg = st.set_buttons_color('title', 1)
        title = Label(
            self.welcome, text='Guess Letters',
            bg=bg, fg=fg,
            font=st.font(self.rem, 24),
            justify=CENTER
        )
        title.pack(side=TOP, padx=20, pady=50)

    # noinspection PyUnusedLocal
    def build_title_label(self, *args):
        """Word categories label"""
        bg, fg = st.set_buttons_color('title', 1)
        title = Label(
            self.row_0_grid, text=self.banner_text.get(),
            bg=bg, fg=fg,
            font=st.font(self.rem, 10),
            width=6
        )
        title.grid(
            row=0, column=5, rowspan=2, columnspan=10,
            sticky='ew', padx=5, pady=2
        )

    # noinspection PyUnusedLocal
    def build_countdown(self, *args):
        """Countdown label"""
        em = self.master.winfo_width() // 50
        # noinspection PyAttributeOutsideInit
        self.count = Label(
            self.row_2_grid, textvariable=self.counter,
            bg=st.color['bg'], fg=st.color['7'],
            font=('Times new Roman', int(4.5*em), 'bold'),
        )
        self.count.grid(
            row=0, column=0,
            sticky='nws', padx=2*em, pady=5
        )

    # noinspection PyUnusedLocal
    def build_clock_label(self, *args):
        """Main clock label"""
        bg, fg = st.set_buttons_color('points', 1)
        # noinspection PyAttributeOutsideInit
        self.clock = Label(
            self.row_0_column_2, textvariable=self.clock_text,
            bg=bg, fg=fg,
            font=st.font(self.rem, 0),
            bd=0,
            width=2
        )
        self.clock.grid(row=0, column=0, sticky='news', padx=0, pady=0)

    # noinspection PyUnusedLocal
    def build_timer(self, *args):
        """Timer label"""
        b, f = st.set_buttons_color('timer', 1)
        # noinspection PyAttributeOutsideInit
        self.timer = Label(
            self.row_0_column_2,
            text=self.timer_text.get(),
            bg=b, fg=f,
            font=st.font(self.rem, 14)
        )
        self.timer.grid(row=1, column=0, rowspan=2, sticky='nsew')

    # noinspection PyUnusedLocal
    def build_word_label(self, *args):
        """Secret word label"""
        bg, fg = st.set_buttons_color('word', 1)
        # noinspection PyAttributeOutsideInit
        self.secret_word_label = Label(
            self.row_2_grid, textvariable=self.word_text,
            bg=bg, fg=fg, justify=RIGHT,
            font=st.font(self.rem, 16), anchor='e'
        )
        self.secret_word_label.grid(row=0, column=1,
                                    sticky='nse',
                                    padx=20, pady=5)

    # noinspection PyUnusedLocal
    def alert(self, *args):
        """Timer alert for the hard level"""
        if not self.time_left.get():
            self.mini_screen()
            self.word_text.set('Choose your category')
            self.counter.set('')
            self.start_stop_action('stop')
            self.banner_text.set('Random')
            self.quit.config(state=NORMAL)
            self.back.config(state=NORMAL)
            self.timer_text.set(strftime("%H:%M"))

    def draw_word(self):
        """Drawing loop for the secret word label"""
        output = []
        index = 1
        for x in self.secret_word.get():
            if self.level_status == 1:
                if x in self.first_last \
                        or x in self.guesses \
                        or x in [' ', '-']:
                    output.append(x)
                elif x == self.char:
                    output.append(self.char)
                else:
                    output.append('_')
                index += 1
            elif self.level_status >= 2:
                if x in self.guesses or x in [' ', '-']:
                    output.append(x)
                elif x == self.char:
                    output.append(self.char)
                else:
                    output.append('_')
        self.word_text.set(' '.join(output))

    def scoring(self):
        """Scoring method for each level"""
        new = self.char
        total = 'Total'
        xp = 7 - len(self.misses)
        n = 0
        t = 0
        if self.char in self.secret_word.get() and self.char in 'AEIOU':
            if self.level_status == 1:
                n = 4 * xp
            if self.level_status == 2:
                n = 5 * xp
            if self.level_status == 3:
                n = 7 * xp
        elif self.char in self.secret_word.get() and self.char not in 'AEIOU':
            if self.level_status == 1:
                n = 5 * xp
            if self.level_status == 2:
                n = 6 * xp
            if self.level_status == 3:
                n = 8 * xp
        self.total += n

        self.score_text.set(
            f'{new}' + (len(total) + 4 + len(str(t)) - 1) * ' ' + f'{n}\n'
            f'{total}' + 6 * ' ' + f'{self.total}'
        )

    def game_status(self):
        """Checks if it's a win or a loss
        Also changes the countdown label foreground color
        depending to the misses"""
        if len(self.misses) == 7:
            self.mini_screen()
            self.word_text.set('Choose your category')
            self.counter.set('')
            self.start_stop_action('stop')
            self.banner_text.set('Random')
            self.quit.config(state=NORMAL)
            self.back.config(state=NORMAL)
            self.timer_text.set(strftime("%H:%M"))

        if sorted(self.guesses) == sorted(self.sorted):
            if len(rc.search()) < 13:
                rc.add_entry(self.level_status, self.total)
            elif len(rc.search()) == 13 \
                    and rc.search()[13].points < self.total:
                rc.delete()
                rc.add_entry(self.level_status, self.total)
            self.mini_screen()
            self.word_text.set('Choose your category')
            self.counter.set('')
            self.start_stop_action('stop')
            self.banner_text.set('Random')
            self.quit.config(state=NORMAL)
            self.back.config(state=NORMAL)
            self.s_w_list.append(self.secret_word.get())
            self.timer_text.set(strftime("%H:%M"))

    def abc_buttons(self):
        """Creates the alphabet buttons"""
        # noinspection PyAttributeOutsideInit
        r, c = 0, 0
        for item in st.ALPHABET:
            b = Button(
                self.row_1_grid, text='%s' % item,
                bg=st.color['bg'], fg=st.color['fg_abc'],
                font=st.font(self.rem, 1),
                command=lambda i=item: self.set_abc(i),
                justify='center', overrelief=SUNKEN,
                anchor=CENTER, bd=0, state=DISABLED,
                disabledforeground=st.color['dfg_abc'],
                activeforeground=st.color['afg_abc'],
                activebackground=st.color['abg_abc'],
            )
            if c == 13:
                r += 1
                c = 0
            b.grid(row=r, column=c, sticky='news', padx=7, pady=6)
            self.abc.append(b)
            c += 1

    def category_buttons(self):
        """Word category buttons"""
        r, c, bg, s = 0, 0, st.color['bg_cat_a'], NORMAL
        for item in st.EN:
            if item == 'random':
                bg = st.color['fg']
                s = DISABLED
            b = Button(
                self.row_3_grid, text='%s' % item.capitalize(),
                bg=bg, fg=st.color['fg_cat'],
                font=st.font(self.rem, 8),
                command=lambda i=item: self.set_category(i),
                overrelief=SUNKEN,
                anchor=CENTER, bd=0, state=s,
                disabledforeground=st.color['bg'],
                activeforeground=st.color['fg_cat'],
                activebackground=st.color['bg_cat_a'],
                width=1
            )
            if c == 4:
                r += 1
                c = 0
            b.grid(row=r, column=c, sticky='news', padx=15, pady=10)
            self.category.append(b)
            c += 1

    def buttons(self):
        """Info, check buttons"""
        close = st.image('quit')
        info = st.image('info')
        rule = st.image('rule')
        # noinspection PyAttributeOutsideInit
        self.start = self.create_button(self.row_0_grid, 'start')
        self.start.config(width=2, font=st.font(self.rem, -2))
        self.start.grid(row=0, column=0,
                        sticky='news', padx=20, pady=7)
        # noinspection PyAttributeOutsideInit
        self.stop = self.create_button(self.row_0_grid, 'stop')
        self.stop.config(state=DISABLED, width=2, font=st.font(self.rem, -2))
        self.stop.grid(row=1, column=0,
                       sticky='news', padx=20, pady=7)
        # noinspection PyAttributeOutsideInit
        self.quit = self.create_button(self.master, 'exit')
        self.quit.config(font=st.font(self.rem, 1),
                         image=close)
        self.quit.image = close
        self.quit.place(relx=0.99, rely=0.01, anchor='ne')
        # noinspection PyAttributeOutsideInit
        self.score = self.create_button(self.row_0_column_1, 'high score')
        self.score.config(font=st.font(self.rem, -2, style='normal'),
                          overrelief=None, relief=SOLID, bd=0,
                          command=lambda: self.score_screen())
        self.score.grid(row=5, column=0, sticky='news')
        # noinspection PyAttributeOutsideInit
        # self.choose = self.create_button(self.row_0_grid, 'english')
        # self.choose.config(font=st.font(self.rem, 1))
        # self.choose.place(relx=0.67, rely=0.23, x=0, y=0, anchor='se')
        # noinspection PyAttributeOutsideInit
        self.info = self.create_button(self.welcome, 'info')
        self.info.config(font=st.font(self.rem, 0),
                         command=lambda: st.set_rules('Game Info',
                                                      st.prompt['Game Info']),
                         image=info)
        self.info.image = info
        self.info.place(relx=0.01, rely=0.01, anchor='nw')
        # noinspection PyAttributeOutsideInit
        self.rule = self.create_button(self.welcome, 'rules')
        self.rule.config(font=st.font(self.rem, 0),
                         command=lambda: st.set_rules('Game Rules',
                                                      st.prompt['Game Rules']),
                         image=rule)
        self.rule.image = rule
        self.rule.place(relx=0.01, rely=0.1, anchor='nw')
        # noinspection PyAttributeOutsideInit
        self.go = self.create_button(self.welcome, 'ENTER')
        self.go.config(font=st.font(self.rem, 16, family='Verdana'),
                       text='ENTER')
        self.go.pack(side=BOTTOM, expand=False,
                     padx=5, pady=60)
        back = st.image('back')
        # noinspection PyAttributeOutsideInit
        self.back = self.create_button(self.row_0_grid, 'Back')
        self.back.config(font=st.font(self.rem, 1),
                         image=back)
        self.back.image = back
        self.back.place(relx=0.99, rely=0.42, x=0, y=0, anchor='se')
        r, s, bg = 0, NORMAL, st.color['bg_level']
        for item in st.L_EN:
            b = self.create_button(self.row_0_column_3, item)
            if item == 'easy':
                s = DISABLED
                bg = st.color['fg']
            b.config(state=s, font=st.font(self.rem, -4, style='bold'),
                     command=lambda i=item: self.set_level(i), bg=bg)
            b.grid(row=r, column=0, sticky='news', pady=3)
            self.level.append(b)
            r += 1

    def destroy_all(self):
        """Close all windows"""
        st.set_rules('Bye', st.prompt['Bye'])
        sleep(0.6)
        # noinspection PyBroadException
        try:
            self.master.destroy()
            # self.master_2.destroy()
        except NotImplementedError:
            pass

    def set_abc(self, item):
        """Sets the alphabet buttons to the desired state
        depending to guesses and misses.
        calls the draw_word and game_status methods
        """
        self.char = item
        self.scoring()
        bg, dfg, s = st.color['bg'], st.color['dfg_abc_b'], DISABLED
        if item in self.secret_word.get():
            bg, dfg, s = st.color['bg'], st.color['dfg_abc_g'], \
                         DISABLED
            self.guesses.append(item)
        else:
            self.misses.append(item)
        index = 0
        for x in st.ALPHABET:
            self.a.update({x: index})
            index += 1
        self.abc[self.a[item]].config(state=s, bg=bg, disabledforeground=dfg)
        c = 7 - len(self.misses)
        if c == 0:
            c = 7
        self.counter.set(f'{c}')
        self.count.config(fg=st.color[f'{c}'])
        self.draw_word()
        self.game_status()

    def set_welcome(self):
        self.welcome.pack_forget()
        sleep(0.6)

        self.mainframe.pack(fill=BOTH, expand=True)

    def set_back(self):
        self.mainframe.pack_forget()
        sleep(0.4)
        self.welcome.pack(fill=BOTH, expand=True)
        # noinspection PyBroadException
        # try:
        #     self.master_2.destroy()
        # except NotImplementedError:
        #     pass
        self.level[0].config(state=NORMAL)
        self.level[1].config(state=NORMAL)
        self.level[2].config(state=DISABLED)
        self.first_last.clear()

    def set_secret_word(self):
        """Sets the secret word by the user choice"""
        self.guesses.clear()
        self.misses.clear()
        self.char = ''
        search = self.prompt.get()
        lang = st.C_EN
        if search.lower() == 'random':
            from random import choice
            search_query = choice(lang)
        else:
            search_query = search.lower()
        try:
            word = st.open_csv(search_query, self.level_status).upper()
            if word in self.s_w_list:
                word = st.open_csv(search_query, self.level_status).upper()
            self.secret_word.set(word)
            for x in word:
                if x == word[0] or x == word[len(word) - 1]:
                    if x.upper() in self.first_last:
                        continue
                    self.first_last.append(x.upper())
            if self.level_status == 1:
                self.sorted = st.sort(word)
            else:
                self.sorted = st.sort(word, True)
            self.draw_word()
            self.banner_text.set(search_query.capitalize())
        except NotImplementedError:
            pass

    def set_command(self, text):
        """Sets command for buttons"""
        command = None
        if text == 'start':
            command = self.set_start_button
        elif text == 'stop':
            command = self.set_stop_button
        elif text == 'exit':
            command = self.destroy_all
        elif text == 'ENTER':
            command = self.set_welcome
        # elif text == 'english':
        #     command = self.set_language
        elif text == 'Back':
            command = self.set_back
        return command

    # def set_language(self):
    #     """Method for change the categories between english and french"""
    #     if self.choose.cget('text').lower() == 'english':
    #         self.choose.config(text='Francais')
    #         self.lang = 'ENG'
    #     elif self.choose.cget('text').lower() == 'francais':
    #         self.choose.config(text='English')
    #         self.lang = 'FRA'

    def start_stop_action(self, text):
        """Start and stop buttons common actions"""
        bc, ba, bb, dfg, s, s_2, s_3 = None, None, None, None, None, None, None
        sbg, stbg = None, None
        if text == 'start':
            if self.level_status == 3:
                self.clock_text.set('Timer')
            for x in range(3):
                if self.level[x].cget('state') == 'disabled':
                    continue
                else:
                    self.level[x].grid_forget()
            bc = st.color['fg']
            ba = st.color['fg']
            bb = st.color['bg_abc_a']
            dfg = st.color['bg']
            s = DISABLED
            s_2 = NORMAL
            s_3 = NORMAL
            sbg = st.color['fg']
            stbg = st.color['bg_stop']
        if text == 'stop':
            self.first_last.clear()
            self.sorted = ''
            self.banner_text.set('')
            self.clock_text.set('Clock')
            self.running = False
            # self.choose.place(relx=0.67, rely=0.23, x=0, y=0, anchor='se')
            r = 0
            for x in range(3):
                self.level[x].grid(row=r, column=0, sticky='news', pady=3)
                r += 1
            bc = st.color['bg_cat_a']
            ba = st.color['fg']
            bb = st.color['bg']
            dfg = st.color['fg']
            s = NORMAL
            s_2 = DISABLED
            s_3 = DISABLED
            sbg = st.color['bg_start']
            stbg = st.color['fg']
        self.start.config(state=s, bg=sbg)
        self.stop.config(state=s_2, bg=stbg)
        self.total = 0
        self.score_text.set('0\n0')
        for a in range(8):
            if self.category[a].cget('text').lower() == self.prompt.get():
                self.category[a].config(state=DISABLED, bg=ba)
            else:
                self.category[a].config(state=s, bg=bc)
        for i in range(0, 26):
            if self.level_status == 1:
                if self.abc[i].cget('text') in self.first_last:
                    self.abc[i].config(bg=st.color['bg'], state=DISABLED,
                                       disabledforeground=st.color['dfg_abc_g'])
                else:
                    self.abc[i].config(bg=bb, disabledforeground=dfg, state=s_3)
            else:
                self.abc[i].config(bg=bb, disabledforeground=dfg, state=s_3)

    def set_start_button(self):
        """Sets start button action"""
        print("This is working")
        self.time_left.set(st.DEFAULT_GAP)
        self.running = True
        self.counter.set('7')
        self.set_secret_word()
        self.quit.config(state=DISABLED)
        self.back.config(state=DISABLED)
        self.start_stop_action('start')
        # self.choose.place_forget()
        # noinspection PyBroadException
        # try:
        #     if self.master_2:
        #         self.master_2.destroy()
        # except NotImplementedError:
        #     pass

    def set_stop_button(self):
        """Sets stop button action"""
        self.word_text.set('Choose your category')
        self.counter.set('')
        self.quit.config(state=NORMAL)
        self.back.config(state=NORMAL)
        self.start_stop_action('stop')
        self.timer_text.set(strftime("%H:%M"))

    def set_category(self, text):
        """Category buttons function"""
        self.prompt.set(text)
        for a in range(8):
            if self.category[a].cget('text').lower() == text:
                self.category[a].config(state=DISABLED, bg=st.color['fg'])
            else:
                self.category[a].config(state=NORMAL, bg=st.color['bg_cat_a'])

    def set_level(self, text):
        """Method for difficulty level"""
        if text == 'hard':
            self.level_status = 3
        if text == 'medium':
            self.level_status = 2
        if text == 'easy':
            self.level_status = 1
        for x in range(3):
            if self.level[x].cget('text').lower() == text:
                self.level[x].config(state=DISABLED, bg=st.color['fg'])
            else:
                self.level[x].config(state=NORMAL, bg=st.color['bg_level'])

    def update(self):
        """Master window refresh rate, 1 second"""
        time_left = self.time_left.get()
        if self.running and time_left and self.level_status == 3:
            minutes, seconds = st.minutes_seconds(time_left)
            self.timer_text.set(
                '{:0>2}:{:0>2}'.format(minutes, seconds)
            )
            self.time_left.set(time_left - 1)
        self.master.after(1000, self.update)


if __name__ == '__main__':
    root = Tk(className='Guess Letter v2.0')
    Hangman(root)
    root.mainloop()
