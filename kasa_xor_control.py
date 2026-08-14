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


def send_command(ip, command):
    """Send a command to the Kasa device and return its response."""

    plaintext = json.dumps(
        command,
        separators=(",", ":")
    ).encode("utf-8")

    packet = encrypt(plaintext)

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM
    )

    sock.settimeout(2.0)

    try:
        sock.sendto(packet, (ip, PORT))

        data, address = sock.recvfrom(4096)

        decrypted = decrypt(data)

        return json.loads(decrypted)

    finally:
        sock.close()


def set_power(ip, state):
    """Turn the Kasa device on or off."""

    command = {
        "system": {
            "set_relay_state": {
                "state": state
            }
        }
    }

    try:
        response = send_command(ip, command)

        print()
        print(json.dumps(response, indent=2))

        return True

    except socket.timeout:
        print("ERROR: No response from the Kasa device.")
        return False

    except (OSError, json.JSONDecodeError) as e:
        print(f"ERROR: {e}")
        return False


# Get the device IP address
ip = input("Enter the Kasa device IP address: ").strip()

print()
print("Kasa Device Controller")
print("----------------------")
print(f"Device: {ip}")
print()
print("Commands:")
print("  on   - Turn device on")
print("  off  - Turn device off")
print("  q    - Quit")

while True:

    command = input("\nEnter command: ").strip().lower()

    if command == "on":
        print("Turning ON...")
        set_power(ip, 1)

    elif command == "off":
        print("Turning OFF...")
        set_power(ip, 0)

    elif command == "q":
        print("Exiting.")
        break

    else:
        print("Invalid command. Enter on, off, or q.")

