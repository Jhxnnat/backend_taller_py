import hashlib

class PasswordUtils:
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Genera un hash SHA-256 en formato hexadecimal para una contraseña.
        """
        sha256 = hashlib.sha256()
        sha256.update(password.encode('utf-8'))
        return sha256.hexdigest()
