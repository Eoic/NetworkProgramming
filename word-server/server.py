import random
from time import sleep
import socket
import sys

WORDS = [
    "a",
    "the",
    "be",
    "in",
    "you",
    "apple",
    "banana",
    "chess",
    "dolphin",
    "eclipse",
    "falcon",
    "guitar",
    "horizon",
    "illusion",
    "jungle",
    "kangaroo",
    "lighthouse",
    "mountain",
    "nebula",
    "ocean",
    "puzzle",
    "quasar",
    "rainbow",
    "spectrum",
    "tornado",
    "umbrella",
    "volcano",
    "whisper",
    "xylophone",
    "yacht",
    "zeppelin",
    "alchemy",
    "breeze",
    "crimson",
    "dynasty",
    "emerald",
    "firefly",
    "galaxy",
    "harbor",
    "island",
    "jigsaw",
    "knight",
    "labyrinth",
    "mirage",
    "nocturne",
    "obsidian",
    "phantom",
    "quiver",
    "riddle",
    "sapphire",
    "twilight",
    "universe",
    "voyage",
    "wanderlust",
    "zenith",
]

WORD_LEN_SIZE = 2


def usage():
    print("Usage: server.py <port>", file=sys.stderr)


def build_word_packet(word_count: int):
    word_packet = b""
    word_list = []

    for _ in range(word_count):
        word = random.choice(WORDS)
        word_bytes = word.encode()
        word_len = len(word_bytes)
        word_len_bytes = word_len.to_bytes(WORD_LEN_SIZE, "big")
        word_packet += word_len_bytes + word_bytes
        word_list.append(word)

    return word_packet, word_list


def send_words(s: socket.socket):
    word_count = random.randrange(1, 10)
    word_packet, word_list = build_word_packet(word_count)
    s.sendall(word_packet)

    return word_list


def main(argv):
    try:
        # port = int(argv[1])
        port = 9000
    except Exception:
        usage()
        return 1

    s = socket.socket()
    s.bind(("", port))
    s.listen()

    try:
        while True:
            print("-" * 80)
            print("| Waiting for connections...")
            print("-" * 80)

            client_s, conn_info = s.accept()
            print(f"Got connection from {conn_info}")
            word_list = send_words(client_s)
            print(f"Send {len(word_list)} words: {''.join(word_list)}")
            client_s.close()
    except KeyboardInterrupt:
        print("Bye.", file=sys.stdout)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
