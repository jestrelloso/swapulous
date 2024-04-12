from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Hashing using passlib with bcrypt algorithm
class Hash:
    def bcrypt(password: str):
        return pwd_cxt.hash(password)

    def verify(hashed_password, plain_password):
        status = pwd_cxt.verify(plain_password, hashed_password)
        return pwd_cxt.verify(plain_password, hashed_password)
