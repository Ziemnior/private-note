from Crypto.Cipher import AES


class Ciphering:
    @staticmethod
    def cipher_message(key, message):
        cipher = AES.new(key, AES.MODE_EAX)
        text, tag = cipher.encrypt_and_digest(message.encode())
        return [text, tag, cipher.nonce]

    @staticmethod
    def decipher_message(key, message):
        cipher = AES.new(key, AES.MODE_EAX, nonce=message[2])
        return cipher.decrypt(message[0]).decode('utf-8')
