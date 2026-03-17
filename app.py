from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import math

app = Flask(__name__)
CORS(app)  # allow frontend to talk to backend

# ── Grocery item database ──────────────────────────────────────────────
ITEMS = [
    {"id": 1,  "name": "Amul Milk 500ml",       "icon": "🥛", "category": "dairy",     "base_price": 28},
    {"id": 2,  "name": "Amul Butter 100g",       "icon": "🧈", "category": "dairy",     "base_price": 56},
    {"id": 3,  "name": "Curd 400g",              "icon": "🫙", "category": "dairy",     "base_price": 42},
    {"id": 4,  "name": "Paneer 200g",            "icon": "🧀", "category": "dairy",     "base_price": 88},
    {"id": 5,  "name": "Amul Cheese Slices",     "icon": "🧀", "category": "dairy",     "base_price": 115},
    {"id": 6,  "name": "Fresh Cream 200ml",      "icon": "🥛", "category": "dairy",     "base_price": 66},
    {"id": 7,  "name": "Tomatoes 500g",          "icon": "🍅", "category": "produce",   "base_price": 33},
    {"id": 8,  "name": "Onions 1kg",             "icon": "🧅", "category": "produce",   "base_price": 38},
    {"id": 9,  "name": "Potatoes 1kg",           "icon": "🥔", "category": "produce",   "base_price": 35},
    {"id": 10, "name": "Spinach 250g",           "icon": "🥬", "category": "produce",   "base_price": 28},
    {"id": 11, "name": "Bananas 6 pcs",          "icon": "🍌", "category": "produce",   "base_price": 46},
    {"id": 12, "name": "Apples 4 pcs",           "icon": "🍎", "category": "produce",   "base_price": 98},
    {"id": 13, "name": "Capsicum 2 pcs",         "icon": "🫑", "category": "produce",   "base_price": 30},
    {"id": 14, "name": "Carrots 500g",           "icon": "🥕", "category": "produce",   "base_price": 28},
    {"id": 15, "name": "Basmati Rice 1kg",       "icon": "🍚", "category": "staples",   "base_price": 118},
    {"id": 16, "name": "Wheat Atta 5kg",         "icon": "🌾", "category": "staples",   "base_price": 255},
    {"id": 17, "name": "Tata Salt 1kg",          "icon": "🧂", "category": "staples",   "base_price": 26},
    {"id": 18, "name": "Toor Dal 500g",          "icon": "🫘", "category": "staples",   "base_price": 74},
    {"id": 19, "name": "Sunflower Oil 1L",       "icon": "🫙", "category": "staples",   "base_price": 148},
    {"id": 20, "name": "Maggi Noodles 4pk",      "icon": "🍜", "category": "staples",   "base_price": 74},
    {"id": 21, "name": "Eggs 12 pcs",            "icon": "🥚", "category": "staples",   "base_price": 90},
    {"id": 22, "name": "Lays Classic 50g",       "icon": "🥔", "category": "snacks",    "base_price": 20},
    {"id": 23, "name": "Parle-G 200g",           "icon": "🍪", "category": "snacks",    "base_price": 20},
    {"id": 24, "name": "KitKat 4-finger",        "icon": "🍫", "category": "snacks",    "base_price": 55},
    {"id": 25, "name": "Kurkure 90g",            "icon": "🌽", "category": "snacks",    "base_price": 30},
    {"id": 26, "name": "Britannia Marie",        "icon": "🍪", "category": "snacks",    "base_price": 40},
    {"id": 27, "name": "Nescafé 50g",            "icon": "☕", "category": "beverages", "base_price": 132},
    {"id": 28, "name": "Tata Tea 250g",          "icon": "🍵", "category": "beverages", "base_price": 96},
    {"id": 29, "name": "Tropicana 1L",           "icon": "🧃", "category": "beverages", "base_price": 112},
    {"id": 30, "name": "Red Bull 250ml",         "icon": "🥤", "category": "beverages", "base_price": 115},
    {"id": 31, "name": "Surf Excel 500g",        "icon": "🧺", "category": "cleaning",  "base_price": 108},
    {"id": 32, "name": "Vim Dishwash 500g",      "icon": "🍽️", "category": "cleaning",  "base_price": 65},
    {"id": 33, "name": "Dettol Soap 75g",        "icon": "🧼", "category": "cleaning",  "base_price": 48},
    {"id": 34, "name": "Harpic 500ml",           "icon": "🚿", "category": "cleaning",  "base_price": 125},
    {"id": 35, "name": "Tropicana Juice 1L", "icon": "🧃", "category": "beverages", "base_price": 115},
    {"id": 36, "name": "Red Bull 250ml", "icon": "🥤", "category": "beverages", "base_price": 120},
    {"id": 37, "name": "Coca-Cola 750ml", "icon": "🥤", "category": "beverages", "base_price": 45},
    {"id": 38, "name": "Bisleri Water 1L", "icon": "💧", "category": "beverages", "base_price": 20},

    {"id": 39, "name": "Surf Excel 500g", "icon": "🧺", "category": "cleaning", "base_price": 110},
    {"id": 40, "name": "Vim Dishwash 500g", "icon": "🍽️", "category": "cleaning", "base_price": 70},
    {"id": 41, "name": "Dettol Soap 75g", "icon": "🧼", "category": "cleaning", "base_price": 50},
    {"id": 42, "name": "Harpic 500ml", "icon": "🚿", "category": "cleaning", "base_price": 130},
    {"id": 43, "name": "Colgate Toothpaste 150g", "icon": "🪥", "category": "cleaning", "base_price": 95},
    {"id": 44, "name": "Head & Shoulders Shampoo 180ml", "icon": "🧴", "category": "cleaning", "base_price": 160}
    {"id": 45, "name": "Amul Vanilla Ice Cream 1L", "icon": "🍦", "category": "icecream", "base_price": 180},
    {"id": 46, "name": "Amul Butterscotch Ice Cream 1L", "icon": "🍦", "category": "icecream", "base_price": 185},
    {"id": 47, "name": "Amul Chocolate Brownie Ice Cream 1L", "icon": "🍦", "category": "icecream", "base_price": 190},
    {"id": 48, "name": "Amul Rajbhog Ice Cream Cup", "icon": "🍦", "category": "icecream", "base_price": 40},

    {"id": 49, "name": "Cornetto Chocolate Cone", "icon": "🍦", "category": "icecream", "base_price": 40},
    {"id": 50, "name": "Cornetto Strawberry Cone", "icon": "🍦", "category": "icecream", "base_price": 40},
    {"id": 51, "name": "Cornetto Butterscotch Cone", "icon": "🍦", "category": "icecream", "base_price": 42},

    {"id": 52, "name": "Magnum Chocolate Ice Cream Bar", "icon": "🍦", "category": "icecream", "base_price": 80},
{"id": 53, "name": "Magnum Almond Ice Cream Bar", "icon": "🍦", "category": "icecream", "base_price": 85},

{"id": 54, "name": "Havmor Belgian Chocolate Ice Cream 750ml", "icon": "🍦", "category": "icecream", "base_price": 275},
{"id": 55, "name": "Havmor Butterscotch Ice Cream 750ml", "icon": "🍦", "category": "icecream", "base_price": 170},

{"id": 56, "name": "Kwality Walls Oreo Ice Cream Tub", "icon": "🍦", "category": "icecream", "base_price": 275},
{"id": 57, "name": "Kwality Walls Chocolate Sensation Tub", "icon": "🍦", "category": "icecream", "base_price": 210},

{"id": 58, "name": "Kulfi Ice Cream Stick", "icon": "🍦", "category": "icecream", "base_price": 35},
{"id": 59, "name": "Mango Ice Cream Cup", "icon": "🍦", "category": "icecream", "base_price": 35},
{"id": 60, "name": "Strawberry Ice Cream Cup", "icon": "🍦", "category": "icecream", "base_price": 35},
# MORE GROCERY ITEMS

{"id": 61, "name": "Sugar 1kg", "icon": "🍬", "category": "staples", "base_price": 45},
{"id": 62, "name": "Brown Sugar 500g", "icon": "🍬", "category": "staples", "base_price": 60},
{"id": 63, "name": "Moong Dal 500g", "icon": "🫘", "category": "staples", "base_price": 85},
{"id": 64, "name": "Masoor Dal 500g", "icon": "🫘", "category": "staples", "base_price": 75},
{"id": 65, "name": "Chana Dal 500g", "icon": "🫘", "category": "staples", "base_price": 70},
{"id": 66, "name": "Besan 500g", "icon": "🌾", "category": "staples", "base_price": 70},
{"id": 67, "name": "Poha 500g", "icon": "🍚", "category": "staples", "base_price": 55},
{"id": 68, "name": "Sooji 500g", "icon": "🌾", "category": "staples", "base_price": 50},
{"id": 69, "name": "Corn Flour 200g", "icon": "🌽", "category": "staples", "base_price": 45},
{"id": 70, "name": "Oats 500g", "icon": "🥣", "category": "staples", "base_price": 95},

{"id": 71, "name": "Peanut Oil 1L", "icon": "🫙", "category": "staples", "base_price": 175},
{"id": 72, "name": "Mustard Oil 1L", "icon": "🫙", "category": "staples", "base_price": 165},
{"id": 73, "name": "Ghee 500ml", "icon": "🧈", "category": "staples", "base_price": 310},
{"id": 74, "name": "Honey 250g", "icon": "🍯", "category": "staples", "base_price": 125},
{"id": 75, "name": "Tomato Ketchup 500g", "icon": "🍅", "category": "staples", "base_price": 110},

{"id": 76, "name": "Coriander Powder 200g", "icon": "🌿", "category": "spices", "base_price": 60},
{"id": 77, "name": "Turmeric Powder 200g", "icon": "🌿", "category": "spices", "base_price": 55},
{"id": 78, "name": "Red Chilli Powder 200g", "icon": "🌶️", "category": "spices", "base_price": 70},
{"id": 79, "name": "Garam Masala 100g", "icon": "🌿", "category": "spices", "base_price": 80},
{"id": 80, "name": "Black Pepper 50g", "icon": "🌶️", "category": "spices", "base_price": 95},

{"id": 81, "name": "Garlic 250g", "icon": "🧄", "category": "produce", "base_price": 35},
{"id": 82, "name": "Ginger 250g", "icon": "🫚", "category": "produce", "base_price": 30},
{"id": 83, "name": "Lemon 4 pcs", "icon": "🍋", "category": "produce", "base_price": 28},
{"id": 84, "name": "Cauliflower 1 pc", "icon": "🥦", "category": "produce", "base_price": 45},
{"id": 85, "name": "Cabbage 1 pc", "icon": "🥬", "category": "produce", "base_price": 40},

{"id": 86, "name": "Orange 4 pcs", "icon": "🍊", "category": "produce", "base_price": 65},
{"id": 87, "name": "Pomegranate 1 pc", "icon": "🍎", "category": "produce", "base_price": 90},
{"id": 88, "name": "Papaya 1 pc", "icon": "🍈", "category": "produce", "base_price": 70},

{"id": 89, "name": "Dairy Milk Chocolate 50g", "icon": "🍫", "category": "snacks", "base_price": 40},
{"id": 90, "name": "Snickers Bar", "icon": "🍫", "category": "snacks", "base_price": 55},
{"id": 91, "name": "Munch Chocolate", "icon": "🍫", "category": "snacks", "base_price": 25},

{"id": 92, "name": "Sprite 750ml", "icon": "🥤", "category": "beverages", "base_price": 45},
{"id": 93, "name": "Pepsi 750ml", "icon": "🥤", "category": "beverages", "base_price": 45},
{"id": 94, "name": "Frooti Mango Drink 1L", "icon": "🧃", "category": "beverages", "base_price": 65},
{"id": 95, "name": "Real Orange Juice 1L", "icon": "🧃", "category": "beverages", "base_price": 110},

{"id": 96, "name": "Handwash 250ml", "icon": "🧴", "category": "cleaning", "base_price": 85},
{"id": 97, "name": "Toilet Paper Roll", "icon": "🧻", "category": "cleaning", "base_price": 60},
{"id": 98, "name": "Floor Cleaner 1L", "icon": "🧴", "category": "cleaning", "base_price": 150},
{"id": 99, "name": "Garbage Bags Pack", "icon": "🗑️", "category": "cleaning", "base_price": 70},
{"id": 100, "name": "Air Freshener Spray", "icon": "🌸", "category": "cleaning", "base_price": 180}]

PLATFORMS = [
    {
        "name": "Blinkit",
        "color": "#f5c400",
        "delivery": "10–20 min",
        "multipliers": [0.95, 1.02, 1.00, 0.98, 1.03, 0.96],
    },
    {
        "name": "Zepto",
        "color": "#8b5cf6",
        "delivery": "10 min",
        "multipliers": [1.00, 0.97, 1.03, 0.95, 0.99, 1.04],
    },
    {
        "name": "Instamart",
        "color": "#f97316",
        "delivery": "20–30 min",
        "multipliers": [1.04, 1.01, 0.94, 1.02, 0.96, 1.00],
    },
    {
        "name": "BigBasket",
        "color": "#22c55e",
        "delivery": "2–4 hrs",
        "multipliers": [0.98, 1.05, 1.02, 0.99, 1.01, 0.97],
    },
]


#apis

@app.route("/api/items", methods=["GET"])
def get_items():
    """Return all grocery items, optionally filtered by category or search query."""
    category = request.args.get("category", "all")
    query = request.args.get("q", "").lower()

    result = ITEMS
    if category != "all":
        result = [i for i in result if i["category"] == category]
    if query:
        result = [i for i in result if query in i["name"].lower()]

    return jsonify({"items": result, "total": len(result)})


@app.route("/api/compare", methods=["POST"])
def compare_prices():
    """
    Accept a cart and return platform-by-platform price comparison.

    Request body:
    {
      "cart": [
        {"id": 1, "name": "Amul Milk 500ml", "price": 28, "qty": 2},
        ...
      ]
    }
    """
    data = request.get_json()
    if not data or "cart" not in data:
        return jsonify({"error": "cart is required"}), 400

    cart = data["cart"]
    if not cart:
        return jsonify({"error": "cart is empty"}), 400

    # Calculate base total from cart
    base_total = sum(item["price"] * item["qty"] for item in cart)
    num_items = sum(item["qty"] for item in cart)

    # Seed for deterministic-ish variance per cart
    seed = sum(item["id"] * item["qty"] for item in cart)

    results = []
    for i, platform in enumerate(PLATFORMS):
        mul_index = (seed + i * 3) % len(platform["multipliers"])
        multiplier = platform["multipliers"][mul_index]
        # small variation based on cart composition
        multiplier *= 1 + math.sin(i * seed * 0.13) * 0.018
        platform_total = round(base_total * multiplier)

        results.append({
            "name": platform["name"],
            "color": platform["color"],
            "delivery": platform["delivery"],
            "total": platform_total,
        })

    # Sort cheapest first
    results.sort(key=lambda x: x["total"])

    best = results[0]["total"]
    worst = results[-1]["total"]
    savings = worst - best

    # Add rank metadata
    medals = ["🥇", "🥈", "🥉", "4️⃣"]
    for idx, r in enumerate(results):
        r["rank"] = idx + 1
        r["medal"] = medals[idx]
        r["is_best"] = idx == 0
        r["savings_vs_best"] = r["total"] - best
        pct = round(((r["total"] - best) / best) * 100) if best > 0 else 0
        r["pct_more"] = pct
        bar_width = 20 if idx == 0 else round(20 + ((r["total"] - best) / (worst - best + 0.01)) * 75)
        r["bar_width"] = bar_width

    return jsonify({
        "results": results,
        "summary": {
            "base_total": base_total,
            "best_price": best,
            "worst_price": worst,
            "max_savings": savings,
            "num_items": num_items,
            "best_platform": results[0]["name"],
        }
    })


@app.route("/api/categories", methods=["GET"])
def get_categories():
    """Return all available categories."""
    cats = list(dict.fromkeys(i["category"] for i in ITEMS))
    return jsonify({"categories": ["all"] + cats})


@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "BestPrice API is running 🚀"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)  # host="0.0.0.0" makes it accessible on your local network (phone, tablet, etc.)
