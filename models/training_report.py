import joblib
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from utils.data_loader import DataLoader

class TrainingReport:
    def __init__(self, model_name, data_file):
        self.model_name = model_name
        self.data_file = f"data/{data_file}.csv"
        self.model_path = f"models/{model_name}.pkl"
        self.report_path = f"reports/{model_name}_report.txt"
        self.confusion_matrix_path = f"reports/{model_name}_confusion_matrix.png"

    def load_data(self):
        """Loads historical data for training & evaluation"""
        data = pd.read_csv(self.data_file)
        X = data[["open", "high", "low", "close", "volume"]].values
        y = np.where(data["close"].shift(-1) > data["close"], 1, 0)  # 1 if price goes up, 0 if down
        return X, y

    def train_model(self):
        """Trains AI model & evaluates performance"""
        X, y = self.load_data()
        model = RandomForestClassifier(n_estimators=100)
        model.fit(X, y)

        # Evaluate performance
        y_pred = model.predict(X)
        accuracy = accuracy_score(y, y_pred)
        precision = precision_score(y, y_pred)
        recall = recall_score(y, y_pred)
        f1 = f1_score(y, y_pred)

        # Save model if it's better than existing one
        if os.path.exists(self.model_path):
            old_model = joblib.load(self.model_path)
            old_accuracy = old_model.score(X, y)
            if accuracy > old_accuracy:
                joblib.dump(model, self.model_path)
                print(f"✅ {self.model_name} Model Improved! Old Accuracy: {old_accuracy:.2f}, New Accuracy: {accuracy:.2f}")
            else:
                print(f"⚠️ New {self.model_name} Model Accuracy is Lower. Keeping Old Model.")
        else:
            joblib.dump(model, self.model_path)
            print(f"✅ First-time training for {self.model_name} completed!")

        # Save report
        self.generate_report(accuracy, precision, recall, f1, y, y_pred)

    def generate_report(self, accuracy, precision, recall, f1, y_true, y_pred):
        """Generates a training report with accuracy, confusion matrix, and feature importance"""
        os.makedirs("reports", exist_ok=True)
        
        with open(self.report_path, "w") as f:
            f.write(f"📊 Model Training Report: {self.model_name}\n")
            f.write(f"--------------------------------------\n")
            f.write(f"✅ Accuracy: {accuracy:.2f}\n")
            f.write(f"✅ Precision: {precision:.2f}\n")
            f.write(f"✅ Recall: {recall:.2f}\n")
            f.write(f"✅ F1 Score: {f1:.2f}\n")

        # Generate Confusion Matrix
        cm = confusion_matrix(y_true, y_pred)
        plt.figure(figsize=(6, 5))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["Down", "Up"], yticklabels=["Down", "Up"])
        plt.xlabel("Predicted")
        plt.ylabel("Actual")
        plt.title(f"Confusion Matrix - {self.model_name}")
        plt.savefig(self.confusion_matrix_path)
        plt.close()

        print(f"📄 Report saved: {self.report_path}")
        print(f"📊 Confusion Matrix saved: {self.confusion_matrix_path}")

# Example Usage
if __name__ == "__main__":
    report = TrainingReport(model_name="index_model", data_file="nifty50_data")
    report.train_model()
