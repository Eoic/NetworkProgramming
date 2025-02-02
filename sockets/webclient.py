import socket
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('domain')
    parser.add_argument('port', default=80, type=int, nargs='?')
    args = parser.parse_args()
    port = args.port
    domain = args.domain

    payload = 'Hello there.'
    content_type = 'text/plain'
    content_length = len(payload)

    data = (
        f"""
GET /index.html HTTP/1.1
Host: {domain}
Content-Type: {content_type}
Content-Length: {content_length}
Connection: close

{payload}
    """.strip()
        .replace('\n', '\r\n')
        .encode('ISO-8859-1')
    )

    client = socket.socket()
    client.connect((domain, port))
    client.sendall(data)
    received = b''

    while True:
        buffer = client.recv(4096)

        if len(buffer) == 0:
            break

        received += buffer

    print(received.decode('ISO-8859-1'))


if __name__ == '__main__':
    main()
