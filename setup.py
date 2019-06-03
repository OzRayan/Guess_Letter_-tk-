from collections import OrderedDict
from PIL import Image, ImageTk
from tkinter import messagebox

# names_file = open("names.txt", encoding="utf-8")
# data = names_file.read()
# names_file.close()


def image(var):
    img = Image.open('PNG/{}.png'.format(var))
    photo = ImageTk.PhotoImage(img)
    return photo


# TODO: Change to English words only, take out 'item'
def open_csv(search_query, level):
    """Open the selected csv file and returns a random word"""
    from random import choice
    from csv import reader
    # from csv import DictReader, DictWriter, reader, writer
    try:
        with open('WORDS/{}.csv'.format(search_query), 'r') as file:
            animals = reader(file)
            words = []
            for item in animals:
                # words.append(item[0])
                if level == 1 and len(item[0]) < 13:
                    words.append(item[0].lower())
                elif level == 2:
                    words.append(item[0].lower())
                elif level == 3 and len(item[0]) >= 13:
                    words.append(item[0].lower())
            #     print(item[0])
            # print([item for item in items])
            # with open('ENG/all.csv', 'w', newline='\n') as wr:
            #     # fields = ['animal', 'plant', 'object', 'geography',
            #     #           'invention', 'history', 'sport']
            #     writer_file = writer(wr, delimiter=',')
            #     # writer_file.writeheader()
            #     writatle = []
            #     # print([item for item in items])
            #     for line in animals:
            #         print(line)
            #         if 7 <= len(line[0]) <= 18 and line[0] not in writatle:
            #             writer_file.writerow(line)
            #             writatle.append(line[0])
            if len(words) != 0:
                word = choice(words)
            else:
                word = open_csv(choice(C_EN), 2)
            # file.close()
        return word
    except FileNotFoundError as err:
        print(err)


# open_csv('convert', 'ENG')


def set_buttons_color(text, item=None):
    """Sets buttons color:
    background (bg)
    foreground (fg)
    disabledforground (dfg)
    activebackground (abg)
    activeforeground (afg)"""
    bg, fg, abg, afg, dfg = None, None, None, None, None
    if text in ['info', 'rules', 'ok']:
        bg = color['bg']
        fg = color['fg']
        abg = color['bg']
        afg = color['afg_info']
        dfg = color['bg']
    elif text == 'exit':
        bg = color['bg']
        fg = color['dfg_start']
        abg = color['bg']
        afg = color['dfg_start']
        dfg = color['bg_info']
    elif text == 'high score':
        bg = color['bg_score']
        fg = color['bg']
        abg = color['bg_score']
        afg = color['fg_score']
        dfg = 'white'
    elif text == 'start':
        bg = color['bg_start']
        fg = color['fg_start']
        abg = color['bg_start']
        afg = color['fg_start']
        dfg = color['bg']
    elif text == 'stop':
        bg = color['fg']
        fg = color['fg_start']
        abg = color['bg_stop']
        afg = color['fg_start']
        dfg = color['bg']
    elif text == 'ENTER':
        bg = color['bg']
        fg = color['fg_enter']
        abg = color['bg']
        afg = color['fg_enter']
        dfg = color['bg']
    elif text == 'Back':
        bg = color['bg']
        fg = color['fg_back']
        abg = color['bg']
        afg = color['fg_back']
        dfg = color['bg']
    elif text in ['english', 'francais']:
        bg = color['bg']
        fg = color['fg_title']
        abg = color['bg']
        afg = color['fg_title']
        dfg = color['bg']
    elif text in L_EN:
        bg = color['bg_level']
        fg = color['fg_level']
        abg = color['bg_level']
        afg = color['fg_level']
        dfg = color['bg']
    elif text == 'score':
        bg = color['bg']
        fg = color['fg_start']
    elif text == 'timer':
        bg = color['bg']
        fg = color['fg_enter']
    elif text == 'points':
        bg = color['fg']
        fg = color['bg']
    elif text == 'word':
        bg = color['bg']
        fg = color['fg_enter']
    elif text in ['welcome', 'title']:
        bg = color['bg']
        fg = color['fg_title']
    if item:
        return bg, fg
    return bg, fg, abg, afg, dfg


def set_rules(key, value):
    """Info, Rules, Bye message"""
    messagebox.showinfo(key, value)


def sort(item, boolean=False):
    """Arranges the secret word letters in alphabetical order"""
    char_list = []
    for x in item:
        if x in char_list:
            continue
        elif x in [' ', '-']:
            continue
        elif x == item[0] or x == item[len(item) - 1]:
            if boolean is True:
                char_list.append(x)
            continue
        else:
            char_list.append(x)
    return char_list


def font(unit, size, family=None, style=None):
    """Font setter for all the widgets"""
    f, s, sy = 'Comic Sans MS', 1, 'bold'
    rem = int(unit / 100 * (size * 0.05 + s))
    if not family and not style:
        return f, rem, sy
    if family and style:
        return family, rem, style
    if not family and style:
        return f, rem, style
    if family and not style:
        return family, rem, sy


def minutes_seconds(seconds):
    """Method for timer time
    Returns a tuple of minutes and second for the timer"""
    return int(seconds / 60), int(seconds % 60)


DEFAULT_GAP = 60 * 3
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
EN = ['animal', 'plant', 'object', 'geography',
      'invention', 'history', 'sport', 'random']
C_EN = ['animal', 'plant', 'object', 'geography',
        'invention', 'history', 'sport']
L_EN = ['hard', 'medium', 'easy']
P_EN = OrderedDict([
    ('won', 'Congratulation\n'
            'You won\n'
            '\n'
            'Level: {}\n'
            'Word: {}\n'
            'Total points: {}\n'
            '{}'),
    ('lose', 'Game over\n'
             'You lost\n')
])
prompt = {'Game Rules': "The game follows the same rules\n"
                        "as Hangman.\n"
                        "Every bad guess will decrease the\n"
                        "the countdown.\n"
                        "Every new game has 7 bad guesses.\n"
                        "The words are selected automatically \n"
                        "from all categories if it's not \n"
                        "selected manually.\n"
                        "After every game the selection jumps\n"
                        "back to all categories\n"
                        "Happy gaming!",
          'Game Info': "Bad 7 it's a version of\n"
                        "Hangman.\n"
                        "The game it's build just only\n"
                        "for entertainment purposes.\n"
                        "For now only available only\n"
                        "first 4 categories.\n"
                        "Score it will be available in future.\n"
                        "Future update_entry may be possible.",
          'Bye': 'Thank you for playing\nBye!'}
color = OrderedDict([
    ('bg', '#d8d8d8'),
    ('fg', '#8B8C8C'),
    ('1', '#FF0000'),
    ('2', '#FF7700'),
    ('3', '#FFC400'),
    ('4', '#FFFB00'),
    ('5', '#B7FF00'),
    ('6', '#7BFF00'),
    ('7', '#00FF15'),
    ('bg_info', '#DBDBDB'),
    ('abg_info', '#8B8C8C'),
    ('afg_info', '#3F4040'),
    ('fg_back', '#0008E3'),
    ('bg_level', '#D18EC7'),
    ('fg_level', '#4A033F'),
    ('bg_score', '#734A94'),
    ('fg_score', '#22013D'),
    ('bg_cat_a', '#0f9'),
    ('fg_cat', '#004A2C'),
    ('abg_cat', '#09f'),
    ('afg_cat', '#229DAB'),
    ('bg_start', '#77FF73'),
    ('fg_start', '#00540D'),
    ('dfg_start', '#bf0000'),
    ('afg_start', '#E60000'),
    ('abg_start', '#011400'),
    ('abg_stop', '#290101'),
    ('bg_stop', '#FF6B7F'),
    ('bg_abc_a', '#A5C2D6'),
    ('fg_abc', '#09f'),
    ('dfg_abc', '#aaa'),
    ('dfg_abc_g', '#0f2'),
    ('dfg_abc_b', '#f66'),
    ('afg_abc', '#333'),
    ('abg_abc', '#aaa'),
    ('fg_word', '#222'),
    ('dfg_word', '#818581'),
    ('fg_title', '#FF8C00'),
    ('fg_enter', '#404040')])
