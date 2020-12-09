while True:
    capitalchars = 0
    smallchars = 0
    notalphanum = 0
    spaces = 0
    nums = 0
    charsinseq = 0
    valid = True
    password = input('Enter password: ')
    for i in range(len(password)):
        if i < len(password) - 1:
            part1 = chr(ord(password[i]) + 32) if 65 <= ord(password[i]) <= 90 else password[i]
            part2 = chr(ord(password[i + 1]) + 32) if 65 <= ord(password[i + 1]) <= 90 else password[i + 1]
            if (part1 + part2 != 'z0' and part1 + part2 in 'abcdefghijklmnopqrstuvwxyz0123456789') or (part1 + part2 != '0z' and part1 + part2 in '9876543210zyxwvutsrqponmlkjihgfedcba'):
                charsinseq += 1
        if password[i] == ' ':
            spaces += 1
        elif 65 <= ord(password[i]) <= 90:
            capitalchars += 1
        elif 97 <= ord(password[i]) <= 122:
            smallchars += 1
        elif 48 <= ord(password[i]) <= 57:
            nums += 1
        else:
            notalphanum += 1

    if len(password) < 8 or len(password) > 12:
        print('Password can\'t be neither less than 8 chars nor more than 12 chars')
        valid = False

    if len(password) != len(set(password)):
        print('Password shouldn\'t contain repeated chars')
        valid = False

    if password[0] in '0123456789' or password[-1] in '0123456789':
        print('Password can\'t start or end with number')
        valid = False

    if capitalchars == 0:
        print('Password should contain at least 1 capital char')
        valid = False

    if smallchars == 0:
        print('Password should contain at least 1 small char')
        valid = False

    if notalphanum == 0:
        print('Password should contain at least 1 non-alphanumeric char')
        valid = False

    if nums == 0:
        print('Password should contain at least 1 number')
        valid = False

    if spaces != 0:
        print('Password shouldn\'t contain spaces')
        valid = False

    if charsinseq != 0:
        print('Password can\'t contain chars or numbers in sequence')
        valid = False

    if valid:
        break

print('Your password is valid and can be used')
