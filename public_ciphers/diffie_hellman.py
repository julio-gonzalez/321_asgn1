from Crypto.Util.number import getPrime
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
def diffie_hellman():
    p = 2970324886
    g = 644868638
    
    #Alice
    a = getPrime(10)
    a_A = pow(g,a,p)
    #Bob
    b = getPrime(10)
    b_B = pow(g,b,p)

    a_s = pow(b_B,a,p)
    b_s = pow(a_A,b,p)

    print("Alice secret:",a_s)
    print("Bob secret:",b_s)

    k_a = SHA256.new()
    k_a.update(bytes(a_s))
    a_iv = k_a.digest()[16:32]
    a_message = "Hi Bob!".encode()
    a_aes = AES.new(k_a.digest()[:16],AES.MODE_CBC,IV=a_iv)
    a_c = a_aes.encrypt(pad(a_message, AES.block_size))


    k_b = SHA256.new()
    k_b.update(bytes(b_s))
    b_iv = k_b.digest()[16:32]
    b_message = "Hi Alice!"
    b_aes = AES.new(k_b.digest()[:16],AES.MODE_CBC,IV=b_iv)
    b_c = b_aes.encrypt(pad(b_message.encode(), AES.block_size))

    #Decode their messages
    a_aes = AES.new(k_a.digest()[:16],AES.MODE_CBC,a_iv)
    a_reads = unpad(a_aes.decrypt(b_c),block_size=AES.block_size)
    print("Alice got:",a_reads)

    b_aes = AES.new(k_b.digest()[:16],AES.MODE_CBC,b_iv)
    b_reads = unpad(b_aes.decrypt(a_c), block_size=AES.block_size)
    print("Bob got:",b_reads)



diffie_hellman()