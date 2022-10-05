import typing as tp

def new_char(c : str, shift: int) -> str:
    if c.isupper():
        l = ord('A')
        r = ord('Z')
    else:
        l = ord('a')
        r = ord('z')

    if l <= ord(c) + shift <= r:
        return chr(ord(c) + shift)
    elif shift > 0:
        return chr(l + (ord(c) + shift - r) - 1)
    else:
        return chr(r - (l - (ord(c) + shift)) + 1)

def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""

    for i in plaintext:
        if i.isalpha():

            ciphertext += new_char(i, shift)
        else:
            ciphertext += i

    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = encrypt_caesar(ciphertext, -shift)
    return plaintext
