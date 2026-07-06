
# Creates a sample user SQL insert (prints an INSERT you can run) with a bcrypt-hashed password
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()
pw_hash = bcrypt.generate_password_hash('password123').decode('utf-8')
print("Run this SQL after creating the DB:\n\nINSERT INTO users (name,email,password_hash) VALUES ('Demo User','demo@example.com', '%s');" % pw_hash)
