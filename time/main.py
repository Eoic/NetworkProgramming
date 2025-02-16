from math import trunc
import time
import socket
from datetime import datetime


def main():
    client = socket.socket()
    client.connect(("time.nist.gov", 37))
    response = bytes()

    while True:
        received = client.recv(1024)

        if len(received) == 0:
            break

        response += received

    nist_time = int.from_bytes(response)
    system_time = trunc(
        int(time.time()) + (datetime(1970, 1, 1) - datetime(1900, 1, 1)).total_seconds()
    )
    delta = nist_time - system_time

    print("NIST time:", nist_time)
    print("System time:", system_time)
    print(f"Error {delta:.2f}")

    client.close()


if __name__ == "__main__":
    main()
