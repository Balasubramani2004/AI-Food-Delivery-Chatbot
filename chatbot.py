"""
chatbot.py — Hybrid Food Delivery Chatbot Engine
Uses ML (TF-IDF + Logistic Regression) for main intent detection
Falls back to rule-based keyword matching for robustness
Handles: menu display, cart, ordering, tracking, cancellation
"""
import random
import ml_intent_detector

# ─── MENU DATA ─────────────────────────────────────────────────────────────────
MENU = {
    "indian": {
        "Starters": [
            {"name": "Samosa (2 pcs)", "price": 49, "veg": True, "emoji": "🥟"},
            {"name": "Paneer Tikka", "price": 179, "veg": True, "emoji": "🧀"},
            {"name": "Chicken Tikka", "price": 219, "veg": False, "emoji": "🍗"},
            {"name": "Veg Spring Roll", "price": 99, "veg": True, "emoji": "🌯"},
            {"name": "Seekh Kebab", "price": 199, "veg": False, "emoji": "🍢"},
        ],
        "Main Course": [
            {"name": "Paneer Butter Masala", "price": 249, "veg": True, "emoji": "🧀"},
            {"name": "Dal Makhani", "price": 199, "veg": True, "emoji": "🫘"},
            {"name": "Butter Chicken", "price": 299, "veg": False, "emoji": "🍗"},
            {"name": "Veg Biryani", "price": 219, "veg": True, "emoji": "🍚"},
            {"name": "Chicken Biryani", "price": 279, "veg": False, "emoji": "🍚"},
            {"name": "Palak Paneer", "price": 229, "veg": True, "emoji": "🥬"},
            {"name": "Mutton Rogan Josh", "price": 349, "veg": False, "emoji": "🍖"},
        ],
        "Breads": [
            {"name": "Butter Naan", "price": 39, "veg": True, "emoji": "🫓"},
            {"name": "Garlic Naan", "price": 49, "veg": True, "emoji": "🫓"},
            {"name": "Aloo Paratha", "price": 69, "veg": True, "emoji": "🥙"},
            {"name": "Puri (4 pcs)", "price": 59, "veg": True, "emoji": "🥐"},
        ],
        "Desserts": [
            {"name": "Gulab Jamun (2 pcs)", "price": 79, "veg": True, "emoji": "🍮"},
            {"name": "Rasgulla (2 pcs)", "price": 79, "veg": True, "emoji": "🍡"},
            {"name": "Gajar Halwa", "price": 119, "veg": True, "emoji": "🥕"},
        ],
        "Drinks": [
            {"name": "Mango Lassi", "price": 99, "veg": True, "emoji": "🥭"},
            {"name": "Sweet Lassi", "price": 79, "veg": True, "emoji": "🥛"},
            {"name": "Masala Chai", "price": 39, "veg": True, "emoji": "☕"},
            {"name": "Nimbu Pani", "price": 49, "veg": True, "emoji": "🍋"},
        ],
    },
    "western": {
        "Burgers": [
            {"name": "Classic Veg Burger", "price": 149, "veg": True, "emoji": "🥗"},
            {"name": "Crispy Chicken Burger", "price": 199, "veg": False, "emoji": "🍗"},
            {"name": "Double Smash Burger", "price": 249, "veg": False, "emoji": "🍔"},
            {"name": "BBQ Bacon Burger", "price": 279, "veg": False, "emoji": "🥓"},
            {"name": "Mushroom Swiss Burger", "price": 219, "veg": True, "emoji": "🍄"},
        ],
        "Pizzas": [
            {"name": 'Margherita (7")', "price": 199, "veg": True, "emoji": "🍕"},
            {"name": 'Pepperoni (7")', "price": 249, "veg": False, "emoji": "🍕"},
            {"name": 'BBQ Chicken (10")', "price": 349, "veg": False, "emoji": "🍕"},
            {"name": 'Farmhouse Veg (10")', "price": 299, "veg": True, "emoji": "🍕"},
            {"name": 'Peri Peri Paneer (7")', "price": 249, "veg": True, "emoji": "🍕"},
        ],
        "Pasta & Mains": [
            {"name": "Spaghetti Arrabbiata", "price": 249, "veg": True, "emoji": "🍝"},
            {"name": "Penne Alfredo", "price": 249, "veg": True, "emoji": "🍝"},
            {"name": "Grilled Chicken Steak", "price": 399, "veg": False, "emoji": "🥩"},
            {"name": "Fish & Chips", "price": 299, "veg": False, "emoji": "🐟"},
        ],
        "Sides": [
            {"name": "French Fries", "price": 99, "veg": True, "emoji": "🍟"},
            {"name": "Onion Rings", "price": 119, "veg": True, "emoji": "🧅"},
            {"name": "Garlic Bread", "price": 99, "veg": True, "emoji": "🥖"},
        ],
        "Desserts": [
            {"name": "Chocolate Lava Cake", "price": 179, "veg": True, "emoji": "🎂"},
            {"name": "Cheesecake Slice", "price": 199, "veg": True, "emoji": "🍰"},
            {"name": "Brownie + Ice Cream", "price": 189, "veg": True, "emoji": "🍫"},
        ],
        "Beverages": [
            {"name": "Cold Coffee", "price": 129, "veg": True, "emoji": "☕"},
            {"name": "Fresh Lemonade", "price": 99, "veg": True, "emoji": "🍋"},
            {"name": "Oreo Milkshake", "price": 149, "veg": True, "emoji": "🥛"},
            {"name": "Iced Tea", "price": 99, "veg": True, "emoji": "🍵"},
        ],
    },
}

OFFERS = [
    {"code": "NEWUSER50", "desc": "50% off your first order (max ₹100)", "icon": "🎉"},
    {"code": "FREEDEL",   "desc": "Free delivery on orders above ₹299",  "icon": "🚚"},
    {"code": "BOGO20",    "desc": "Buy 2 get 20% off on pizzas",          "icon": "🍕"},
    {"code": "WEEKEND30", "desc": "30% off on weekends (Sat & Sun)",      "icon": "🎊"},
    {"code": "COMBO15",   "desc": "15% off on combo meals",               "icon": "🤝"},
]

PAYMENT_METHODS = [
    {"method": "UPI",            "desc": "GPay, PhonePe, Paytm UPI",      "icon": "📱"},
    {"method": "Credit/Debit Card","desc": "Visa, Mastercard, RuPay",     "icon": "💳"},
    {"method": "Net Banking",    "desc": "All major banks supported",      "icon": "🏦"},
    {"method": "Digital Wallet", "desc": "Paytm, Freecharge, MobiKwik",   "icon": "👛"},
    {"method": "Cash on Delivery","desc": "Pay when your food arrives",    "icon": "💵"},
]

BESTSELLERS = [
    {"name": "Butter Chicken",      "price": 299, "veg": False, "emoji": "🍗", "cuisine": "indian"},
    {"name": "Paneer Butter Masala","price": 249, "veg": True,  "emoji": "🧀", "cuisine": "indian"},
    {"name": "Chicken Biryani",     "price": 279, "veg": False, "emoji": "🍚", "cuisine": "indian"},
    {"name": "Double Smash Burger", "price": 249, "veg": False, "emoji": "🍔", "cuisine": "western"},
    {"name": 'BBQ Chicken Pizza (10")' , "price": 349, "veg": False, "emoji": "🍕", "cuisine": "western"},
    {"name": 'Farmhouse Veg Pizza (10")', "price": 299, "veg": True, "emoji": "🍕", "cuisine": "western"},
    {"name": "Mango Lassi",         "price": 99,  "veg": True,  "emoji": "🥭", "cuisine": "indian"},
    {"name": "Chocolate Lava Cake", "price": 179, "veg": True,  "emoji": "🎂", "cuisine": "western"},
]

# ─── INTENT DETECTION ──────────────────────────────────────────────────────────
INTENT_KEYWORDS = {
    "track_order":   ["track", "where is my order", "where's my order", "order status",
                      "delivery status", "how long", "when will", "eta", "out for delivery"],
    "cancel_order":  ["cancel", "cancel order", "cancel my order", "don't want", "stop order", "abort"],
    "place_order":   ["place order", "checkout", "confirm order", "order now", "place my order",
                      "finalize", "proceed to pay", "i want to order"],
    "view_cart":     ["cart", "my cart", "view cart", "show cart", "basket", "what i have",
                      "cart total", "what's in my cart"],
    "payment":       ["pay", "payment", "upi", "gpay", "phonepe", "card", "cash", "wallet",
                      "cod", "net banking", "paytm", "credit", "debit", "emi", "how to pay"],
    "offers":        ["offer", "discount", "coupon", "deal", "promo", "code", "combo", "free delivery"],
    "menu_veg":      ["veg", "vegetarian", "veggie", "no meat", "plant based", "vegan",
                      "only veg", "pure veg"],
    "menu_indian":   ["indian", "desi", "biryani", "curry", "masala", "naan", "roti", "dal",
                      "paneer", "tikka", "lassi", "chai", "paratha", "kebab", "samosa",
                      "idli", "dosa", "gulab", "halwa", "rasgulla"],
    "menu_western":  ["western", "pizza", "burger", "pasta", "continental", "sandwich",
                      "fries", "steak", "spaghetti", "pepperoni", "cheesecake", "milkshake",
                      "alfredo", "bbq", "barbeque", "lava cake"],
    "menu_all":      ["menu", "food", "eat", "hungry", "items", "dishes", "list", "show menu",
                      "see menu", "available", "options", "what do you have", "what can i order",
                      "suggest", "recommend", "bestseller", "popular", "special", "what's good"],
    "greeting":      ["hi", "hello", "hey", "good morning", "good afternoon", "good evening",
                      "hii", "helo", "howdy", "namaste", "hola"],
    "goodbye":       ["bye", "goodbye", "thank you", "thanks", "see you", "later", "exit"],
}

def detect_intent(message: str) -> str:
    """
    Hybrid Intent Detection: ML (primary) + Rule-Based (fallback)
    
    1. Try ML model first (fast, learns patterns)
    2. Fall back to rule-based keywords (reliable)
    3. Return 'unknown' if both fail
    """
    # ─── ML Detection (Primary) ────────────────────────────────────────────
    ml_intent, confidence = ml_intent_detector.detect_intent_ml(message)
    if ml_intent:
        return ml_intent
    
    # ─── Rule-Based Detection (Fallback) ───────────────────────────────────
    msg = message.lower().strip()
    for intent, keywords in INTENT_KEYWORDS.items():
        for kw in keywords:
            if kw in msg:
                return intent
    
    return "unknown"

def get_veg_menu():
    result = {}
    for cuisine, cats in MENU.items():
        result[cuisine] = {}
        for cat, items in cats.items():
            veg = [i for i in items if i["veg"]]
            if veg:
                result[cuisine][cat] = veg
    return result

# ─── RESPONSE BUILDER ──────────────────────────────────────────────────────────
def process_message(message: str, state: dict) -> dict:
    intent = detect_intent(message)

    # ── Greeting ──────────────────────────────────────────────────────────────
    if intent == "greeting":
        greets = [
            "Hey there! 👋 Welcome to **FoodieBot**! I'm your smart food delivery assistant.\n\nWhat are you craving today?",
            "Hello! 😊 Great to see you at **FoodieBot**! Ready for something delicious?\n\nExplore our Indian 🍛 or Western 🍔 menu!",
            "Hi! 🌟 Welcome! I'm here to get you the best food delivered fast.\n\nWhat would you like to order today?",
        ]
        return {
            "text": random.choice(greets),
            "type": "greeting",
            "quick_actions": ["🍛 Indian Menu", "🍔 Western Menu", "⭐ Bestsellers", "🎁 Offers"],
        }

    # ── Goodbye ───────────────────────────────────────────────────────────────
    if intent == "goodbye":
        cart = state.get("cart", [])
        hint = f"\n\n🛒 P.S. You have **{len(cart)} item(s)** in your cart — come back and checkout anytime!" if cart else ""
        return {
            "text": f"Thanks for visiting **FoodieBot**! 😊 Hope to see you again soon!{hint}\n\n🍕 We deliver happiness daily!",
            "type": "text",
            "quick_actions": ["🍛 Indian Menu", "🍔 Western Menu"],
        }

    # ── Indian Menu ───────────────────────────────────────────────────────────
    if intent == "menu_indian":
        return {
            "text": "Here's our **Indian Menu** 🍛 — tap **Add to Cart** on any item!",
            "type": "menu",
            "menu_type": "indian",
            "menu_data": MENU["indian"],
            "quick_actions": ["🍔 Western Menu", "🥗 Veg Only", "🛒 View Cart", "✅ Place Order"],
        }

    # ── Western Menu ──────────────────────────────────────────────────────────
    if intent == "menu_western":
        return {
            "text": "Here's our **Western Menu** 🍔🍕 — tap **Add to Cart** on any item!",
            "type": "menu",
            "menu_type": "western",
            "menu_data": MENU["western"],
            "quick_actions": ["🍛 Indian Menu", "🥗 Veg Only", "🛒 View Cart", "✅ Place Order"],
        }

    # ── Veg Menu ──────────────────────────────────────────────────────────────
    if intent == "menu_veg":
        return {
            "text": "Here are all **Vegetarian Options** 🥗🌿 — 100% veg items only!",
            "type": "menu",
            "menu_type": "veg",
            "menu_data": get_veg_menu(),
            "quick_actions": ["🍛 Full Indian Menu", "🍔 Full Western Menu", "🛒 View Cart"],
        }

    # ── Full Menu / Hungry / Recommend ───────────────────────────────────────
    if intent == "menu_all":
        recs = random.sample(BESTSELLERS, 4)
        return {
            "text": "🍽️ What would you like today? Here are our **top picks** — or browse our full menu below!",
            "type": "recommendations",
            "items": recs,
            "quick_actions": ["🍛 Indian Menu", "🍔 Western Menu", "🥗 Veg Only", "🎁 Offers"],
        }

    # ── View Cart ─────────────────────────────────────────────────────────────
    if intent == "view_cart":
        cart = state.get("cart", [])
        if not cart:
            return {
                "text": "Your cart is empty! 🛒\n\nAdd some delicious items from our menu:",
                "type": "empty_cart",
                "quick_actions": ["🍛 Indian Menu", "🍔 Western Menu", "⭐ Bestsellers"],
            }
        total = sum(i["price"] for i in cart)
        return {
            "text": f"Here's your cart 🛒 — **{len(cart)} item(s)**, total **₹{total}**:",
            "type": "cart",
            "cart": cart,
            "total": total,
            "quick_actions": ["✅ Place Order", "🍛 Add More", "❌ Clear Cart"],
        }

    # ── Place Order ───────────────────────────────────────────────────────────
    if intent == "place_order":
        cart = state.get("cart", [])
        if not cart:
            return {
                "text": "Your cart is empty! Please add items first. 🛒",
                "type": "empty_cart",
                "quick_actions": ["🍛 Indian Menu", "🍔 Western Menu"],
            }
        total = sum(i["price"] for i in cart)
        return {
            "text": f"Almost there! 🎉 You have **{len(cart)} item(s)** | Total: **₹{total}**\n\nChoose your payment method to confirm:",
            "type": "checkout",
            "cart": cart,
            "total": total,
            "payment_methods": PAYMENT_METHODS,
        }

    # ── Track Order ───────────────────────────────────────────────────────────
    if intent == "track_order":
        if not state.get("order_placed"):
            return {
                "text": "You don't have any active order yet. 📦\n\nWould you like to order something delicious?",
                "type": "text",
                "quick_actions": ["🍛 Indian Menu", "🍔 Western Menu", "⭐ Bestsellers"],
            }
        return {
            "text": f"📦 Live tracking for Order **#{state['order_id']}**:",
            "type": "tracking",
            "order_id": state.get("order_id"),
            "status": state.get("order_status", "confirmed"),
            "items": state.get("order_items", []),
            "total": state.get("order_total", 0),
            "payment_method": state.get("payment_method", ""),
            "quick_actions": ["❌ Cancel Order", "💬 Contact Support"],
        }

    # ── Cancel Order ──────────────────────────────────────────────────────────
    if intent == "cancel_order":
        if not state.get("order_placed"):
            return {
                "text": "You don't have any active order to cancel. 🤔\n\nWould you like to place a new order?",
                "type": "text",
                "quick_actions": ["🍛 Indian Menu", "🍔 Western Menu"],
            }
        return {
            "text": f"Are you sure you want to cancel order **#{state['order_id']}**? 😢",
            "type": "cancel_confirm",
            "order_id": state.get("order_id"),
            "items": state.get("order_items", []),
            "total": state.get("order_total", 0),
        }

    # ── Payment ───────────────────────────────────────────────────────────────
    if intent == "payment":
        return {
            "text": "💳 We offer multiple secure payment options:",
            "type": "payment",
            "payment_methods": PAYMENT_METHODS,
            "quick_actions": ["🛒 View Cart", "✅ Place Order"],
        }

    # ── Offers ────────────────────────────────────────────────────────────────
    if intent == "offers":
        return {
            "text": "🎁 Hot deals just for you — use these codes at checkout!",
            "type": "offers",
            "offers": OFFERS,
            "quick_actions": ["🍛 Indian Menu", "🍔 Western Menu", "🛒 View Cart"],
        }

    # ── Unknown ───────────────────────────────────────────────────────────────
    fallbacks = [
        "Hmm, I didn't quite get that! 🤔 Here's what I can help you with:",
        "I'm not sure about that. Let me show you what I can do:",
        "Could you rephrase that? Here's what's available:",
    ]
    return {
        "text": random.choice(fallbacks),
        "type": "help",
        "quick_actions": ["🍛 Indian Menu", "🍔 Western Menu", "🛒 View Cart",
                          "💳 Payment", "🎁 Offers", "📦 Track Order"],
    }

def init():
    """Initialize chatbot engine (ML model + rule-based system)"""
    print("\n" + "="*60)
    print("🤖 FoodieBot Initialization")
    print("="*60)
    ml_intent_detector.init_ml_detector()
    detector_info = ml_intent_detector.get_detector_info()
    print(f"📊 Intent Detector Config:")
    print(f"   • Model: {detector_info['model_type']}")
    print(f"   • Intents: {detector_info['intents_trained']}")
    print(f"   • Training Examples: {detector_info['training_examples']}")
    print(f"   • Model Loaded: {'✅' if detector_info['model_loaded'] else '❌'}")
    print(f"   • Confidence Threshold: {detector_info['confidence_threshold']*100:.0f}%")
    print("✅ FoodieBot engine ready (Hybrid ML + Rule-Based)")
    print("="*60 + "\n")

def get_response(message: str) -> dict:
    """Legacy shim for old app.py callers."""
    return process_message(message, {})
