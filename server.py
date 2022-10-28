import socket
import threading


HOST = '127.0.0.1'
PORT = 1234
LISTENER_LIMIT = 5
active_clients = [] # list of connected users

#----This listens for any upcoming msgs from a client----

def listen_for_messages(client, username):

    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            final_msg = username + '~' + message
            send_messages_to_all(final_msg)
        else: 
            print(f"Message from client {username} is empty")

#----Function to send msg to a singlt client----

def send_message_to_client(client, message):

    client.sendall(message.encode())

# ----This sends any new msg to all the clients that are currently connected to the server-----

def send_messages_to_all(message):
    
    for user in active_clients:

        send_message_to_client(user[1], message)

# ------------This handles clients --------------

def client_handler(client):
    
    while 1:
        username = client.recv(2048).decode('utf-8') 
        if username != '':
            active_clients.append((username, client))
            prompt_msg = "SERVER~" + f"{username} added to the chat"
            send_messages_to_all(prompt_msg)
            break
        else:
            print("Client username is empty")

    # To call this method, we use threading. Now this function runs concurrently with server side script
    threading.Thread(target=listen_for_messages, args=(client, username, )).start()


def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # created a socket class obj
    # AF_NET means I'm using IPV4 addresses
    # SOCK_STREAM cuz I'm using TCP for communication...if u wanna use UDP then use SOCK_DGRAM

    try:

        #Providing the server with an address
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except:
        print(f"Unable to bind to host {HOST} and port {PORT}")

    #setting a server limit as in specifying the no. of clients that are gonna connect at a time
    server.listen(LISTENER_LIMIT)

    # This loop keeps listening to client connections
    while 1:

        client, address = server.accept() # accept() waits for an incoming connection, return a new socket representing the connection and the address of the client
        print(f"Successfully connected to client {address[0]} {address[1]}") #address is a tuple with 1st value as host and 2nd value as port

        threading.Thread(target=client_handler, args=(client, )).start()

if __name__ == '__main__': 
    main()














