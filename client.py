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
		print("")

	def decide_send_or_recieve(self):
		self.send_or_recieve = input("do you want to send or recieve file: ")
		if(self.send_or_recieve in ["", " "]):
			exit()
		elif(self.send_or_recieve.lower() in ["s", "send", "send file"]):
			self.send_or_recieve = "send"
			self.main.send("recieve".encode("utf-8"))
		elif(self.send_or_recieve.lower() in ["r", "recieve", "recieve file"]):
			self.send_or_recieve = "recieve"
			self.main.send("send".encode("utf-8"))
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
			self.shutdown()
			exit()
		self.main.send(self.file_name.encode("utf-8"))
		if(self.main.recv(1024).decode("utf-8") == "0"):
			self.get_file_name()

	def send_file(self):
		try:
			with open(self.file_name, "rb") as f: #sending the file
				data = f.read(1024)
				while(data): #checking the end of the file
					self.main.send(data)
					data = f.read(1024)
		except:
			return 0
		else:
			return 1

	def recieve_file(self):
		try:
			data = self.main.recv(1024)
			1/len(data) #checking for the empty data
			with open(self.file_name, "wb") as x: #creating the file
				x.write(data)
				data = self.main.recv(1024)
			with open(self.file_name, "ab") as f: #adding to the file
				while(data): #checking the end of the file 
					f.write(data)
					data = self.main.recv(1024)	
		except:
			return 0
		else:
			return 1

	def shutdown(self):
		self.main.close()

system("clear || cls") #clearing the terminal
client = Client()
client.connect()
client.decide_send_or_recieve()
client.get_file_name()

if(client.send_or_recieve == "send"):
	print("")
	print("sending...")
	if (client.send_file()):
		print("file sent succesfully.")
	else:
		print("couldnt send the file!")

elif(client.send_or_recieve == "recieve"):
	print("")
	print("recieving...")
	if (client.recieve_file()):
		print("file recieved succesfully.")
	else:
		# deleting the empty file
		system("rm " + client.file_name + " >/dev/null 2>&1")
		system("del " + client.file_name + " >/dev/null 2>&1")
		print("couldnt recieve the file!")

client.shutdown()