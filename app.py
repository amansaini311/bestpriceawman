from flask import Flask, jsonify, request
from flask_cors import CORS
import math

app = Flask(__name__)
CORS(app)

# ── Grocery item database ──────────────────────────────────────────────

ITEMS = [
    {"id": 1, "name": "Amul Milk 500ml", "icon": "🥛", "category": "dairy", "base_price": 36},
    {"id": 2, "name": "Amul Butter 100g", "icon": "🧈", "category": "dairy", "base_price": 60},
    {"id": 3, "name": "Curd 400g", "icon": "🫙", "category": "dairy", "base_price": 45},
    {"id": 4, "name": "Paneer 200g", "icon": "🧀", "category": "dairy", "base_price": 95},
    {"id": 5, "name": "Amul Cheese Slices", "icon": "🧀", "category": "dairy", "base_price": 125},
    {"id": 6, "name": "Fresh Cream 200ml", "icon": "🥛", "category": "dairy", "base_price": 70},

    {"id": 7, "name": "Tomatoes 500g", "icon": "🍅", "category": "produce", "base_price": 35},
    {"id": 8, "name": "Onions 1kg", "icon": "🧅", "category": "produce", "base_price": 40},
    {"id": 9, "name": "Potatoes 1kg", "icon": "🥔", "category": "produce", "base_price": 38},
    {"id": 10, "name": "Spinach 250g", "icon": "🥬", "category": "produce", "base_price": 30},
    {"id": 11, "name": "Bananas 6 pcs", "icon": "🍌", "category": "produce", "base_price": 50},
    {"id": 12, "name": "Apples 4 pcs", "icon": "🍎", "category": "produce", "base_price": 110},

    {"id": 17, "name": "Basmati Rice 1kg", "icon": "🍚", "category": "staples", "base_price": 120},
    {"id": 18, "name": "Wheat Atta 5kg", "icon": "🌾", "category": "staples", "base_price": 265},
    {"id": 19, "name": "Tata Salt 1kg", "icon": "🧂", "category": "staples", "base_price": 28},
    {"id": 20, "name": "Toor Dal 500g", "icon": "🫘", "category": "staples", "base_price": 80},
    {"id": 21, "name": "Sunflower Oil 1L", "icon": "🫙", "category": "staples", "base_price": 155},

    {"id": 26, "name": "Lays Classic 50g", "icon": "🥔", "category": "snacks", "base_price": 20},
    {"id": 27, "name": "Parle-G 200g", "icon": "🍪", "category": "snacks", "base_price": 22},
    {"id": 28, "name": "KitKat 4-finger", "icon": "🍫", "category": "chocolate", "base_price": 55},

    {"id": 33, "name": "Nescafe Coffee 50g", "icon": "☕", "category": "beverages", "base_price": 135},
    {"id": 34, "name": "Tata Tea 250g", "icon": "🍵", "category": "beverages", "base_price": 100},

    {"id": 35, "name": "Tropicana Juice 1L", "icon": "🧃", "category": "beverages", "base_price": 115},
    {"id": 36, "name": "Red Bull 250ml", "icon": "🥤", "category": "beverages", "base_price": 120},

    {"id": 39, "name": "Surf Excel 500g", "icon": "🧺", "category": "cleaning", "base_price": 110},
    {"id": 40, "name": "Vim Dishwash 500g", "icon": "🍽️", "category": "cleaning", "base_price": 70},
    {"id": 41, "name": "Dettol Soap 75g", "icon": "🧼", "category": "cleaning", "base_price": 50},
    {"id": 42, "name": "Harpic 500ml", "icon": "🚿", "category": "cleaning", "base_price": 130},
    {"id": 43, "name": "Colgate Toothpaste 150g", "icon": "🪥", "category": "cleaning", "base_price": 95},
    {"id": 44, "name": "Head & Shoulders Shampoo 180ml", "icon": "🧴", "category": "cleaning", "base_price": 160},

    {"id": 45, "name": "Amul Vanilla Ice Cream 1L", "icon": "🍦", "category": "icecream", "base_price": 180},
    {"id": 46, "name": "Amul Butterscotch Ice Cream 1L", "icon": "🍦", "category": "icecream", "base_price": 185},

    {"id": 100, "name": "Air Freshener Spray", "icon": "🌸", "category": "cleaning", "base_price": 180},

    # Skincare
    {"id": 201, "name": "Himalaya Neem Face Wash 50ml", "icon": "🧴", "category": "skincare", "base_price": 90},
    {"id": 202, "name": "Himalaya Neem Face Wash 100ml", "icon": "🧴", "category": "skincare", "base_price": 150},
    {"id": 203, "name": "Himalaya Neem Face Wash 150ml", "icon": "🧴", "category": "skincare", "base_price": 210},

    {"id": 204, "name": "Nivea Soft Moisturising Cream 50ml", "icon": "🧴", "category": "skincare", "base_price": 95},
    {"id": 205, "name": "Nivea Soft Moisturising Cream 100ml", "icon": "🧴", "category": "skincare", "base_price": 150},
    {"id": 206, "name": "Nivea Soft Moisturising Cream 200ml", "icon": "🧴", "category": "skincare", "base_price": 290},

    {"id": 207, "name": "Pond's Super Light Gel 50g", "icon": "🧴", "category": "skincare", "base_price": 110},
    {"id": 208, "name": "Pond's Super Light Gel 147g", "icon": "🧴", "category": "skincare", "base_price": 280},

    {"id": 209, "name": "Neutrogena Ultra Sheer Sunscreen SPF50+ 30ml", "icon": "🧴", "category": "skincare", "base_price": 260},
    {"id": 210, "name": "Neutrogena Ultra Sheer Sunscreen SPF50+ 50ml", "icon": "🧴", "category": "skincare", "base_price": 430},
    {"id": 211, "name": "Neutrogena Ultra Sheer Sunscreen SPF50+ 88ml", "icon": "🧴", "category": "skincare", "base_price": 700},

    {"id": 212, "name": "Cetaphil Gentle Skin Cleanser 125ml", "icon": "🧴", "category": "skincare", "base_price": 380},
    {"id": 213, "name": "Cetaphil Gentle Skin Cleanser 250ml", "icon": "🧴", "category": "skincare", "base_price": 720},
]

# Platforms
PLATFORMS = [
    {"name": "Blinkit", "color": "#f5c400", "delivery": "10–20 min", "multipliers": [0.95,1.02,1.00,0.98,1.03,0.96]},
    {"name": "Zepto", "color": "#8b5cf6", "delivery": "10 min", "multipliers": [1.00,0.97,1.03,0.95,0.99,1.04]},
    {"name": "Instamart", "color": "#f97316", "delivery": "20–30 min", "multipliers": [1.04,1.01,0.94,1.02,0.96,1.00]},
    {"name": "BigBasket", "color": "#22c55e", "delivery": "2–4 hrs", "multipliers": [0.98,1.05,1.02,0.99,1.01,0.97]},
]

@app.route("/api/items")
def get_items():
    category = request.args.get("category", "all")
    query = request.args.get("q", "").lower()

    result = ITEMS
    if category != "all":
        result = [i for i in result if i["category"] == category]
    if query:
        result = [i for i in result if query in i["name"].lower()]

    return jsonify({"items": result, "total": len(result)})

@app.route("/api/categories")
def get_categories():
    cats = list(dict.fromkeys(i["category"] for i in ITEMS))
    return jsonify({"categories": ["all"] + cats})

@app.route("/api/compare", methods=["POST"])
def compare_prices():

    data = request.get_json()
    cart = data["cart"]

    base_total = sum(item["price"] * item["qty"] for item in cart)
    num_items = sum(item["qty"] for item in cart)

    seed = sum(item["id"] * item["qty"] for item in cart)

    results = []

    for i, platform in enumerate(PLATFORMS):

        mul_index = (seed + i*3) % len(platform["multipliers"])
        multiplier = platform["multipliers"][mul_index]
        multiplier *= 1 + math.sin(i*seed*0.13)*0.018

        platform_total = round(base_total * multiplier)

        results.append({
            "name": platform["name"],
            "color": platform["color"],
            "delivery": platform["delivery"],
            "total": platform_total
        })

    results.sort(key=lambda x: x["total"])

    best = results[0]["total"]
    worst = results[-1]["total"]
    savings = worst - best

    medals = ["🥇","🥈","🥉","4️⃣"]

    for idx,r in enumerate(results):
        r["rank"] = idx+1
        r["medal"] = medals[idx]
        r["is_best"] = idx == 0
        r["savings_vs_best"] = r["total"] - best

    return jsonify({
        "results": results,
        "summary": {
            "base_total": base_total,
            "best_price": best,
            "worst_price": worst,
            "max_savings": savings,
            "num_items": num_items,
            "best_platform": results[0]["name"]
        }
    })

@app.route("/")
def health():
    return jsonify({"status": "ok", "message": "BestPrice API running 🚀"})

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=5000)
