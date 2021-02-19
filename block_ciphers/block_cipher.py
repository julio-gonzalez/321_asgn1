from Crypto.Cipher import AES
from pkcs_padding import pad, unpad
import base64
import codecs
import secrets
block_size = AES.block_size
def ecb_encrypt(key, plaintext):
    key_b = key
    padded_message = pad(plaintext, block_size)
    aes = AES.new(key_b, AES.MODE_ECB, b'0')
    blocks = int(len(padded_message) / block_size)
    ciphertext = b''
    for i in range(blocks):
        start = i * block_size
        end = start + block_size
        block = padded_message[start:end]
        c_block = aes.encrypt(block)
        ciphertext += c_block
    return ciphertext

def bxor(b1, b2):
    parts = []
    for b1, b2 in zip(b1, b2):
        parts.append(bytes([b1 ^ b2]))
    return b''.join(parts)

def cbc_encrypt(plaintext, key, IV):
    key_b = key
    iv_b = IV
    padded_message = pad(plaintext, block_size)
    aes = AES.new(key_b, AES.MODE_ECB, IV)
    blocks = int(len(padded_message) / block_size)
    ciphertext = b''
    c_block = b''
    for i in range(blocks):
        start = i * block_size
        end = start + block_size
        block = padded_message[start:end]
        if i == 0:
            block = bxor(block, iv_b)
        else:
            block = bxor(block, c_block)
        c_block = aes.encrypt(block)
        ciphertext += c_block
    return ciphertext

def cbc_decrypt(ciphertext, key, IV):
    key_b = key
    iv_b = IV
    aes = AES.new(key_b, AES.MODE_ECB, b'0')
    
    blocks = int(len(ciphertext) / block_size)
    plaintext = b''
    prev_block = None
    for i in range(blocks):
        start = i * block_size
        end = start + block_size
        block = ciphertext[start:end]
        message_byte = aes.decrypt(block)
        if i == 0:
            pt_block = bxor(message_byte, iv_b)
            prev_block = block
        else:
            pt_block = bxor(message_byte, prev_block)
            prev_block = block
        plaintext += pt_block
    
    plaintext = unpad(plaintext)
    if plaintext == None:
        print("Error")  
        return None
    return plaintext

def call_aes():
    random_iv = secrets.token_bytes(block_size)
    key = 'California love!'.encode()
    with open("cp-logo.bmp", "rb") as f:
        image_byte = bytearray(f.read())
    
    header = bytes(image_byte[:14])
    image_byte = bytes(image_byte[14:])
    ecb_image_cipher = ecb_encrypt(key,image_byte)
    cbc_image_cipher = cbc_encrypt(image_byte,key,random_iv)

    ecb_to_write = header + ecb_image_cipher
    f = open("ecb_bytes.txt", "wb")
    f.write(ecb_to_write)
    f.close

    cbc_to_write = header + cbc_image_cipher
    f = open("cbc_bytes.txt", "wb")
    f.write(cbc_to_write)
    f.close

call_aes()