import socket
import time
import pickle
import select
import sqlite3
import dbHandler as db
import mediator as med

conn = sqlite3.connect('Wasteapp.db')
conn.row_factory = sqlite3.Row

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))
server_socket.listen()

sockets_list = [server_socket]

clients = {}

def receive_message(client_socket):
	try:
		message_header = client_socket.recv(HEADER_LENGTH)

		if not len(message_header):
			return False

		message_length = int(message_header.decode('utf-8'))
		return {"header": message_header, "data": client_socket.recv(message_length)}
	except:
		return False

def listToString(s):  
    
    # initialize an empty string 
    str1 = ""  
    
    # traverse in the string   
    for ele in s:  
        str1 += ele   
    
    # return string   
    return str1  


while True:
	read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

	for notified_socket in read_sockets:
		if notified_socket == server_socket:							#If a new user tries to connect
			client_socket, client_address = server_socket.accept()		

			user = receive_message(client_socket)						

			if user is False:											#If the server gets something
				continue
			elif db.userExists(conn, user['data'].decode('utf-8').split()[0], user['data'].decode('utf-8').split()[1]) is not None:
				#If we can create the new user
				sockets_list.append(client_socket)							#Let the user enter

				clients[client_socket] = user								#Register his address
				print(f"New connection from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')}")
				client_socket.send(f"{len('Logged in'):<{HEADER_LENGTH}}".encode('utf-8') + 'Logged in'.encode('utf-8'))
			else:
				client_socket.send(f"{len('Login failed'):<{HEADER_LENGTH}}".encode('utf-8') + 'Login failed'.encode('utf-8'))

		else:
			message = receive_message(notified_socket)

			if message is False:																				#If the user closes his connection remove his address
				print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
				sockets_list.remove(notified_socket)
				del clients[notified_socket]
				continue

			user = clients[notified_socket]																		#Get the pipe
			print(f"Received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")	#Print on server console what it received
			
			result = med.processCMD(conn, user['data'].decode('utf-8').split()[0], message['data'].decode('utf-8'))

			notified_socket.send(f"{len(result):<{HEADER_LENGTH}}".encode('utf-8') + result.encode('utf-8'))


			#notified_socket.send(f"{len(db.getUserPassword(conn, int(message['data']))):<{HEADER_LENGTH}}".encode('utf-8') + db.getUserPassword(conn, int(message['data'])).encode('utf-8'))

	
	for notified_socket in exception_sockets:
		sockets_list.remove(notified_socket)
		del clients[notified_socket]
	