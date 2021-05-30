import socket
import threading
import sys
import pickle
import pyfiglet

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
		result = pyfiglet.figlet_format("TermChat", font = "smslant")
		print(result)

		msg = self.socket.recv(1024).decode('utf-8')
		print('┝━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┥')
		print(msg)
		print('┝━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┥')

		answer = input('    |ᛞ| R |ᛞ| ᛟᚱ |ᛞ| L |ᛞ|: ')
		self.socket.send(bytes(answer, 'utf-8'))
		if answer == 'R':
			self.register()
		elif answer == 'L':
			self.login()

	def register(self):
		print('┝━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┥')
		print('	     |ᛟ| REGISTER |ᛟ|')
		print('┝━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┥')
		self.json_register['login'] = input('    |ᛟ| Enter your login |ᛟ|: ')
		self.json_register['password'] = input('    |ᛟ| Enter your password |ᛟ|: ')

		global name
		name = self.json_register['login']

		res = pickle.dumps(self.json_register)
		self.socket.send(res)

		msg = self.socket.recv(1024).decode('utf-8')

		if msg == ' User with this login is already exists.':
			print('┝━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┥')
			print(msg)
			print('┝━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┥')
			self.register()
		elif msg == ' You have been successfully registered.':
			print('┝━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┥')
			print(msg)
			print('┝━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┥')
			threading.Thread(target=self.msg_recv, daemon=True).start()
			self.msg_send()

	def login(self):
		print('┝━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┥')
		print('	     |ᛟ| LOGIN |ᛟ|')
		print('┝━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┥')
		self.json_login['login'] = input('    |ᛟ| Enter your login |ᛟ|: ')
		self.json_login['password'] = input('    |ᛟ| Enter your password |ᛟ|: ')

		global name
		name = self.json_login['login']

		res = pickle.dumps(self.json_login)
		self.socket.send(res)

		msg = self.socket.recv(1024).decode('utf-8')

		if msg == '  You have been successfully logged in!':
			print('┝━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┥')
			print(msg)
			print('┝━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┥')
			threading.Thread(target=self.msg_recv, daemon=True).start()
			self.msg_send()
		elif msg == ' Incorrect login of password. Try again.':
			print('┝━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┥')
			print(msg)
			print('┝━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┥')
			self.login()

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
				self.socket.send(bytes('|ᛟ| ' + name + ' |ᛟ|: ' + input(''), 'utf-8'))
			except:
				break


c1 = Client('', 8000)
