import socket
import threading
import select
import sys

class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.ip, self.port))
        self.socket.listen(0)
        if self.socket:
            print('[SERVER STARTED]')
        else:
            sys.exit()
        self.list1 = []
        self.list_to_send = []
        self.list1.append(self.socket)
        self.event_loop()

    def handle(self, new_socket):
        client, address = new_socket.accept()
        print(f'Conn from |{address[0]}:{address[1]}|')
        self.list1.append(client)
        self.list_to_send.append(client)
        threading.Thread(target=self.msg, args=(client, ), daemon=True).start()

    def msg(self, client):
        while True:
            msg = client.recv(1024).decode('utf-8')
            if not msg:
                break
            print(msg)
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
