import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

TRAINING_DATA_PATH = "data/training_data.csv"
MODEL_PATH = "models/trading_model.pkl"
REPORT_PATH = "models/training_report.txt"

def train_model(force_retrain=False):
    """Train AI model to predict BUY/SELL signals."""

    # Check if model already exists
    if not force_retrain and os.path.exists(MODEL_PATH):
        print(f"✅ AI Model Already Trained. Skipping Retraining.")
        return joblib.load(MODEL_PATH)  # Load existing model

    print("📊 Loading Training Data...")
    df = pd.read_csv(TRAINING_DATA_PATH)

    # Ensure correct columns exist
    required_cols = ["SMA_50", "EMA_50", "RSI", "MACD", "Close", "Target"]
    missing_cols = [col for col in required_cols if col not in df.columns]

    if missing_cols:
        print(f"❌ Missing column in dataset: {missing_cols}")
        return

    X = df[["SMA_50", "EMA_50", "RSI", "MACD"]]
    y = df["Target"]

    # Split Data for Training & Testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train Model
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)

    # Evaluate Model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)

    # Save Model
    joblib.dump(model, MODEL_PATH)
    print(f"✅ AI Model Trained & Saved: {MODEL_PATH}")

    # Save Report
    with open(REPORT_PATH, "w") as f:
        f.write(f"📊 Training Report:\n")
        f.write(f"Accuracy: {accuracy:.4f}\n\n")
        f.write(f"Classification Report:\n{report}\n")
        f.write(f"Confusion Matrix:\n{conf_matrix}\n")

    print(f"📊 Training Report Saved: {REPORT_PATH}")
    return model

if __name__ == "__main__":
    train_model()
