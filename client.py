import socket
import threading
nickname = input("Enter a nickname: ")

HEADER = 1024
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5050
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))

def recieve():
  while True:
    try:
      message = client.recv(1024).decode('ascii')
      if message == 'NICK':
        client.send(nickname.encode('ascii'))
      else:
        print(message)
    except:
      print("an error occured")
      client.close()
      break
def write():
  while True:
    message = f'{nickname}: {input(" ")}'
    client.send(message.encode('ascii'))
    
recv_thread = threading.Thread(target=recieve)
recv_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
