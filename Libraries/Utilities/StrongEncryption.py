from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
from robot.api.deco import keyword, library


@library(doc_format='ROBOT')
class StrongEncryption:
    """
    A Robot Framework library for strong encryption and decryption using AES-256 GCM.
    """

    def __init__(self, key: str = None):
        """
        Initialize the encryption class with a 32-byte AES key.
        If no key is provided, a random one is generated.
        """
        if key:
            self.key = base64.urlsafe_b64decode(key)
        else:
            self.key = get_random_bytes(32)

    @keyword("Generate Encryption Key")
    def generate_encryption_key(self) -> str:
        """
        Generate a secure AES-256 key and return it as a base64-encoded string.
        """
        return base64.urlsafe_b64encode(self.key).decode('utf-8')

    @keyword("Encrypt Text")
    def encrypt_text(self, plaintext: str) -> str:
        """
        Encrypt the given text using AES-256 GCM and return the encrypted data as a base64-encoded string.
        """
        cipher = AES.new(self.key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode('utf-8'))
        return base64.urlsafe_b64encode(cipher.nonce + tag + ciphertext).decode('utf-8')

    @keyword("Decrypt Text")
    def decrypt_text(self, encrypted_text: str) -> str:
        """
        Decrypt the given base64-encoded text using AES-256 GCM and return the original plaintext.
        """
        encrypted_data = base64.urlsafe_b64decode(encrypted_text)
        nonce, tag, ciphertext = encrypted_data[:16], encrypted_data[16:32], encrypted_data[32:]
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=nonce)
        return cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')
