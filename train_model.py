
# Train a RandomForestClassifier on synthetic data and save it to backend/model.joblib
import numpy as np
import pandas as pd
from faker import Faker
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from joblib import dump
import os

def generate(n=3000, random_state=42):
    np.random.seed(random_state)
    data = []
    for i in range(n):
        session_length = max(0.1, np.random.exponential(scale=20.0))
        levels_completed = np.random.poisson(lam=3)
        in_game_currency = abs(np.random.normal(loc=50, scale=40))
        past_purchases = np.random.binomial(5, 0.1)
        engagement_score = np.clip(np.random.beta(2,5), 0, 1)
        # define a synthetic target: players with high engagement, high session length and high currency more likely to purchase
        score = (session_length/60.0) + (levels_completed/10.0) + (engagement_score*2) + (past_purchases*0.6) + (in_game_currency/200.0)
        prob = 1/(1+np.exp(-5*(score-0.6)))
        will_purchase = np.random.binomial(1, prob)
        data.append([session_length, levels_completed, in_game_currency, past_purchases, engagement_score, will_purchase])
    df = pd.DataFrame(data, columns=['session_length','levels_completed','in_game_currency','past_purchases','engagement_score','will_purchase'])
    return df

if __name__ == '__main__':
    df = generate(5000)
    X = df[['session_length','levels_completed','in_game_currency','past_purchases','engagement_score']]
    y = df['will_purchase']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    os.makedirs('backend', exist_ok=True)
    dump(model, 'backend/model.joblib')
    print('Trained model saved to backend/model.joblib')
