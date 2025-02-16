import socket
import threading

class EchoServer:
    def __init__(self, host='localhost', port=12345):
        # Create server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Bind socket to address
        self.server_socket.bind((host, port))
        
        # Listen for connections
        self.server_socket.listen(5)
        
        print(f"[*] Echo Server listening on {host}:{port}")

    def handle_client(self, client_socket, client_address):
        """Handle individual client connection"""
        print(f"[+] Accepted connection from {client_address}")
        
        try:
            while True:
                # Receive data from client
                data = client_socket.recv(1024)
                
                # If no data, client disconnected
                if not data:
                    break
                
                # Decode and print received message
                message = data.decode('utf-8')
                print(f"[RECEIVED] from {client_address}: {message}")
                
                # Echo back the same message
                client_socket.send(data)
                print(f"[ECHOED] back to {client_address}: {message}")
        
        except ConnectionResetError:
            print(f"[-] Connection reset by {client_address}")
        
        finally:
            # Close client connection
            client_socket.close()
            print(f"[-] Connection with {client_address} closed")

    def start(self):
        """Start server and accept connections"""
        try:
            while True:
                # Wait for client connection
                client_socket, client_address = self.server_socket.accept()
                
                # Create thread to handle client
                client_handler = threading.Thread(
                    target=self.handle_client, 
                    args=(client_socket, client_address)
                )
                client_handler.start()
        
        except KeyboardInterrupt:
            print("\n[*] Server shutting down...")
        
        finally:
            # Close server socket
            self.server_socket.close()

def main():
    # Initialize and start server
    echo_server = EchoServer()
    echo_server.start()

if __name__ == "__main__":
    main()