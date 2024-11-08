from os import system
try:
	import tkinter as tk
	from tkinter import messagebox
except:
	print("Make sure tkinter is installed!")
	exit()
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
		self.main = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def connect(self):
		global CL_X
		global CL_Y
		_text = ""
		try:
			self.ip = ip_entry.get()
			self.port = int(port_entry.get())
			self.main.connect((self.ip, self.port))
		except:
			_text = "Couldn't connect"
			CL_X = 350
			CL_Y = 50
		else:
			file_label.place(x=FL_X, y=FL_Y)
			file_entry.place(x=FL_X + 150, y=FL_Y + 5)
			recieve_button.place(x=FL_X + 150, y=FL_Y + 50)
			send_button.place(x=FL_X + 300, y=FL_Y + 50)
			_text = "Connected to\n" + self.ip + ":" + str(self.port)
			CL_X = 350
			CL_Y = 20
		finally:
			connected_label.configure(text=_text)
			connected_label.place(x=CL_X, y=CL_Y)

	def decide_send_or_recieve(self, d):
		if(d == "s"):
			self.send_or_recieve = "send"
			self.main.send("recieve".encode("utf-8"))
		elif(d == "r"):
			self.send_or_recieve = "recieve"
			self.main.send("send".encode("utf-8"))
		p = self.main.recv(1024).decode("utf-8")
		if(p == "0"):
			messagebox.showerror(title=None, message="Something went wrong.")
		elif(p == "1"):
			return 0

	def get_file_name(self):
		self.file_name = file_entry.get()
		if(self.file_name in ["", " "]):
			self.shutdown()
			exit()
		self.main.send(self.file_name.encode("utf-8"))
		if(self.main.recv(1024).decode("utf-8") == "0"):
			messagebox.showerror(title=None, message="Something went wrong.")

	def send_file(self):
		global CL_X
		global CL_Y
		self.decide_send_or_recieve("s")
		self.get_file_name()
		getting_label.config(text="sending...")
		getting_label.place(x=CL_X + 50, y=CL_Y + 120)
		root.update() #updating the getting_label
		try:
			with open(self.file_name, "rb") as f: #sending the file
				data = f.read(1024)
				while(data): #checking the end of the file
					self.main.send(data)
					data = f.read(1024)
		except:
			messagebox.showerror(title=None, message="Couldn't send the file.")
		else:
			messagebox.showinfo(title=None, message="File sent succesfully.")
		finally:
			getting_label.configure(text="")
			self.shutdown()

	def recieve_file(self):
		global CL_X
		global CL_Y
		self.decide_send_or_recieve("r")
		self.get_file_name()
		getting_label.config(text="recieving...")
		getting_label.place(x=CL_X + 50, y=CL_Y + 120)
		root.update() #updating the getting_label
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
			# deleting empty file
			system("rm " + client.file_name + " >/dev/null 2>&1")
			system("del " + client.file_name + " >/dev/null 2>&1")
			messagebox.showerror(title=None, message="Couldn't recieve the file.")
		else:
			messagebox.showinfo(title=None, message="File recieved succesfully.")
		finally:
			getting_label.configure(text="")
			self.shutdown()

	def shutdown(self):
		self.main.close()

client = Client()

root = tk.Tk()
root.geometry("680x440")
root.title("FileTransporter")

font1 = ("Cambria", 32) #for labels
font2 = ("Arial", 24) #for buttons and entries

IL_X = 30
IL_Y = 20
ip_label = tk.Label(root, text="IP: ", font=font1)
ip_label.place(x=IL_X, y=IL_Y)
ip_entry = tk.Entry(root, width=13, font=font2)
ip_entry.place(x=IL_X + 80, y=IL_Y + 5)
port_label = tk.Label(root, text="Port: ", font=font1)
port_label.place(x=IL_X, y=IL_Y + 50)
port_entry = tk.Entry(root, width=13, font=font2)
port_entry.place(x=IL_X + 80, y=IL_Y + 55)
connect_button = tk.Button(root, text="Connect", font=font2, command=client.connect)
connect_button.place(x=IL_X, y=IL_Y + 120)

CL_X = 0
CL_Y = 0
connected_label = tk.Label(root, font=font1)
getting_label = tk.Label(root, font=font1)

FL_X = 30
FL_Y = 270
file_label = tk.Label(root, text="File name: ", font=font1)
file_entry = tk.Entry(root, width=30, font=font2)
recieve_button = tk.Button(root, text="Recieve", font=font2, command=client.recieve_file)
send_button = tk.Button(root, text="Send", font=font2, command=client.send_file)



root.mainloop()


"""system("clear || cls")
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
		system("rm " + client.file_name + " >/dev/null 2>&1")
		system("del " + client.file_name + " >/dev/null 2>&1")
		print("couldnt recieve the file!")

client.shutdown()"""