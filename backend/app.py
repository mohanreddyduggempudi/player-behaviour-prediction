
# Minimal Flask app wiring routes, sessions, and ML demo
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from backend.db import get_db_connection
from backend.ml_model import predict, load_model
from backend.auth import auth, bcrypt
from backend.utils import login_required


load_dotenv()

def create_app():
    app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
    app.secret_key = os.getenv('FLASK_SECRET_KEY', 'change_me')
    app.register_blueprint(auth)
    bcrypt.init_app(app)

    # Load model at startup (safe lazy loader in ml_model)
    try:
        load_model()
        app.logger.info('ML model loaded successfully.')
    except Exception as e:
        app.logger.warning('Model not loaded: ' + str(e))

    @app.route('/')
    def index():
        return redirect(url_for('dashboard'))

    @app.route('/login', methods=['GET','POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            conn = get_db_connection()
            cur = conn.cursor(dictionary=True)
            cur.execute('SELECT id, password_hash, name FROM users WHERE email = %s', (email,))
            user = cur.fetchone()
            cur.close(); conn.close()
            if user and bcrypt.check_password_hash(user['password_hash'], password):
                session['user_id'] = user['id']
                session['user_name'] = user['name']
                flash('Logged in successfully', 'success')
                return redirect(url_for('dashboard'))
            flash('Invalid credentials', 'danger')
            return redirect(url_for('login'))
        return render_template('login.html')

    @app.route('/dashboard')
    @login_required
    def dashboard():
        # Basic stats summary (reads from database if available)
        stats = {}
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('SELECT COUNT(*) FROM players')
            stats['players'] = cur.fetchone()[0]
            cur.execute('SELECT COUNT(*) FROM predictions')
            stats['predictions'] = cur.fetchone()[0]
            cur.close(); conn.close()
        except Exception as e:
            app.logger.warning('DB not available: ' + str(e))
            stats['players'] = 'N/A'
            stats['predictions'] = 'N/A'
        return render_template('dashboard.html', stats=stats)

    @app.route('/demo', methods=['GET','POST'])
    @login_required
    def demo():
        result = None
        if request.method == 'POST':
            # parse inputs and call model
            try:
                features = {
                    'session_length': float(request.form.get('session_length',0)),
                    'levels_completed': int(request.form.get('levels_completed',0)),
                    'in_game_currency': float(request.form.get('in_game_currency',0)),
                    'past_purchases': int(request.form.get('past_purchases',0)),
                    'engagement_score': float(request.form.get('engagement_score',0))
                }
                pred, prob = predict(features)
                result = {'will_purchase': bool(pred), 'probability': round(prob,3)}
            except Exception as e:
                app.logger.error('Prediction error: ' + str(e))
                flash('Error making prediction: ' + str(e), 'danger')
        return render_template('demo.html', result=result)

    @app.route('/api/predict', methods=['POST'])
    def api_predict():
        data = request.get_json() or {}
        pred, prob = predict(data)
        return jsonify({'prediction': int(pred), 'probability': float(prob)})

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
