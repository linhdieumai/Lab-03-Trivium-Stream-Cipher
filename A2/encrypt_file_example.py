"""
Task A2 --- encrypt and decrypt a file with Trivium.


Trivium is a stream cipher: to encrypt, XOR the data with the key stream; to
decrypt, XOR again with the SAME key stream. Because one key must never be
reused with the same IV, generate a fresh random IV for every file and store
it at the front of the ciphertext.


Usage (once you finish the TODOs):
    python3 encrypt_file.py enc KEYHEX  plain.txt  cipher.bin
    python3 encrypt_file.py dec KEYHEX  cipher.bin recovered.txt
KEYHEX is 20 hex chars (80-bit key), e.g. 00112233445566778899.


Check yourself: enc then dec must give back a file identical to the original.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'A1'))
from trivium import keystream


IV_LEN = 10   # 80-bit IV, stored as the first 10 bytes of the ciphertext


def encrypt_file(key: bytes, infile: str, outfile: str):
    with open(infile, 'rb') as source:
        data = source.read()
    iv = b'\x00' * IV_LEN  # use same iv with the same key
    ks = keystream(key, iv, len(data))
    cipher = bytes(data_byte ^ key_byte for data_byte, key_byte in zip(data, ks))
    with open(outfile, 'wb') as destination:
        destination.write(iv + cipher)


def decrypt_file(key: bytes, infile: str, outfile: str):
    with open(infile, 'rb') as source:
        blob = source.read()
    if len(blob) < IV_LEN:
        raise ValueError(f"ciphertext must contain at least {IV_LEN} IV bytes")
    iv, cipher = blob[:IV_LEN], blob[IV_LEN:]
    #   2. ks = keystream(key, iv, len(cipher))
    ks = keystream(key, iv, len(cipher))
    #   3. plain = XOR of cipher and ks
    plain = bytes(cipher_byte ^ key_byte for cipher_byte, key_byte in zip(cipher, ks))
    #   4. write plain to outfile
    with open(outfile, 'wb') as destination:
        destination.write(plain)


if __name__ == '__main__':
    mode, keyhex, infile, outfile = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    if mode not in ('enc', 'dec'):
        raise SystemExit("mode must be 'enc' or 'dec'")
    try:
        key = bytes.fromhex(keyhex)
    except ValueError as error:
        raise SystemExit("key must contain exactly 20 hexadecimal characters") from error
    if len(key) != 10 or len(keyhex) != 20:
        raise SystemExit("key must contain exactly 20 hexadecimal characters")
    (encrypt_file if mode == 'enc' else decrypt_file)(key, infile, outfile)
    print(f"{mode}: wrote {outfile}")