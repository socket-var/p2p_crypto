import os
import pickle
# TODO: make this reusable
from p2p_module.config import dest_server_host, dest_server_port, dest_client_host, dest_client_port, self_client_host, self_client_port, owner_key_file_name, receiver_key_file_name, encryption_file_name, decryption_file_name
from p2p_module.crypto_utils import *

def get_url(host, port):
    return "{}:{}".format(host, port)

def start_kx():

    private_key = int(input("Enter private key for Diffie-Hellman: "))
    public_modulus = int(input("Enter the public modulus: "))
    public_base = int(input("Enter the public base: "))

    # destination client to receive the secret

    encrypted_key = diffie_hellman(private_key, public_modulus, public_base)

    print(
        "sender: sending encrypted key to {} using {!r} {!r} {!r} {!r}".format(
            get_url(dest_client_host, dest_client_port), "start-kx", public_modulus, public_base, encrypted_key
        )
    )

    data = {
        "from_address": get_url(self_client_host, self_client_port),
        "to_address": get_url(dest_client_host, dest_client_port),
        "command": "start-kx",
        "public_modulus": public_modulus,
        "public_base": public_base,
        "encrypted_key": encrypted_key
    }

    with open(owner_key_file_name, "wb") as write_obj:
        pickle.dump(data, write_obj)


    return pickle.dumps(data)

def reply_kx():
    
    data = {}
    with open(receiver_key_file_name, 'rb') as pickle_file:
        data = pickle.load(pickle_file)
    
    public_modulus, public_base = data["public_modulus"], data["public_base"]
    
    dest_address = data["from_address"]
    src_address = data["to_address"]

    private_key = int(input("Enter private key for Diffie-Hellman: "))


    # destination client to receive the secret
    encrypted_key = diffie_hellman(private_key, public_modulus, public_base)

    print(
        "sender: sending encrypted key to {} using {!r} {!r} {!r} {!r}".format(
            dest_address, "reply-kx", public_modulus, public_base, encrypted_key
        )
    )

    data = {
        "from_address": src_address,
        "to_address": dest_address,
        "command": "reply-kx",
        "public_modulus": public_modulus,
        "public_base": public_base,
        "encrypted_key": encrypted_key
    }

    return pickle.dumps(data)


def caesar_encrypt():
    my_message = input("Enter the message to encrypt and send: ")
    private_key = int(input("Enter your private key:"))
    filename = input("Enter the file name containing encrypted key:")
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    with open(filename, 'rb') as pickle_file:
        data = pickle.load(pickle_file)    

    print(data)
    # private_key * cipher_key
    key = ((data["encrypted_key"] ** private_key) % data["public_modulus"]) % 26
    
    new_key = shift_alphabet(alphabet, key)
    print(new_key)

    encrypted_text = encrypt_caesar(my_message, new_key)

    result = {
        "from_address": get_url(self_client_host, self_client_port), 
        "to_address": get_url(dest_client_host, dest_client_port), 
        "command": "caesar-encrypt", 
        "encrypted_text": encrypted_text
    }
    print(result)
    print("Sending encrypted text: {}.....".format(encrypted_text))
    return pickle.dumps(result)

def caesar_decrypt():
    private_key = int(input("Enter your private key:"))
    key_filename = input("Enter the file name containing encrypted key: ")

    encrypted_text = ""
    # read encrypted text
    with open(encryption_file_name, 'rb') as encrypt_file_obj:
        data = pickle.load(encrypt_file_obj)
        encrypted_text = data["encrypted_text"]
    
    # form new_key

    new_key = ""
    
    with open(key_filename, 'rb') as key_file_obj:
        new_key = pickle.load(key_file_obj)
    
    print(new_key)


    # private_key * encrypted_key
    key = (new_key["encrypted_key"] ** private_key) % data["public_modulus"]
    key = -key
    print(key)
    
    new_key = shift_alphabet(alphabet, key)
    print(new_key)
    
    # decrypt it
    decrypted_text = decrypt_caesar(encrypted_text, new_key)
    print(decrypted_text)

    with open(decryption_file_name, 'wb') as decrypt_file_obj:
        pickle.dump(decrypted_text, decrypt_file_obj)
