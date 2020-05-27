import socket
import time
import pickle
import select
import errno
import sys
from decorators import report

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234

def tryPrintMessage(client_socket):
	time.sleep(0.1)
	try: 
		while True:
			#receive things
			message_header = client_socket.recv(HEADER_LENGTH)
			if not len(message_header):
				print("Connection closed by the server")
				sys.exit()
			message_length = int(message_header.decode('utf-8'))
			message = client_socket.recv(message_length).decode('utf-8')

			print(message)
		return True

	except IOError as e:
		if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
			print('Reading error', str(e))
			sys.exit()
		return False

	except Exception as e:
		print('General error', str(e))
		sys.exit()
		return False
	return False

def tryGetMessage(client_socket):
	time.sleep(0.1)
	try: 
		while True:
			#receive things
			message_header = client_socket.recv(HEADER_LENGTH)
			if not len(message_header):
				print("Connection closed by the server")
				sys.exit()
			message_length = int(message_header.decode('utf-8'))
			message = client_socket.recv(message_length).decode('utf-8')
			return message

	except IOError as e:
		if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
			print('Reading error', str(e))
			sys.exit()
		return False

	except Exception as e:
		print('General error', str(e))
		sys.exit()
		return False
	return False

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)
my_username = ""
my_password = ""

while True:										#Login
	my_username = input("Username: ")
	my_password = input("Password: ")

	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_socket.connect((IP, PORT))
	client_socket.setblocking(False)

	username = (my_username + " " + my_password).encode('utf-8')
	username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
	client_socket.send(username_header + username)
	response = tryGetMessage(client_socket)
	if response is not False:
		print (response)
		if response == "Logged in":
			break

while True:
	message = input(f"{my_username.split()[0]} > ")

	if message:
		ok = 0
		if message == "get items":
			ok = 1
		message = message.encode('utf-8')											#encode the message
		message_header = f"{len(message) :< {HEADER_LENGTH}}".encode('utf-8')		#encode the message header
		client_socket.send(message_header + message)								#send the message
		newMessage = tryGetMessage(client_socket)
		if ok == 1:
			print("get items")
			items = newMessage.split("\n")
			@report
			def print_item(item):
				print(f'{item[3]:<10}: calories {item[5]} expires {item[7]}\n')
			for i in items:
				if i != "":
					print(i + "\n")
					it = i.split()
					print_item(it)
		else:	
			print(newMessage)

	



