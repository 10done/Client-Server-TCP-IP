import socket
import threading

class ReverseServer:
    def __init__(self, host='localhost', port=12345):
        # Create server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Bind socket to address
        self.server_socket.bind((host, port))
        
        # Listen for connections
        self.server_socket.listen(5)
        
        print(f"[*] Reverse Message Server listening on {host}:{port}")

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
                
                # Decode and reverse the message
                message = data.decode('utf-8')
                reversed_message = message[::-1]
                
                print(f"[RECEIVED] from {client_address}: {message}")
                print(f"[REVERSED] message: {reversed_message}")
                
                # Send reversed message back to client
                client_socket.send(reversed_message.encode('utf-8'))
        
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
    reverse_server = ReverseServer()
    reverse_server.start()

if __name__ == "__main__":
    main()