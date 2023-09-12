from unicurses import *
import argparse
from random import choice
import string


def get_args():
    p = argparse.ArgumentParser(
        prog='hangman.py',
        description='Игра виселица (балда)',
        epilog='(с) Александр Килинкаров'
    )
    p.add_argument('-c', default=10, type=int, help='всего сколько ошибок можно допустить')
    p.add_argument('-f', required=True, help='имя файла со словами (слова по одному в строке)')
    return p.parse_args()


def prepare(filename='russian_nouns.txt'):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            word = choice([word.lower().strip() for word in f if word.strip()])
    except FileNotFoundError:
        print('Нет такого файла')
        exit()
    except PermissionError:
        print('Невозможно прочесть файл')
        exit()
    except:
        print('Что-то пошло не так')
        exit()
    tablo = list('*' * len(word))
    return word, tablo


def hangman(tries_count=5, filename='russian_nouns.txt'):
    word, tablo = prepare(filename=filename)
    alpha = string.digits + string.ascii_lowercase + 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    used_letters = []
    tries = 0
    while tries < tries_count:
        wborder(stdscr, 0)
        mvaddstr(3, 5, f'Игра Виселица', A_BOLD | color_pair(1))
        mvaddstr(5, 5, f'Ошибок {tries}/{tries_count}')
        mvaddstr(6, 5, '0 - слово целиком, или буква (Escape - выход)')
        if used_letters:
            mvaddstr(7, 5, 'Использованные буквы: ' + ', '.join(used_letters))
        mvaddstr(ROWS//2, COLS//2 - len(word)//2, ''.join(tablo))
        
        refresh()
        
        k = get_wch()
        
        # Check Esc or Alt
        if k == 27: 
            # Esc or Alt
            # Don't need to wait for another key
            # If it was Alt then curses has already sent the other key
            # If it was Escape key, -1 is sent
            nodelay(stdscr, True)
            x = getch()
            if x == -1: # Escape
                exit()
            nodelay(stdscr, False)
            
        answer = chr(k).lower()
        if answer not in alpha:
            continue
        used_letters.append(answer)        

        if answer == '0':
            clear()
            wborder(stdscr, 0)
            mvaddstr(3, 5, f'Игра Виселица', A_BOLD | color_pair(1))
            mvaddstr(ROWS//2, COLS//2 - len(word)//2, ''.join(tablo))
            mvaddstr(ROWS//2 + 1, COLS//2 - len(word)//2, 'Назови слово: ')
            
            curs_set(1)
            echo()
            refresh()
            
            u_word = getstr().lower().strip()
            
            if u_word == word:
                tablo = [i for i in word]
            break
        else:
            u_letter = answer
            
            if u_letter in word:
                for i in range(len(word)):
                    if word[i] == u_letter:
                        tablo[i] = word[i]
                if '*' not in tablo:
                    break
            else:
                tries += 1
        clear()
        
    clear()
    wborder(stdscr, 0)
    mvaddstr(3, 5, f'Игра Виселица', A_BOLD | color_pair(1))
    msg = ('Ты проиграл!', 2) if '*' in tablo else ('Ты выиграл!', 1)

    mvaddstr(5, 5, f'Ошибок {tries}/{tries_count}')
    mvaddstr(ROWS//2-1, COLS//2 - len(word)//2, f'Загаданное слово: {word}')
    mvaddstr(ROWS//2, COLS//2 - len(word)//2, msg[0], A_BOLD | color_pair(msg[1]))
    mvaddstr(ROWS//2+1, COLS//2 - len(word)//2, 'Нажми enter для выхода...')
    curs_set(0)
    refresh()

if __name__ == '__main__':    
    stdscr = initscr()
    ROWS, COLS = getmaxyx(stdscr)

    noecho()
    curs_set(0)
    start_color()
    init_pair(1, COLOR_GREEN, COLOR_BLACK)
    init_pair(2, COLOR_RED, COLOR_BLACK)
    
    args = get_args()
    hangman(tries_count=args.c, filename=args.f)
    
    getch()
    endwin()

