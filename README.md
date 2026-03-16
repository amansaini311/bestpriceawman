# 🛒 BestPrice

> Compare grocery prices across Blinkit, Zepto, Swiggy Instamart & BigBasket — all in one cart.

BestPrice lets you add grocery items once and instantly shows which app gives you the cheapest total. Built as a personal side project to stop overpaying for the same basket every week.

---

## 📁 Project Structure

```
bestprice/
├── frontend/
│   └── index.html        ← the entire UI (HTML + CSS + JS)
├── backend/
│   ├── app.py            ← Flask API (Python)
│   └── requirements.txt  ← Python dependencies
└── README.md
```

---

## 🚀 Running Locally

### 1. Start the backend (Python / Flask)

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Flask will start on **http://localhost:5000**

### 2. Open the frontend

Just open `frontend/index.html` in your browser. That's it — no build step, no npm, nothing.

> Make sure the backend is running first, otherwise the item list won't load.

---

## 🔌 API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/api/items` | Get all grocery items (supports `?category=dairy&q=milk`) |
| POST | `/api/compare` | Compare cart prices across all platforms |
| GET | `/api/categories` | List all categories |

### Example: Compare prices

**POST** `/api/compare`

```json
{
  "cart": [
    { "id": 1, "name": "Amul Milk 500ml", "price": 28, "qty": 2 },
    { "id": 7, "name": "Tomatoes 500g", "price": 33, "qty": 1 }
  ]
}
```

**Response:**
```json
{
  "results": [
    { "name": "Blinkit", "total": 84, "rank": 1, "is_best": true, "medal": "🥇" },
    { "name": "Zepto",   "total": 89, "rank": 2, "is_best": false, "medal": "🥈" },
    ...
  ],
  "summary": {
    "best_price": 84,
    "max_savings": 12,
    "best_platform": "Blinkit",
    "num_items": 3
  }
}
```

---

## ⚠️ Note on Prices

Right now prices are **simulated** using multipliers per platform. Real-time pricing would require scraping each app's API — which is the next step! Contributions welcome.

---

## 🛠️ Tech Stack

- **Frontend** — plain HTML, CSS, JavaScript. No frameworks.
- **Backend** — Python + Flask + flask-cors

---

## 📬 Contributing

Pull requests are welcome. If you figure out how to plug in real prices from any of these apps, please open a PR — that's the dream!

---

*built with ☕ and a lot of googling*
