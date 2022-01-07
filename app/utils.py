from passlib.context import CryptContext

#todo BCRYPT STUFF
# telling passlib what is the hashing algorithm we chose. 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#utliity function that grabs the passed in password and returns the hash
def hash(password: str):
    return pwd_context.hash(password)


#this will compare the given password with the hased password in database, to determine if they match.
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)