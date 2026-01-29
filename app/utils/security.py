from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Example usage
if __name__ == "__main__":
    raw_password = "mysecretpassword"

    hashed = hash_password(raw_password)

    print("Raw:", raw_password)
    print("Hashed:", hashed)
    print("Verified:", verify_password(raw_password, hashed))
