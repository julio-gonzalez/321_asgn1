def pad(text, k):
    byte_text = text
    lth = len(byte_text)
    pad = (k - lth) % k

    pad_str = bytes(chr(pad),'ascii') * pad

    return byte_text + pad_str

def check_valid_pad(pad_bytes, pad):
    for b in pad_bytes:
        if b != pad:
            return False
    return True

def unpad(text):
    pad = int(text[-1])
    pad_bytes = text[len(text)-pad:]
    
    return text[:len(text)-pad]