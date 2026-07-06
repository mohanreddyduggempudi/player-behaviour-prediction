
# ML model loader: loads the pre-trained model.joblib
import os
from joblib import load
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.joblib')

_model = None
def load_model():
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f'Model not found at {MODEL_PATH}. Run the training script.')
        _model = load(MODEL_PATH)
    return _model

def predict(features_dict):
    model = load_model()
    # Order of features must match training order
    X = [[
        features_dict.get('session_length',0.0),
        features_dict.get('levels_completed',0),
        features_dict.get('in_game_currency',0.0),
        features_dict.get('past_purchases',0),
        features_dict.get('engagement_score',0.0)
    ]]
    pred = model.predict(X)[0]
    prob = model.predict_proba(X)[0].max()
    return int(pred), float(prob)
