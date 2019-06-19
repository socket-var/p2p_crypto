alphabet = "abcdefghijklmnopqrstuvwxyz"


def diffie_hellman(private_key, public_modulus, public_base):

    encrypted_key = public_base ** int(private_key) % public_modulus

    return encrypted_key


def shift_alphabet(alphabet, key):
    new_alphabet = ""
    partial_one = ""
    partial_two = ""
    
    if key == 0:
        new_alphabet = alphabet
    elif key > 0:
        partial_one = alphabet[:key]
        partial_two = alphabet[key:]
        new_alphabet = partial_two + partial_one
    else:
        partial_one = alphabet[:(26 + key)]
        partial_two = alphabet[(26 + key):]
        new_alphabet = partial_two + partial_one

    return new_alphabet


def encrypt_caesar(my_message, new_key):
    cipher_text = ""
    for i in range(len(my_message)):
        index = alphabet.find(my_message[i])
        if index < 0:
            cipher_text += my_message[i]
        else:
            cipher_text += new_key[index]

    return cipher_text


def decrypt_caesar(my_message, new_key):
    cipher_text = ""
    for i in range(len(my_message)):
        index = alphabet.find(my_message[i])
        if index < 0:
            cipher_text += my_message[i]
        else:
            cipher_text += new_key[index]

    return cipher_text