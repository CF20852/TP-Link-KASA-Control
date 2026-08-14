import socket
import json


PORT = 9999


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


# Prompt for the Kasa XOR device IP address
KASA_IP = input("Enter the Kasa XOR device IP address: ").strip()

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

print()
print("Kasa XOR device test")
print("----------------")
print("Target:", KASA_IP)
print("Port:", PORT)
print()
print("Command:")
print(plaintext.decode())
print()
print("Sending...")

sock = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM
)

sock.settimeout(3)

try:
    sock.sendto(packet, (KASA_IP, PORT))

    print("Packet sent.")
    print("Waiting for response...")

    data, address = sock.recvfrom(4096)

    print()
    print("Response received from:", address)
    print("Length:", len(data))

    print()
    print("Raw response:")
    print(data.hex(" "))

    decrypted = decrypt(data)

    print()
    print("Decrypted response:")
    print(decrypted.decode("utf-8", errors="replace"))

    try:
        obj = json.loads(decrypted)

        print()
        print("Formatted JSON:")
        print(json.dumps(obj, indent=2))

    except json.JSONDecodeError:
        print()
        print("Response was not valid JSON.")

except socket.timeout:
    print()
    print("TIMEOUT")
    print()
    print("The Kasa device did not respond on UDP port 9999.")

except OSError as e:
    print()
    print("Windows socket error:")
    print(e)

finally:
    sock.close()

