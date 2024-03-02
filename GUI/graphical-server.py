import socket
import threading

# Constants
PORT = 5050
# decoding and encoding format
FORMAT = 'utf-8'
# IPV4 obtained from server
SERVER = socket.gethostbyname(socket.gethostname())
# Address of the server
ADDR = (SERVER, PORT)

# A list of clients and their names
clients, names = [], []

# Create a new IPV4 socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the server to the address
server.bind(ADDR)

def server_start():
    print("[STARTING] Server is starting...")
    print("Server started on " + SERVER)
    
    # Start listening for connections
    server.listen()
    
    while True:
        # Accept new connections and address bound to the socket
        conn, address = server.accept()
        conn.send("NAME".encode(FORMAT))
        
        # Get the name of the client
        name = conn.recv(1024).decode(FORMAT)
        
        # Add the names and clients to their respective lists
        names.append(name)
        clients.append(conn)
        
        print(f"Name is :{name}")
        
        # Broadcast message to all clients
        broadcast(f"{name} has joined the chat!".encode(FORMAT))
        
        # Success connection message to the client
        conn.send("Connected to the server!".encode(FORMAT))
        
        # Threading allows concurrent client connections to the server
        thread = threading.Thread(target=handle_client, args=(conn, address))
        
        # Start the thread
        thread.start()
        
        # Show the number of active client connections
        print(f"[ACTIVE CONNECTIONS]: {threading.activeCount() - 1}")
        
        
def handle_client(conn, addr):
    # Handles incoming messages
    print(f"New connection - {addr}")
    connected = True
    
    while connected:
        message = conn.recv(1024)
        
        # Broadcast the message sent
        broadcast(message)
        
    conn.close()
    
def broadcast(message):
    # Broadcasting every client's messages
    for client in clients:
        client.send(message)
        

# Start the chat
server_start()