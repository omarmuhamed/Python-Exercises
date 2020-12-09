#Colorama package should be installed
from random import randint
import subprocess
import sys

try:
    from colorama import Fore
except:
    print('Installing Colorama package, please wait.')
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "colorama"])


def cls():
    #os.system('cls') is not working on pycharm so that i am printing new-lines instead
    print('\n' * 25)


def distance(p1, p2):
    return ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5


def check_direction(part, ships, shipsize, size):
    checked = []
    valid = True
    while True:
        randdir = randint(0, 1)
        if randdir == 0:
            subdir = randint(0, 1)
            if subdir == 0 and (randdir, subdir) not in checked:
                checked.append((randdir, subdir))
                if part[1] + shipsize - 1 <= size - 1:
                    for i in range(shipsize):
                        if len(list(filter(lambda x: distance((part[0], part[1] + i), x) < 2, ships))) != 0:
                            valid = False
                            break
                    if valid:
                        return (randdir, subdir)
            elif subdir == 1 and (randdir, subdir) not in checked:
                checked.append((randdir, subdir))
                if part[1] - shipsize + 1 >= 0:
                    for i in range(shipsize):
                        if len(list(filter(lambda x: distance((part[0], part[1] - i), x) < 2, ships))) != 0:
                            valid = False
                            break
                    if valid:
                        return (randdir, subdir)
        else:
            subdir = randint(0, 1)
            if subdir == 0 and (randdir, subdir) not in checked:
                checked.append((randdir, subdir))
                if part[0] + shipsize - 1 <= size - 1:
                    for i in range(shipsize):
                        if len(list(filter(lambda x: distance((part[0] + i, part[1]), x) < 2, ships))) != 0:
                            valid = False
                            break
                    if valid:
                        return (randdir, subdir)
            elif subdir == 1 and (randdir, subdir) not in checked:
                checked.append((randdir, subdir))
                if part[0] - shipsize + 1 >= 0:
                    for i in range(shipsize):
                        if len(list(filter(lambda x: distance((part[0] - i, part[1]), x) < 2, ships))) != 0:
                            valid = False
                            break
                    if valid:
                        return (randdir, subdir)
        if len(checked) == 4:
            break
    return None


def print_matrix(board, ships, hits, parts, mode):
    print(' ', end='')
    for i in range(board):
        print(f'{i:4}', end='')

    for i in range(board):

        print(f'{Fore.WHITE}\n{i:<4}', end='')
        for j in range(board):
            if (i, j) in parts:
                print(f'{Fore.GREEN}{"X":<4}', end='')
                continue
            if (i, j) in hits:
                print(f'{Fore.RED}{"*":<4}', end='')
                continue
            if (i, j) in ships and mode == 0:
                print(f'{Fore.GREEN}{"@":<4}', end='')
                continue
            print(f"{Fore.WHITE}{'?':<4}", end='')


def add_ships(a):
    ships = [(randint(0, a - 1), randint(0, a - 1))]
    ships2 = [[ships[0]], [], [], []]
    for i in range(2, 5):
        direction = None
        ship_part = None
        for j in range(i):
            while direction is None:
                ship_part = (randint(0, a - 1), randint(0, a - 1))
                if ship_part not in ships and len(list(filter(lambda x: distance(ship_part, x) < 2, ships))) == 0:
                    direction = check_direction(ship_part, ships, i, a)
                else:
                    continue

            if direction == (0, 0):
                ships.append((ship_part[0], ship_part[1] + j))
                ships2[i - 1].append((ship_part[0], ship_part[1] + j))
            elif direction == (0, 1):
                ships.append((ship_part[0], ship_part[1] - j))
                ships2[i - 1].append((ship_part[0], ship_part[1] - j))
            elif direction == (1, 0):
                ships.append((ship_part[0] + j, ship_part[1]))
                ships2[i - 1].append((ship_part[0] + j, ship_part[1]))
            else:
                ships.append((ship_part[0] - j, ship_part[1]))
                ships2[i - 1].append((ship_part[0] - j, ship_part[1]))
    return [ships, ships2]


def main():
    while True:
        cls()
        diff = int(input('1. Easy\n2. Medium\n3. Hard\n4. Other (Enter by your self)\nSelect Difficulty: '))
        if not 1 <= diff <= 4:
            cls()
            print('Wrong Selection, try again.')
            continue
        elif diff == 1:
            col = 10
        elif diff == 2:
            col = 15
        elif diff == 3:
            col = 20
        elif diff == 4:
            while True:
                col = input('Enter row count: ')
                if col.isnumeric():
                    col = int(col)
                    break
        mode = int(input('1: Açık mode\n2: gizli mode\nSelection (you can change in in game by typing "mode 1" or "mode 2"): '))
        if mode == 1:
            mode = 0
        elif mode == 2:
            mode = 1
        else:
            mode = 1

        ships = add_ships(col)
        ships_list = ships[1]
        ships = ships[0]
        tries = col ** 2 // 3
        hits = []
        broken_parts = []
        check_len = 0
        check_len2 = 0
        error = None
        while True:
            cls()
            print_matrix(col, ships, hits, broken_parts, mode)
            print('\n', end='')
            if len(broken_parts) > check_len:
                counter = 0
                for i in range(4):
                    if len(ships_list[i]) == 0:
                        counter += 1
                if counter > check_len2:
                    print('Congratulations, ship destroyed')
                    check_len2 += 1
                    if check_len2 == 4:
                        print(f'Congratulations, you won!\nScore: {tries}')
                        break
                else:
                    print("Congratulations, part destroyed")
                check_len += 1
            elif tries != col ** 2 // 3 and error is None:
                print("You didn't hit part")
            print(f'Tries left: {tries}')
            if tries == 0:
                print("You lost")
                break
            if error == 1:
                print("Wrong target, try again")
                error = None
            elif error == 2:
                print("You can't hit the same target again.")
                error = None
            print("To reset the game type 'reset'")
            target = input('Enter row and col separated by space (5 6): ')
            if target == 'mode 1':
                mode = 0
                continue
            elif target == 'mode 2':
                mode = 1
                continue
            elif target == 'reset':
                ships = add_ships(col)
                ships_list = ships[1]
                ships = ships[0]
                tries = col ** 2 // 3
                hits = []
                broken_parts = []
                check_len = 0
                check_len2 = 0
                error = None
                continue
            target = target.split(' ')
            if len(target) != 2:
                error = 1
                continue
            if not target[0].isnumeric() or not target[1].isnumeric() or int(target[0]) > col - 1 or int(
                    target[1]) > col - 1:
                error = 1
                continue
            if (int(target[0]), int(target[1])) in ships and (int(target[0]), int(target[1])) not in broken_parts:
                broken_parts.append((int(target[0]), int(target[1])))
                for i in range(4):
                    if (int(target[0]), int(target[1])) in ships_list[i]:
                        ships_list[i].remove((int(target[0]), int(target[1])))
            elif (int(target[0]), int(target[1])) not in hits and (int(target[0]), int(target[1])) not in ships:
                hits.append((int(target[0]), int(target[1])))
            else:
                error = 2
                continue
            tries -= 1
        q = input('Do you want to play again (Y: Yes, N: No): ')
        q = q.upper()
        if q == 'Y':
            continue
        else:
            break


main()