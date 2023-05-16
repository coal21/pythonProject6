from flask import Flask, render_template, request, redirect, session, url_for
from sqlalchemy import Column, Integer, String, Numeric, create_engine, text


app = Flask(__name__)
app.secret_key = 'Coal'
conn_str = "mysql://root:simplepassword@localhost/StoreDB"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()

@app.route('/', methods=['POST', 'GET'])
def create_reg():
    if request.method == 'POST':
        email = request.form['Email']
        username = request.form['username']
        password = request.form['Password']
        Job = request.form.get('Job')
        conn.execute(text(
            'INSERT INTO Users (Email, Username, Password, Job) VALUES (:email, :username, :password, :Job)'),
                {'email': email, 'username': username, 'password': password, 'Job': Job})
        conn.commit()
        products = conn.execute(text('SELECT * From Product')).fetchall()
        return render_template('index.html', username=username, products=products)
    else:
        return render_template('Register.html')

import logging
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['Email']
        password = request.form['Password']

        logging.info(f"User login attempt with email: {email}, password: {password}")

        result = conn.execute(text(
            'SELECT * FROM Users WHERE Email = :email AND Password = :password'),
            {'email': email, 'password': password})
        user = result.fetchone()
        print(user)

        if user:
            if user[3] == 'Vendor':
                session['Email'] = user[0]
                username=user[1]
                print(user[0])
                print(email)
                return redirect(url_for('display', username=username))
            elif user[3] == 'Customer':
                session['Email'] = user[0]
                username=user[1]
                print(user[0])
                print(email)
                return redirect(url_for('add_to_cart_route', username=username))
            elif user[3] == 'Admin':
                session['Email'] = user[0]
                username=user[1]
                print(user[0])
                print(email)
                return render_template('AdminPage.html', username=username)


            return redirect(url_for('base', username=user[1]))
        else:
            return render_template('login.html', error="Invalid email or password")
    else:
        return render_template('login.html')


@app.route('/Coalll', methods=['POST'])
def vendorItems():
    product_ID = request.form['product_ID']
    email = session['Email']
    title = request.form['title']
    prices = request.form['prices']
    description = request.form['description']
    image = request.form['image']
    category = request.form['category']
    inventory = request.form['inv']
    conn.execute(text(
        'INSERT INTO Product (product_ID, Email, title, prices, description, image, category, inv) VALUES (:product_ID, :email, :title, :prices, :description, :image, :category, :inventory)'),
        {'product_ID': product_ID,'email': email, 'title': title, 'prices': prices, 'description': description, 'image': image, 'category': category, 'inventory': inventory})
    conn.commit()
    return redirect('/vendor')
@app.route('/index', methods=['GET'])
def base():
    products = conn.execute(text('SELECT * From Product')).fetchall()
    return render_template('index.html', products=products)




# @app.route('/checkout', methods=['POST', 'GET'])
# def checkout():
#     if request.method == 'POST':
#         email = session['Email']
#         title = request.form['title']
#         product_ID = request.form['product_ID']
#         card_number = request.form['card_number']
#         prices = request.form['prices']
#         conn.execute(text(
#             'INSERT INTO checkout (Email, title, product_ID, card_number, prices) VALUES (:Email, :title, :product_ID, :card_number, :prices)'),
#             {'email': email, 'title': title, 'product_ID': product_ID, 'card_number': card_number, 'prices': prices })
#         conn.commit()
#     return render_template('Checkout.html')



@app.route('/vendor', methods=['GET'])
def display():
    products = conn.execute(text('SELECT * From Product')).fetchall()
    return render_template('Vendor.html', products=products)


@app.route('/index', methods=['POST'])
def add_to_cart_route():
    if request.method == 'POST':
        email = session['Email']
        title = request.form['title']
        product_ID = request.form['product_ID']
        prices = request.form['prices']
        conn.execute(text(
            'INSERT INTO cart (Email, title, product_ID, prices) VALUES (:email, :title, :product_ID, :prices)'),
            {'email': email, 'title': title, 'product_ID': product_ID, 'prices': prices})
        conn.commit()
        cart = conn.execute(text('SELECT * From cart')).fetchall()
        products = conn.execute(text('SELECT * From Product')).fetchall()
        return render_template('index.html' , cart=cart, products=products)
    else:
        cart = conn.execute(text('SELECT * From cart')).fetchall()
        products = conn.execute(text('SELECT * From Product')).fetchall()
        return render_template('index.html', products=products, cart=cart)

@app.route('/vendor/<int:product_ID>', methods=['POST'])
def delete_product(product_ID):
    # product_id = request.form['product_ID']
    conn.execute(text('DELETE FROM Product WHERE product_ID = :product_ID'), {'product_ID': product_ID})
    conn.commit()
    return render_template('Vendor.html')

# @app.route('/checkout', methods=['POST'])
# def checkout():
#     if request.method == 'POST':
#         email = session['Email']
#         title = request.form['title']
#         prices = request.form['prices']
#         product_ID = request.form['product_ID']
#         first_name = request.form['first_name']
#         last_name = request.form['last_name']
#         card_number = request.form['card_number']
#         CVV = request.form['CVV']
#         ExpDate = request.form['ExpDate']
#         conn.execute(text(
#             'INSERT INTO checkout (Email, title, prices, product_ID, first_name,last_name,card_number,CVV,ExpDate ) VALUES (:email, :title, :prices, :product_ID, :first_name, :last_name,:card_number, :CVV, :ExpDate)'),
#             {'email': email, 'title': title, 'prices': prices, 'product_ID': product_ID, 'first_name' : first_name, 'last_name' : last_name, 'card_number' : card_number, 'CVV' :CVV, 'ExpDate' :ExpDate})
#         conn.commit()


@app.route('/account', methods=['GET'])
def Accountview():
    if request.method == 'GET':
        email = session['Email']
        user = conn.execute(text(f'SELECT * From Users where Email = \'{email}\'')).fetchall()
        print(email)
        return render_template('Account.html', user=user[0])

# @app.route('/coal', methods=['GET'])
# def checkouts():
#     if request.method == 'POST':
#         email = session['Email']
#         conn.execute(text(
#             'INSERT INTO checkout (Email) VALUES (:Email)'),
#             {'email': email})
#         conn.commit()
#     products = conn.execute(text('SELECT * From cart')).fetchall()
#     return render_template('index.html', products=products)

@app.route('/CartDelete', methods=['GET', 'POST'])
def ordercart():
    if request.method == 'GET'or request.method == 'POST':
        email = session['Email']
        conn.execute(text(f'DELETE From cart where Email = \'{email}\''))
        conn.commit()
        return redirect(url_for('add_to_cart_route'))

@app.route('/review', methods=['GET', 'POST'])
def review():
    if request.method == 'POST':
        email = session['Email']
        review_text = request.form['review_text']
        rating = request.form['rating']
        conn.execute(text('INSERT INTO Review(Email, review_text, rating) VALUES (:Email, :review_text, :rating)'), {'Email': email, 'review_text': review_text, 'rating': rating})
        conn.commit()
        return render_template('thank_you.html')
    else:
        return render_template('Review.html')

@app.route('/Rdisplay', methods=['Get'])
def reviewdisplay():
    Review = conn.execute(text('SELECT * From Review')).fetchall()
    return render_template('AdminReview.HTML', Review=Review)

@app.route('/logout')
def logout():
    if 'Email' in session:
        session.pop("Email")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)