from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"])


def generate_password_hash(password: str) -> str:
    password_hash = password_context.hash(password)

    return password_hash


def verify_password(password: str, hash: str) -> bool:
    return password_context.verify(password, hash)
