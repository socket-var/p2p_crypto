# import sys
import os
import trio
import pickle
from p2p_module.helpers import start_kx, reply_kx, caesar_encrypt, caesar_decrypt
from p2p_module.config import dest_server_host, dest_server_port, dest_client_host, dest_client_port, self_client_host, self_client_port, owner_key_file_name, receiver_key_file_name, decryption_file_name


# perform diffie hellman


async def sender(client_stream):
    print("sender started")
    while True:
        result = None
        # user enters a command like "init-key" (key exchange)
        command = input(
            ">>> Enter your command: "
        )

        if command == "start-kx":
            # user wants to send g**a mod p or g**b mod p
            result = start_kx()

        elif command == "reply-kx":
            result = reply_kx()

        elif command == "caesar-encrypt":
            result = caesar_encrypt()

        elif command == "caesar-decrypt":
            caesar_decrypt()

        # refreshes the screen to show any updates
        elif command == "refresh":
            print("Refreshing...Please wait...")
            await trio.sleep(5)

        if result:
            await client_stream.send_all(result)


async def parent():
    server_id = "{}:{}".format(dest_server_host, dest_server_port)

    # Some useful instructions for the user
    print("Hi, sender!!\n"
          "Type 'start-kx' for sending your symmetric key using Diffie-Hellman \n"
          "Type 'reply-kx' for sending your symmetric key using Diffie-Hellman \n"
          "Type 'caesar-encrypt' and enter for encryption \n"
          "Type 'caesar-decrypt' and enter for decryption \n"
          "Type 'refresh' to refresh the page \n")

    print("Connecting to {}".format(server_id))
    client_stream = await trio.open_tcp_stream(dest_server_host, dest_server_port)

    async with client_stream:
        async with trio.open_nursery() as nursery:
            # Sender async task will be started
            print("Spawning sender...")
            nursery.start_soon(sender, client_stream)

trio.run(parent)
