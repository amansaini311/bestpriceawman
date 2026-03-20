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
    {"id": 401, "name": "Lizol Citrus Floor Cleaner 500ml", "icon": "🧽", "category": "cleaning", "base_price": 105},
    {"id": 402, "name": "Lizol Lavender Floor Cleaner 1L", "icon": "🧽", "category": "cleaning", "base_price": 190},
    {"id": 403, "name": "Lizol Jasmine Floor Cleaner 1L", "icon": "🧽", "category": "cleaning", "base_price": 195},
    
    {"id": 404, "name": "Harpic Power Plus Toilet Cleaner 1L", "icon": "🚽", "category": "cleaning", "base_price": 175},
    {"id": 405, "name": "Harpic Bathroom Cleaner 500ml", "icon": "🚿", "category": "cleaning", "base_price": 120},
    
    {"id": 406, "name": "Domex Ocean Fresh Toilet Cleaner 1L", "icon": "🚽", "category": "cleaning", "base_price": 170},
    {"id": 407, "name": "Domex Lime Fresh Toilet Cleaner 750ml", "icon": "🚽", "category": "cleaning", "base_price": 140},
    
    {"id": 408, "name": "Colin Glass Cleaner Spray 500ml", "icon": "🪟", "category": "cleaning", "base_price": 115},
    {"id": 409, "name": "Colin Lemon Surface Cleaner 500ml", "icon": "🪟", "category": "cleaning", "base_price": 120},
    
    {"id": 410, "name": "Vim Dishwash Liquid Lemon 750ml", "icon": "🍽️", "category": "cleaning", "base_price": 160},
    {"id": 411, "name": "Vim Dishwash Liquid Refill 1L", "icon": "🍽️", "category": "cleaning", "base_price": 180},
    
    {"id": 412, "name": "Dettol Antiseptic Liquid 500ml", "icon": "🧴", "category": "cleaning", "base_price": 190},
    {"id": 413, "name": "Dettol Surface Disinfectant Spray 450ml", "icon": "🧴", "category": "cleaning", "base_price": 210},
    
    {"id": 414, "name": "Cif Cream Surface Cleaner 500ml", "icon": "🧽", "category": "cleaning", "base_price": 180},
    {"id": 415, "name": "Phenyl Floor Cleaner 1L", "icon": "🧽", "category": "cleaning", "base_price": 120},
    
    {"id": 416, "name": "Kitchen Degreaser Spray 500ml", "icon": "🧽", "category": "cleaning", "base_price": 160},
    {"id": 417, "name": "Tap & Tile Cleaner Spray 500ml", "icon": "🚿", "category": "cleaning", "base_price": 150},
    
    {"id": 418, "name": "Steel Scrub Pads Pack", "icon": "🧽", "category": "cleaning", "base_price": 40},
    {"id": 419, "name": "Microfiber Cleaning Cloth Pack", "icon": "🧽", "category": "cleaning", "base_price": 90},
    {"id": 420, "name": "Floor Wiper", "icon": "🧹", "category": "cleaning", "base_price": 120},

    {"id": 45, "name": "Amul Vanilla Ice Cream 1L", "icon": "🍦", "category": "icecream", "base_price": 180},
    {"id": 46, "name": "Amul Butterscotch Ice Cream 1L", "icon": "🍦", "category": "icecream", "base_price": 185},
    {"id": 301, "name": "Amul Vanilla Ice Cream 750ml", "icon": "🍦", "category": "icecream", "base_price": 150},
    {"id": 302, "name": "Amul Strawberry Ice Cream 750ml", "icon": "🍦", "category": "icecream", "base_price": 155},
    {"id": 303, "name": "Amul Mango Ice Cream 750ml", "icon": "🍦", "category": "icecream", "base_price": 160},
    
    {"id": 304, "name": "Kwality Walls Cornetto Chocolate Cone", "icon": "🍦", "category": "icecream", "base_price": 45},
    {"id": 305, "name": "Kwality Walls Cornetto Butterscotch Cone", "icon": "🍦", "category": "icecream", "base_price": 45},
    {"id": 306, "name": "Kwality Walls Cornetto Double Chocolate", "icon": "🍦", "category": "icecream", "base_price": 50},
    
    {"id": 307, "name": "Kwality Walls Magnum Classic Bar", "icon": "🍦", "category": "icecream", "base_price": 90},
    {"id": 308, "name": "Kwality Walls Magnum Almond Bar", "icon": "🍦", "category": "icecream", "base_price": 95},
    {"id": 309, "name": "Kwality Walls Magnum Chocolate Truffle", "icon": "🍦", "category": "icecream", "base_price": 100},
    
    {"id": 310, "name": "Vadilal American Nuts Ice Cream 1L", "icon": "🍦", "category": "icecream", "base_price": 220},
    {"id": 311, "name": "Vadilal Rajbhog Ice Cream 1L", "icon": "🍦", "category": "icecream", "base_price": 210},
    {"id": 312, "name": "Vadilal Chocolate Ice Cream 1L", "icon": "🍦", "category": "icecream", "base_price": 205},
    
  
    {"id": 314, "name": "Mother Dairy Mango Ice Cream 1L", "icon": "🍦", "category": "icecream", "base_price": 205},
    {"id": 315, "name": "Mother Dairy Butterscotch Ice Cream 1L", "icon": "🍦", "category": "icecream", "base_price": 215},
    
    {"id": 316, "name": "Naturals Tender Coconut Ice Cream 500ml", "icon": "🍦", "category": "icecream", "base_price": 280},
    {"id": 317, "name": "Naturals Sitaphal Ice Cream 500ml", "icon": "🍦", "category": "icecream", "base_price": 300},
    {"id": 318, "name": "Naturals Mango Ice Cream 500ml", "icon": "🍦", "category": "icecream", "base_price": 290},
    
    {"id": 319, "name": "Havmor Premium Vanilla Ice Cream 1L", "icon": "🍦", "category": "icecream", "base_price": 180},
    {"id": 320, "name": "Havmor Dry Fruit Malai Ice Cream 750ml", "icon": "🍦", "category": "icecream", "base_price": 250},
    {"id": 321, "name": "Havmor Shahi Kesar Ice Cream 750ml", "icon": "🍦", "category": "icecream", "base_price": 300},
    {"id": 322, "name": "Havmor Nutty Belgian Dark Chocolate Ice Cream 750ml", "icon": "🍦", "category": "icecream", "base_price": 285},
    {"id": 323, "name": "Havmor Mocha Brownie Fudge Ice Cream 750ml", "icon": "🍦", "category": "icecream", "base_price": 290},
    {"id": 324, "name": "Havmor American Mud Cake Ice Cream 750ml", "icon": "🍦", "category": "icecream", "base_price": 300},
    {"id": 325, "name": "Havmor Rajwadi Kulfi Falooda Ice Cream 750ml", "icon": "🍦", "category": "icecream", "base_price": 300},
    {"id": 326, "name": "Havmor Maple Walnut Praline Ice Cream 750ml", "icon": "🍦", "category": "icecream", "base_price": 280},
    {"id": 327, "name": "Havmor Rolled Oats Cranberry Nuts Ice Cream 750ml", "icon": "🍦", "category": "icecream", "base_price": 250},
    {"id": 328, "name": "Havmor Sitafal Ice Cream 750ml", "icon": "🍦", "category": "icecream", "base_price": 325},
    {"id": 329, "name": "Havmor Mahabaleshwar Strawberry Ice Cream 500ml", "icon": "🍦", "category": "icecream", "base_price": 200},
    {"id": 330, "name": "Havmor Kulfi Ice Cream 1L", "icon": "🍦", "category": "icecream", "base_price": 300},
    {"id": 331, "name": "Havmor Choco Brownie Ice Cream 750ml", "icon": "🍦", "category": "icecream", "base_price": 260},
    {"id": 332, "name": "Havmor Hazelnut Chiffon Ice Cream 1L", "icon": "🍦", "category": "icecream", "base_price": 300},
    {"id": 333, "name": "Amul Rajbhog Ice Cream 1L", "icon": "🍦", "category": "icecream", "base_price": 210},
    {"id": 334, "name": "Amul Chocolate Magic Ice Cream 1L", "icon": "🍦", "category": "icecream", "base_price": 220},
    {"id": 335, "name": "Amul Kesar Pista Ice Cream 1L", "icon": "🍦", "category": "icecream", "base_price": 215},
    
    {"id": 336, "name": "Vadilal Rajbhog Ice Cream 1L", "icon": "🍦", "category": "icecream", "base_price": 220},
    {"id": 337, "name": "Vadilal American Nuts Ice Cream 1L", "icon": "🍦", "category": "icecream", "base_price": 225},
    {"id": 338, "name": "Vadilal Butterscotch Ice Cream 1L", "icon": "🍦", "category": "icecream", "base_price": 210},
    
    {"id": 339, "name": "Mother Dairy Cookie Crum Ice Cream 700ml", "icon": "🍦", "category": "icecream", "base_price": 190},
    {"id": 340, "name": "Mother Dairy Chocolate Ice Cream 1L", "icon": "🍦", "category": "icecream", "base_price": 205},
    
    {"id": 341, "name": "Cream Bell Crunchy Butterscotch Ice Cream 700ml", "icon": "🍦", "category": "icecream", "base_price": 230},
    {"id": 342, "name": "Cream Bell Chocolate Ice Cream 700ml", "icon": "🍦", "category": "icecream", "base_price": 220},

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
    {"id": 214, "name": "Clean & Clear Foaming Face Wash 100ml", "icon": "🧴", "category": "skincare", "base_price": 150},
    {"id": 215, "name": "Clean & Clear Foaming Face Wash 150ml", "icon": "🧴", "category": "skincare", "base_price": 210},
    
    {"id": 216, "name": "Garnier Men Turbo Bright Face Wash 100g", "icon": "🧴", "category": "skincare", "base_price": 180},
    {"id": 217, "name": "Garnier Men Turbo Bright Face Wash 150g", "icon": "🧴", "category": "skincare", "base_price": 240},
    
    {"id": 218, "name": "Vaseline Deep Moisture Lotion 200ml", "icon": "🧴", "category": "skincare", "base_price": 280},
    {"id": 219, "name": "Vaseline Deep Moisture Lotion 400ml", "icon": "🧴", "category": "skincare", "base_price": 520},
    
    {"id": 220, "name": "Lakme Peach Milk Moisturiser 120ml", "icon": "🧴", "category": "skincare", "base_price": 210},
    {"id": 221, "name": "Lakme Peach Milk Moisturiser 200ml", "icon": "🧴", "category": "skincare", "base_price": 340},
    
    {"id": 222, "name": "Biotique Bio Honey Gel Face Wash 120ml", "icon": "🧴", "category": "skincare", "base_price": 180},
    {"id": 223, "name": "Biotique Morning Nectar Moisturiser 120ml", "icon": "🧴", "category": "skincare", "base_price": 220},
    
    {"id": 224, "name": "Mamaearth Vitamin C Face Wash 100ml", "icon": "🧴", "category": "skincare", "base_price": 260},
    {"id": 225, "name": "Mamaearth Ubtan Face Wash 100ml", "icon": "🧴", "category": "skincare", "base_price": 250},
    
    {"id": 226, "name": "Minimalist Vitamin C Serum 10% 30ml", "icon": "🧴", "category": "skincare", "base_price": 699},
    {"id": 227, "name": "Minimalist Niacinamide Serum 10% 30ml", "icon": "🧴", "category": "skincare", "base_price": 599},
    
    {"id": 228, "name": "Dot & Key Vitamin C Face Wash 100ml", "icon": "🧴", "category": "skincare", "base_price": 295},
    {"id": 229, "name": "Dot & Key Watermelon Cooling Gel 50g", "icon": "🧴", "category": "skincare", "base_price": 495},
    
    {"id": 230, "name": "Dove Deep Moisture Body Wash 190ml", "icon": "🧴", "category": "skincare", "base_price": 240},
    {"id": 231, "name": "Dove Deep Moisture Body Wash 400ml", "icon": "🧴", "category": "skincare", "base_price": 480},
    {"id": 232, "name": "Lotus Herbals Safe Sun Sunscreen SPF50 50g", "icon": "🧴", "category": "skincare", "base_price": 475},
    {"id": 233, "name": "Lotus Herbals Safe Sun Sunscreen SPF50 100g", "icon": "🧴", "category": "skincare", "base_price": 695},
    
    {"id": 234, "name": "VLCC De Tan Face Wash 100ml", "icon": "🧴", "category": "skincare", "base_price": 190},
    {"id": 235, "name": "VLCC De Tan Scrub 80g", "icon": "🧴", "category": "skincare", "base_price": 225},
    
    {"id": 236, "name": "Plum Green Tea Face Wash 100ml", "icon": "🧴", "category": "skincare", "base_price": 345},
    {"id": 237, "name": "Plum Green Tea Mattifying Moisturizer 50ml", "icon": "🧴", "category": "skincare", "base_price": 470},
    
    {"id": 238, "name": "WOW Skin Science Aloe Vera Gel 150ml", "icon": "🧴", "category": "skincare", "base_price": 299},
    {"id": 239, "name": "WOW Vitamin C Face Wash 100ml", "icon": "🧴", "category": "skincare", "base_price": 320},
    
    {"id": 240, "name": "The Derma Co 1% Hyaluronic Sunscreen 50g", "icon": "🧴", "category": "skincare", "base_price": 499},
    {"id": 241, "name": "The Derma Co Salicylic Acid Face Wash 100ml", "icon": "🧴", "category": "skincare", "base_price": 349},
    
    {"id": 242, "name": "Olay Total Effects Day Cream 50g", "icon": "🧴", "category": "skincare", "base_price": 799},
    {"id": 243, "name": "Olay Natural White Cream 50g", "icon": "🧴", "category": "skincare", "base_price": 699},
    
    {"id": 244, "name": "L'Oreal Paris Revitalift Day Cream 50ml", "icon": "🧴", "category": "skincare", "base_price": 999},
    {"id": 245, "name": "L'Oreal Paris Hyaluron Moisture Cream 50ml", "icon": "🧴", "category": "skincare", "base_price": 849},
    
    {"id": 246, "name": "Simple Kind To Skin Refreshing Face Wash 150ml", "icon": "🧴", "category": "skincare", "base_price": 385},
    {"id": 247, "name": "Simple Hydrating Light Moisturiser 125ml", "icon": "🧴", "category": "skincare", "base_price": 465},
    
    {"id": 248, "name": "Aroma Magic Neem & Tea Tree Face Wash 100ml", "icon": "🧴", "category": "skincare", "base_price": 220},
    {"id": 249, "name": "Aroma Magic Aloe Vera Gel 100ml", "icon": "🧴", "category": "skincare", "base_price": 210},
    
    {"id": 250, "name": "Khadi Natural Sandalwood Face Wash 100ml", "icon": "🧴", "category": "skincare", "base_price": 210},
    {"id": 251, "name": "Khadi Natural Rose Water Toner 210ml", "icon": "🧴", "category": "skincare", "base_price": 190},
    {"id": 501, "name": "Aavin Premium Full Cream Milk 500ml", "icon": "🥛", "category": "dairy", "base_price": 30},
    {"id": 502, "name": "Aavin Nice Toned Milk 500ml", "icon": "🥛", "category": "dairy", "base_price": 22},
    {"id": 503, "name": "Aavin Green Magic Standardised Milk 500ml", "icon": "🥛", "category": "dairy", "base_price": 24},
    {"id": 504, "name": "Aavin Delite Homogenised Milk 500ml", "icon": "🥛", "category": "dairy", "base_price": 26},
    
    {"id": 505, "name": "Aavin Curd 500g", "icon": "🫙", "category": "dairy", "base_price": 35},
    {"id": 506, "name": "Aavin Premium Curd 200g", "icon": "🫙", "category": "dairy", "base_price": 20},
    
    {"id": 507, "name": "Aavin Butter 100g", "icon": "🧈", "category": "dairy", "base_price": 70},
    {"id": 508, "name": "Aavin Ghee 500ml", "icon": "🧈", "category": "dairy", "base_price": 350},
    
    {"id": 509, "name": "Aavin Paneer 200g", "icon": "🧀", "category": "dairy", "base_price": 110},
    {"id": 510, "name": "Aavin Paneer 500g", "icon": "🧀", "category": "dairy", "base_price": 275},
    
    {"id": 511, "name": "Amul Cow Milk 500ml", "icon": "🥛", "category": "dairy", "base_price": 30},
    {"id": 512, "name": "Amul Gold Milk 500ml", "icon": "🥛", "category": "dairy", "base_price": 35},
    {"id": 513, "name": "Amul Slim n Trim Milk 500ml", "icon": "🥛", "category": "dairy", "base_price": 26},
    
    {"id": 514, "name": "Amul Fresh Paneer 200g", "icon": "🧀", "category": "dairy", "base_price": 90},
    {"id": 515, "name": "Amul Paneer 1kg", "icon": "🧀", "category": "dairy", "base_price": 390},
    
    {"id": 516, "name": "Amul Cheese Cubes 200g", "icon": "🧀", "category": "dairy", "base_price": 120},
    {"id": 517, "name": "Amul Cheese Block 200g", "icon": "🧀", "category": "dairy", "base_price": 110},
    
    {"id": 518, "name": "Milky Mist Paneer 200g", "icon": "🧀", "category": "dairy", "base_price": 85},
    {"id": 519, "name": "Milky Mist Curd 400g", "icon": "🫙", "category": "dairy", "base_price": 45},
    {"id": 520, "name": "Milky Mist Cheese Slices", "icon": "🧀", "category": "dairy", "base_price": 130},
    
    {"id": 521, "name": "Nandini Toned Milk 500ml", "icon": "🥛", "category": "dairy", "base_price": 25},
    {"id": 522, "name": "Nandini Curd 500g", "icon": "🫙", "category": "dairy", "base_price": 30},
    {"id": 523, "name": "Nandini Paneer 200g", "icon": "🧀", "category": "dairy", "base_price": 85},
    
    {"id": 524, "name": "Mother Dairy Full Cream Milk 500ml", "icon": "🥛", "category": "dairy", "base_price": 32},
    {"id": 525, "name": "Mother Dairy Paneer 200g", "icon": "🧀", "category": "dairy", "base_price": 95},
    {"id": 526, "name": "Mother Dairy Butter 100g", "icon": "🧈", "category": "dairy", "base_price": 65}]

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
