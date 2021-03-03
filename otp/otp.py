import codecs
import Crypto.Random

def xorstrings(text1, text2):
    enc = bytes([a^b for (a,b) in zip(text1,text2)])
    return codecs.encode(enc,'hex').decode()

def check_xor():
    string = 'Darlin dont you go'.encode()
    string2 = 'and cut your hair!'.encode()
    xord = xorstrings(string,string2)
    if xord != '250f164c0a1b54441601015259071449154e':
        print("Incorrect XOR")
    else:
        print("XOR IS WORKING PROPERLY")

def otp():
    with open('mustang.bmp','rb') as file:
        image_byte = file.read()
    header = bytes(image_byte[:54])
    image_byte = bytes(image_byte[54:])

    key = Crypto.Random.get_random_bytes(len(image_byte))

    mustang_cipher = codecs.decode(xorstrings(image_byte,key),"hex")
    image_cipher = header + mustang_cipher
    f = open("mustang_cipher.bmp", "wb")
    f.write(image_cipher)
    f.close


    with open('cp-logo.bmp','rb') as file:
        image_byte = file.read()
    header = bytes(image_byte[:54])
    image_byte = bytes(image_byte[54:])
    logo_cipher = codecs.decode(xorstrings(image_byte,key),"hex")
    image_cipher = header + logo_cipher
    f = open("cp-logo_cipher.bmp", "wb")
    f.write(image_cipher)
    f.close

    both_cipher = codecs.decode(xorstrings(mustang_cipher,logo_cipher),"hex")
    image_cipher = header + both_cipher
    f = open("both-cp.bmp", "wb")
    f.write(image_cipher)
    f.close
    
otp()