import argparse
from random import choice


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
            word = choice([word.lower().strip() for word in f])
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
    tries = 0
    while tries < tries_count:
        print(f'Ошибок {tries}/{tries_count}')
        print(''.join(tablo))
        answer = input('0 - слово целиком, или буква --> ').lower().strip()
        if answer == '0':
            u_word = input('Назови слово: ').lower().strip()
            if u_word == word:
                tablo = [i for i in word]
            break
        else:
            u_letter = answer
            if u_letter in word and len(u_letter) == 1:
                for i in range(len(word)):
                    if word[i] == u_letter:
                        tablo[i] = word[i]
                if '*' not in tablo:
                    break
            else:
                tries += 1
    if '*' in tablo:
        print('Ты проиграл!')
    else:
        print('Ты выиграл!')
    print(word)


if __name__ == '__main__':
    args = get_args()
    hangman(tries_count=args.c, filename=args.f)
