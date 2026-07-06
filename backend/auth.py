
# Authentication blueprint (simple)
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from .db import get_db_connection
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        if not (name and email and password):
            flash('All fields required', 'danger')
            return redirect(url_for('auth.register'))
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute('INSERT INTO users (name, email, password_hash) VALUES (%s,%s,%s)', (name,email,pw_hash))
            conn.commit()
            flash('Registration successful. Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            conn.rollback()
            current_app.logger.error(str(e))
            flash('Error during registration. Maybe email already exists.', 'danger')
            return redirect(url_for('auth.register'))
        finally:
            cur.close(); conn.close()
    return render_template('register.html')

@auth.route('/logout')
def logout():
    session.clear()
    flash('Logged out.', 'info')
    return redirect(url_for('login'))
