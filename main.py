'''Simple calculator with database'''
import json
import datetime
import pytz
import sys
import time

timezone = pytz.timezone('EET')
'''I don't have first user creation in Database, as my base user is Admin,Admin'''


# Creating general User class
class User:
    '''User object.
    kwargs/args
    login - user login
    password - user password
    user_group - regs or public.
                    regs - registered users with additional rights
                    public - unregistered user limited to *,/,+,- operators
    methods - __init__
              __str__
              check_info - prints __str__'''

    def __init__(self, login: str, password: str, user_group: str, log=None):
        if log is None:
            log = []  # default value as empty list (Intellij didnt like mutable value in the header
        self.login = login
        self.password = password
        self.log = log
        self.user_group = user_group

    def __str__(self):  # string representation of User class
        return f'{"Registered" if self.user_group == "regs" else "Unregistered"} user. Login {self.login} has {len(Database(self).find_user()["log"])} calculations'

    def check_info(self):  # printing ___str___of self
        print(self)


class Calculator:  # main calculation class. Has 2 levels of access "regs" and "public"
    '''Calculator class -
        kwargs/args
        user - User object
        nom1 - first number
        nom2 - second number
        operator - operator - *,/,+,-,sin,cos,tan,cotan
    methods -
            __init__
            __str__ - verbose string representing the operation
            __repr__-short basic operation representation  e.g nom1,operator,nom2=result
            engine - calculation returning actual result'''

    def __init__(self, user: User, nom1, operator, nom2=1):
        self.user = user
        self.nom1 = nom1
        self.nom2 = nom2
        self.operator = operator

    def __str__(self):
        return f'Operation for {self.user.login}\n{self.nom1} {self.operator}' \
               f' {self.nom2 if self.nom2 != 1 else ""} is equal {self.engine()}' if self.engine() else 'Access denied'

    def __repr__(self):
        return f'{self.nom1}{self.operator}{self.nom2}={self.engine()}'

    def engine(self):
        import math
        try:
            calculations = {'+': self.nom1 + self.nom2, '-': self.nom1 - self.nom2, '*': self.nom1 * self.nom2,
                            '/': self.nom1 / self.nom2}
            reg_calc = {'sin': math.sin(self.nom1), 'cos': math.cos(self.nom1), 'tan': math.tan(self.nom1),
                        'cotan': 1 / math.tan(self.nom1)}
            if self.user.user_group == 'regs':  # REGISTERED users operator-key withdrawal
                return calculations.get(self.operator) or reg_calc.get(self.operator)
            else:
                try:  # nonregistered users operator-key withdrawal
                    return calculations[self.operator]
                except KeyError:
                    print(f'{self.user.login} has no access to this operation!')
                    return None
        except Exception as e:
            return f'{e} cause you are too dumb not do that!'


class Database:  # database manipulation - basically I/O JSON data
    ''' Database object
    performs all database operations I/O, is_check etc.
    kwargs/args
    user = User object,active_user
    methods -
            __init__
            read_db - returns fully read Database file
            write_db(data) - writes data into Database file
            find_user - searches for active user e.g Database(active_user).find_user
            is_user - bool check if active user is present in the Database
            add_user - writes new user into Database e.g Database(active_user).find_user
            add_calc - writes datetime,Calculator().engine()result and string representation
            show_stat - kwarg type='simple'(detailed) 2 different options of string return of formatted 'log' info from
            Database'''

    def __init__(self, user: User):
        self.user = user

    def read_db(self):  # reading JSON file - dict-list-dict
        with open('calc_db.json', 'r+') as db:
            return json.load(db)

    def write_db(self, write):  # dumping all everything that is in the "write" argument into JSON file
        with open('calc_db.json', 'w+') as db:
            return json.dump(write, db)

    def find_user(self):  # searches for specific user and give access to his section of json for ***reading***
        for user in self.read_db()['user']:
            if user['login'] == self.user.login:
                return user

    def is_user(self):  # boolean is user check
        for users in self.read_db()['user']:
            if users['login'] == self.user.login:
                return True
        return False

    def add_user(self):  # adding user to the data base with basic CHECK IF EXISTS - using 'write' mode -
        # withdrawing all the data modifying it and dropping back in to avoid doubling.
        if not self.is_user():
            file = self.read_db()
            file['user'].append({'login': self.user.login, 'password': self.user.password,
                                 'user_group': self.user.user_group, 'log': self.user.log})
            self.write_db(file)

    def add_calc(self, calc):  # reads db, withdraws whole log and adds to it
        # (using 'write' mode to avoid doubling data with 'append'
        file = self.read_db()
        for user in file['user']:
            if user['login'] == self.user.login:
                user['log'].append(
                    (f"{timezone.localize(datetime.datetime.now())}", calc.engine(), calc.__repr__()))
                self.write_db(file)

    def show_stat(self, type='simple'):  # showing stat of calculations with time for given user
        if self.is_user():
            if type == 'detailed':
                return "\n\n\n{} stat:\n{}\n#  Date:\t\t\t\t\t\t\t\t" \
                       "Result:\t\t\tDetails:\n\n{}".format(self.user,
                                                            '=' * 40,
                                                            # returning raw pytz data log
                                                            '\n'.join(
                                                                [
                                                                    f"{i + 1}. {d}:\t\t{b}\t\t{c}"
                                                                    for i, (
                                                                    d, b, c) in
                                                                    enumerate(
                                                                        self.find_user()[
                                                                            'log'])]))
            elif type == 'simple':
                return "\n\n\n{} stat:\n{}\n#  Date:\t\t\t\t\t\tResult:\n{}".format(self.user, '=' * 40, '\n'.join(
                    [f"{a + 1}. {datetime.datetime.strptime(i, '%Y-%m-%d %H:%M:%S.%f%z').strftime('%c')}:\t\t{b}\t\t"
                     for
                     a, (i, b, c) in enumerate(self.find_user()['log'])]))
                # returning formatted pytz data example Sat Jan 25 10:26:15 2020
        print('\n\n\n\n')


def slow_animation():  # funny animation imitatting loading...
    for i in range(5, -1, -1):
        print((i * '.'), end='', flush=True)
        time.sleep(0.5)
        sys.stdout.flush()
        print('\r', end='', flush=True)


def login_input():  # shortcut to get input
    print('=' * 40, '\n')
    login = quit_filter(input('Login: '))
    password = quit_filter(input("Password: "))
    print('=' * 40)
    return login, password


def quit_filter(input):  # filter of the input to always
    if 'quit' in input.casefold():
        sys.exit('Respecting your desire to quit')
    else:
        return input.strip()


def login_menu_choice():  # login menu sequence
    global new_user
    login_count = 3
    active_user = None
    print('Hello My dear noisy friend\n1 to create account\n2 to login \nany other number ='
          ' you are doomed to be anonymous\t\t\t\t\t\tat any time type "quit" to leave us :(')
    while True:
        try:
            menu = float(quit_filter(input('>>> ')))
            break
        except Exception as e:
            print(f'{e} Please re-enter')

    while True:
        if active_user:
            print('Logged in as', 'registered' if active_user.user_group == 'regs' else 'unregistered', 'user')
            break
        if active_user == None and login_count < 3:
            print(f'{login_count} attempts to log in left...\n\n\n{"*" * 40}')

        if menu == 1:
            print('Create new user')
            while True:
                login, password = login_input()
                print(40 * '*')
                password2 = input('Repeat your password, plz...')
                if password == password2:
                    new_user = User(login, password, 'regs')
                if not Database(new_user).is_user():
                    Database(new_user).add_user()
                    break
                else:
                    print(f'\n\n{new_user.login} exists in my data base, please choose another name')
            print('Now please log in...\n\n\n')
            time.sleep(2)
            menu = 2
        elif menu == 2:

            login, password = login_input()
            if login_count <= 0:
                print('Wrong password or login information')
                slow_animation()
                active_user = User(login='Ananymous', password='', user_group='public')

            for user in Database.read_db('yo')['user']:
                if user['login'] == login and user['password'] == password:
                    print(f'logging in as {user["login"]}')
                    active_user = User(user['login'], user['password'], user['user_group'], user['log'])
                    slow_animation()
                    break
            else:
                login_count -= 1
        elif menu != 1 and menu != 2:
            print('Welcome my dear Anonymous')
            active_user = User(login='Ananymous', password='', user_group='public')
    return active_user


def operational_menu(active_user):  # program sequence after active_user has been assigned
    while True:
        print('\n\n\n\nMenu:\n1.User Stat\n2.Calculations log\n3.Calculate\n\t\t\t\t\t\tType quit any time to quit')
        oper = choice()
        if oper == 1:
            if active_user.user_group == 'regs':
                print(active_user)
            else:
                print('Anons have no stats, you pleb')
        elif oper == 2:
            if active_user.user_group == 'regs':
                while True:
                    try:
                        d = float(quit_filter(input('\t\t\t1.Simple stat format\n\t\t\t2.Detailed format'
                                                    '\n\t\t\t3.Previous menu')))
                        if d == 1:
                            print(Database(active_user).show_stat())
                        elif d == 2:
                            print(Database(active_user).show_stat('detailed'))
                        elif d == 3:

                            break
                        else:
                            raise ValueError
                    except Exception as e:
                        print(f"{e}, we don't have that format yet")
            else:
                print('Anons have no log, you rediska')
        elif oper == 3:
            operators = ['*', '+', '-', '/', 'sin', 'cos', 'tan', 'cotan']
            print('Calculations = *,+,-,/,sin,cos,tan,cotan')
            while True:
                while True:
                    try:
                        nom1 = float(quit_filter(input('Nom1>>>')))
                        break
                    except Exception as e:
                        print(f'{e} I need nomber dude')
                pip = True
                while pip:
                    print('Please enter correct operator')
                    op = quit_filter(input('operator'))
                    for ops in operators:
                        if str(op) == str(ops):
                            pip = False
                while True:
                    try:
                        if op in 'sincosancotan':
                            nom2 = 1
                            break
                        else:
                            nom2 = float(quit_filter(input('Nom2>>>')))
                            break
                    except Exception as e:
                        print(f'{e}, please enter smthing, dude')
                print('*' * 40)
                resolt = Calculator(active_user, nom1, op, nom2)
                print(resolt)
                if active_user.user_group == 'regs':
                    Database(active_user).add_calc(resolt)
                slow_animation()
                break


def choice():
    while True:
        try:
            choice = int(quit_filter(input('>>>> ')))
            return choice
        except Exception as e:
            print(f'{e},please input correct menu choice or "qui"')


def init_db():
    import os
    file = os.path.join('calc_db.json')
    try:
        if open(file):
            if json.load(open(file))['user'][0]['login'] == 'admin':
                return
            raise FileNotFoundError
    except:
        with open(os.path.join('calc_db.json'), 'w') as foil:
            json.dump({"user": [{"login": "admin", "password": "admin", "user_group": "regs", "log": []}]}, foil)


def main():
    init_db()
    active_user = login_menu_choice()
    operational_menu(active_user)


if __name__ == '__main__':
    main()
