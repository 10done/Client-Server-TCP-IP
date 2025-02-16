import socket
import threading
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import base64

class SecureServer:
    def __init__(self, host='localhost', port=12345):
        # Generate private key
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()

        # Create server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        
        print("[*] Secure Server initialized")

    def encrypt_message(self, message, public_key):
        """Encrypt message with given public key"""
        encrypted = public_key.encrypt(
            message.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return base64.b64encode(encrypted)

    def decrypt_message(self, encrypted_message):
        """Decrypt message using server's private key"""
        encrypted = base64.b64decode(encrypted_message)
        decrypted = self.private_key.decrypt(
            encrypted,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted.decode()

    def handle_client(self, client_socket, client_address):
        """Handle individual client connection"""
        try:
            # Send server's public key to client
            public_key_bytes = self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            client_socket.send(public_key_bytes)

            # Receive client's public key
            client_public_key_bytes = client_socket.recv(2048)
            client_public_key = serialization.load_pem_public_key(client_public_key_bytes)

            while True:
                # Receive encrypted message
                encrypted_data = client_socket.recv(2048)
                
                if not encrypted_data:
                    break

                # Decrypt received message
                decrypted_message = self.decrypt_message(encrypted_data)
                print(f"[RECEIVED] from {client_address}: {decrypted_message}")

                # Create echo message and encrypt with client's public key
                echo_message = f"Echo: {decrypted_message}"
                encrypted_echo = self.encrypt_message(echo_message, client_public_key)
                client_socket.send(encrypted_echo)

        except Exception as e:
            print(f"[ERROR] {e}")
        finally:
            client_socket.close()

    def start(self):
        """Start server and accept connections"""
        print("[*] Secure Server listening")
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"[+] Connection from {client_address}")
                
                # Handle each client in a separate thread
                client_thread = threading.Thread(
                    target=self.handle_client, 
                    args=(client_socket, client_address)
                )
                client_thread.start()
        
        except KeyboardInterrupt:
            print("\n[*] Server shutting down...")
        finally:
            self.server_socket.close()

class SecureClient:
    def __init__(self, host='localhost', port=12345):
        # Generate client private key
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()
        
        # Create client socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        
        print("[*] Secure Client initialized")

    def encrypt_message(self, message, public_key):
        """Encrypt message with given public key"""
        encrypted = public_key.encrypt(
            message.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return base64.b64encode(encrypted)

    def decrypt_message(self, encrypted_message):
        """Decrypt message using client's private key"""
        encrypted = base64.b64decode(encrypted_message)
        decrypted = self.private_key.decrypt(
            encrypted,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted.decode()

    def start_communication(self):
        try:
            # Receive server's public key
            server_public_key_bytes = self.client_socket.recv(2048)
            server_public_key = serialization.load_pem_public_key(server_public_key_bytes)

            # Send client's public key to server
            client_public_key_bytes = self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            self.client_socket.send(client_public_key_bytes)

            while True:
                # Get user message
                message = input("Enter message (or 'quit' to exit): ")
                
                if message.lower() in ['quit', 'exit']:
                    break

                # Encrypt message with server's public key
                encrypted_message = self.encrypt_message(message, server_public_key)
                self.client_socket.send(encrypted_message)

                # Receive and decrypt echo
                encrypted_echo = self.client_socket.recv(2048)
                decrypted_echo = self.decrypt_message(encrypted_echo)
                print(f"[SERVER ECHO] {decrypted_echo}")

        except Exception as e:
            print(f"[ERROR] {e}")
        finally:
            self.client_socket.close()

def run_server():
    server = SecureServer()
    server.start()

def run_client():
    client = SecureClient()
    client.start_communication()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'server':
            run_server()
        elif sys.argv[1] == 'client':
            run_client()
    else:
        print("Usage: python script.py [server|client]")