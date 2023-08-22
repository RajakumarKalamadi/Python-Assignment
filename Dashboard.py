from flask import Flask, request, jsonify

app = Flask(__name__)

users = []

@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    users.append(data)
    return jsonify({"message": "User registered successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
# Add this to the existing code
@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    for user in users:
        if user['username'] == data['username'] and user['password'] == data['password']:
            return jsonify({"message": "Login successful!"})
    return jsonify({"message": "Invalid username or password"})
# Add this to the existing code
@app.route('/upload_products', methods=['POST'])
def upload_products():
    # Here, you would handle the CSV file upload and parsing
    # You can use libraries like pandas to handle CSV data
    # After parsing, save the product details to a database or a list
    return jsonify({"message": "Products uploaded successfully!"})
# Add this to the existing code
products = []

@app.route('/review_product', methods=['POST'])
def review_product():
    data = request.get_json()
    product_id = data['product_id']
    rating = data['rating']
    review = data['review']
    # You would typically associate reviews with products in your database
    # For this example, let's assume products are stored in the 'products' list
    products[product_id]['reviews'].append({"rating": rating, "review": review})
    return jsonify({"message": "Review added successfully!"})
# Add this to the existing code
@app.route('/get_products', methods=['GET'])
def get_products():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    sort_by = request.args.get('sort_by', 'rating')

    # Here, you would retrieve and paginate products from the database
    # You can use libraries like SQLAlchemy for database interactions
    # For this example, let's assume products are stored in the 'products' list

    sorted_products = sorted(products, key=lambda x: x.get(sort_by, 0), reverse=True)
    paginated_products = sorted_products[(page - 1) * per_page:page * per_page]

    return jsonify({"products": paginated_products})
# Continuing from the previous code snippets

# Define a Product class for better organization
class Product:
    def __init__(self, name, barcode, brand, description, price, available):
        self.name = name
        self.barcode = barcode
        self.brand = brand
        self.description = description
        self.price = price
        self.available = available
        self.reviews = []

# Use a list to store product instances
products = []

# Add sample products to the list
products.append(Product("Product 1", "34567890", "Brand 1", "This is sample description", 200, True))
products.append(Product("Product 2", "4567890", "Brand 2", "This is sample description", 100, False))
# Add more products...

# API to add a review for a product
@app.route('/review_product', methods=['POST'])
def review_product():
    data = request.get_json()
    product_id = data['product_id']
    rating = data['rating']
    review = data['review']
    
    if product_id < len(products):
        products[product_id].reviews.append({"rating": rating, "review": review})
        return jsonify({"message": "Review added successfully!"})
    else:
        return jsonify({"message": "Invalid product ID"}), 400

# API to get paginated and sorted products
@app.route('/get_products', methods=['GET'])
def get_products():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    sort_by = request.args.get('sort_by', 'rating')

    if sort_by not in ["rating", "price"]:
        return jsonify({"message": "Invalid sort parameter"}), 400

    sorted_products = sorted(products, key=lambda x: getattr(x, sort_by), reverse=True)
    paginated_products = sorted_products[(page - 1) * per_page:page * per_page]

    product_data = []
    for product in paginated_products:
        product_info = {
            "name": product.name,
            "barcode": product.barcode,
            "brand": product.brand,
            "description": product.description,
            "price": product.price,
            "available": product.available,
            "reviews": product.reviews
        }
        product_data.append(product_info)

    return jsonify({"products": product_data})

if __name__ == '__main__':
    app.run(debug=True)
