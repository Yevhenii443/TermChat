import socket
import threading
import select
import json
import sys
import pickle
import sqlite3
from create_table import create_db
from json_insertion import insert_into_db

class Server:
	def __init__(self, ip, port):
		self.ip = ip
		self.port = port
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.bind((self.ip, self.port))
		self.socket.listen(0)
		create_db()
		if self.socket:
			print('[SERVER STARTED]')
		else:
			sys.exit()
		self.list1 = []
		self.list1.append(self.socket)
		self.event_loop()

	def register_or_login(self, client):
		client.send(bytes('    |ᛟ| REGISTER |ᛟ| ᛟᚱ |ᛟ| LOGIN |ᛟ|', 'utf-8'))
		msg = client.recv(1024).decode('utf-8')
		if msg == 'R':
			self.register(client)
		elif msg == 'L':
			self.login(client)

	def register(self, client):
		msg = client.recv(1024)
		res = pickle.loads(msg)

		register_validation = sqlite3.connect('TermChat.db')
		cursor = register_validation.cursor()
		cursor.execute('SELECT login FROM TermChat WHERE login = ?', (res['login'], ))

		if cursor.fetchall():
			client.send(bytes(' User with this login is already exists.', 'utf-8'))
			self.register(client)
		else:
			with open('register.json', 'w') as f:
				json.dump(res, f)

			client.send(bytes(' You have been successfully registered.', 'utf-8'))
			insert_into_db(res)
			threading.Thread(target=self.msg, args=(client, ), daemon=True).start()

	def login(self, client):
		msg = client.recv(1024)
		res = pickle.loads(msg)

		login_validation = sqlite3.connect('TermChat.db')
		cursor = login_validation.cursor()

		cursor.execute('SELECT * FROM TermChat WHERE login = ? AND password = ?', (res['login'], res['password']))

		if cursor.fetchall():
			client.send(bytes('  You have been successfully logged in!', 'utf-8'))
			threading.Thread(target=self.msg, args=(client, ), daemon=True).start()
		else:
			client.send(bytes(' Incorrect login of password. Try again.', 'utf-8'))
			self.login(client)

	def handle(self, new_socket):
		client, address = new_socket.accept()
		print(f'Conn from |{address[0]}:{address[1]}|')
		self.list1.append(client)
		threading.Thread(target=self.register_or_login, args=(client, ), daemon=True).start()

	def msg(self, client):
		while True:
			msg = client.recv(1024).decode('utf-8')
			if not msg:
				break
			for i in self.list1:
				if i != self.socket and i != client:
					try:
						i.send(bytes(msg, 'utf-8'))
					except:
						i.close()
						self.list1.remove(i)

	def event_loop(self):
		while True:
			ready_to_read, _, _ = select.select(self.list1, [], [])
			for socket in ready_to_read:
				if socket == self.socket:
					self.handle(socket)

s1 = Server('127.0.0.1', 8000)
