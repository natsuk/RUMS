import bcrypt

def hash_password(password, rounds=12):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds)).decode()[6:]

def check_password(hashed_password, user_password):
    return bcrypt.checkpw(user_password.encode(), ("$2b$12" + hashed_password).encode())


password = "hogehoge"

hashedpass = hash_password(password)

ans = check_password( hashedpass ,"hogehoge")
print(ans)

print( hashedpass  )
print( "$2b$12" + hashedpass[6:] )
