
Security notes and best-practices included in the scaffold:
- Passwords are stored hashed using bcrypt (Flask-Bcrypt).
- No credentials are hard-coded; fill them in `.env` which is ignored by git.
- Database queries use parameterized queries to mitigate SQL injection (see db usage).
- Session secret key must be random and kept secret.
- For production: run behind a WSGI server (gunicorn/uwsgi), enable TLS, and restrict DB access.
