from hashlib import sha1
from datetime import datetime, time
def generateToken(email):
    timeStamp = datetime.now()
    token = str(timeStamp)+email
    token = sha1(token.encode()).hexdigest()
    return token