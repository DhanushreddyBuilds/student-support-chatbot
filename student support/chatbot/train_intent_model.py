import pandas as pd
import joblib
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

nltk.download('punkt')

# Load dataset
data = pd.read_csv("intent_dataset.csv")

X = data["text"]
y = data["intent"]

# Build NLP + ML pipeline
model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", MultinomialNB())
])

# Train model
model.fit(X, y)

# Save model
joblib.dump(model, "intent_model.pkl")

print("✅ Intent classification model trained and saved successfully.")
