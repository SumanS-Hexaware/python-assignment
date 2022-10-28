import socket
import threading
from datetime import datetime 

HOST = '127.0.0.1'
PORT = 1234
now = datetime.now()

def listen_for_messages_from_server(client):

    while 1: 
        message = client.recv(2048).decode('utf-8')
        if message != '':
            current_datetime = now.strftime("%H:%M, %D")
            username = message.split("~")[0]
            content = message.split("~")[1]

            print(f"[{current_datetime}] [{username}] {content}")
        else: 
            print("No message")

def send_message_to_server(client):

    while 1:

        message = input("Message: ")
        if message != '':
            client.sendall(message.encode())
        else:
            print("Empty message")
            exit(0)


def talk_to_server(client):

    username = input("Enter username: ")
    if username != '':
        client.sendall(username.encode())
    else:
        print("Username can't be empty")
        exit(0)

    threading.Thread(target=listen_for_messages_from_server, args=(client,)).start()

    send_message_to_server(client)

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST,PORT))
        print("Successfully connected")
    except:
        print(f"Unable to connect to server {HOST} {PORT}")

    talk_to_server(client)

if __name__ == '__main__':
    main()





























    