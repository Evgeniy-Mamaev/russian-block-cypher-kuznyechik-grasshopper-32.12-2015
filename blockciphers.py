from kuznyechiktransformations import encrypt, decrypt

"""
General note: digital indexes can be used either for pointing an index in an array 
or for showing upper (power) or lower literal index.
"""


def ecb2(iterative_keys, message):
    """
    Electronic code book encryption method. Sequentially apply encrypt()
    for all the blocks.
    :param iterative_keys: expanded keys,
    :param message: message consists of blocks.
    """
    for i in range(len(message)):
        message[i] = encrypt(iterative_keys, message[i])
    return message


def ecb2_reversed(iterative_keys, cipher):
    """
    Electronic code book decryption method. Sequentially apply decrypt()
    for all the blocks.
    :param iterative_keys: expanded keys,
    :param cipher: cipher consists of blocks.
    """
    for i in range(len(cipher)):
        cipher[i] = decrypt(iterative_keys, cipher[i])
    return cipher
