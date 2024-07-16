import socket

# Define the host and port for the server
HOST = '127.0.0.1'
PORT = 8080

# Define the HTTP response messages
HTTP_RESPONSES = {
    200: 'OK',
    304: 'Not Modified',
    400: 'Bad request',
    404: 'Not Found',
    408: 'Request Timed Out'
}

# Define the HTML content to be served
HTML_CONTENT = """
<!DOCTYPE html>
<html>
<head>
    <title>Simple Web Server</title>
</head>
<body>
    <h1>Hello, World!</h1>
    <p>This is a simple web server implemented in Python.</p>
</body>
</html>
"""

# Function to handle HTTP requests
def handle_request(client_socket):
    request_data = client_socket.recv(1024).decode('utf-8')

    if not request_data:
        return

    # Extract the HTTP method and path from the request
    http_method = request_data.split(' ')[0]
    path = request_data.split(' ')[1]

    # Check if the requested path is valid
    if path == '/':
        status_code = 200
        response_message = HTTP_RESPONSES[status_code]
        content = HTML_CONTENT
    else:
        status_code = 404
        response_message = HTTP_RESPONSES[status_code]
        content = ''

    # Construct the HTTP response
    http_response = f'HTTP/1.1 {status_code} {response_message}\r\nContent-Length: {len(content)}\r\n\r\n{content}'
    
    # Send the HTTP response to the client
    client_socket.sendall(http_response.encode('utf-8'))

    # Close the client socket
    client_socket.close()







# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen(1)
print(f'Server listening on {HOST}:{PORT}')

try:
    while True:
        # Accept incoming connection
        client_socket, client_address = server_socket.accept()
        print(f'Connection from {client_address}')

        # Handle the HTTP request
        handle_request(client_socket)
except KeyboardInterrupt:
    print('Server shutting down...')
finally:
    # Close the server socket
    server_socket.close()