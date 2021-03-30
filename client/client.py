import socket
import threading
import sys
import pickle

class Client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, self.port))
        self.json_register = {}
        self.register_or_login()

    def register(self):
        self.json_register['login'] = input('Enter your login: ')
        self.json_register['password'] = input('Enter your password: ')

        res = pickle.dumps(self.json_register)

        self.socket.send(res)

        msg = self.socket.recv(1024).decode('utf-8')

        if msg == 'User with this login exists. Try another login.':
            print(msg)
            self.register()
        elif msg == 'You have been successfully registered!':
            print('WELCOME!')

    def login(self):
        print('login 2')

    def register_or_login(self):
        msg = self.socket.recv(1024).decode('utf-8')
        print(msg)

        answer = input('(1/2): ')
        self.socket.send(bytes(answer, 'utf-8'))
        if answer == '1':
            self.register()
        elif answer == '2':
            self.login()


c1 = Client('', 8000)
