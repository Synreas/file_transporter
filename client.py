from os import system
import socket

class Client:
	ip = None
	port = None
	main = None
	server_socket = None
	server_address = None
	file_name = None
	send_or_recieve = None

	def __init__(self):
		print("Welcome to FileTransporter")
		print("##########################")
		print("")
		print("choose the server")
		self.ip = input("IP:")
		self.port = int(input("Port:"))
		self.main = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def connect(self):
		print("")
		self.main.connect((self.ip, self.port))
		print("connected!")

	def decide_send_or_recieve(self):
		self.send_or_recieve = input("do you want to send or recieve file: ")
		if(self.send_or_recieve in ["", " "]):
			exit()
		elif(self.send_or_recieve.lower() in ["s", "send", "send file"]):
			self.send_or_recieve = "send"
			self.main.send("send".encode("utf-8"))
		elif(self.send_or_recieve.lower() in ["r", "recieve", "recieve file"]):
			self.send_or_recieve = "recieve"
			self.main.send("recieve".encode("utf-8"))
		else:
			self.decide_send_or_recieve()
			return 0
		p = self.main.recv(1024).decode("utf-8")
		if(p == "0"):
			self.decide_send_or_recieve()
		elif(p == "1"):
			return 0

	def get_file_name(self):
		self.file_name = input("file name: ")
		if(self.file_name in ["", " "]):
			exit()
		self.main.send(self.file_name.encode("utf-8"))
		if(self.main.recv(1024).decode("utf-8") == "0"):
			self.get_file_name()

	def send_file(self):
		try:
			with open(self.file_name, "rb") as f:
				data = f.read(1024)
				while(data):
					self.main.send(data)
					data = f.read(1024)
		except:
			return 0
		else:
			return 1

	def recieve_file(self):
		try:
			data = self.main.recv(1024)
			with open(self.file_name, "wb") as x:
				x.write(data)
				data = self.main.recv(1024)
			with open(self.file_name, "ab") as f:
				while(data):
					f.write(data)
					data = self.main.recv(1024)	
		except:
			return 0
		else:
			return 1

	def shutdown(self):
		self.main.close()

system("clear || cls")
client = Client()
client.connect()
client.decide_send_or_recieve()
client.get_file_name()

if(client.send_or_recieve == "send"):
	if (client.send_file()):
		print("file sent succesfully.")
	else:
		print("couldnt send the file!")

elif(client.send_or_recieve == "recieve"):
	if (client.recieve_file()):
		print("file recieved succesfully.")
	else:
		print("couldnt recieve the file!")