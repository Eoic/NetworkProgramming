import socket
import argparse
from datetime import datetime

response = """
HTTP/1.1 200 OK
Connection: close
Content-Type: text/plain; charset=UTF-8
Content-Length: 2

OK
""".strip().replace(
    '\n', '\r\n'
)


def get_content_length(header):
    tokens = header.split('\r\n')

    for token in tokens:
        if token.startswith('Content-Length'):
            return int(token.split(': ')[1])

    return 0


def main():
    buffer_size = 4
    parser = argparse.ArgumentParser()
    parser.add_argument('port', default=28333, type=int, nargs='?')
    args = parser.parse_args()
    port = args.port
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('', port))
    server.listen()

    print(f'Server is listening on: http://localhost:{port}.')

    try:
        while True:
            data = ''
            new_conn = server.accept()
            new_socket = new_conn[0]
            print(f'New connection from: {new_conn[1][0]}:{new_conn[1][1]}.')

            while True:
                buffer = new_socket.recv(buffer_size)
                decoded = buffer.decode('ISO-8859-1')
                data += decoded

                if '\r\n\r\n' in data:
                    break

            header, payload = data.split('\r\n\r\n')
            print(f'[{datetime.now()}]:', header.split(' ', maxsplit=1)[0])
            length = get_content_length(header)

            if len(payload) < length:
                unread_bytes = length - len(payload)

                while unread_bytes > 0:
                    payload += new_socket.recv(buffer_size).decode('ISO-8859-1')
                    unread_bytes -= buffer_size

            print('Received payload:', payload)
            new_socket.sendall(response.encode('ISO-8859-1'))
            new_socket.close()
    except KeyboardInterrupt:
        print('Bye.')
    except Exception as error:
        print('An error ocurred:', error)


if __name__ == '__main__':
    main()
