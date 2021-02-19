"""
Choose two large primes 𝑝 and 𝑞. 
Let 𝑛=𝑝⋅𝑞. 
Choose 𝑒 such that 𝑔𝑐𝑑(𝑒,𝜑(𝑛))=1 (where 𝜑(𝑛)=(𝑝−1)⋅(𝑞−1)). 
Find 𝑑 such that 𝑒⋅𝑑≡1mod𝜑(𝑛). 
In other words, 𝑑 is the modular inverse of 𝑒, (𝑑≡𝑒−1mod𝜑(𝑛)).
"""
from Crypto.Util.number import getPrime
from Crypto.Random.random import randrange
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import codecs
class textbook_rsa():
    key_log = {}
    def key_gen(self, length):
        e = 65537
        sub = 5
        if length < sub:
            sub = -5
        p = getPrime(length)
        q = getPrime(length-sub)

        n = p * q
        alpha_n = (p-1) * (q-1)
        d = pow(e,-1,alpha_n)
        self.key_log[(e,n)] = (d,n)
        return (e,n)
    
    """
    RSA En/decryption
    • to encrypt a message M the sender:
    • obtains public key of recipient PU={e,n}
    • computes: C = M**e mod n, where 0≤M<n
    """
    def encrypt(self, M, pk):
        e = pk[0]
        n = pk[1]
        C = pow(M,e,n)
        return C
    """
    • to decrypt the ciphertext C the owner:
    • uses their private key PR={d,n}
    • computes: M = C**d mod n
    • note that the message
    """
    def decrypt(self, C, pk):
        pr_k = None
        try:
            pr_k = self.key_log[pk]
        except:
            pr_k = None
        
        if pr_k == None:
            print("Could not decrypt C")
            return None
        else:
            d = pk[0]
            n = pk[1]
            M = pow(C,d,n)
        return M

def test_rsa():
    t_rsa = textbook_rsa()
    my_pk = t_rsa.key_gen(256)
    m = 721011081081113211610410511532105115329732116101115116 #Hello this is a test
    print("Message:", m)
    c = t_rsa.encrypt(m, my_pk)
    c_d = t_rsa.decrypt(c, my_pk)
    if m == c_d:
        print("Decrypted:", c_d)
    else:
        print("RSA NOT WORKING")

#c’ = F(c)
def F(c,e,n):
    return pow(2,e,n)

def malleability_test():
    t_rsa = textbook_rsa()
    alice_pk = t_rsa.key_gen(16)
    #Alice sends (e,n) public key
    e = alice_pk[0]
    n = alice_pk[1]
    
    #Bob computes
    bob_s = randrange(n)
    c = pow(bob_s,e,n)#Bob sends c

    #Mallory c' = F(c)
    c_prime = F(c,e,n)
    
    #Alice
    d = t_rsa.key_log[alice_pk][0]
    a_s = pow(c_prime,d,n)
    
    k = SHA256.new()
    k.update(bytes(a_s))
    a_iv = k.digest()[16:32]
    a_message = "Hi Bob!".encode()
    a_aes = AES.new(k.digest()[:16],AES.MODE_CBC,IV=a_iv)
    c0 = a_aes.encrypt(pad(a_message, AES.block_size))
    #Alice sends c0

    #Mallory
    m_s = 2
    k_m = SHA256.new()
    k_m.update(bytes(m_s))
    m_iv = k_m.digest()[16:32]
    m_aes = AES.new(k_m.digest()[:16],AES.MODE_CBC,IV=m_iv)
    mess = unpad(m_aes.decrypt(c0), block_size=AES.block_size)
    print("Mallory got:",mess)

malleability_test()