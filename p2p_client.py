# import sys
import os
import trio
import json
from crypto_utils.helpers import *
from dotenv import load_dotenv

load_dotenv()

dest_server_host = os.getenv(
    "DESTINATION_SERVER_ADDRESS")

dest_server_port = int(os.getenv(
    "DESTINATION_SERVER_PORT"))

# dest_client_host = os.getenv(
#     "DESTINATION_SERVER_ADDRESS")

# dest_client_port = int(os.getenv(
#     "DESTINATION_SERVER_PORT"))

store_file_name = os.getenv(
    "STORE_FILE_NAME")

server_id = "{}:{}".format(dest_server_host, dest_server_port)

BUFSIZE = 16384

state = {}

# perform diffie hellman


async def send_key(client_stream, options):

    (dest_address,
     command,
     private_key,
     public_modulus,
     public_base) = options

    # destination client to receive the secret

    encrypted_key = diffie_hellman(private_key, public_modulus, public_base)

    print(
        "sender: sending encrypted key to {} using {!r} {!r} {!r} {!r}".format(
            dest_address, command, public_modulus, public_base, encrypted_key
        )
    )

    data = (dest_address, command,
            public_modulus, public_base, encrypted_key)

    print(json.dumps(data))
    return await client_stream.send_all(json.dumps(data))


async def sender(client_stream):
    print("sender started")
    while True:
        # user enters a command like "init-key" (key exchange)
        command = input(
            ">>> Enter your command: "
        ).strip()

        if command == "key-exchange":

            private_key = int(input("Enter private key for Diffie-Hellman: "))
            public_modulus = int(input("Enter the public modulus: "))
            public_base = int(input("Enter the public base: "))
            dest_address = input(
                "Enter the destination address (Eg: 'localhost:5000'): ")

            options = (
                dest_address,
                command,
                private_key,
                public_modulus,
                public_base
            )

            # user wants to send g**a mod p or g**b mod p
            await send_key(client_stream, options)

        # refreshes the screen to show any updates
        elif command == "refresh":
            print("Refreshing...Please wait...")
            await trio.sleep(5)


async def receiver(client_stream):
    print("receiver: started!")
    while True:
        data = await client_stream.receive_some(BUFSIZE)
        print("receiver: got data {!r}".format(data))
        address = data[1]+":"+data[2]
        command = data[2]

        if command == "key-exchange" and address == dest_client_host+":"+dest_client_port:
            state[server_id] = {
                "public_modulus": data[1],
                "public_base": data[2],
                "cipher_key": data[3]
            }
            # TODO: call make_key function to make the key for encryption
        else:
            print("default")


async def parent():
    # TODO: check data types
    # 1. User enters some default parameters

    # 2. The entered key is stored in a file
    server_id = "{}:{}".format(dest_server_host, dest_server_port)

    # 3. Some useful instructions for the user
    print("Hi, sender!!\n"
          "Type 'key-exchange' for sending your symmetric key using Diffie-Hellman \n"
          "Type 'aes-encrypt' and enter for encryption \n"
          "Type 'aes-decrypt' and enter for decryption \n"
          "Type 'refresh' to refresh the page \n")

    print("Connecting to {}:{}".format(dest_server_host, dest_server_port))
    client_stream = await trio.open_tcp_stream(dest_server_host, dest_server_port)

    async with client_stream:
        async with trio.open_nursery() as nursery:
            # 4. Sender and receiver async tasks will be started
            print("Spawning sender...")
            nursery.start_soon(sender, client_stream)

            print("Spawning receiver...")
            nursery.start_soon(
                receiver, client_stream)


trio.run(parent)
