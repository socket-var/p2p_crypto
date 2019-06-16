# TODO: remove defaults
def diffie_hellman(private_key, public_modulus=23, public_base=5):

    encrypted_key = public_base ** int(private_key) % public_modulus

    return public_modulus, public_base, encrypted_key


# TODO: make_key
