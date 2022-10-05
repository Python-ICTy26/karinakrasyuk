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


def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    key = keyword
    while len(key) < len(plaintext):
        key += keyword

    for i in range(0, len(plaintext)):

        if key[i].isupper():
            shift = ord(key[i]) - ord('A')
        else:
            shift = ord(key[i]) - ord('a')

        ciphertext += new_char(plaintext[i], shift)

    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    key = keyword
    while len(key) < len(ciphertext):
        key += keyword

    for i in range(0, len(ciphertext)):


        if key[i].isupper():
            shift = ord(key[i]) - ord('A')
        else:
            shift = ord(key[i]) - ord('a')

        plaintext += new_char(ciphertext[i], -shift)

    return plaintext
