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
from trivium import keystream


IV_LEN = 10   # 80-bit IV, stored as the first 10 bytes of the ciphertext


def encrypt_file(key: bytes, infile: str, outfile: str):
    data = open(infile, 'rb').read()
    # TODO:
    #   1. iv = os.urandom(IV_LEN)         
    iv = os.urandom(IV_LEN)     # fresh random IV
    #   2. ks = keystream(key, iv, len(data))
    ks = keystream(key, iv, len(data))  # generate key stream
    #   3. cipher = XOR of data and ks
    cipher = bytes([data[i] ^ ks[i] for i in range(len(data))])
    #   4. write iv + cipher to outfile
    open(outfile, 'wb').write(iv + cipher)
    raise NotImplementedError("encrypt_file")


def decrypt_file(key: bytes, infile: str, outfile: str):
    blob = open(infile, 'rb').read()
    # TODO:
    #   1. split off the first IV_LEN bytes as iv, the rest is cipher
    iv, cipher = blob[:IV_LEN],blob[IV_LEN:]
    #   2. ks = keystream(key, iv, len(cipher))
    ks = keystream(key, iv, len(cipher))
    #   3. plain = XOR of cipher and ks
    plain = bytes([cipher[i] ^ ks[i] for i in range(len(cipher))])
    #   4. write plain to outfile
    open(outfile, 'wb').write(plain)
    raise NotImplementedError("decrypt_file")


if __name__ == '__main__':
    mode, keyhex, infile, outfile = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    key = bytes.fromhex(keyhex)
    assert len(key) == 10, "key must be 20 hex chars (80 bits)"
    (encrypt_file if mode == 'enc' else decrypt_file)(key, infile, outfile)
    print(f"{mode}: wrote {outfile}")