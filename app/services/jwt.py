from jose import JWTError, jwt
import os
from dotenv import load_dotenv
from passlib.hash import pbkdf2_sha256
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends
from typing import Annotated

load_dotenv()
security = HTTPBearer()

jwt_key = os.getenv('JWT_SECRET_KEY')
jwt_algorithm = os.getenv('JWT_ALGORITHM')


def encodeToken(email, role):
    """
    Generate JWT token using passed parameters
    
    :param email: user email address
    :param role: user role in the system [lister, viwer, admin]
    """
    try:
        token = jwt.encode({'email': email,
                        'role': role}, jwt_key, algorithm=jwt_algorithm)
        return token
    except Exception as e:
        return 'error in token generation'
        
def decodeToken(token):
    """
    decode JWT token and return the data
    
    :param token: JWT token that pass by user
    """
    try:
        data = jwt.decode(token, jwt_key, algorithms=[jwt_algorithm])
        return data
    except JWTError:
        return False

def encodePassword(plainPassword):
    """
    encode plain password to encripted password that pass by user
    
    :param plainPassword: user plain password
    """
    try:
        encriptPassword = pbkdf2_sha256.hash(plainPassword)
        return encriptPassword
    except Exception as e:
        return 'error in password encryption'

# decode password
def decodePasword(palinPassword, encriptPassword):
    """
    decode encrypted password and compare with plain passwords
    
    :param palinPassword: user plain password
    :param encriptPassword: user encrypted password that get from db
    """
    try:
        decriptedPassword = pbkdf2_sha256.verify(palinPassword, encriptPassword)
        return decriptedPassword
    except Exception as e:
        return 'error in password decryption'
    
# deal with barer token
def authVerification(details: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    """
    verify the barer token and decode the token data
    
    :param details: HTTP authorization credentials
    """
    return decodeToken(details.credentials)