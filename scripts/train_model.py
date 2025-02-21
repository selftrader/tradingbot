import sys
import os
from pathlib import Path
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import joblib
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from models.ml_model import SectoralMLModel
from config import SECTORAL_INDICES

def generate_model_report(model, X_test, y_test, sector_data, save_dir, test_indices, test_symbols):
    """Generate comprehensive model performance report"""
    # Predictions on test set
    y_pred = model.model.predict(X_test)
    
    # Calculate metrics
    report = classification_report(y_test, y_pred, output_dict=True)
    
    # Create confusion matrix plot
    plt.figure(figsize=(10, 8))
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.savefig(save_dir / 'confusion_matrix.png')
    plt.close()
    
    # Feature importance plot
    feature_imp = pd.DataFrame(
        model.model.feature_importances_,
        index=['returns', 'vol_change', 'high_low_ratio', 'rsi', 'macd', 'macd_signal', 'bb_position'],
        columns=['importance']
    ).sort_values('importance', ascending=False)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=feature_imp['importance'], y=feature_imp.index)
    plt.title('Feature Importance')
    plt.savefig(save_dir / 'feature_importance.png')
    plt.close()
    
    # Generate sector-wise performance
    sector_performance = {}
    for sector, symbols in sector_data.items():
        sector_pred = []
        sector_true = []
        for symbol in symbols:
            if symbol in test_symbols:
                idx = test_symbols.index(symbol)
                symbol_pred = y_pred[test_indices[idx]]
                symbol_true = y_test[test_indices[idx]]
                sector_pred.extend(symbol_pred)
                sector_true.extend(symbol_true)
        if sector_pred:
            sector_performance[sector] = classification_report(
                sector_true, sector_pred, output_dict=True
            )
    
    # Save report to file
    report_path = save_dir / 'model_report.txt'
    with open(report_path, 'w') as f:
        f.write("MODEL PERFORMANCE REPORT\n")
        f.write("======================\n\n")
        f.write("Overall Performance:\n")
        f.write("-----------------\n")
        f.write(f"Accuracy: {report['accuracy']:.4f}\n")
        f.write(f"Macro Avg F1-Score: {report['macro avg']['f1-score']:.4f}\n\n")
        
        f.write("Class-wise Performance:\n")
        f.write("---------------------\n")
        for label in ['0', '1']:
            f.write(f"Class {label}:\n")
            f.write(f"  Precision: {report[label]['precision']:.4f}\n")
            f.write(f"  Recall: {report[label]['recall']:.4f}\n")
            f.write(f"  F1-Score: {report[label]['f1-score']:.4f}\n\n")
        
        f.write("Sector-wise Performance:\n")
        f.write("----------------------\n")
        for sector, metrics in sector_performance.items():
            f.write(f"\n{sector}:\n")
            f.write(f"  Accuracy: {metrics['accuracy']:.4f}\n")
            f.write(f"  Macro Avg F1-Score: {metrics['macro avg']['f1-score']:.4f}\n")

def train_model():
    # Create models directory if it doesn't exist
    models_dir = project_root / "models" / "trained"
    models_dir.mkdir(parents=True, exist_ok=True)

    model = SectoralMLModel()
    all_features = []
    all_targets = []
    
    print("Starting model training...")
    
    # Use historical data instead of future dates
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)  # Get 1 year of historical data
    
    # Get training data from all sectors
    for sector, symbols in SECTORAL_INDICES.items():
        print(f"\nProcessing {sector}...")
        for symbol in symbols:
            try:
                print(f"Getting data for {symbol}")
                # Use period parameter instead of start/end dates
                df = yf.download(
                    symbol,
                    period="1y",  # Get 1 year of data
                    interval="1d",
                    auto_adjust=True
                )
                
                if not df.empty and len(df) > 30:  # Ensure we have enough data
                    print(f"Retrieved {len(df)} days of data for {symbol}")
                    features, target = model.prepare_features(df)
                    all_features.append(features)
                    all_targets.append(target)
                else:
                    print(f"Insufficient data for {symbol}")
                    
            except Exception as e:
                print(f"Error getting data for {symbol}: {str(e)}")
                continue
    
    if not all_features:
        raise ValueError("No training data collected!")

    # Combine all data
    X = np.vstack(all_features)
    y = np.concatenate(all_targets)
    
    # Train the model
    print(f"\nTraining model with {len(X)} samples...")
    model.model.fit(X, y)
    
    # Save the model
    model_path = models_dir / "sectoral_model.pkl"
    print(f"\nSaving model to {model_path}")
    joblib.dump(model, model_path)
    print("Model training complete!")

    # Print basic model statistics
    print("\nModel Training Summary:")
    print(f"Total samples: {len(X)}")
    print(f"Features shape: {X.shape}")
    print(f"Class distribution: {np.bincount(y)}")

if __name__ == "__main__":
    try:
        train_model()
    except Exception as e:
        print(f"Training failed: {str(e)}")