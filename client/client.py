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
		self.json_login = {}
		self.register_or_login()

	def register_or_login(self):
		msg = self.socket.recv(1024).decode('utf-8')
		print(msg)

		answer = input('(1/2): ')
		self.socket.send(bytes(answer, 'utf-8'))
		if answer == '1':
			self.register()
		elif answer == '2':
			self.login()

	def register(self):
		print('|||REGISTER|||')
		self.json_register['login'] = input('Enter your login: ')
		self.json_register['password'] = input('Enter your password: ')

		global name
		name = self.json_register['login']

		res = pickle.dumps(self.json_register)
		self.socket.send(res)

		msg = self.socket.recv(1024).decode('utf-8')

		if msg == 'User with this login exists. Try another login.':
			print(msg)
			self.register()
		elif msg == 'You have been successfully registered!':
			print(msg)
			threading.Thread(target=self.msg_recv, daemon=True).start()
			self.msg_send()

	def login(self):
		print('|||LOGIN|||')
		self.json_login['login'] = input('Enter your login: ')
		self.json_login['password'] = input('Enter your password: ')

		global name
		name = self.json_login['login']

		res = pickle.dumps(self.json_login)
		self.socket.send(res)

		msg = self.socket.recv(1024).decode('utf-8')

		if msg:
			print(msg)
			threading.Thread(target=self.msg_recv, daemon=True).start()
			self.msg_send()

	def msg_recv(self):
		while True:
			try:
				msg = self.socket.recv(1024).decode('utf-8')
				if not msg:
					break
				print(msg)
			except:
				break

	def msg_send(self):
		while True:
			try:
				self.socket.send(bytes(name + ': ' + input(''), 'utf-8'))
			except:
				break


c1 = Client('', 8000)
