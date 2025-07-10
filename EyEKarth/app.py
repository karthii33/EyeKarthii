from flask import Flask, render_template, request, redirect, session, url_for
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this!

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client['eyekarthii_store']
users = db['users']
products = db['products']
carts = db['carts']
orders = db['orders']

bcrypt = Bcrypt(app)

# Home Page
@app.route('/')
def index():
    product_list = list(products.find())
    return render_template('index.html', products=product_list)

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        mobile = request.form['mobile']
        address = request.form['address']
        gender = request.form['gender']
        dob = request.form['dob']

        existing_user = users.find_one({'email': email})
        if existing_user:
            return "User already exists. Try logging in."

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        users.insert_one({
            'name': name,
            'email': email,
            'password': hashed_password,
            'mobile': mobile,
            'address': address,
            'gender': gender,
            'dob': dob
        })

        return redirect('/login')
    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = users.find_one({'email': email})
        if user and bcrypt.check_password_hash(user['password'], password):
            session['user'] = user['email']
            return redirect('/profile')
        return "Invalid credentials. Try again."
    return render_template('login.html')

# Profile
@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect('/login')
    user = users.find_one({'email': session['user']})
    return render_template('profile.html', user=user)

# Add to Cart
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'user' not in session:
        return redirect('/login')

    product_id = request.form['product_id']
    product = products.find_one({'_id': ObjectId(product_id)})

    if product:
        product_data = {
            'name': product['name'],
            'description': product['description'],
            'price': product['price'],
            'image_url': product.get('image_url', '')
        }
        carts.update_one(
            {'user': session['user']},
            {'$push': {'items': product_data}},
            upsert=True
        )
    return redirect('/cart')

# Buy Now
@app.route('/buy_now', methods=['POST', 'GET'])
def buy_now():
    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST' and 'confirm' not in request.form:
        session['buy_now_product'] = request.form['product_id']
        return render_template('cod_confirm.html')

    if request.method == 'POST' and request.form.get('confirm') == 'yes':
        product_id = session.pop('buy_now_product', None)
        if product_id:
            product = products.find_one({'_id': ObjectId(product_id)})
            if product:
                orders.insert_one({
                    'user': session['user'],
                    'items': [product],
                    'total': product['price'],
                    'status': 'Confirmed (Cash on Delivery)'
                })
        return redirect('/orders')

    return redirect('/')

# View Cart
@app.route('/cart')
def cart():
    if 'user' not in session:
        return redirect('/login')

    cart_data = carts.find_one({'user': session['user']}) or {'items': []}
    total = sum(item['price'] for item in cart_data['items'])
    return render_template('cart.html', cart=cart_data['items'], total=total)

# Place Order
@app.route('/place_order', methods=['GET', 'POST'])
def place_order():
    if 'user' not in session:
        return redirect('/login')

    if request.method == 'GET':
        return render_template('cod_confirm.html')

    if request.method == 'POST' and request.form.get('confirm') == 'yes':
        cart_data = carts.find_one({'user': session['user']})
        if cart_data and cart_data.get('items'):
            orders.insert_one({
                'user': session['user'],
                'items': cart_data['items'],
                'total': sum(item['price'] for item in cart_data['items']),
                'status': 'Confirmed (Cash on Delivery)'
            })
            carts.delete_one({'user': session['user']})
        return redirect('/orders')

    return redirect('/cart')

# View Orders
@app.route('/orders')
def view_orders():
    if 'user' not in session:
        return redirect('/login')

    user_orders = list(orders.find({'user': session['user']}))
    return render_template('orders.html', orders=user_orders)

# Remove from Cart
@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    if 'user' not in session:
        return redirect('/login')

    item_name = request.form['item_name']
    carts.update_one(
        {'user': session['user']},
        {'$pull': {'items': {'name': item_name}}}
    )
    return redirect('/cart')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# Seed sample products
if __name__ == '__main__':
    products.delete_many({})
    products.insert_many([
        {"name": "Sunglasses", "description": "Stylish black frame", "price": 499, "image_url": "images/sunglasses1.jpg"},
        {"name": "Contact Lens", "description": "Blue soft lens", "price": 299, "image_url": "images/contactlens.jpeg"},
        {"name": "Reading Glass", "description": "Anti-glare lens", "price": 399, "image_url": "images/eadglass.jpeg"},
        {"name": "Sports Shades", "description": "Wrap-around UV protection", "price": 599, "image_url": "images/sports.jpeg"},
        {"name": "Designer Frames", "description": "Premium acetate frame", "price": 999, "image_url": "images/desgin.jpeg"},
        {"name": "Eye Drops", "description": "Lubricant for dry eyes", "price": 149, "image_url": "images/eyedrop.jpeg"},
        {"name": "Lens Solution", "description": "Cleaning and storage", "price": 199, "image_url": "images/lensol.jpeg"},
        {"name": "Blue Light Glasses", "description": "For screen protection", "price": 449, "image_url": "images/lue.jpeg"}
    ])
    app.run(debug=True)
