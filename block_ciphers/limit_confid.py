from Crypto.Cipher import AES
import secrets
from pkcs_padding import pad, unpad
import base64
import codecs
from block_cipher import cbc_encrypt, cbc_decrypt


class Oracle():
    key = secrets.token_bytes(AES.block_size)
    iv = secrets.token_bytes(AES.block_size)

    #takes in a user input
    #url encodes the input txt and appends to other strings and pads it
    #returns a ciphertext encrypted by AES mode CBC
    def submit(self,text):
        encoded_url = ""
        for ch in text:
            if ch == ';' or ch == '=':
                encode = '%' + str(hex(ord(ch)))[2:]
                encoded_url += encode
            else:
                encoded_url += ch
        text = encoded_url
        cookie = "userid=456;userdata=" + text + ";session-id=31337"
        padded_coockie = pad(cookie.encode(),AES.block_size)
        cipher = cbc_encrypt(padded_coockie, self.key, self.iv)
        
        return cipher
    
    #takes in a ciphertext that was encrypted by AES mode CBC
    #decrypts the ciphertext and checks for the b';admin=true;'
    #returns True if it finds it, False otherwise
    def verify(self,ciphertext):
        message = cbc_decrypt(ciphertext,self.key,self.iv)
        for ibyte,byte in enumerate(message):
            if byte == ord(';') and len(message) - ibyte > 12:
                if message[ibyte:ibyte+12] == b';admin=true;':
                    return True
        return False 

#takes in a ciphertext  
#modifies the ciphertext by flipping two bit in ciphertext for ';' before admin
#and '=' inbetween 'admin' and 'true'
#returns the modified ciphertext
def flip_bit(cipher):
    #userid=456;userd
    #ata=?admin?true;
    #session-id=31337
    cipher_array = bytearray(cipher)
    cipher_array[4] = cipher_array[4] ^ ord('?') ^ ord(';')
    cipher_array[10] = cipher_array[10] ^ ord('?') ^ ord('=')
    return bytes(cipher_array)

oracle = Oracle()
x = input("Please enter a string or 'x' to exit: ")
while x != 'x':
    cipher = oracle.submit(x)
    new_cipher = flip_bit(cipher)
    if oracle.verify(new_cipher):
        print("True")
        break
    else:
        print("False")
    x = input("Please enter a string or 'x' to exit: ")