import socket
import threading
import sys

class CaseClient:
    def __init__(self, host='localhost', port=12345):
        # Create client socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            # Connect to server
            self.client_socket.connect((host, port))
            print(f"[*] Connected to server at {host}:{port}")
        except ConnectionRefusedError:
            print("[!] Connection failed. Ensure server is running.")
            sys.exit(1)

    def receive_messages(self):
        """Listen for server converted messages"""
        try:
            while True:
                # Receive uppercase message from server
                data = self.client_socket.recv(1024)
                
                # If no data, server disconnected
                if not data:
                    break
                
                # Print converted message
                print(f"\r[SERVER RESPONSE] {data.decode('utf-8')}")
                print("Enter message: ", end='', flush=True)
        
        except Exception as e:
            print(f"[!] Error receiving messages: {e}")
        
        finally:
            self.client_socket.close()

    def send_messages(self):
        """Send messages to server"""
        try:
            while True:
                # Get user input (converted to lowercase)
                message = input("Enter message: ").lower()
                
                # Option to quit
                if message in ['quit', 'exit', 'q']:
                    break
                
                # Send lowercase message to server
                self.client_socket.send(message.encode('utf-8'))
        
        except Exception as e:
            print(f"[!] Error sending messages: {e}")
        
        finally:
            self.client_socket.close()

    def start(self):
        """Start client communication"""
        # Thread to receive messages
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()

        # Send messages in main thread
        self.send_messages()

def main():
    # Initialize and start client
    case_client = CaseClient()
    case_client.start()

if __name__ == "__main__":
    main()