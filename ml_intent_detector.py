"""
ml_intent_detector.py — Machine Learning Intent Detection
Uses TF-IDF + Logistic Regression for improved intent recognition
Training happens automatically on module load with curated training examples
"""
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle
import os

# ─── TRAINING DATA ─────────────────────────────────────────────────────────────
# Curated examples for each intent (expanded for better generalization)
TRAINING_DATA = {
    "greeting": [
        "hi", "hello", "hey", "good morning", "good afternoon", "good evening",
        "hii", "helo", "howdy", "namaste", "hola", "greetings", "welcome",
        "what's up", "yo", "sup", "hello there", "hi there", "hey there",
        "good day", "cheers", "g'day", "ello", "hai",
    ],
    "goodbye": [
        "bye", "goodbye", "thank you", "thanks", "see you", "later", "exit",
        "bye bye", "see ya", "catch you", "cya", "take care", "farewell",
        "adios", "cheerio", "peace out", "leaving", "gotta go", "talk soon",
        "until later", "bye for now", "see ya later", "ta ta", "quit",
    ],
    "menu_indian": [
        "indian", "desi", "biryani", "curry", "masala", "naan", "roti", "dal",
        "paneer", "tikka", "lassi", "chai", "paratha", "kebab", "samosa",
        "idli", "dosa", "gulab", "halwa", "rasgulla", "indian food",
        "show me indian", "indian menu", "indian dishes", "spicy food",
        "butter chicken", "makhani", "tandoori",
    ],
    "menu_western": [
        "western", "pizza", "burger", "pasta", "continental", "sandwich",
        "fries", "steak", "spaghetti", "pepperoni", "cheesecake", "milkshake",
        "alfredo", "bbq", "barbeque", "lava cake", "carbs", "western food",
        "western menu", "show western", "american", "pizza time",
    ],
    "menu_veg": [
        "veg", "vegetarian", "veggie", "no meat", "plant based", "vegan",
        "only veg", "pure veg", "vegetables", "veggie options", "meat free",
        "vegetable dishes", "non-meat", "without meat", "just vegetables",
    ],
    "menu_all": [
        "menu", "food", "eat", "hungry", "items", "dishes", "list", "show menu",
        "see menu", "available", "options", "what do you have", "what can i order",
        "suggest", "recommend", "bestseller", "popular", "special", "what's good",
        "show me", "give me", "hungry for", "what's available", "options please",
    ],
    "view_cart": [
        "cart", "my cart", "view cart", "show cart", "basket", "what i have",
        "cart total", "what's in my cart", "my items", "my order", "bag",
        "show my cart", "check cart", "my bag",
    ],
    "place_order": [
        "place order", "checkout", "confirm order", "order now", "place my order",
        "finalize", "proceed to pay", "i want to order", "buy", "purchase",
        "checkout now", "confirm", "let's order", "submit order",
    ],
    "track_order": [
        "track", "where is my order", "where's my order", "order status",
        "delivery status", "how long", "when will", "eta", "out for delivery",
        "track my order", "where is it", "delivery time", "when arriving",
    ],
    "cancel_order": [
        "cancel", "cancel order", "cancel my order", "don't want", "stop order", "abort",
        "stop please", "cancel this", "wrong order", "cancel it",
    ],
    "payment": [
        "pay", "payment", "upi", "gpay", "phonepe", "card", "cash", "wallet",
        "cod", "net banking", "paytm", "credit", "debit", "emi", "how to pay",
        "payment methods", "payment options", "how can i pay",
    ],
    "offers": [
        "offer", "discount", "coupon", "deal", "promo", "code", "combo", "free delivery",
        "discount code", "promo code", "offer today", "discount today", "deals",
        "what offers", "any deals", "save money",
    ],
}

# ─── MODEL PERSISTENCE ────────────────────────────────────────────────────────
MODEL_PATH = os.path.join(os.path.dirname(__file__), "ml_model.pkl")
VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), "ml_vectorizer.pkl")

class MLIntentDetector:
    """Machine Learning Intent Detector using TF-IDF + Logistic Regression"""
    
    def __init__(self):
        self.vectorizer = None
        self.model = None
        self.intent_labels = None
        self.confidence_threshold = 0.5  # Min confidence for ML prediction
        
    def train(self):
        """Train the ML model on curated training data"""
        print("🤖 Training ML Intent Detector...")
        
        # Flatten training data
        messages = []
        labels = []
        for intent, examples in TRAINING_DATA.items():
            messages.extend(examples)
            labels.extend([intent] * len(examples))
        
        # Train vectorizer
        self.vectorizer = TfidfVectorizer(max_features=100, lowercase=True, 
                                          stop_words='english', ngram_range=(1, 2))
        X = self.vectorizer.fit_transform(messages)
        
        # Train classifier
        self.model = LogisticRegression(max_iter=200, random_state=42, multi_class='multinomial')
        self.model.fit(X, labels)
        self.intent_labels = self.model.classes_
        
        print(f"✅ ML Model trained with {len(TRAINING_DATA)} intents and {len(messages)} examples")
        self._save_model()
        
    def _save_model(self):
        """Save model to disk"""
        try:
            with open(MODEL_PATH, 'wb') as f:
                pickle.dump(self.model, f)
            with open(VECTORIZER_PATH, 'wb') as f:
                pickle.dump(self.vectorizer, f)
        except Exception as e:
            print(f"⚠️ Could not save model: {e}")
    
    def _load_model(self):
        """Load model from disk if available"""
        try:
            if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
                with open(MODEL_PATH, 'rb') as f:
                    self.model = pickle.load(f)
                with open(VECTORIZER_PATH, 'rb') as f:
                    self.vectorizer = pickle.load(f)
                self.intent_labels = self.model.classes_
                print("✅ Loaded pre-trained ML model")
                return True
        except Exception as e:
            print(f"⚠️ Could not load model: {e}")
        return False
    
    def predict(self, message: str) -> tuple:
        """
        Predict intent using ML model
        Returns: (predicted_intent, confidence_score)
        """
        if self.model is None or self.vectorizer is None:
            return None, 0.0
        
        try:
            X = self.vectorizer.transform([message.lower().strip()])
            predicted_intent = self.model.predict(X)[0]
            
            # Get confidence score (probability)
            probabilities = self.model.predict_proba(X)[0]
            confidence = float(np.max(probabilities))
            
            return predicted_intent, confidence
        except Exception as e:
            print(f"⚠️ ML prediction error: {e}")
            return None, 0.0

# ─── GLOBAL DETECTOR INSTANCE ─────────────────────────────────────────────────
_detector = MLIntentDetector()

def init_ml_detector():
    """Initialize ML detector — called once at app startup"""
    global _detector
    
    # Try loading pre-trained model
    if not _detector._load_model():
        # Train from scratch if no saved model
        _detector.train()

def detect_intent_ml(message: str) -> tuple:
    """
    Detect intent using ML (primary method)
    Returns: (intent, confidence)
    If confidence is too low, returns (None, 0.0) to trigger rule-based fallback
    """
    intent, confidence = _detector.predict(message)
    
    # Only return ML prediction if confident enough
    if confidence >= _detector.confidence_threshold:
        return intent, confidence
    return None, 0.0

def get_detector_info() -> dict:
    """Get detector status info"""
    return {
        "model_type": "Logistic Regression + TF-IDF",
        "intents_trained": len(TRAINING_DATA),
        "training_examples": sum(len(v) for v in TRAINING_DATA.values()),
        "model_loaded": _detector.model is not None,
        "confidence_threshold": _detector.confidence_threshold,
    }
