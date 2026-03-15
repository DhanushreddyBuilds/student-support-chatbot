import joblib
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# Paths
MODEL_PATH = os.path.join(os.path.dirname(__file__), "intent_model.pkl")
DATASET_PATH = os.path.join(os.path.dirname(__file__), "intent_dataset.csv")

_model = None

def load_model():
    """Loads the trained intent classification model."""
    global _model
    if os.path.exists(MODEL_PATH):
        _model = joblib.load(MODEL_PATH)
    else:
        print("⚠️ Model not found. Training a new one...")
        train_model()

def train_model():
    """Trains the model if not found."""
    global _model
    if not os.path.exists(DATASET_PATH):
        print("❌ Dataset not found!")
        return

    data = pd.read_csv(DATASET_PATH)
    X = data["text"]
    y = data["intent"]

    _model = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("clf", MultinomialNB())
    ])
    _model.fit(X, y)
    joblib.dump(_model, MODEL_PATH)
    print("✅ Model trained and saved.")

def predict_intent(text):
    """Predicts the intent of a given text."""
    if _model is None:
        load_model()
    
    if _model:
        prediction = _model.predict([text])[0]
        # Get probability
        probs = _model.predict_proba([text])[0]
        confidence = max(probs)
        return prediction, confidence
    return None, 0.0

if __name__ == "__main__":
    load_model()
    print(predict_intent("when is my exam?"))
