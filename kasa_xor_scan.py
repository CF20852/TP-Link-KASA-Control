import socket
import json


PORT = 9999


def get_subnet():
    """Prompt the user for a subnet prefix, e.g. '192.168.4' or '192.168.4.'."""
    while True:
        raw = input("Enter the subnet to scan (e.g. 192.168.4): ").strip()

        # Accept either "192.168.4" or "192.168.4." and normalize to end with a dot.
        if raw.endswith("."):
            raw = raw[:-1]

        octets = raw.split(".")
        if len(octets) == 3 and all(o.isdigit() and 0 <= int(o) <= 255 for o in octets):
            return raw + "."

        print("Invalid subnet. Please enter the first three octets, e.g. 192.168.4")


SUBNET = get_subnet()


def encrypt(data):
    key = 0xAB
    result = bytearray()

    for byte in data:
        encrypted = byte ^ key
        result.append(encrypted)
        key = encrypted

    return bytes(result)


def decrypt(data):
    key = 0xAB
    result = bytearray()

    for byte in data:
        decrypted = byte ^ key
        result.append(decrypted)
        key = byte

    return bytes(result)


# Kasa system information request
command = {
    "system": {
        "get_sysinfo": {}
    }
}

plaintext = json.dumps(
    command,
    separators=(",", ":")
).encode("utf-8")

packet = encrypt(plaintext)


for last_octet in range(2, 255):

    ip = SUBNET + str(last_octet)

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM
    )

    # Short timeout so the scan completes quickly
    sock.settimeout(0.15)

    try:
        sock.sendto(packet, (ip, PORT))

        data, address = sock.recvfrom(4096)

        decrypted = decrypt(data)

        try:
            response = json.loads(decrypted)

            # Print IP address followed by JSON response
            print(ip)
            print(json.dumps(response, indent=2))
            print()

        except (json.JSONDecodeError, UnicodeDecodeError):
            pass

    except (socket.timeout, OSError):
        pass

    finally:
        sock.close()