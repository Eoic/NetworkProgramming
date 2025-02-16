import sys
import socket

packet_buffer = b""
WORD_LEN_SIZE = 2
BUFF_SIZE = 5


def usage():
    print("Usage: client.py <server> <port>", file=sys.stderr)


def get_next_word_packet(socket: socket.socket) -> bytes | None:
    global packet_buffer

    while True:
        if len(packet_buffer) >= WORD_LEN_SIZE:
            word_size_bytes = packet_buffer[0:WORD_LEN_SIZE]
            word_size = int.from_bytes(word_size_bytes, "big")
            packet_size = word_size + WORD_LEN_SIZE
            remaining_size = packet_size - len(packet_buffer)

            while remaining_size > 0:
                data = socket.recv(BUFF_SIZE)
                remaining_size -= len(data)
                packet_buffer += data

            full_packet = packet_buffer[:packet_size]
            packet_buffer = packet_buffer[packet_size:]

            return full_packet
        else:
            data = socket.recv(BUFF_SIZE)

            if len(data) == 0:
                return None

            packet_buffer += data


def extract_word(word_packet: bytes) -> str:
    word_bytes = word_packet[WORD_LEN_SIZE:]
    word = word_bytes.decode()

    return word


def main(argv):
    try:
        # server = argv[1]
        server = "127.0.0.1"
        # port = int(argv[2])
        port = 9000
    except Exception:
        usage()
        return 1

    s = socket.socket()
    s.connect((server, port))

    print("Getting words...")

    while True:
        word_packet = get_next_word_packet(s)

        if word_packet is None:
            break

        word = extract_word(word_packet)
        print(f"{word}")

    s.close()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
