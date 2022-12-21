import random
import string
import hashlib
from app.core.config import settings


async def generate_password(length=20):
    return "".join(random.sample(string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation, length))


async def password_hash(password):
    return hashlib.sha256((password+settings.HASH_SALT).encode()).hexdigest()

class Password():
    def __init__(self):
        self.password = ""
    
    def generate(self, length=20):
        self.password = "".join(random.sample(string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation, length))
    
    @property
    def hash(self):
        return hashlib.sha256((self.password+settings.HASH_SALT).encode()).hexdigest()
    
    @property
    def hex(self):
        return self.password
    