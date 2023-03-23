import os
from datetime import datetime
from flask import Flask, redirect, render_template, request, send_from_directory, url_for, flash , g
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import session
from sqlite3 import dbapi2 as sqlite3
from database.db import create_db, Product
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secretkey'
app.config['UPLOAD_FOLDER'] = 'static'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])

db = SQLAlchemy(app)
DATABASE = 'flask.db'
app.debug = True

def connect_db():
    return sqlite3.connect(DATABASE)


create_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/indexzh")
def indexzh():
    return render_template("indexzh.html")

@app.route("/products")
def products():
    conn = sqlite3.connect('flask.db')
    c = conn.cursor()
    c.execute("SELECT * FROM product")
    products = c.fetchall()
    conn.close()
    return render_template('products.html', products=products)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route("/productszh")
def productszh():
    conn = sqlite3.connect('flask.db')
    c = conn.cursor()
    c.execute("SELECT * FROM product")
    products = c.fetchall()
    conn.close()
    return render_template('productszh.html', products=products)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/cart')
def cart():
    conn = sqlite3.connect('flask.db')
    c = conn.cursor()
    c.execute("SELECT cart.id, product.name, product.price, cart.quantity, product.price * cart.quantity FROM cart INNER JOIN product ON cart.product_id = product.id")
    cart_items = c.fetchall()
    c.execute("SELECT SUM(product.price * cart.quantity) FROM cart INNER JOIN product ON cart.product_id = product.id")
    total_price = c.fetchone()[0]
    conn.close()
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/contactzh")
def contactzh():
    return render_template("contactzh.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('flask.db')
        conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
        conn.commit()
        conn.close()
        return redirect(url_for('account'))
    return render_template('register.html')

@app.route('/registerzh', methods=['GET', 'POST'])
def registerzh():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('flask.db')
        conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
        conn.commit()
        conn.close()
        return redirect(url_for('account'))
    return render_template('registerzh.html')


@app.route('/account', methods=['GET', 'POST'])
def account():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('flask.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
        user = cur.fetchone()
        conn.close()
        if user:
            return redirect(url_for('index'))
        else:
            error = 'Invalid email or password. Please try again.'
            return render_template('account.html', error=error)
    return render_template('account.html')

@app.route('/accountzh', methods=['GET', 'POST'])
def accountzh():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('flask.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
        user = cur.fetchone()
        conn.close()
        if user:
            return redirect(url_for('indexzh'))
        else:
            error = '無效的電子郵件或密碼。 請再試一次。'
            return render_template('accountzh.html', error=error)
    return render_template('accountzh.html')

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        # get form data
        name = request.form['name']
        namezh = request.form['namezh']
        description = request.form['description']
        descriptionzh = request.form['descriptionzh']
        price = request.form['price']
        image = request.files['image']

        # save image file
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], 'images', filename))

        # insert product into database
        conn = sqlite3.connect('flask.db')
        c = conn.cursor()
        c.execute('INSERT INTO product (name, namezh, description, descriptionzh, price, image) VALUES (?, ?, ?, ?, ?, ?)', (name, namezh, description, descriptionzh, price, filename))
        conn.commit()
        conn.close()

        return redirect(url_for('products'))
    else:
        return render_template('add_product.html')

@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    product_id = request.form['product_id']
    quantity = int(request.form['quantity'])

    conn = sqlite3.connect('flask.db')
    c = conn.cursor()
    c.execute("SELECT * FROM cart WHERE product_id = ?", (product_id,))
    cart_item = c.fetchone()
    if cart_item:
        new_quantity = cart_item[2] + quantity
        c.execute("UPDATE cart SET quantity = ? WHERE id = ?", (new_quantity, cart_item[0]))
    else:
        c.execute("INSERT INTO cart (product_id, quantity) VALUES (?, ?)", (product_id, quantity))
    conn.commit()
    conn.close()

    return redirect(url_for('cart'))

@app.route('/update-cart', methods=['POST'])
def update_cart():
    cart_id = request.form['cart_id']
    quantity = int(request.form['quantity'])

    conn = sqlite3.connect('flask.db')
    c = conn.cursor()
    if quantity > 0:
        c.execute("UPDATE cart SET quantity = ? WHERE id = ?", (quantity, cart_id))
    else:
        c.execute("DELETE FROM cart WHERE id = ?", (cart_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('cart'))

if __name__ == "__main__": 
    app.run(debug=True)

