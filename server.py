from os import system
import socket

class Server:
	ip = None
	port = None
	main = None
	client_socket = None
	client_address = None
	file_name = None
	send_or_recieve = None

	def __init__(self, ip="0.0.0.0", port=8000):
		if(ip == "0.0.0.0"):
			self.ip = self.get_ip()
		else:
			self.ip = ip
		self.port = port
		self.main = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.main.bind((self.ip, self.port))

	def get_ip(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.settimeout(0)
		try:
			s.connect(("8.8.8.8", 1))
			ip = s.getsockname()[0]
		except Exception:
			ip = "127.0.0.1"
		finally:
			s.close()
		return ip

	def wait_for_connection(self):
		self.main.listen(0)
		print(f"listenning on {self.ip}:{self.port}")
		self.client_socket, self.client_address = self.main.accept()
		print(f"accepted connection from {self.client_address[0]}:{self.client_address[1]}")
		print("")
		return True

	def decide_send_or_recieve(self):
		try:
			self.send_or_recieve = self.client_socket.recv(1024).decode("utf-8")
		except:
			print("couldnt get the send or recieve info")
			self.client_socket.send("0".encode("utf-8"))
			self.decide_send_or_recieve()
		else:
			self.client_socket.send("1".encode("utf-8"))
			print("Mode:", self.send_or_recieve)

	def get_file_name(self):
		try:
			self.file_name = self.client_socket.recv(1024).decode("utf-8")
		except:
			print("couldnt get the file name")
			self.client_socket.send("0".encode("utf-8"))
			self.get_file_name()
		else:
			self.client_socket.send("1".encode("utf-8"))
			print(f'"{self.file_name}"')

	def send_file(self):
		try:
			with open(self.file_name, "rb") as f:
				data = f.read(1024)
				while(data):
					self.client_socket.send(data)
					data = f.read(1024)
		except:
			return 0
		else:
			return 1

	def recieve_file(self):
		try:
			data = self.client_socket.recv(1024)
			with open(self.file_name, "wb") as x:
				x.write(data)
				data = self.client_socket.recv(1024)
			with open(self.file_name, "ab") as f:
				while(data):
					f.write(data)
					data = self.client_socket.recv(1024)
		except:
			return 0
		else:
			return 1

	def shutdown(self):
		self.main.close()

system("clear || cls")
server = Server()
server.wait_for_connection()
server.decide_send_or_recieve()
server.get_file_name()

if(server.send_or_recieve == "send"):
	server.recieve_file()

elif(server.send_or_recieve == "recieve"):
	server.send_file()