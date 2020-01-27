# 1) Создать воможность регистрации , авторизации.
# 2) Хранить данные о пользователе в формате json.
# 3) Для неавторизованого юзера  - калькулятор имеет 4 функции: + - * /.
# 4) Для авторизированого  еще + синус косинус тангес котангенс.
# 5) Авторизированый юзер имеет возможность просмотреть исторю своих операций за последний день(или всю историю).
# 6) Историю всех операций предлагаю хранить в формате json. Поля для операции - id(уникальное число) , date -
# дата операции , operation - сама операция
# Пример: \
# [{
#
#     id : 1,
#     date: '20-10-1953',
#     operation: '2+2=4'
# }]
import json
import pprint
import datetime
import pytz
import sys
import time

timezone = pytz.timezone('EET')


# Creating general User class
class User(object):

    def __init__(self, login, password, user_group, log=None):
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

    def check_pass(self):
        pass


# class Login(object):
#     def __init__(self, user, password):
#         self.user = user
#         self.password = password
#
#     def check_user(self):
#         return Database(self.user).is_user()
#
#     def add_user(self):
#         Database(self.user).add_user()
#


class Calculator(object):  # main calculation class. Has 2 levels of access "regs" and "public"

    def __init__(self, user, nom1, operator, nom2=1):
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

    def next_calc(self):  # TODO add next calculation if user wants to calculate smthing else with the result of calc

        pass


class Database(object):  # database manipulation - basically I/O JSON data
    def __init__(self, user):
        self.user = user
        pass

    def read_db(self):  # reading JSON file - dict-list-dict
        with open('calc_db.json', 'r') as db:
            return json.load(db)

    def write_db(self, write):  # dumping all everything that is in the "write" argument into JSON file
        with open('calc_db.json', 'w') as db:
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
                return "\n\n\n{} stat:\n{}\n{}".format(self.user, '=' * 40,  # returning raw pytz data log
                                                 '\n'.join(
                                                     [f"{i}:\t\t{b}\t\t{c}" for i, b, c in self.find_user()['log']]))
            elif type == 'simple':
                return "\n\n\n{} stat:\n{}\n{}".format(self.user, '=' * 40, '\n'.join(
                    [f"{datetime.datetime.strptime(i, '%Y-%m-%d %H:%M:%S.%f%z').strftime('%c')}:\t\t{b}\t\t" for
                     i, b, c in self.find_user()['log']]))
                # returning formatted pytz data example Sat Jan 25 10:26:15 2020
        print('\n\n\n\n')



def slow_animation():
    for i in range(5, -1, -1):
        print((i * '.'), end='', flush=True)
        time.sleep(0.5)
        sys.stdout.flush()
        print('\r', end='', flush=True)


def login_input():
    print('=' * 40, '\n')
    login = quit_filter(input('Login: '))
    password = quit_filter(input("Password: "))
    print('=' * 40)
    return login, password


def quit_filter(input):
    if 'quit' in input.casefold():
        sys.exit('Respecting your desire to quit')
    else:
        return input.strip()


def login_menu_choice():
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
            login, password = login_input()
            new_user = User(login, password, 'regs')
            Database(new_user).add_user()
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


def choice():
    while True:
        try:
            choice = int(quit_filter(input('>>>> ')))
            return choice
        except Exception as e:
            print(f'{e},please input correct menu choice or "qui"')


def main():
    # print('Welcome, to calc! Please log in  or create account')
    # pablito = User(login='pablito', password='qwerty', user_group='regs', log=[])
    # Database(pablito).add_user()
    # pablito2 = User(login='pablito2', password='qwerty', user_group='public', log=[])
    # pablito3 = User(login='pablito3', password='qwerty', user_group='public', log=[])
    # caloc = Calculator(pablito, -225, '/', 13)
    # print(Calculator(pablito,nom2=1, nom1=5, operator='cos'))
    # Database(pablito).add_user()
    # Database(pablito2).add_user()
    # Database(pablito3).add_user()
    # pablito.check_info()
    # pablito2.check_info()
    # polina=User('polina','polina','regs')
    # Database(pablito).add_calc(caloc)
    # print(Database(pablito).show_stat())
    # print(Database(polina).show_stat('detailed'))
    # Database(pablito).add_calc(78)
    # Database(pablito).add_calc(98)
    # pablito.check_info()
    # print(timezone.localize(datetime.datetime.now()))
    # b = Database.read_db('hi')['user'][1]['log'][0][0]
    # print(datetime.datetime.strptime(b,'%Y-%m-%d %H:%M:%S.%f%z').strftime('%c'))
    # print(Database(pablito).show_stat())
    active_user = login_menu_choice()
    # Operational Menu
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
                pip=True
                while pip:
                    print('Please enter correct operator')
                    op=quit_filter(input('operator'))
                    for ops in operators:
                        if str(op)==str(ops):
                            pip=False


                if op in 'sincotancotan':
                    nom2 = 1
                else:
                    nom2 = float(quit_filter(input('Nom2>>>')))
                print('*' * 40)
                resolt=Calculator(active_user, nom1, op, nom2)
                print(resolt)
                if active_user.user_group == 'regs':
                    Database(active_user).add_calc(resolt)
                slow_animation()
                break


if __name__ == '__main__':
    main()
