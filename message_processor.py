from email import message
from winsound import PlaySound
from cryptographyUtils import Cryptography
from message import Message, MessageType
from cryptography.fernet import Fernet
import binascii

class MessageProcessor:
    def __init__(self, socket):
        self.socket = socket
        self.private_key = Cryptography.generate_privatekey()
        self.public_key = self.private_key.public_key()
        self.symmetric_key = Fernet.generate_key()
        self.authenticated = False
        self.not_auth_types = [MessageType.FIRST]

        self.request_auth()
    
    def send_simple_message(self, content):
        if(self.authenticated == False):
            return ""

        ciphertext = Cryptography.encript_symmetric(content.encode(), self.symmetric_key)
        message = Message(ciphertext.decode(), MessageType.SIMPLE)
        message.sign(self.private_key)
        self.socket.send(message.mount().encode())

    def process(self, message):
        message_type = message.type

        if(message_type not in self.not_auth_types):
            valid_signature = Cryptography.verify_message(message.content.encode(), message.signature, Cryptography.deserialize_publickey(message.public))
            if(valid_signature == False):
                print("Invalid Signature")
                return

        match message_type:
            case MessageType.SIMPLE:
                self.process_simple(message)
            case MessageType.PUBLIC_KEY:
                self.process_publickey(message)
            case MessageType.SYMMETRICAL:
                self.process_symmetrical(message)
            case MessageType.FIRST:
                self.authenticated = True
            
    
    def process_simple(self, message):
        plaintext = Cryptography.decript_symmetric(message.content.encode(), self.symmetric_key).decode()
        print(plaintext)
    
    def request_auth(self):
        message = Message(content="a",type=MessageType.PUBLIC_KEY)
        message.sign(self.private_key)
        self.socket.send(message.mount().encode())

    def process_publickey(self, message):
        publickey = Cryptography.deserialize_publickey(message.public)
        ciphertext = Cryptography.encrypt_asymmetric(self.symmetric_key, publickey)
        message = Message(ciphertext.hex(), MessageType.SYMMETRICAL)
        message.sign(self.private_key)
        self.socket.send(message.mount().encode())
    
    def process_symmetrical(self, message):
        if(self.authenticated == True):
            return
        ciphertext = bytes.fromhex(message.content)
        self.symmetric_key = Cryptography.decrypt_asymmetric(ciphertext, self.private_key)
        self.authenticated = True

