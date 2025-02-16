import socket

def start_server():
    # Create socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to a specific address and port
    server_socket.bind(('localhost', 12345))
    
    # Listen for incoming connections
    server_socket.listen(1)
    
    print("Server waiting for connection...")
    
    # Accept client connection
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")
    
    # Send handshake message
    client_socket.send("Hello, Client! Connection established.".encode())
    
    # Receive client's response
    client_response = client_socket.recv(1024).decode()
    print(f"Client says: {client_response}")
    
    # Close connections
    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    start_server()