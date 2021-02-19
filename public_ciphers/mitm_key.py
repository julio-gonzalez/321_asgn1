from Crypto.Util.number import getPrime
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
def diffie_hellman():
    #Alice sends:
    p = 29703
    g = 6441

    #Alice
    a = getPrime(10)
    a_A = pow(g,a,p)
    #MITM ATTACK Mallory
    g = p-1
    m = getPrime(10)
    #Bob
    b = getPrime(10)
    b_B = pow(g,b,p)

    #Mallory
    m_s = p-1
    #Bob
    b_s = pow(a_A,b,p)
    #Alice
    a_s = pow(b_B,a,p)

    print("Alice secret:",a_s)
    print("Bob secret:",b_s)
    print("Mallo secret:",m_s)

    #Alice encrypts
    k_a = SHA256.new()
    k_a.update(bytes(a_s))
    a_iv = k_a.digest()[16:32]
    a_message = "Hi Bob!".encode()
    a_aes = AES.new(k_a.digest()[:16],AES.MODE_CBC,IV=a_iv)
    c0 = a_aes.encrypt(pad(a_message, AES.block_size))

    k_m = SHA256.new()
    k_m.update(bytes(m_s))
    m_iv = k_m.digest()[16:32]
    m_aes = AES.new(k_m.digest()[:16],AES.MODE_CBC,IV=m_iv)

    #Bob encrypts
    k_b = SHA256.new()
    k_b.update(bytes(b_s))
    b_iv = k_b.digest()[16:32]
    b_message = "Hi Alice!"
    b_aes = AES.new(k_b.digest()[:16],AES.MODE_CBC,IV=b_iv)
    c1 = b_aes.encrypt(pad(b_message.encode(), AES.block_size))

    #Decode their messages
    m_read = unpad(m_aes.decrypt(c0), block_size=AES.block_size)
    print("Mallory got:",m_read)
    m_read = unpad(m_aes.decrypt(c1), block_size=AES.block_size)
    print("Mallory got:",m_read)
    a_aes = AES.new(k_a.digest()[:16],AES.MODE_CBC,a_iv)
    a_reads = unpad(a_aes.decrypt(c1),block_size=AES.block_size)
    print("Alice got:",a_reads)

    b_aes = AES.new(k_b.digest()[:16],AES.MODE_CBC,b_iv)
    b_reads = unpad(b_aes.decrypt(c0), block_size=AES.block_size)
    print("Bob got:",b_reads)


diffie_hellman()