import bcrypt
def hash_password(plain_password: str) -> str:
    hashed = bcrypt.hashpw(
        plain_password.encode("utf-8"),
        bcrypt.gensalt()
    )
    print(hashed.decode("utf-8"))

hash_password("root")