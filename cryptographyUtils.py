from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from cryptography.exceptions import InvalidSignature
import binascii

class Cryptography:
    @staticmethod
    def generate_privatekey():
        return rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )

    @staticmethod
    def deserialize_publickey(key):
        return serialization.load_pem_public_key(key)
    
    @staticmethod
    def serialize_publickey(key):
        pem = key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return pem
        #return "".join(pem.decode().splitlines()).encode()
    
    @staticmethod
    def encrypt_asymmetric(plaintext, publickey):
        ciphertext = publickey.encrypt(
            plaintext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return ciphertext

    @staticmethod
    def decrypt_asymmetric(ciphertext, privatekey):
        plaintext = privatekey.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return plaintext

    @staticmethod
    def encript_symmetric(plaintext, key):
        f = Fernet(key)
        return f.encrypt(plaintext)

    @staticmethod
    def decript_symmetric(ciphertext, key):
        f = Fernet(key)
        return f.decrypt(ciphertext)
    
    @staticmethod
    def sign_message(message, privatekey):
        return privatekey.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
    
    @staticmethod
    def verify_message(message, signature, publickey):
        try:
            publickey.verify(
                signature,
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except InvalidSignature:
            return False





# pr = Cryptography.generate_privatekey()
# pu = pr.public_key()

# t = Cryptography.encrypt_asymmetric("TESTE".encode(), pu)

# s = Cryptography.serialize_publickey(pu)
# d = Cryptography.deserialize_publickey(s)

# print(binascii.hexlify(t).decode())