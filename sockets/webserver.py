import os
import socket
import argparse
from datetime import datetime


def create_response(content, mime_type, code, code_name):
    return f"""
HTTP/1.1 {code} {code_name}
Connection: close
Content-Type: {mime_type};
Content-Length: {len(content)}

{content}
""".strip().replace(
        '\n', '\r\n'
    )


def parse_header(header):
    data = dict()
    tokens = header.split('\r\n')
    first = tokens[0]

    for token in tokens[1:]:
        pair = token.split(': ')

        if len(pair) == 2:
            data[pair[0].strip()] = pair[1].strip()

    first = first.split(' ')

    return {'method': first[0], 'path': first[1], 'version': first[2]}, data


def read_payload(pathname):
    mime_type = 'text/plain'
    _, extension = os.path.splitext(pathname)

    if extension == '.html':
        mime_type = 'text/html'

    try:
        with open(pathname, 'rb') as file:
            content = file.read()
            return content, mime_type, 200, 'OK'
    except FileNotFoundError:
        return 'File was not found.', 'text/plain', 404, 'Not Found'


def send_response(client_socket, pathname):
    content, mime_type, response_code, response_name = read_payload(pathname)
    response = create_response(content, mime_type, response_code, response_name)
    client_socket.sendall(response.encode('ISO-8859-1'))
    client_socket.close()


def main():
    buffer_size = 4096
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
            leading, header = parse_header(header)
            print(f'[{datetime.now()}]:', leading['method'])
            length = int(header.get('Content-Length', '0'))

            pathname = os.path.basename(leading['path'])
            print('Rquesting:', pathname)

            if len(payload) < length:
                unread_bytes = length - len(payload)

                while unread_bytes > 0:
                    payload += new_socket.recv(buffer_size).decode('ISO-8859-1')
                    unread_bytes -= buffer_size

            print(f'Received {length} bytes:', payload)
            send_response(new_socket, pathname)
    except KeyboardInterrupt:
        print('Bye.')
    except Exception as error:
        print('An error ocurred:', error)


if __name__ == '__main__':
    main()
