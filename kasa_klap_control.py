import asyncio
import getpass
import json

from kasa import DeviceConfig, Credentials
from kasa.deviceconfig import (
    DeviceConnectionParameters,
    DeviceEncryptionType,
    DeviceFamily,
)
from kasa.transports.klaptransport import KlapTransportV2


async def main():

    print()
    print("TP-Link Kasa Device KLAP-v2 Controller")
    print("======================================")
    print()

    ip = input("Enter device IP address: ").strip()
    username = input("Enter Kasa account email: ").strip()
    password = getpass.getpass("Enter Kasa account password: ")

    # Your device discovery information:
    #
    # device_type:       IOT.SMARTPLUGSWITCH
    # encrypt_type:      KLAP
    # http_port:         80
    # is_support_https:  False
    # lv:                2
    # new_klap:          1

    connection_type = DeviceConnectionParameters(
        device_family=DeviceFamily.IotSmartPlugSwitch,
        encryption_type=DeviceEncryptionType.Klap,
        login_version=2,
        https=False,
        http_port=80,
    )

    config = DeviceConfig(
        host=ip,
        timeout=5,
        credentials=Credentials(
            username=username,
            password=password,
        ),
        connection_type=connection_type,
    )

    transport = KlapTransportV2(config=config)

    try:

        print()
        print("Performing KLAP-v2 handshake...")

        await transport.perform_handshake()

        print("KLAP-v2 authentication successful.")
        print()

        # ------------------------------------------------------------
        # Get system information
        # ------------------------------------------------------------

        request = json.dumps(
            {
                "system": {
                    "get_sysinfo": {}
                }
            },
            separators=(",", ":"),
        )

        response = await transport.send(request)

        print("Device information:")
        print(json.dumps(response, indent=2))

        print()
        print("Commands:")
        print("  on     Turn plug ON")
        print("  off    Turn plug OFF")
        print("  state  Get current state")
        print("  info   Get device information")
        print("  q      Quit")

        while True:

            command = input("\nCommand: ").strip().lower()

            if command == "q":
                break

            elif command == "on":

                request = json.dumps(
                    {
                        "system": {
                            "set_relay_state": {
                                "state": 1
                            }
                        }
                    },
                    separators=(",", ":"),
                )

                response = await transport.send(request)

                print()
                print("ON response:")
                print(json.dumps(response, indent=2))

            elif command == "off":

                request = json.dumps(
                    {
                        "system": {
                            "set_relay_state": {
                                "state": 0
                            }
                        }
                    },
                    separators=(",", ":"),
                )

                response = await transport.send(request)

                print()
                print("OFF response:")
                print(json.dumps(response, indent=2))

            elif command == "state":

                request = json.dumps(
                    {
                        "system": {
                            "get_sysinfo": {}
                        }
                    },
                    separators=(",", ":"),
                )

                response = await transport.send(request)

                print()
                print("State response:")
                print(json.dumps(response, indent=2))

            elif command == "info":

                request = json.dumps(
                    {
                        "system": {
                            "get_sysinfo": {}
                        }
                    },
                    separators=(",", ":"),
                )

                response = await transport.send(request)

                print()
                print("Device information:")
                print(json.dumps(response, indent=2))

            else:

                print(
                    "Invalid command. "
                    "Enter on, off, state, info, or q."
                )

    except Exception as e:

        print()
        print("ERROR:")
        print(type(e).__name__)
        print(str(e))

    finally:

        await transport.close()

        print()
        print("Connection closed.")


if __name__ == "__main__":
    asyncio.run(main())

