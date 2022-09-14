from enum import Enum
import re
from signal import signal

from cryptographyUtils import Cryptography

class Message:
    def __init__(self, content="", type=None, param="",raw=""):
        self.content = content
        self.type = type
        self.param = param
        self.signature = ""
        self.public = ""
        self.raw = raw

    def mount(self):
        type = MessageDividers.OPEN_TYPE + str(self.type.value) + MessageDividers.CLOSE_TYPE
        param = MessageDividers.OPEN_PARAM + self.param + MessageDividers.CLOSE_PARAM
        content = MessageDividers.OPEN_CONTENT + self.content + MessageDividers.CLOSE_CONTENT
        signature = MessageDividers.OPEN_SIGN + self.signature + MessageDividers.CLOSE_SIGN
        public = MessageDividers.OPEN_PUBLIC + self.public + MessageDividers.CLOSE_PUBLIC
        return type + param + content + signature + public
    
    def unmount(self):
        try:
            self.content = re.search(MessageDividers.OPEN_CONTENT + "([\s\S]*?)" + MessageDividers.CLOSE_CONTENT, self.raw).group(0)[1:-1]
            self.type = MessageType(int(re.search("\\" + MessageDividers.OPEN_TYPE + "([\s\S]*?)" + "\\" + MessageDividers.CLOSE_TYPE, self.raw).group(0)[1:-1]))
            self.param = re.search("\\" + MessageDividers.OPEN_PARAM   + "([\s\S]*?)" + "\\" + MessageDividers.CLOSE_PARAM,   self.raw).group(0)[1:-1]
            self.signature = bytes.fromhex(re.search("\\" + MessageDividers.OPEN_SIGN   + "([\s\S]*?)" + "\\" + MessageDividers.CLOSE_SIGN,   self.raw).group(0)[1:-1])
            self.public = bytes.fromhex(re.search("\\" + MessageDividers.OPEN_PUBLIC   + "([\s\S]*?)" + "\\" + MessageDividers.CLOSE_PUBLIC,   self.raw).group(0)[1:-1])
            return True
        except:
            return False
    
    def sign(self, privatekey):
        self.signature = Cryptography.sign_message(self.content.encode(), privatekey).hex()
        self.public = Cryptography.serialize_publickey(privatekey.public_key()).hex()
        

class MessageType(Enum):
    SIMPLE = 0
    FIRST  = 1
    AUTHORIZED = 2
    SYMMETRICAL = 3
    PUBLIC_KEY = 4
    REQUEST_AUTH = 5

class MessageDividers:
    OPEN_TYPE     = "("
    CLOSE_TYPE    = ")"
    OPEN_CONTENT  = "<"
    CLOSE_CONTENT = ">"
    OPEN_PARAM    = "["
    CLOSE_PARAM   = "]"
    OPEN_SIGN     = "{"
    CLOSE_SIGN    = "}"
    OPEN_PUBLIC   = "*"
    CLOSE_PUBLIC  = "*"
