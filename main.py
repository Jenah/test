import socket

HOST = '0.0.0.0'
PORT = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(5)

print(f"Listening on port {PORT}...")

while True:
    client_socket, addr = s.accept()
    request = client_socket.recv(4096).decode(errors='ignore')
    print(request.splitlines()[0])  # print first line of request

    # Prepare response
    try:
        with open('Index.html', 'r') as f:
            content = f.read()
    except FileNotFoundError:
        content = "<h1>404 Not Found</h1>"

    content_bytes = content.encode('utf-8')
    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(content_bytes)}\r\n"
        "Connection: close\r\n"
        "\r\n"
    ).encode('utf-8') + content_bytes

    client_socket.sendall(response)
    client_socket.close()
