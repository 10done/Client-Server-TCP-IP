import socket

def start_client():
    # Create socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the server
    client_socket.connect(('localhost', 12345))
    
    # Receive server's handshake message
    server_greeting = client_socket.recv(1024).decode()
    print(f"Server says: {server_greeting}")
    
    # Send response
    client_socket.send("Hi Server, Connection received!".encode())
    
    # Close connection
    client_socket.close()

if __name__ == "__main__":
    start_client()