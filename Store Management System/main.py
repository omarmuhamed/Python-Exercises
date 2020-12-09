from datetime import datetime
import os

Error_Codes = {
    45: 'Login failed, account is not active',
    1: 'Username not found.',
    2: 'password is not correct',
    3: 'Your new password can\'t be the same as old password',
    4: 'Password can\'t be neither less than 8 chars nor more than 12 chars',
    5: 'Password shouldn\'t contain repeated chars',
    6: 'Password can\'t start or end with number',
    7: 'Password should contain at least 1 capital char',
    8: 'Password should contain at least 1 small char',
    9: 'Password should contain at least 1 non-alphanumeric char',
    10: 'Password should contain at least 1 number',
    11: 'Password shouldn\'t contain spaces',
    12: 'Password can\'t contain chars or numbers in sequence',
    13: 'ID should be 11 digits',
    14: 'ID already used',
    15: 'Invalid Number',
    16: 'Invalid Name',
    17: 'Name already used',
    18: 'Category not found',
    19: 'Item not found',
    20: 'Quantity should be more than 0',
    21: 'There are not enough items in stock',
    22: 'Quantity you entered exceeds the quantity in cart',
    23: 'Cart is empty',
    24: 'The amount can\'t be less than the total price',
    25: 'Refund should be made within 3 days after buying',
    26: 'Transaction not found',
    27: 'There are no refundable transactions',
    28: 'Invalid username',
    29: 'Username can\'t start with number.',
    30: 'Username can\'t contain any special character including spaces',
    31: 'Username is already used.',
    32: 'Birth date should be in dd-mm-yyyy format',
    33: 'User not found',
    34: 'User is already suspended.',
    35: 'User is already active',
    36: 'User is already admin',
    37: 'User is not admin',
    38: 'This field is required',
    39: 'Inventory is empty',
    40: 'There are no categories',
    41: 'No users found',
    42: 'ID can only contain numbers',
    43: 'Can\'t add item because there are no categories',
    44: 'There are no transactions'
}
Success_Codes = {
    1: 'Successfully logged in as admin.',
    2: 'Successfully logged in as staff.',
    3: 'Item added successfully',
    4: 'Item removed successfully',
    5: 'Category added successfully',
    6: 'Category removed successfully',
    7: 'Category edited successfully',
    8: 'Item edited successfully',
    9: 'Item added to cart',
    10: 'Item removed from the cart',
    11: 'Entered quantity removed from the cart',
    12: 'Thanks for visiting us.',
    13: 'Successfully refunded',
    14: 'Password changed successfully',
    15: 'User added successfully',
    16: 'User removed successfully',
    17: 'User successfully suspended',
    18: 'User successfully activated',
    19: 'Admin role given successfully',
    20: 'Admin role removed successfully',
    21: 'User edited successfully',
    22: 'Quantity changed successfully'
}
Note_Codes = {
    0: 'Press ENTER to continue......',
    1: 'leave blank if you don\'t want to change.',
    2: "leave blank if you want to back to the menu",
    3: 'leave blank to remove the item from the cart or enter specific quantity to remove',
    4: 'leave blank to back to the menu',
    5: 'leave blank to enter the total',
    6: 'Enter "exit" to back to the menu'
}


class COLORS:
    RED = "\x1b[91;1m"
    GREEN = "\x1b[92;1m"
    YELLOW = "\x1b[93;1m"
    RESET = "\x1b[96;1m"


print(COLORS.RESET)


class Table:
    def __init__(self, content, headers):
        self.table = self.create_table(content, headers)

    @staticmethod
    def special_len(string):
        if isinstance(string, str):
            if "\x1b" in string:
                return len(string) - 7
        return len(string)

    @staticmethod
    def build_row(padded_cells, rowfmt):
        begin, sep, end = rowfmt
        return (begin + sep.join(padded_cells) + end).rstrip()

    @staticmethod
    def build_line(colwidths, linefmt):
        begin, fill, sep, end = linefmt
        cells = [fill * w for w in colwidths]
        return (begin + sep.join(cells) + end).rstrip()

    @staticmethod
    def padding(width, s):
        fmt = "{0:^%ds}" % width
        if "\x1b" in s:
            fmt = "{0:^%ds}" % (int(width) + 7)
        return fmt.format(s)

    @staticmethod
    def pad_row(cells):
        pad = " "
        padded_cells = [pad + cell + pad for cell in cells]
        return padded_cells

    def align_col(self, strings, minwidth):
        maxwidth = max(max(map(self.special_len, strings)), minwidth)
        padded_strings = [self.padding(maxwidth, s) for s in strings]
        return padded_strings

    def create_table(self, data, headers):
        lines = []
        cols = list(zip(*data))
        minwidths = [len(h) + 2 for h in headers]
        cols = [self.align_col(c, minw) for c, minw in zip(cols, minwidths)]
        minwidths = [max(minw, self.special_len(c[0])) for minw, c in zip(minwidths, cols)]
        headers = [self.padding(minw, h) for h, minw in zip(headers, minwidths)]
        rows = list(zip(*cols))
        padded_widths = [(w + 2) for w in minwidths]
        padded_headers = self.pad_row(headers)
        padded_rows = [self.pad_row(row) for row in rows]
        lines.append(self.build_line(padded_widths, ('┌', '─', '+', '┐')))
        if padded_headers:
            lines.append(self.build_row(padded_headers, ('|', '|', '|')))
            lines.append(self.build_line(padded_widths, ('|', '=', '+', '|')))
        if padded_rows:
            for row in padded_rows[:-1]:
                lines.append(self.build_row(row, ('|', '|', '|')))
                lines.append(self.build_line(padded_widths, ('|', '─', '+', '|')))
            lines.append(self.build_row(padded_rows[-1], ('|', '|', '|')))
        lines.append(self.build_line(padded_widths, ('└', '─', '+', '┘')))
        return "\n".join(lines)

    def __str__(self):
        return self.table


class File:
    def __init__(self, file, ext):
        self.filename = file
        self.extension = ext

    def read(self):
        my_file = open(self.filename + self.extension)
        content = my_file.read().rsplit('\n')
        my_file.close()
        return content

    def write(self, content):
        my_file = open(self.filename + self.extension, 'w')
        my_file.write(content)
        my_file.close()

    def edit(self, old_content, new_content, line):
        if new_content == '':
            old_content.pop(line)
        else:
            old_content[line] = new_content
        self.write('\n'.join(old_content))

    def append(self, content):
        my_file = open(self.filename + self.extension, 'a')
        my_file.write('\n')
        my_file.write(','.join(content))
        my_file.close()


class UserManagement:
    def __init__(self):
        self.users_data = File('users', '.txt')
        self.isAdmin = None
        self.loggedUser = None
        self.operations = {'username': ['check_username', ['users']], 'password': ['check_password_strength', ['None']],
                           'name': ['check_name', ['None']], 'email': ['check_email', ['None']],
                           'birth_date': ['check_birth_date', ['None']], 'id': ['check_id', ['users']]}
        self.input_messages = {'username': 'Enter username: ', 'password': 'Enter password: ', 'name': 'Enter name: ',
                               'email': 'Enter email: ', 'birth_date': 'Enter date of birth: ', 'id': 'Enter ID No: '}

    def login(self):
        users = self.users_data.read()
        while True:
            username = input('\t' + 5 * ' ' + 'Enter username: ')
            if not username.isalnum():
                yield {'error': 28}
                continue
            password = input('\t' + 5 * ' ' + 'Enter password: ')
            found = None
            match = None
            active = None
            admin = None
            for i in range(1, len(users)):
                if users[i].rsplit(',')[0].lower() == username.lower():
                    found = True
                    if users[i].rsplit(',')[1] == password:
                        match = True
                        if users[i].rsplit(',')[6] == '1':
                            active = True
                            if users[i].rsplit(',')[7] == '1':
                                admin = True
                                break

            if match and not active:
                yield {'error': 45}
            elif match and admin:
                self.loggedUser = username
                self.isAdmin = True
                yield {'success': 1}
                break
            elif match and not admin:
                self.loggedUser = username
                yield {'success': 2}
                break
            elif not found:
                yield {'error': 1}
            elif not match:
                yield {'error': 2}

    def edit(self, inside=True):
        users = self.users_data.read()

        exit = False
        yield {'note': 6}
        while True:
            if inside:
                user = self.loggedUser
            else:
                user = input('Enter user\'s name or ID number: ')
                if user.lower() == 'exit':
                    break
                elif not user:
                    yield {'error': 38}
                    continue
            row = self.search(users, user, 0) or self.search(users, user, 5)
            if row:
                yield {'note': 1}
                old_data = users[row].rsplit(',')
                inputs = []
                i = 0
                for key, value in self.operations.items():
                    while True:
                        if (self.isAdmin and key != 'password') or (
                                not self.isAdmin and key != 'password' and key != 'id'):
                            user_input = input(self.input_messages[key])
                            if user_input == '':
                                inputs.append(old_data[i])
                                break
                            elif user_input.lower() == 'exit':
                                exit = True
                                break
                            func_call = getattr(self, value[0])(user_input, eval(*value[1]))
                            if isinstance(func_call, bool) and func_call is True:
                                inputs.append(user_input)
                                break
                            else:
                                yield func_call
                        else:
                            break
                    if exit:
                        break
                    i += 1
                if not exit:
                    new_data = inputs
                    new_data.insert(1, old_data[1])
                    if not self.isAdmin:
                        new_data.insert(5, old_data[5])
                    self.users_data.edit(users, ','.join(new_data + old_data[6:]), row)
                    yield {'success': 21}
                    break
                else:
                    break
            else:
                yield {'error': 33}
                continue

    def change_password(self):
        users = self.users_data.read()
        yield {'note': 6}
        while True:
            old_password = input('Enter your old password: ')
            if old_password.lower() == 'exit':
                break
            elif not old_password:
                yield {'error': 38}
                continue
            row = self.search(users, self.loggedUser, 0)
            if users[row].rsplit(',')[1] == old_password:
                while True:
                    new_password = input('Enter a new password: ')
                    if new_password == old_password:
                        yield {'error': 3}
                        continue
                    elif not new_password:
                        yield {'error': 38}
                        continue
                    elif new_password.lower() == 'exit':
                        break
                    func_call = self.check_password_strength(new_password)
                    if isinstance(func_call, bool) and func_call is True:
                        new_row = users[row].rsplit(',')
                        new_row[1] = new_password
                        new_row = ','.join(new_row)
                        users[row] = new_row
                        self.users_data.edit(users, new_row, row)
                        yield {'success': 14}
                        break
                    else:
                        yield func_call
                break
            else:
                yield {'error': 2}

    @staticmethod
    def check_password_strength(password, *_):
        capitalchars = 0
        smallchars = 0
        notalphanum = 0
        spaces = 0
        nums = 0
        charsinseq = 0
        errors = []
        valid = True
        for j in range(len(password)):
            if j < len(password) - 1:
                part1 = chr(ord(password[j]) + 32) if 65 <= ord(password[j]) <= 90 else password[j]
                part2 = chr(ord(password[j + 1]) + 32) if 65 <= ord(password[j + 1]) <= 90 else password[j + 1]
                if (part1 + part2 != 'z0' and part1 + part2 in 'abcdefghijklmnopqrstuvwxyz0123456789') or (
                        part1 + part2 != '0z' and part1 + part2 in '9876543210zyxwvutsrqponmlkjihgfedcba'):
                    charsinseq += 1
            if password[j] == ' ':
                spaces += 1
            elif 65 <= ord(password[j]) <= 90:
                capitalchars += 1
            elif 97 <= ord(password[j]) <= 122:
                smallchars += 1
            elif 48 <= ord(password[j]) <= 57:
                nums += 1
            else:
                notalphanum += 1

        if len(password) < 8 or len(password) > 12:
            errors.append({'error': 4})
            valid = False

        if len(password) != len(set(password)):
            errors.append({'error': 5})
            valid = False

        if password[0] in '0123456789' or password[-1] in '0123456789':
            errors.append({'error': 6})
            valid = False

        if capitalchars == 0:
            errors.append({'error': 7})
            valid = False

        if smallchars == 0:
            errors.append({'error': 8})
            valid = False

        if notalphanum == 0:
            errors.append({'error': 9})
            valid = False

        if nums == 0:
            errors.append({'error': 10})
            valid = False

        if spaces != 0:
            errors.append({'error': 11})
            valid = False

        if charsinseq != 0:
            errors.append({'error': 12})
            valid = False

        if valid:
            return True
        else:
            return errors

    @staticmethod
    def search(users, a, col):
        for i in range(1, len(users)):
            if a.lower() == users[i].rsplit(',')[col].lower():
                return i
        return False

    def check_username(self, username, users, *_):
        if not username.isalnum():
            return {'error': 30}
        if username[0].isnumeric():
            return {'error': 29}
        if self.search(users, username, 0):
            return {'error': 31}
        return True

    @staticmethod
    def check_name(name, *_):
        if name.replace(' ', '').isalpha():
            return True
        return {'error': 16}

    @staticmethod
    def check_email(email, *_):
        return True

    @staticmethod
    def check_birth_date(birth_date, *_):
        birth_date = birth_date.split('-')
        if len(birth_date) == 3:
            if birth_date[0].isnumeric() and birth_date[1].isnumeric() and birth_date[2].isnumeric() and \
                    1 <= int(birth_date[0]) <= 31 and \
                    1 <= int(birth_date[1]) <= 12 and \
                    1900 <= int(birth_date[2]) <= 2000:
                return True
        return {'error': 32}

    @staticmethod
    def check_id(id_no, users, *_):
        if len(id_no) != 11 or not id_no.isnumeric():
            return {'error': 13}
        for i in range(1, len(users)):
            if id_no == users[i].rsplit(',')[5]:
                return {'error': 14}
        return True


class StaffManagement(UserManagement):
    def __init__(self):
        UserManagement.__init__(self)

    def add_staff(self):
        users = self.users_data.read()
        inputs = []
        exit = False
        yield {'note': 6}
        for key, value in self.operations.items():
            while True:
                user_input = input(self.input_messages[key])
                if not user_input:
                    yield {'error': 38}
                    continue
                if user_input.lower() == 'exit':
                    exit = True
                    break
                func_call = getattr(self, value[0])(user_input, eval(*value[1]))
                if isinstance(func_call, bool) and func_call is True:
                    inputs.append(user_input)
                    break
                else:
                    yield func_call
            if exit:
                break
        if not exit:
            self.users_data.append(inputs + ['1', '0'])
            yield {'success': 15}

    def remove_staff(self):
        users = self.users_data.read()
        yield {'note': 2}
        while True:
            user = input('Enter username or ID number: ')
            if not user:
                break
            row = self.search(users, user, 5) or self.search(users, user, 0)
            if row:
                self.users_data.edit(users, '', row)
                yield {'success': 16}
                break
            else:
                yield {'error': 33}

    def edit_staff(self):
        yield from self.edit(False)

    def suspend_staff(self):
        yield from self.change_status(6, '0', 17, 34)

    def activate_staff(self):
        yield from self.change_status(6, '1', 18, 35)

    def add_admin(self):
        yield from self.change_status(7, '1', 19, 36)

    def remove_admin(self):
        yield from self.change_status(7, '0', 20, 37)

    def change_status(self, col, status, success, error):
        users = self.users_data.read()
        yield {'note': 2}
        while True:
            user_input = input('Enter username or ID number: ')
            if not user_input:
                break
            row = self.search(users, user_input, 5) or self.search(users, user_input, 0)
            if row:
                if users[row].rsplit(',')[col] != status:
                    new_data = users[row].rsplit(',')
                    new_data[col] = status
                    new_data = ','.join(new_data)
                    self.users_data.edit(users, new_data, row)
                    yield {'success': success}
                    break
                else:
                    yield {'error': error}
                    break
            else:
                yield {'error': 33}

    def listing(self):
        users = self.users_data.read()
        headers = users[0].rsplit(',')
        headers.pop(1)
        content = []
        if len(users) > 1:
            for user in users[1:]:
                splitted_row = user.rsplit(',')
                splitted_row[7] = 'Admin' if splitted_row[7] == '1' else 'Staff'
                if splitted_row[6] == '0':
                    splitted_row[6] = 'Suspended'
                    splitted_row[0] = COLORS.RED + splitted_row[0]
                    splitted_row[-1] = splitted_row[-1] + COLORS.RESET
                else:
                    splitted_row[6] = 'Active'
                    splitted_row[0] = COLORS.GREEN + splitted_row[0]
                    splitted_row[-1] = splitted_row[-1] + COLORS.RESET
                splitted_row.pop(1)
                content.append(splitted_row)

        return [content, headers]


class Inventory:
    def __init__(self):
        self.inventory = File('inventory', '.txt')
        self.categories = File('Categories', '.txt')
        self.inventory_operation = {'id': ['check_id', ['inventory']], 'name': ['check_name', ['inventory']],
                                    'category': ['check_category', ['categories']],
                                    'quantity': ['check_num', ['"int"']],
                                    'cost_price': ['check_num', ['None']], 'profit_ratio': ['check_num', ['None']],
                                    'vendor': ['check_name', ['None']]}
        self.inv_input_messages = {'id': 'Enter item ID: ', 'name': 'Enter item\'s name: ',
                                   'category': 'Enter category name or ID: ',
                                   'quantity': 'Enter quantity: ',
                                   'cost_price': 'Enter cost price: ', 'profit_ratio': 'Enter the profit ratio(%): ',
                                   'vendor': 'Enter vendor\'s name: '}
        self.cat_operations = {'id': ['check_id', ['categories']], 'name': ['check_name', ['categories']],
                               'tax': ['check_num', ['None']]}
        self.cat_input_messages = {'id': 'Enter ID no: ', 'name': 'Enter name: ', 'tax': 'Enter tax percentage: '}

    def add_item(self):
        inventory = self.inventory.read()
        categories = self.categories.read()
        if len(categories) > 1:
            inputs = []
            exit = False
            yield {'note': 6}
            for key, value in self.inventory_operation.items():
                while True:
                    user_input = input(self.inv_input_messages[key])
                    if user_input.lower() == 'exit':
                        exit = True
                        break
                    elif not user_input:
                        yield {'error': 38}
                        continue
                    func_call = getattr(self, value[0])(user_input, eval(*value[1]))
                    if isinstance(func_call, bool) and func_call is True:
                        inputs.append(user_input)
                        break
                    else:
                        yield func_call
                if exit:
                    break
            if not exit:
                sell_price = float(inputs[4]) * (1. + float(inputs[5]) / 100.) + self.calculate_tax(inputs[2],
                                                                                                    float(inputs[4]))
                inputs.insert(6, str(format(sell_price, '.2f')))
                self.inventory.append(inputs)
                yield {'success': 3}
        else:
            yield {'error': 43}

    def remove_item(self):
        inventory = self.inventory.read()
        if len(inventory) > 1:
            yield {'note': 2}
            while True:
                user_input = input('Enter item ID or name: ')
                if not user_input:
                    break
                row = self.search(inventory, user_input)
                if row:
                    self.inventory.edit(inventory, '', row)
                    yield {'success': 4}
                    break
                else:
                    yield {'error': 19}
        else:
            yield {'error': 39}

    def increase_quantity(self):
        yield from self.change_quantity(1)

    def decrease_quantity(self):
        yield from self.change_quantity(-1)

    def change_quantity(self, a):
        inventory = self.inventory.read()
        done = None
        yield {'note': 2}
        while True:
            user_input = input('Enter item ID or name: ')
            if not user_input:
                break
            row = self.search(inventory, user_input)
            if row:
                while True:
                    user_input_2 = input('Enter Quantity: ')
                    if not user_input_2:
                        done = True
                        break
                    num_check = self.check_num(user_input_2, 'int')
                    if isinstance(num_check, bool) and num_check is True:
                        if int(inventory[row].rsplit(',')[3]) + a * int(user_input_2) >= 0:
                            new_row = inventory[row].rsplit(',')
                            new_row[3] = str(int(new_row[3]) + a * int(user_input_2))
                            new_row = ','.join(new_row)
                            self.inventory.edit(inventory, new_row, row)
                            yield {'success': 22}
                            done = True
                            break
                        else:
                            yield {'error': 20}
                    else:
                        yield num_check
            else:
                yield {'error': 19}
            if done:
                break

    def edit_item(self):
        inventory = self.inventory.read()
        if len(inventory) > 1:
            categories = self.categories.read()
            exit = False
            yield {'note': 6}
            while True:
                item = input('Enter item\'s name or ID : ')
                if item.lower() == 'exit':
                    break
                elif not item:
                    yield {'error': 38}
                    continue
                row = self.search(inventory, item)
                if row:
                    yield {'note': 1}
                    old_data = inventory[row].rsplit(',')
                    old_data.pop(6)
                    inputs = [old_data[0]]
                    i = 0
                    for key, value in self.inventory_operation.items():
                        while True:
                            if key != 'id':
                                user_input = input(self.inv_input_messages[key])
                                if user_input == '':
                                    inputs.append(old_data[i])
                                    break
                                elif user_input.lower() == 'exit':
                                    exit = True
                                    break
                                func_call = getattr(self, value[0])(user_input, eval(*value[1]))
                                if isinstance(func_call, bool) and func_call is True:
                                    inputs.append(user_input)
                                    break
                                else:
                                    yield func_call
                            else:
                                break
                        if exit:
                            break
                        i += 1
                    if not exit:
                        sell_price = float(inputs[4]) * (1. + float(inputs[5]) / 100.) + self.calculate_tax(inputs[2], float(inputs[4]))
                        inputs.insert(6, str(format(sell_price, '.2f')))
                        new_data = inputs
                        self.inventory.edit(inventory, ','.join(new_data), row)
                        yield {'success': 8}
                        break
                    else:
                        break
                else:
                    yield {'error': 19}
                    continue
        else:
            yield {'error': 39}

    def add_category(self):
        categories = self.categories.read()
        inputs = []
        exit = False
        yield {'note': 6}
        for key, value in self.cat_operations.items():
            while True:
                user_input = input(self.cat_input_messages[key])
                if user_input.lower() == 'exit':
                    exit = True
                    break
                elif not user_input:
                    yield {'error': 38}
                    continue
                func_call = getattr(self, value[0])(user_input, eval(*value[1]))
                if isinstance(func_call, bool) and func_call is True:
                    inputs.append(user_input)
                    break
                else:
                    yield func_call
            if exit:
                break
        if not exit:
            self.categories.append(inputs)
            yield {'success': 5}

    def remove_category(self):
        categories = self.categories.read()
        if len(categories) > 1:
            yield {'note': 2}
            while True:
                user_input = input('Enter category ID or name: ')
                if not user_input:
                    break
                row = self.search(categories, user_input)
                if row:
                    self.categories.edit(categories, '', row)
                    yield {'success': 6}
                    break
                else:
                    yield {'error': 18}
        else:
            yield {'error': 40}

    def edit_category(self):
        categories = self.categories.read()
        if len(categories) > 1:
            yield {'note': 6}
            exit = False
            while True:
                category = input("Enter category name or ID: ")
                if category.lower() == 'exit':
                    exit = True
                    break
                elif not category:
                    yield {'error': 38}
                    continue
                row = self.search(categories, category)
                if row:
                    old_data = categories[row].rsplit(',')
                    new_data = old_data.copy()
                    yield {'note': 1}
                    while True:
                        name = input("Enter name: ")
                        if name.lower() == 'exit':
                            exit = True
                            break
                        if name != '':
                            func_call = self.check_name(name, categories)
                            if isinstance(func_call, bool):
                                new_data[1] = name
                                break
                            else:
                                yield func_call
                        else:
                            new_data[1] = old_data[1]
                            break
                    if exit:
                        break
                    while True:
                        tax = input("Enter tax ratio: ")
                        if tax.lower() == 'exit':
                            exit = True
                            break
                        if tax != '':
                            func_call = self.check_num(tax)
                            if isinstance(func_call, bool):
                                new_data[2] = tax
                                break
                            else:
                                yield func_call
                        else:
                            new_data[2] = old_data[2]
                            break
                    break
                else:
                    yield {'error': 18}
            if not exit:
                self.categories.edit(categories, ','.join(new_data), row)
                self.change_group_item_price(old_data[0])
                yield {'success': 7}
        else:
            yield {'error': 40}

    def calculate_tax(self, category, price):
        categories = self.categories.read()
        for i in range(1, len(categories)):
            if category.lower() in list(map(lambda x: x.lower(), categories[i].rsplit(',')[:2])):
                return float(price * float(categories[i].rsplit(',')[2]) / 100.)

    def change_group_item_price(self, category):
        inventory = self.inventory.read()
        for i in range(len(inventory)):
            row = inventory[i].rsplit(',')
            if row[2] == category:
                row[6] = str(
                    format(float(row[4]) * (1. + float(row[5]) / 100.) + self.calculate_tax(category, float(row[4])),
                           '.2f'))
                self.inventory.edit(inventory, ','.join(row), i)

    def listing(self, categories=False):
        cat_list = self.categories.read()
        cat_list_splitted = list(map(lambda x: x.rsplit(','), cat_list))
        if categories:
            data = cat_list.copy()
        else:
            data = self.inventory.read()
        header = data[0].rsplit(',')
        content = [[a for a in b.rsplit(',')] for b in data[1:]]
        if not categories:
            for i in range(len(content)):
                content[i][2] = cat_list_splitted[self.search(cat_list, content[i][2])][1]
                if int(content[i][3]) == 0:
                    content[i][0] = COLORS.RED + content[i][0]
                    content[i][-1] = content[i][-1] + COLORS.RESET
                elif int(content[i][3]) <= 20:
                    content[i][0] = COLORS.YELLOW + content[i][0]
                    content[i][-1] = content[i][-1] + COLORS.RESET

        return [content, header]

    @staticmethod
    def check_id(_id, _list):
        if not _id.isnumeric():
            return {'error': 42}
        for i in range(1, len(_list)):
            if _id == _list[i].rsplit(',')[0]:
                return {'error': 14}
        return True

    @staticmethod
    def check_num(num, *_type):
        try:
            if 'int' in _type:
                int(num)
            else:
                float(num)
            if not float(num) > 0:
                return {'error': 15}
            return True
        except ValueError:
            return {'error': 15}

    def check_name(self, name, _list, *_):
        if not name.replace(' ', '').isalnum() or name.replace(' ', '').isnumeric():
            return {'error': 16}
        if _list and self.search(_list, name):
            return {'error': 17}
        return True

    def check_category(self, category, categories):
        if not self.search(categories, category):
            return {'error': 18}
        return True

    @staticmethod
    def search(_list, searchfor):
        for i in range(1, len(_list)):
            if searchfor.lower() in list(map(lambda x: x.lower(), _list[i].rsplit(',')[:2])):
                return i
        return False


class Cashier(Inventory):
    def __init__(self, user):
        Inventory.__init__(self)
        self.username = user.loggedUser
        self.items = []
        self.transactions = File('transactions', '.txt')
        self.total = 0

    def add_to_cart(self):
        inventory = self.inventory.read()
        content = self.listing(inventory)
        if len(content) != 0:
            print(Table(content, ['ID', 'Name', 'Price', 'Vendor']))
            yield {'note': 2}
            while True:
                added = False
                exit = False
                item_id = input('Enter item\'s ID or Name: ')
                if not item_id:
                    break
                row = self.search(content, item_id)
                if not isinstance(row, bool):
                    if not item_id.isnumeric():
                        item_id = inventory[super().search(inventory, item_id)].rsplit(',')[0]
                    while True:
                        quantity = input('How much do you want: ')
                        if not quantity:
                            exit = True
                            break
                        func_call = self.check_num(quantity)
                        if isinstance(func_call, bool) and func_call is True:
                            if self.check_quantity(item_id, int(quantity)):
                                for i in range(len(self.items)):
                                    if self.items[i][0] == item_id:
                                        self.items[i][1] = str(int(self.items[i][1]) + int(quantity))
                                        added = True
                                        break
                                if not added:
                                    self.items.append([item_id, quantity, content[row][2]])
                                self.total += float(content[row][2]) * float(quantity)
                                yield {'success': 9}
                                break
                            else:
                                yield {'error': 21}
                        else:
                            yield func_call
                    if exit:
                        break
                else:
                    yield {'error': 19}
        else:
            yield {'error': 39}

    def remove_from_cart(self):
        if len(self.items) != 0:
            inventory = self.inventory.read()
            while True:
                removed = False
                exit = False
                table = []
                for item in self.items:
                    row = super().search(inventory, item[0])
                    splitted_row = inventory[row].rsplit(',')
                    table.append([item[0], splitted_row[1], item[2], item[1]])
                if not len(table) > 0:
                    yield {'error': 23}
                    break
                print(Table(table, ['ID', 'Name', 'Price', 'Quantity']))
                yield {'note': 4}
                while True:
                    item_id = input('Enter item\'s ID or Name: ')
                    if not item_id:
                        exit = True
                        break
                    row = self.search(table, item_id)
                    if not isinstance(row, bool):
                        yield {'note': 3}
                        while True:
                            quantity = input('Enter quantity: ')
                            if not quantity:
                                self.total -= float(table[row][2]) * float(self.items[row][1])
                                self.items.pop(row)
                                yield {'success': 10}
                                removed = True
                                break
                            else:
                                func_call = self.check_num(quantity)
                                if isinstance(func_call, bool) and func_call is True:
                                    if int(self.items[row][1]) - int(quantity) > 0:
                                        self.items[row][1] = str(int(self.items[row][1]) - int(quantity))
                                        self.total -= float(table[row][2]) * float(quantity)
                                        yield {'success': 11}
                                        removed = True
                                        break
                                    elif int(self.items[row][1]) - int(quantity) == 0:
                                        self.total -= float(table[row][2]) * float(self.items[row][1])
                                        self.items.pop(row)
                                        yield {'success': 10}
                                        removed = True
                                        break
                                    else:
                                        yield {'error': 22}
                                else:
                                    yield func_call
                    else:
                        yield {'error': 19}
                    if removed:
                        break
                if exit:
                    break

        else:
            yield {'error': 23}

    def review_cart(self):
        table = []
        inventory = self.inventory.read()
        for item in self.items:
            row = super().search(inventory, item[0])
            splitted_row = inventory[row].rsplit(',')
            price = float(splitted_row[6]) * float(item[1])
            table.append([item[0], splitted_row[1], splitted_row[6], item[1], str(price)])
        return [table, str(self.total)]

    def checkout(self):
        if self.total > 0:
            print(Table([[str(self.total)]], ['To be paid']))
            exit = False
            yield {'note': 6}
            yield {'note': 5}
            while True:
                amount = input('How much you will pay: ')
                if not amount:
                    amount = str(self.total)
                elif amount.lower() == 'exit':
                    exit = True
                    break
                try:
                    float(amount)
                    if float(amount) < self.total:
                        yield {'error': 24}
                    break
                except ValueError:
                    yield {'error': 15}
            if not exit:
                inventory = self.inventory.read()
                timestamp = int(datetime.timestamp(datetime.now()))
                company = "\t\t\t\tOmar Store\n"
                address = "\t\t\t\tKonya, Turkey\n"
                phone = "\t\t\t\t555055500\n"
                sample = "\t\t\t\t\tInvoice\n"
                dt = "\t\t\t\t\t" + str(datetime.fromtimestamp(timestamp))
                table_header = "\n\n\t\t\t---------------------------------------\n\t\t\tSN.\tProducts\t\tQty\t\tAmount\n\t\t\t---------------------------------------"
                content = ''
                _items = ''
                r = 0
                for item in self.items:
                    _items += item[0] + ':' + str(item[1]) + '|'
                    row = super().search(inventory, item[0])
                    new_row = inventory[row].rsplit(',')
                    name = new_row[1]
                    new_row[3] = str(int(new_row[3]) - int(item[1]))
                    new_row = ','.join(new_row)
                    self.inventory.edit(inventory, new_row, row)
                    r += 1
                    content += "\n\t\t\t" + str(r) + "\t" + str(name + ".......")[:8] + "\t\t" + str(
                        item[1]) + "\t\t" + str(float(item[2]) * float(item[1]))
                final = company + address + phone + sample + dt + "\n" + table_header + content + '\n\n\t\t\tTotal: ' + str(
                    self.total) + ' TL' + '\n\t\t\tPaid: ' + amount + '\t\t\t\tChange: ' + str(
                    format(float(amount) - float(self.total), '.2f')) + '\n\t\t\tCashier: ' + self.username
                file_name = 'invoices/' + str(timestamp)
                invoice = File(file_name, '.rtf')
                invoice.write(final)
                transactions = self.transactions.read()
                if len(transactions) == 1:
                    _id = 1
                else:
                    _id = int(transactions[-1].rsplit(',')[0]) + 1
                self.transactions.append(
                    [str(_id), 'Sell', self.username, str(self.total), str(datetime.fromtimestamp(timestamp)),
                     file_name + '.rtf', str(_items), '0'])
                self.items = []
                self.total = 0
                yield {'success': 12}
        else:
            yield {'error': 23}

    def refund(self):
        transactions = self.transactions.read()
        inventory = self.inventory.read()
        table = []
        expired_transactions = []
        for transaction in transactions[1:]:
            splitted_row = transaction.rsplit(',')
            if splitted_row[1].lower() == 'sell' and splitted_row[-1] == '0':
                time_now = int(datetime.timestamp(datetime.now()))
                transaction_date = int(datetime.timestamp(datetime.strptime(splitted_row[4], '%Y-%m-%d %H:%M:%S')))
                days_count = (time_now - transaction_date) / (60 * 60 * 24)
                if days_count <= 3:
                    table.append(splitted_row)
                else:
                    expired_transactions.append(splitted_row)
        if len(table) > 0:
            print(Table([x[:-2] for x in table], ['ID', 'Type', 'Cashier', 'Amount', 'Date', 'Invoice']))
            yield {'note': 2}
            while True:
                id = input('Enter transaction ID: ')
                if not id:
                    break
                try:
                    int(id)
                except ValueError:
                    yield {'error': 15}
                    continue
                row = self.search(table, id)
                if not isinstance(row, bool):
                    table[row][1] = 'Refund'
                    table[row][4] = str(datetime.fromtimestamp(int(datetime.timestamp(datetime.now()))))
                    table[row][2] = self.username
                    row_3 = super().search(transactions, id)
                    splitted_row_3 = transactions[row_3].rsplit(',')
                    splitted_row_3[-1] = '1'
                    self.transactions.edit(transactions, ','.join(splitted_row_3), row_3)
                    self.transactions.append(table[row])
                    for item in table[row][-2].rsplit('|')[:-1]:
                        item = item.rsplit(':')
                        row_2 = super().search(inventory, item[0])
                        if row_2:
                            new_row = inventory[row_2].rsplit(',')
                            new_row[3] = str(int(new_row[3]) + int(item[1]))
                            new_row = ','.join(new_row)
                            self.inventory.edit(inventory, new_row, row_2)
                    yield {'success': 13}
                    break
                elif self.search(expired_transactions, id):
                    yield {'error': 25}
                else:
                    yield {'error': 26}
        else:
            yield {'error': 27}

    def list_transactions(self):
        transactions = self.transactions.read()
        content = []
        headers = transactions[0].rsplit(',')
        headers.pop(-1)
        if len(transactions) > 1:
            for transaction in transactions[1:]:
                splitted_row = transaction.rsplit(',')[:-2]
                if splitted_row[1].lower() == 'refund':
                    splitted_row[0] = COLORS.RED + splitted_row[0]
                else:
                    splitted_row[0] = COLORS.GREEN + splitted_row[0]
                splitted_row[-1] += COLORS.RESET
                content.append(splitted_row)
        return [content, headers]

    def listing(self, inventory):
        content = []
        for row in inventory[1:]:
            splitted_row = row.rsplit(',')
            if not int(splitted_row[3]) > 0:
                continue
            else:
                temp = [splitted_row[0], splitted_row[1], splitted_row[6], splitted_row[7]]
                content.append(temp)
        return content

    @staticmethod
    def search(_list, searchfor):
        for i in range(len(_list)):
            if searchfor.lower() in list(map(lambda x: x.lower(), _list[i][:2])):
                return i
        return False

    @staticmethod
    def check_num(num):
        try:
            int(num)
            if not int(num) > 0:
                return {'error': 20}
        except ValueError:
            return {'error': 15}
        return True

    def check_quantity(self, item, requested_quantity):
        inventory = self.inventory.read()
        row = inventory[super().search(inventory, item)].rsplit(',')
        quantity = row[3]
        quantity_in_cart = 0
        for i in range(len(self.items)):
            if self.items[i][0] == item:
                quantity_in_cart = int(self.items[i][1])
                break
        return int(quantity) - requested_quantity - quantity_in_cart >= 0


def main():
    def initialize():
        files = ['users.txt', 'inventory.txt', 'categories.txt', 'transactions.txt']
        default_values = ['Username,Password,Name,E-mail,Birth Date,ID No,Status,Role',
                          'ID,Name,Category,Quantity,Cost Price,Profit Ratio,Sell Price,Vendor', 'ID,Name,Tax',
                          'ID,Type,Cashier,Amount,Date,Invoice,Items']
        error = False
        for i in range(4):
            if os.path.exists(files[i]):
                try:
                    my_file = open(files[i], 'r')
                    if len(my_file.readlines()) == 0:
                        my_file = open(files[i], 'a+')
                        my_file.write(default_values[i])
                        my_file.close()
                except:
                    try:
                        my_file = open(files[i], 'a+')
                        if len(my_file.readlines()) == 0:
                            my_file.write(default_values[i])
                            my_file.close()
                    except:
                        error = True
            else:
                try:
                    my_file = open(files[i], 'a+')
                    if len(my_file.readlines()) == 0:
                        my_file.write(default_values[i])
                        my_file.close()
                except:
                    error = True
        if error:
            print(COLORS.RED + '[✘] ' + 'Couldn\'t open the required files' + COLORS.RESET)
            exit(0)



    def header(menu):
        vertical_char = "│"
        horizontal_char = "─"
        Top_left = "┌"
        Top_right = "┐"
        Bottom_left = "└"
        Bottom_right = "┘"

        def margin(character_sign, total_times):
            margin_character = ""
            for i in range(total_times):
                margin_character = margin_character + character_sign
            return margin_character

        def draw_menu(menus):
            main_menu = menus
            maximum_text_length = len(main_menu) + 20

            maximum_text_size = maximum_text_length
            y = maximum_text_length

            top_margin_left_to_right = Top_left + margin(horizontal_char, y) + Top_right
            print(" " * 20 + top_margin_left_to_right)

            free_space = maximum_text_size - len(main_menu) - 10
            right_vertical_wall = margin(" ", free_space) + vertical_char
            print(" " * 20 + vertical_char + " " * 10 + main_menu + right_vertical_wall)

            lower_margin_left_to_right = Bottom_left + margin(horizontal_char, y) + Bottom_right
            print(" " * 20 + lower_margin_left_to_right)

        draw_menu(menu)

    def print_error(no):
        return COLORS.RED + '[✘] ' + Error_Codes[no] + COLORS.RESET

    def print_success(no):
        return COLORS.GREEN + '[✔] ' + Success_Codes[no] + COLORS.RESET

    def print_note(no):
        return COLORS.YELLOW + '[!] ' + Note_Codes[no] + COLORS.RESET

    def wait():
        input(print_note(0))

    cls = lambda: print('\n' * 25)

    def call_method(method, *args):
        for result in method():
            if not isinstance(result, list):
                if 'note' in result:
                    print(print_note(result['note']))
                elif 'success' in result:
                    print(print_success(result['success']))
                    for arg in args:
                        arg()
                else:
                    print(print_error(result['error']))
            else:
                for _result in result:
                    if 'note' in _result:
                        print(print_note(_result['note']))
                    elif 'success' in _result:
                        print(print_success(_result['success']))
                        for arg in args:
                            arg()
                    else:
                        print(print_error(_result['error']))

    def login():
        user = StaffManagement()
        tab = '\t'
        error = None
        success = None
        while True:
            cls()
            header('Login Page')
            print('\n' + tab + ' ' * 5 + '[!] Default username and password for admin is "admin"')
            print(tab + ' ' * 5 + '[!] Default username and password for staff is "staff"\n')
            if error:
                print(tab + ' ' * 5 + print_error(error))
            elif success:
                print(tab + ' ' * 5 + print_success(success))
                wait()
                return user
            error = None
            for _return in user.login():
                if 'error' in _return:
                    error = _return['error']
                else:
                    success = _return['success']
                break

    def main_menu():
        cls()
        if user.isAdmin:
            while True:
                header('Admin Dashboard')
                choice = input('\nPlease enter your choice:\n'
                               '[1] Point of sales\n'
                               '[2] Inventory\n'
                               '[3] Staff Management\n'
                               '[4] Edit Personal Information\n'
                               '[0] Exit\n'
                               '\n'
                               '>>>> ')
                if choice == '1':
                    _pos()
                elif choice == '2':
                    inv()
                elif choice == '3':
                    staff()
                elif choice == '4':
                    edit_personal_info()
                elif choice == '0':
                    exit(0)
        else:
            while True:
                header('Staff Dashboard')
                choice = input('\nPlease enter your choice:\n'
                               '[1] Point of sales\n'
                               '[2] Edit personal information\n'
                               '[0] Exit\n'
                               '\n'
                               '>>>> ')
                if choice == '1':
                    _pos()
                elif choice == '2':
                    edit_personal_info()
                elif choice == '0':
                    exit(0)

    def _pos():
        def new_order():
            nonlocal user
            pos = Cashier(user)
            cls()
            while True:
                choice = input('\nPlease enter your choice:\n'
                               '[1] Add to cart\n'
                               '[2] Remove from cart\n'
                               '[3] Review cart\n'
                               '[4] Checkout\n'
                               '[0] Back\n'
                               '\n'
                               '>>>> ')
                if choice == '1':
                    call_method(pos.add_to_cart)
                elif choice == '2':
                    call_method(pos.remove_from_cart)
                elif choice == '3':
                    cart = pos.review_cart()
                    if float(cart[1]) != 0:
                        print(Table(cart[0], ['ID', 'Name', 'Price', 'Quantity', 'Total Price']))
                        print(Table([[cart[1]]], ['Cart total price']))
                        wait()
                    else:
                        print(print_error(23))

                elif choice == '4':
                    call_method(pos.checkout, wait)
                    break
                elif choice == '0':
                    break

        def refund():
            nonlocal user
            pos = Cashier(user)
            cls()
            call_method(pos.refund, wait)

        def list_trans():
            nonlocal user
            pos = Cashier(user)
            cls()
            contents = pos.list_transactions()
            if len(contents[0]) != 0:
                print(Table(*contents))
            else:
                print(print_error(44))
            wait()

        cls()

        while True:
            choice = input('\nPlease enter your choice:\n'
                           '[1] New order\n'
                           '[2] Refund\n'
                           '[3] List transactions\n'
                           '[0] Back\n'
                           '\n'
                           '>>>> ')
            cls()
            if choice == '1':
                new_order()
            elif choice == '2':
                refund()
            elif choice == '3':
                list_trans()
            elif choice == '0':
                break

    def edit_personal_info():
        nonlocal user
        cls()
        while True:
            choice = input('\nPlease enter your choice:\n'
                           '[1] Edit personal information\n'
                           '[2] Change password\n'
                           '[0] Back'
                           '\n'
                           '>>>> ')
            if choice == '1':
                call_method(user.edit, wait)
            elif choice == '2':
                call_method(user.change_password, wait)
            elif choice == '0':
                break

    def staff():
        cls()
        nonlocal user
        while True:
            choice = input('\nPlease enter your choice:\n'
                           '[1] Add staff\n'
                           '[2] Remove staff\n'
                           '[3] Edit staff information\n'
                           '[4] Suspend staff\n'
                           '[5] Activate stuff\n'
                           '[6] Assign admin role\n'
                           '[7] Remove admin role\n'
                           '[8] List staff\n'
                           '[0] Back\n'
                           '\n'
                           '>>>> ')
            if choice == '1':
                call_method(user.add_staff, wait)
            elif choice == '2':
                call_method(user.remove_staff, wait)
            elif choice == '3':
                call_method(user.edit_staff, wait)
            elif choice == '4':
                call_method(user.suspend_staff, wait)
            elif choice == '5':
                call_method(user.activate_staff, wait)
            elif choice == '6':
                call_method(user.add_admin, wait)
            elif choice == '7':
                call_method(user.remove_admin, wait)
            elif choice == '8':
                content = user.listing()
                if len(content[0]) != 0:
                    print(Table(*content))
                else:
                    print(print_error(41))
                wait()
            elif choice == '0':
                break

    def inv():
        inventory = Inventory()
        def change_quan():
            cls()
            while True:
                choice = input('\nPlease enter your choice:\n'
                               '[1] Increase quantity\n'
                               '[2] Decrease quantity\n'
                               '[0] Back'
                               '\n'
                               '>>>> ')
                if choice == '1':
                    call_method(inventory.increase_quantity, wait)
                elif choice == '2':
                    call_method(inventory.decrease_quantity, wait)
                elif choice == '0':
                    break

        cls()
        while True:
            choice = input('\nPlease enter your choice:\n'
                           '[1] List items\n'
                           '[2] Add item\n'
                           '[3] Edit item\n'
                           '[4] Remove item\n'
                           '[5] List categories\n'
                           '[6] Add category\n'
                           '[7] Edit category\n'
                           '[8] Remove category\n'
                           '[9] Change item\'s quantity\n'
                           '[0] Back\n'
                           '\n'
                           '>>>> ')
            cls()
            if choice == '1':
                content = inventory.listing(False)
                if len(content[0]) != 0:
                    print(Table(*content))
                else:
                    print(print_error(39))
                wait()
            elif choice == '2':
                call_method(inventory.add_item, wait)
            elif choice == '3':
                call_method(inventory.edit_item, wait)
            elif choice == '4':
                call_method(inventory.remove_item, wait)
            elif choice == '5':
                content = inventory.listing(True)
                if len(content[0]) != 0:
                    print(Table(*content))
                else:
                    print(print_error(40))
                wait()
            elif choice == '6':
                call_method(inventory.add_category, wait)
            elif choice == '7':
                call_method(inventory.edit_category, wait)
            elif choice == '8':
                call_method(inventory.remove_category, wait)
            elif choice == '9':
                change_quan()
            elif choice == '0':
                break
    initialize()
    user = login()
    main_menu()


main()
