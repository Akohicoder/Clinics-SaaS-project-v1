import bcrypt

print("bcrypt path:", bcrypt.__file__)

password = b"123456"

hashed = bcrypt.hashpw(password, bcrypt.gensalt())

print("Hashed:", hashed)

print("Verify:", bcrypt.checkpw(password, hashed))