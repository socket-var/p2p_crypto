import os
import pickle
# TODO: make this reusable
from p2p_module.config import dest_server_host, dest_server_port, dest_client_host, dest_client_port, self_client_host, self_client_port, owner_key_file_name, receiver_key_file_name, decryption_file_name
from p2p_module.crypto_utils import *

def start_kx():

    private_key = int(input("Enter private key for Diffie-Hellman: "))
    public_modulus = int(input("Enter the public modulus: "))
    public_base = int(input("Enter the public base: "))
    dest_address = input("Enter the destination address (Eg: 'localhost:5000'): ")

    # destination client to receive the secret

    encrypted_key = diffie_hellman(private_key, public_modulus, public_base)

    print(
        "sender: sending encrypted key to {} using {!r} {!r} {!r} {!r}".format(
            dest_address, "start-kx", public_modulus, public_base, encrypted_key
        )
    )

    data = (dest_address, "start-kx",
            public_modulus, public_base, encrypted_key)

    with open(owner_key_file_name, "wb") as write_obj:
        pickle.dump(data, write_obj)


    return pickle.dumps(data)

def reply_kx():
    
    data = ()
    with open(receiver_key_file_name, 'rb') as pickle_file:
        data = pickle.load(pickle_file)
    
    public_modulus, public_base = data[2], data[3]

    private_key = int(input("Enter private key for Diffie-Hellman: "))
    dest_address = input("Enter the destination address (Eg: 'localhost:5000'): ")


    # destination client to receive the secret
    encrypted_key = diffie_hellman(private_key, public_modulus, public_base)

    print(
        "sender: sending encrypted key to {} using {!r} {!r} {!r} {!r}".format(
            dest_address, "reply-kx", public_modulus, public_base, encrypted_key
        )
    )

    data = (dest_address, "reply-kx",
            public_modulus, public_base, encrypted_key)

    return pickle.dumps(data)


def caesar_encrypt():
    my_message = input("Enter the message to encrypt and send: ")
    private_key = int(input("Enter your private key:"))
    filename = input("Enter the file name containing encrypted key:")
    dest_address = input("Enter the destination address (Eg: 'localhost:5000'): ")
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    with open(filename, 'rb') as pickle_file:
        data = pickle.load(pickle_file)    

    print(data)
    # private_key * cipher_key
    key = (private_key * data[4]) % 26
    
    new_key = shift_alphabet(alphabet, key)
    print(new_key)

    encrypted_text = encrypt_caesar(my_message, new_key)

    result = (dest_address, "caesar-encrypt", encrypted_text)
    print("Sending encrypted text: {}.....".format(encrypted_text))
    return pickle.dumps(result)

def caesar_decrypt():
    private_key = int(input("Enter your private key:"))
    filename = input("Enter the file name containing encrypted text: ")
    key_filename = input("Enter the file name containing encrypted key: ")

    encrypted_text = ""
    # read encrypted text
    with open(filename, 'rb') as encrypt_file_obj:
        data = pickle.load(encrypt_file_obj)
        encrypted_text = data[2]
    
    # form new_key

    new_key = ""
    
    with open(key_filename, 'rb') as key_file_obj:
        new_key = pickle.load(key_file_obj)
    # TODO: remove hard-coding
    print(new_key)


    # private_key * encrypted_key
    key = -(private_key * new_key[4]) % 26
    
    new_key = shift_alphabet(alphabet, key)
    print(new_key)
    
    # decrypt it
    decrypted_text = decrypt_caesar(encrypted_text, new_key)
    print(decrypted_text)

    with open(decryption_file_name, 'wb') as decrypt_file_obj:
        pickle.dump(decrypted_text, decrypt_file_obj)
