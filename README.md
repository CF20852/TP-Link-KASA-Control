This repository contains several Python 3 programs that can be used to find and control TP-Link Kasa devices.

Another useful collection of Python Kasa discovery and control software can be found in the python-kasa repo.

TP-Link seems to have started with a simple XOR-based encryption technique where the first byte of a message is XOR'd with 0xAB and the remaining bytes of the message are XOR'd with the result XORing the bytes with the XOR'd previous byte.  TP-Link now uses a handshake/encryption protocol called KLAP.

According to ChatGPT,
What KLAP actually does is, at a high level:

1.  Discovery occurs locally, typically via UDP.
2.  The controller contacts the device over HTTP port 80.
3.  The device and controller perform a cryptographic handshake.
4.  They establish a temporary encryption session.
5.  Kasa commands such as:
`{"system":{"set_relay_state":{"state":1}}}` are encrypted before being sent to the device.
6. The device decrypts the request and returns an encrypted response.

KLAP does not require access to TP-Link's cloud once the device is configured. Your computer can communicate directly with the Kasa device using KLAP over your LAN.

Here are some brief (very brief) descriptions of what the Python programs in this repo do:
- kasa_xor_scan.py scans an entire subnet for kasa devices that use the XOR encryption protocol and returns their IP addresses and device info.
- kasa_xor_test.py interrogates a single Kasa device that uses the XOR encryption protocol and returns its device info.
- kasa_xor_control.py allows the user to turn a single Kasa device that uses the XOR encryption protocol on and off.
- kasa_klap_control.py allows the user to turn a single Kasa device that uses the KLAP v2 encryption protocol on and off

To discover devices that use the KLAP encryption protocol, use the python-kasa library's `kasa discover` command.
