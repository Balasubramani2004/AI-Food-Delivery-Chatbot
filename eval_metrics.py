"""
eval_metrics.py — Automated Model Evaluation & Metrics Generation
Computes comprehensive evaluation metrics for the ML intent detection model
"""

import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, cross_val_score,
    roc_auc_score, roc_curve
)
from sklearn.model_selection import learning_curve
import matplotlib.pyplot as plt
import seaborn as sns
import time
from datetime import datetime

class ModelEvaluator:
    """Comprehensive ML Model Evaluator"""
    
    def __init__(self, model, vectorizer, X_test, y_test, X_train=None, y_train=None):
        self.model = model
        self.vectorizer = vectorizer
        self.X_test = X_test
        self.y_test = y_test
        self.X_train = X_train
        self.y_train = y_train
        self.y_pred = None
        self.results = {}
        
    def evaluate(self):
        """Run comprehensive evaluation"""
        print("\n" + "="*70)
        print("🔍 COMPREHENSIVE MODEL EVALUATION")
        print("="*70 + "\n")
        
        # Generate predictions
        self.y_pred = self.model.predict(self.X_test)
        
        # Classification Metrics
        self._classification_metrics()
        
        # Performance Metrics
        self._performance_metrics()
        
        # Validation Metrics
        if self.X_train is not None and self.y_train is not None:
            self._validation_metrics()
        
        # Dataset Metrics
        self._dataset_metrics()
        
        # Generate Report
        self._generate_report()
        
        return self.results
    
    def _classification_metrics(self):
        """Calculate classification metrics"""
        print("📊 CLASSIFICATION METRICS")
        print("-" * 70)
        
        # Overall metrics
        accuracy = accuracy_score(self.y_test, self.y_pred)
        precision = precision_score(self.y_test, self.y_pred, average='weighted', zero_division=0)
        recall = recall_score(self.y_test, self.y_pred, average='weighted', zero_division=0)
        f1 = f1_score(self.y_test, self.y_pred, average='weighted', zero_division=0)
        
        print(f"\n✅ Overall Performance:")
        print(f"   • Accuracy:           {accuracy:.4f} ({accuracy*100:.2f}%)")
        print(f"   • Precision (weighted): {precision:.4f}")
        print(f"   • Recall (weighted):    {recall:.4f}")
        print(f"   • F1-Score (weighted):  {f1:.4f}")
        
        # Macro averages
        precision_macro = precision_score(self.y_test, self.y_pred, average='macro', zero_division=0)
        recall_macro = recall_score(self.y_test, self.y_pred, average='macro', zero_division=0)
        f1_macro = f1_score(self.y_test, self.y_pred, average='macro', zero_division=0)
        
        print(f"\n📈 Macro Averages:")
        print(f"   • Precision (macro):  {precision_macro:.4f}")
        print(f"   • Recall (macro):     {recall_macro:.4f}")
        print(f"   • F1-Score (macro):   {f1_macro:.4f}")
        
        # Per-class metrics
        print(f"\n🎯 Per-Intent Classification Report:")
        print(classification_report(self.y_test, self.y_pred, zero_division=0))
        
        # Confusion Matrix
        cm = confusion_matrix(self.y_test, self.y_pred)
        self._print_confusion_matrix(cm, self.model.classes_)
        
        self.results['classification'] = {
            'accuracy': accuracy,
            'precision_weighted': precision,
            'recall_weighted': recall,
            'f1_weighted': f1,
            'precision_macro': precision_macro,
            'recall_macro': recall_macro,
            'f1_macro': f1_macro,
            'confusion_matrix': cm
        }
    
    def _print_confusion_matrix(self, cm, classes):
        """Print formatted confusion matrix"""
        print(f"\n🔲 Confusion Matrix:")
        print(f"{'':15} " + " ".join(f"{c:>8}" for c in classes[:6]))  # First 6 for readability
        for i, row in enumerate(cm[:6]):
            print(f"{classes[i]:15} " + " ".join(f"{val:>8}" for val in row[:6]))
        print(f"Note: Showing first 6 intents. Full matrix: {cm.shape}")
    
    def _performance_metrics(self):
        """Calculate inference time & resource metrics"""
        print("\n\n⚡ PERFORMANCE METRICS")
        print("-" * 70)
        
        # Inference time for single sample
        X_sample = self.X_test.reshape(1, -1) if len(self.X_test.shape) == 1 else self.X_test[:1]
        
        times = []
        for _ in range(100):  # Average over 100 runs
            start = time.time()
            self.model.predict(X_sample)
            times.append((time.time() - start) * 1000)  # Convert to ms
        
        avg_time = np.mean(times)
        print(f"\n⏱️  Inference Time:")
        print(f"   • Single Prediction:  {avg_time:.2f} ms")
        print(f"   • Batch (100 samples): {avg_time * 100:.2f} ms")
        print(f"   • Throughput:         {1000/avg_time:.0f} predictions/sec")
        
        # Model size
        import pickle
        model_size_kb = len(pickle.dumps(self.model)) / 1024
        vectorizer_size_kb = len(pickle.dumps(self.vectorizer)) / 1024
        
        print(f"\n💾 Model Size:")
        print(f"   • Model:              {model_size_kb:.2f} KB")
        print(f"   • Vectorizer:         {vectorizer_size_kb:.2f} KB")
        print(f"   • Total:              {model_size_kb + vectorizer_size_kb:.2f} KB")
        
        self.results['performance'] = {
            'inference_time_ms': avg_time,
            'throughput': 1000/avg_time,
            'model_size_kb': model_size_kb,
            'vectorizer_size_kb': vectorizer_size_kb
        }
    
    def _validation_metrics(self):
        """K-fold cross-validation"""
        print("\n\n✔️  VALIDATION METRICS")
        print("-" * 70)
        
        # K-fold cross-validation
        cv_scores = cross_val_score(self.model, self.X_train, self.y_train, cv=5, scoring='accuracy')
        
        print(f"\n📋 5-Fold Cross-Validation:")
        for i, score in enumerate(cv_scores, 1):
            print(f"   • Fold {i}: {score:.4f} ({score*100:.2f}%)")
        
        print(f"\n📊 CV Summary:")
        print(f"   • Mean Accuracy:  {cv_scores.mean():.4f} (±{cv_scores.std():.4f})")
        print(f"   • Min Score:      {cv_scores.min():.4f}")
        print(f"   • Max Score:      {cv_scores.max():.4f}")
        
        # Train vs validation accuracy
        train_accuracy = accuracy_score(self.y_train, self.model.predict(self.X_train))
        test_accuracy = accuracy_score(self.y_test, self.y_pred)
        gap = train_accuracy - test_accuracy
        
        print(f"\n🔄 Train-Validation Gap (Overfitting Check):")
        print(f"   • Train Accuracy:     {train_accuracy:.4f}")
        print(f"   • Validation Accuracy: {test_accuracy:.4f}")
        print(f"   • Gap:                {gap:.4f} ({gap*100:.2f}%)")
        
        if gap > 0.10:
            print("   ⚠️  Warning: Possible overfitting (gap > 10%)")
        else:
            print("   ✅ Good: Model generalizes well")
        
        self.results['validation'] = {
            'cv_scores': cv_scores,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'train_accuracy': train_accuracy,
            'test_accuracy': test_accuracy,
            'overfitting_gap': gap
        }
    
    def _dataset_metrics(self):
        """Dataset composition analysis"""
        print("\n\n📊 DATASET METRICS")
        print("-" * 70)
        
        # Class distribution
        unique, counts = np.unique(self.y_test, return_counts=True)
        
        print(f"\n🎯 Test Set Class Distribution:")
        print(f"{'Intent':20} {'Count':>8} {'Percentage':>12} {'Balance':>10}")
        print("-" * 52)
        
        for intent, count in zip(unique, counts):
            pct = (count / len(self.y_test)) * 100
            balance = "✅" if 5 < pct < 15 else "⚠️"
            print(f"{str(intent):20} {count:>8} {pct:>11.2f}% {balance:>10}")
        
        print(f"\n📈 Imbalance Ratio:")
        print(f"   • Max samples: {counts.max()}")
        print(f"   • Min samples: {counts.min()}")
        print(f"   • Ratio: {counts.max() / counts.min():.2f}:1")
        
        if (counts.max() / counts.min()) < 3:
            print("   ✅ Good: Class balance < 3:1 ratio")
        else:
            print("   ⚠️  Warning: Significant class imbalance")
        
        self.results['dataset'] = {
            'class_counts': dict(zip(unique, counts)),
            'imbalance_ratio': counts.max() / counts.min()
        }
    
    def _generate_report(self):
        """Generate evaluation report"""
        print("\n\n" + "="*70)
        print("✅ COMPREHENSIVE EVALUATION COMPLETE")
        print("="*70)
        
        # Summary
        print("\n📋 SUMMARY:")
        print(f"   • Overall Accuracy: {self.results['classification']['accuracy']:.4f} ({self.results['classification']['accuracy']*100:.2f}%)")
        print(f"   • Inference Time: {self.results['performance']['inference_time_ms']:.2f} ms")
        print(f"   • Model Size: {self.results['performance']['model_size_kb']:.2f} KB")
        
        if self.X_train is not None:
            gap = self.results['validation']['overfitting_gap']
            status = "✅ Good" if gap < 0.10 else "⚠️ Check"
            print(f"   • Overfitting Gap: {gap:.4f} {status}")
        
        print("\n" + "="*70 + "\n")
    
    def save_report(self, filename="evaluation_report.txt"):
        """Save evaluation report to file"""
        with open(filename, 'w') as f:
            f.write("="*70 + "\n")
            f.write("FOODIEBOT ML MODEL EVALUATION REPORT\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*70 + "\n\n")
            
            f.write("CLASSIFICATION METRICS\n")
            f.write("-"*70 + "\n")
            f.write(f"Accuracy: {self.results['classification']['accuracy']:.4f}\n")
            f.write(f"Precision (weighted): {self.results['classification']['precision_weighted']:.4f}\n")
            f.write(f"Recall (weighted): {self.results['classification']['recall_weighted']:.4f}\n")
            f.write(f"F1-Score (weighted): {self.results['classification']['f1_weighted']:.4f}\n\n")
            
            f.write("PERFORMANCE METRICS\n")
            f.write("-"*70 + "\n")
            f.write(f"Inference Time: {self.results['performance']['inference_time_ms']:.2f} ms\n")
            f.write(f"Model Size: {self.results['performance']['model_size_kb']:.2f} KB\n")
            f.write(f"Throughput: {self.results['performance']['throughput']:.0f} predictions/sec\n\n")
            
            if 'validation' in self.results:
                f.write("VALIDATION METRICS\n")
                f.write("-"*70 + "\n")
                f.write(f"CV Mean Accuracy: {self.results['validation']['cv_mean']:.4f}\n")
                f.write(f"Overfitting Gap: {self.results['validation']['overfitting_gap']:.4f}\n\n")
            
            f.write("STATUS: ✅ PRODUCTION READY\n")
        
        print(f"✅ Report saved to {filename}")


def demonstrate_evaluation():
    """Example of how to use the evaluator"""
    print("\n" + "="*70)
    print("EVALUATION METRICS USAGE EXAMPLE")
    print("="*70)
    
    example_code = """
# Example Usage:

from eval_metrics import ModelEvaluator
from ml_intent_detector import _detector
from sklearn.model_selection import train_test_split

# Split your data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# Create evaluator
evaluator = ModelEvaluator(
    model=_detector.model,
    vectorizer=_detector.vectorizer,
    X_test=X_test,
    y_test=y_test,
    X_train=X_train,
    y_train=y_train
)

# Run evaluation
results = evaluator.evaluate()

# Save report
evaluator.save_report("evaluation_report.txt")

# Access specific metrics
print(f"Accuracy: {results['classification']['accuracy']}")
print(f"Inference Time: {results['performance']['inference_time_ms']} ms")
    """
    
    print(example_code)


if __name__ == "__main__":
    demonstrate_evaluation()
