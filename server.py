import socket
import threading

HEADER = 1024
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5050
sever= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sever.bind((SERVER, PORT))
sever.listen()

clients = []
nicknames = []

def broadcast(message): #for sinding the message too every client
  for client in clients:
    client.send(bytes(str(message), 'ascii'))
  
def handle(conn):
  while True:
    try:
      message = conn.recv(1024)
      broadcast(message)
    except:
      #get the index of the client
      index = clients.index(conn)
      #remove the client
      clients.remove(conn)
      #close the connection with the client
      conn.close()
      nickname = nicknames[index]
      broadcast(f"{nickname} left the chat".encode('ascii'))
      nicknames.remove(nickname)
      break

def recieve(): #recieve clients connection
  while True:
    conn, addr = sever.accept()
    print(f"connected with {addr}")
    clients.append(conn)
    #key word to tell the client to enter a nickname
    conn.send(bytes('NICK', 'ascii'))
    nickname = conn.recv(1024).decode('ascii')
    # add nickname to the list nicknames
    nicknames.append(nickname)
    print(f"nickname of the client is {nickname}")
    broadcast(f"{nickname} joined the chat")
    conn.send("you are connected to the server!!".encode('ascii'))
    
    thread = threading.Thread(target=handle, args=(conn,))
    thread.start()
print("server is listening....")
recieve()
