
# Generate synthetic player data using Faker, numpy, pandas
# Optionally insert into MySQL if environment variables are set.
import os, json
import numpy as np
import pandas as pd
from faker import Faker
from dotenv import load_dotenv
load_dotenv()

def generate_synthetic(n=1000, random_state=42):
    fake = Faker()
    np.random.seed(random_state)
    data = []
    for i in range(n):
        session_length = max(0.1, np.random.exponential(scale=20.0))
        levels_completed = np.random.poisson(lam=3)
        in_game_currency = abs(np.random.normal(loc=50, scale=40))
        past_purchases = np.random.binomial(5, 0.1)
        engagement_score = np.clip(np.random.beta(2,5), 0, 1)
        player_id = fake.uuid4()
        data.append({
            'player_id': player_id,
            'session_length': session_length,
            'levels_completed': int(levels_completed),
            'in_game_currency': float(in_game_currency),
            'past_purchases': int(past_purchases),
            'engagement_score': float(engagement_score)
        })
    return pd.DataFrame(data)

if __name__ == '__main__':
    df = generate_synthetic(2000)
    print(df.head().to_dict(orient='records')[:3])
    # If DB configured, insert
    if os.getenv('MYSQL_DB'):
        import mysql.connector
        conn = mysql.connector.connect(host=os.getenv('MYSQL_HOST','127.0.0.1'),
                                       port=int(os.getenv('MYSQL_PORT',3306)),
                                       user=os.getenv('MYSQL_USER'),
                                       password=os.getenv('MYSQL_PASSWORD'),
                                       database=os.getenv('MYSQL_DB'))
        cur = conn.cursor()
        for _, row in df.iterrows():
            cur.execute('INSERT IGNORE INTO players (player_id, session_length, levels_completed, in_game_currency, past_purchases, engagement_score) VALUES (%s,%s,%s,%s,%s,%s)',
                        (row.player_id, float(row.session_length), int(row.levels_completed), float(row.in_game_currency), int(row.past_purchases), float(row.engagement_score)))
        conn.commit()
        cur.close(); conn.close()
        print('Inserted data into DB.')
