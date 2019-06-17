# import sys
import os
import trio
import pickle
from crypto_utils.helpers import *
from dotenv import load_dotenv

load_dotenv()

dest_server_host = os.getenv(
    "DESTINATION_SERVER_ADDRESS")

dest_server_port = int(os.getenv(
    "DESTINATION_SERVER_PORT"))

dest_client_host = os.getenv(
    "DESTINATION_SERVER_ADDRESS")

dest_client_port = int(os.getenv(
    "DESTINATION_SERVER_PORT"))


self_client_host = os.getenv(
    "DESTINATION_SERVER_ADDRESS")

self_client_port = int(os.getenv(
    "DESTINATION_SERVER_PORT"))

sender_key_file_name = os.getenv(
    "SENDER_KEY_FILE_NAME")

receiver_key_file_name = os.getenv(
    "RECEIVER_KEY_FILE_NAME")

server_id = "{}:{}".format(dest_server_host, dest_server_port)

BUFSIZE = 16384

state = {}

# perform diffie hellman


async def start_kx(client_stream, command):

    private_key = int(input("Enter private key for Diffie-Hellman: "))
    public_modulus = int(input("Enter the public modulus: "))
    public_base = int(input("Enter the public base: "))
    dest_address = input("Enter the destination address (Eg: 'localhost:5000'): ")

    # destination client to receive the secret

    encrypted_key = diffie_hellman(private_key, public_modulus, public_base)

    print(
        "sender: sending encrypted key to {} using {!r} {!r} {!r} {!r}".format(
            dest_address, command, public_modulus, public_base, encrypted_key
        )
    )

    data = (dest_address, command,
            public_modulus, public_base, encrypted_key)

    with open(sender_key_file_name, "wb") as write_obj:
        pickle.dump(data, write_obj)


    return await client_stream.send_all(pickle.dumps(data))

async def reply_kx(client_stream, command):
    
    data = ()
    with open(receiver_key_file_name, 'rb') as pickle_file:
        data = pickle.load(pickle_file)
    
    (_, command,
            public_modulus, public_base, _) = data

    private_key = int(input("Enter private key for Diffie-Hellman: "))
    dest_address = input("Enter the destination address (Eg: 'localhost:5000'): ")


    # destination client to receive the secret
    encrypted_key = diffie_hellman(private_key, public_modulus, public_base)

    print(
        "sender: sending encrypted key to {} using {!r} {!r} {!r} {!r}".format(
            dest_address, command, public_modulus, public_base, encrypted_key
        )
    )

    data = (dest_address, command,
            public_modulus, public_base, encrypted_key)

    return await client_stream.send_all(pickle.dumps(data))


async def sender(client_stream):
    print("sender started")
    while True:
        # user enters a command like "init-key" (key exchange)
        command = input(
            ">>> Enter your command: "
        ).strip()

        if command == "start-kx":
            # user wants to send g**a mod p or g**b mod p
            await start_kx(client_stream, command)
        elif command == "reply-kx":
            await reply_kx(client_stream, command)
            
        # refreshes the screen to show any updates
        elif command == "refresh":
            print("Refreshing...Please wait...")
            await trio.sleep(5)


async def receiver(client_stream):
    print("receiver: started!")
    while True:
        data = await client_stream.receive_some(BUFSIZE)

        print("receiver: got data {!r}".format(data))

        # if command == "start-kx" and dest_address == "{}:{}".format(self_client_host, self_client_port):
        #     with open(store_file_name, 'wb') as pickle_file:
        #         pickle.dump(data, pickle_file)
        # else:
        #     print("default")


async def parent():

    # Some useful instructions for the user
    print("Hi, sender!!\n"
        "Type 'start-kx' for sending your symmetric key using Diffie-Hellman \n"
        "Type 'reply-kx' for sending your symmetric key using Diffie-Hellman \n"
        "Type 'aes-encrypt' and enter for encryption \n"
        "Type 'aes-decrypt' and enter for decryption \n"
        "Type 'refresh' to refresh the page \n")

    print("Connecting to {}:{}".format(dest_server_host, dest_server_port))
    client_stream = await trio.open_tcp_stream(dest_server_host, dest_server_port)

    async with client_stream:
        async with trio.open_nursery() as nursery:
            # Sender async task will be started
            print("Spawning sender...")
            nursery.start_soon(sender, client_stream)

trio.run(parent)