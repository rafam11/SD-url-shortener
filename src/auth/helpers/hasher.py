from pwdlib.hashers.bcrypt import BcryptHasher

hasher = BcryptHasher()


class Hasher:

    @staticmethod
    def get_password_hash(
        password: str
    ) -> str:
        return hasher.hash(password)
    
    @staticmethod
    def verify_password(
        plain_password: str,
        hashed_password: str
    ) -> bool:
        return hasher.verify(plain_password, hashed_password)