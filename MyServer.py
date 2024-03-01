import socket
import sys
import select

HOST = '127.0.0.1'
PORT = 200
HEADER_LENGTH = 10

def main():
    # Start the server
    start_server()
    
def start_server():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Set the socket option to reuse the address
    server_socket.setsockopt(socket.SQL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((HOST, PORT))
        print(f"Server is up and running on {HOST}:{PORT}")
    except:
        print('Bind failed. Error : ' + str(sys.exec_info))
        sys.exit()
    
    # Listen for incoming connections
    server_socket.listen()
    
    # List of sockets
    sockets_list = [server_socket]
    
    # Dictionary of clients - socket as key, user header and name as data
    clients = {}   
    
    print()
    print(f'Listening for connections on {HOST}:{PORT}...')
    
    while True:
        # Call to select() blocks and waits for an activity on any of the sockets
        read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
        
        for notified_socket in read_sockets:
            # If notified socket is a server socket, new connection
            if notified_socket == server_socket:
                client_socket, client_address = server_socket.accept()
                user = receive_message(client_socket)
                
                if user is False:
                    continue
                # New client is added to the list of clients
                sockets_list.append(client_socket)
                clients[client_socket] = user
                print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))
                
            else:
                message = receive_message(notified_socket)
                
                # If no message received, client their closed a connection
                if message is False:
                    print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))
                    sockets_list.remove(notified_socket)
                    del clients[notified_socket]
                    continue
                
                user = clients[notified_socket]
                print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')
                
                for client_socket in clients:
                    if client_socket != notified_socket:
                        client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])


def receive_message(client_socket):
    try:
        # Receive the "header" containing message length
        message_header = client_socket.recv(HEADER_LENGTH)
        # If no data received, client closed a connection
        if not len(HEADER_LENGTH):
            return False
        
        # Convert header to int value
        message_length = int(message_header.decode('utf-8').strip())
        
        # Dictionary with header and data
        return {'header': message_header, 'data': client_socket.recv(message_length)}
    
    except:
        print('Error receiving message header')
        return False
    
    
if __name__ == "__main__":
    main()
