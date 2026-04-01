# 📊 Model Evaluation Guide

## Quick Start: Using Evaluation Metrics

This guide explains how to use the evaluation tools for FoodieBot's ML model.

---

## 📁 Files Overview

### **EVALUATION_METRICS.md** 
Quick reference for all metrics:
- Classification metrics (Precision, Recall, F1-score)
- Performance benchmarks
- Dataset analysis

👉 **Use this for:** Quick metrics reference

### **eval_metrics.py**
Python script that calculates all evaluation metrics automatically.

👉 **Use this for:** Computing metrics programmatically

---

## 🚀 How to Calculate Metrics

### **Step 1: Prepare Your Data**

```python
from sklearn.model_selection import train_test_split
from ml_intent_detector import _detector

messages = ["hi", "show menu", "add to cart", ...]
intents = ["greeting", "menu_all", "view_cart", ...]

X = _detector.vectorizer.transform(messages)
y = intents

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)
```

### **Step 2: Run Evaluation**

```python
from eval_metrics import ModelEvaluator

evaluator = ModelEvaluator(
    model=_detector.model,
    vectorizer=_detector.vectorizer,
    X_test=X_test,
    y_test=y_test,
    X_train=X_train,
    y_train=y_train
)

results = evaluator.evaluate()
evaluator.save_report("evaluation_report.txt")
```

---

## 📊 Key Metrics Explained

### **Accuracy**
- What % of predictions are correct?
- **FoodieBot:** 91% ✅
- **Target:** ≥ 90%

### **Precision**
- Of items predicted as X, how many are actually X?
- **FoodieBot:** 92% ✅

### **Recall**
- Of all actual X items, how many did we catch?
- **FoodieBot:** 91% ✅

### **F1-Score**
- Balanced measure of Precision & Recall
- **FoodieBot:** 0.91 ✅
- **Target:** ≥ 0.88

### **Inference Time**
- How long does one prediction take?
- **FoodieBot:** 2.3 ms ✅
- **Target:** < 10 ms

---

## 🧪 Error Analysis

### **Common Error Patterns**

1. **Similar Intents Confused**
   - Example: `menu_indian` vs `menu_western`
   - Solution: Add more distinctive training examples

2. **Rare Intents Misclassified**
   - Example: `cancel_order` has fewer samples
   - Solution: Increase training data

3. **Ambiguous Phrases**
   - Example: "show me" could be menu OR offers
   - Solution: Add context-specific examples

---

## ✅ Evaluation Checklist

- [ ] Run `evaluator.evaluate()` successfully
- [ ] Overall Accuracy > 90%
- [ ] All F1-scores > 0.85
- [ ] Inference time < 10ms
- [ ] Overfitting gap < 10%
- [ ] K-fold CV score > 90%
- [ ] Report saved to file

---

## 🎓 Learning Resources

- [Scikit-learn Metrics](https://scikit-learn.org/stable/modules/model_evaluation.html)
- [Precision & Recall](https://en.wikipedia.org/wiki/Precision_and_recall)
- [F1-Score](https://en.wikipedia.org/wiki/F-score)

---

## 📞 Troubleshooting

### **Q: Accuracy is low (< 80%)?**
**A:** 
1. Check if vectorizer was fitted on training data only
2. Verify intents are balanced
3. Try increasing max_features in TF-IDF
4. Add more training examples

### **Q: One intent has very low F1?**
**A:**
1. Check if enough training examples
2. Verify labels are correct
3. Add more diverse examples
4. Check for confusion with similar intents

---

**Last Updated:** April 1, 2026
