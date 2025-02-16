import socket
import ssl
import urllib.request
import certifi

def connect_to_url(url, port=443):
    try:
        # Remove protocol prefixes
        hostname = url.replace('https://', '').replace('http://', '').split('/')[0]
        
        # Create SSL context with certificate verification
        context = ssl.create_default_context(cafile=certifi.where())
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        # Establish secure connection
        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as secure_sock:
                # Construct HTTP GET request
                request = (
                    f"GET / HTTP/1.1\r\n"
                    f"Host: {hostname}\r\n"
                    "User-Agent: Mozilla/5.0\r\n"
                    "Accept: text/html\r\n"
                    "Connection: close\r\n\r\n"
                )
                
                # Send request
                secure_sock.send(request.encode())
                
                # Receive response
                response = b""
                while True:
                    chunk = secure_sock.recv(4096)
                    if not chunk:
                        break
                    response += chunk
                
                # Decode and print response
                decoded_response = response.decode('utf-8', errors='ignore')
                print(f"Connection to {url} successful!")
                
                # Print first few lines of response
                print("\nResponse Headers:")
                print('\n'.join(decoded_response.split('\n')[:10]))
                
                return decoded_response
    
    except Exception as e:
        print(f"Connection error to {url}: {e}")
        
        # Fallback method using urllib
        try:
            with urllib.request.urlopen(url) as response:
                print(f"Fallback connection to {url} successful!")
                print("\nResponse Headers:")
                for header, value in response.headers.items():
                    print(f"{header}: {value}")
                return response.read().decode('utf-8')
        except Exception as fallback_error:
            print(f"Fallback connection error: {fallback_error}")
            return None

def main():
    # List of URLs to test
    urls_to_test = [
        'https://iitj.ac.in/',
        'https://www.example.com/',
        'https://www.python.org/',
        'https://www.google.com/'
    ]
    
    # Test each URL
    for url in urls_to_test:
        print(f"\n{'='*50}")
        print(f"Connecting to: {url}")
        print(f"{'='*50}")
        connect_to_url(url)

if __name__ == "__main__":
    main()