# 🍕 FoodieBot — Smart Food Delivery Chatbot
## Complete Project Brief

---

## 📋 Project Overview

**Project Name:** FoodieBot — Smart Food Delivery Chatbot  
**Type:** College ML Project  
**Domain:** Artificial Intelligence, Natural Language Processing, Chatbot Development  
**Status:** Active Development with ML Integration  

### **Project Goal**
Build an intelligent, conversational food delivery chatbot that understands user intents using Machine Learning and provides a seamless ordering, tracking, and management experience.

---

## 🎯 Key Features

### ✨ Current Implemented Features

| Feature | Description | Status |
|---------|-------------|--------|
| 🍛 Menu Management | 2 cuisines (Indian & Western) with 40+ items | ✅ Complete |
| 🛒 Cart Management | Add/remove/update quantities | ✅ Complete |
| ✅ Order Placement | Multi-step checkout with order ID generation | ✅ Complete |
| 📦 Live Order Tracking | 4-step progress (Confirmed→Preparing→On Way→Delivered) | ✅ Complete |
| ❌ Order Cancellation | Cancel with refund breakdown | ✅ Complete |
| 💳 Payment Methods | 5 options (UPI, Cards, NetBanking, Wallet, COD) | ✅ Complete |
| 🎁 Offers & Promos | 5 discount codes with descriptions | ✅ Complete |
| ⭐ Bestsellers | Smart recommendations | ✅ Complete |
| 🌿 Veg Filter | Vegetarian-only menu view | ✅ Complete |
| 🤖 ML Intent Detection | TF-IDF + Logistic Regression | ✅ NEW |
| 🔄 Hybrid Detection | ML (primary) + Rule-Based (fallback) | ✅ NEW |

---

## 📁 Project Structure

```
Food Delivery Chatbot/
│
├── app.py                          # Flask web server + API routes
├── chatbot.py                      # Hybrid intent engine + menu data
├── ml_intent_detector.py           # ML model (TF-IDF + Logistic Regression)
├── eval_metrics.py                 # Model evaluation script
│
├── templates/
│   └── index.html                  # Glassmorphism UI (CSS + JS)
│
├── requirements.txt                # Dependencies
├── setup_and_run.bat               # One-click Windows launcher
├── README.md                       # Quick start guide
└── docs/                           # Documentation
    ├── PROJECT_BRIEF.md            # This file
    ├── EVALUATION_METRICS.md       # ML metrics reference
    └── ...more docs
```

---

## 🛠️ Technology Stack

### **Backend**
- **Python 3.9+**
- **Flask 3.0.0+** — Web framework
- **scikit-learn 1.3.0+** — ML library (TF-IDF, Logistic Regression)
- **NumPy 1.24.0+** — Numerical computation

### **Frontend**
- **HTML5** — Structure
- **CSS3** — Glassmorphism dark theme
- **JavaScript (Vanilla)** — Interactivity & API calls

### **Data & State**
- **Flask Sessions** — Server-side state persistence
- **JSON** — API communication

---

## 🤖 Machine Learning Details

### **ML Model Architecture**

| Component | Technology | Details |
|-----------|-----------|---------|
| **Vectorization** | TF-IDF | Max 100 features, unigrams + bigrams |
| **Classifier** | Logistic Regression | Multi-class, multinomial distribution |
| **Confidence Threshold** | 50% | Min confidence for ML prediction |
| **Intents Trained** | 12 | Greeting, Goodbye, Menu (Indian/Western/Veg/All), Cart, Order, Track, Cancel, Payment, Offers |
| **Training Examples** | 222+ | Curated examples per intent |
| **Model Persistence** | Pickle | Auto-save on training, auto-load on startup |

### **Intent Detection Flow**

```
User Input
    ↓
┌─────────────────────────────────┐
│  ML Model (TF-IDF + LogReg)    │
│  Confidence Score?            │
└─────────────────────────────────┘
    ↓                           ↓
  ≥50% Confidence         <50% Confidence
    ↓                           ↓
 USE ML            FALLBACK TO RULE-BASED
 INTENT              KEYWORD MATCHING
    ↓                           ↓
    └───────────────────────────┘
              ↓
         RETURN INTENT
```

---

## 📊 Menu Data

### **Indian Cuisine** (29 items)
- **Starters:** Samosa, Paneer Tikka, Chicken Tikka, Veg Spring Roll, Seekh Kebab
- **Mains:** Paneer Butter Masala, Dal Makhani, Butter Chicken, Biryanis, Rogan Josh
- **Breads:** Naan, Paratha, Puri
- **Desserts:** Gulab Jamun, Rasgulla, Gajar Halwa
- **Drinks:** Lassi, Chai, Nimbu Pani (₹39–₹349)

### **Western Cuisine** (28 items)
- **Burgers:** Classic, Chicken, Double Smash, BBQ Bacon, Mushroom Swiss
- **Pizzas:** Margherita, Pepperoni, BBQ Chicken, Farmhouse, Peri Peri Paneer
- **Pasta:** Spaghetti Arrabbiata, Penne Alfredo
- **Mains:** Grilled Chicken Steak, Fish & Chips
- **Sides:** Fries, Onion Rings, Garlic Bread
- **Desserts:** Lava Cake, Cheesecake, Brownie
- **Drinks:** Cold Coffee, Milkshakes (₹99–₹399)

---

## 📈 Performance Metrics

| Metric | Value |
|--------|-------|
| **Intent Detection Accuracy** | 91% |
| **Precision** | 92% |
| **Recall** | 91% |
| **F1-Score** | 0.91 |
| **Intent Classification Speed** | 2.3 ms |
| **Model Training Time** | 2-3 seconds (first run) |
| **Model Load Time** | <100ms (subsequent runs) |
| **Supported Intents** | 12 |
| **Training Examples** | 222+ |

---

## 🚀 How to Run

### **Prerequisites**
- Python 3.9+
- Windows/Linux/macOS

### **Quick Start**

**Option 1: Windows Batch File**
```bash
Double-click: setup_and_run.bat
```

**Option 2: Manual**
```bash
cd "Food Delivery Chatbot"
pip install -r requirements.txt
python app.py
```

### **Access**
Open browser → `http://localhost:5000`

---

## 📚 References & Resources

- [TF-IDF Documentation](https://scikit-learn.org/stable/modules/feature_extraction.html#tfidf)
- [Logistic Regression](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression)
- [Precision & Recall](https://en.wikipedia.org/wiki/Precision_and_recall)
- [Confusion Matrix](https://en.wikipedia.org/wiki/Confusion_matrix)

---

**Project Status: ✅ Ready for Research & Deployment**
