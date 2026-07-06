
# Player Behaviour Prediction on In-game Purchases (Base Project)

This is a starter scaffold for the **Player Behaviour Prediction** project — a secure Flask web app with a MySQL database and an ML model (Random Forest). The scaffold includes:
- Flask backend with authentication (hashed passwords) and session management
- Pre-trained Random Forest model (trained on synthetic data)
- Frontend templates (Bootstrap + Chart.js)
- Database schema and seed script (synthetic data generator)
- Example `.env.example`, `requirements.txt`, and documentation to run locally

## Quick start (local demo without MySQL)
1. Create and activate a Python venv (recommended).
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python backend/app.py
   ```
4. Open http://127.0.0.1:5000/ in your browser.

## If you want to connect to MySQL
1. Create a database (see `database/schema.sql`).
2. Copy `.env.example` to `.env` and fill DB credentials.
3. Run `python database/seed_data.py` to generate and optionally insert seed data.
4. Start the app as above.

See file-level comments for more details.
