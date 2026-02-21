from flask import Flask , render_template , request , redirect , session , flash # Flask is framework that runs web server
import mysql.connector # connects pyhton + mysql database

app = Flask(__name__) # flask application , like turning on the server 
app.secret_key ='restaurantapp'

def get_db():
    return mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'restaurant_db'
)

'''
Flask is telling mysql.connector — here's where the database lives (localhost),
 here's the username (root), no password, and this is the database we want to use (restaurant_db). 
 Now connect!!
'''
@app.route('/')   #in terminal it gives the link of browser
def home(): 
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('home.html')  # when clicked on link browser runs and displays the msg.

@app.route('/register' , methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['reg_email']
    password = request.form['reg_password']

    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users WHERE email=%s' ,(email,))
    existing_user = cursor.fetchone()
    
    if existing_user:
        flash('Email already registered! Please login' , 'error')
        return redirect('/')
    else:
        cursor.execute('INSERT INTO users (name , email , password) VALUES (%s, %s,%s)',(name , email , password))
        db.commit()
        flash('Account created! Please login.','success')
    db.close()
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    db = get_db()
    cursor = db.cursor(buffered=True)

    # Checks admin table first
    cursor.execute('SELECT * FROM admin WHERE email=%s AND password=%s', (email, password))
    admin_user = cursor.fetchone()

    if admin_user:
        session['user_id'] = admin_user[0]
        session['user_name'] = admin_user[1]
        session['is_admin'] = True
        db.close()
        return redirect('/dashboard')

    # Check users table
    cursor.execute('SELECT * FROM users WHERE email=%s AND password=%s', (email, password))
    user = cursor.fetchone()
    db.close()

    if user:
        session['user_id'] = user[0]
        session['user_name'] = user[1]
        session['is_admin'] = False
        return redirect('/dashboard')
    else:
        flash('Invalid email or password!', 'error')
        return redirect('/')
    
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('dashboard.html', name=session['user_name'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/categories')   
def categories(): 
    db = get_db()
    cursor = db.cursor()    # it does reading and writing like pen for database like reads data from bd and writes in bowser
    cursor.execute('SELECT * FROM  categories') #running sql in query 
    data = cursor.fetchall()  #collects all the data from execute 
    db.close()
    return render_template('categories.html' , categories = data) # putting data inside html

@app.route('/food')
def food():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM food')
    data = cursor.fetchall()
    db.close()
    return render_template('food.html', food = data)

@app.route('/orders')
def orders():
    if 'user_id' not in session:
        flash('Please login to view orders!', 'error')
        return redirect('/')
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT orders.order_id, users.name, food.name, orders.quantity, orders.order_date,food.price, (orders.quantity * food.price) as total FROM orders JOIN users ON orders.user_id = users.user_id JOIN food ON orders.food_id = food.food_id WHERE orders.user_id = %s',(session['user_id'],))
    data = cursor.fetchall()
    db.close()
    return render_template('orders.html',orders = data)

@app.route('/users')
def users():
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied!' , 'error')
        return redirect('/')
    
    db= get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users')
    data = cursor.fetchall()
    db.close()
    return render_template('users.html',users = data)

@app.route('/admin')
def admin():
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied!' , 'error')
        return redirect('/')
    
    db= get_db()
    cursor = db.cursor()

    cursor.execute('SELECT COUNT(*) FROM users')
    total_users = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM orders')
    total_orders = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM bookings')
    total_bookings = cursor.fetchone()[0]

    # All orders
    cursor.execute('''SELECT orders.order_id, users.name, food.name, 
                   orders.quantity, food.price,
                   (orders.quantity * food.price) as total,
                   orders.order_date 
                   FROM orders 
                   JOIN users ON orders.user_id = users.user_id 
                   JOIN food ON orders.food_id = food.food_id''')
    all_orders = cursor.fetchall()

     #All bookings
    cursor.execute('''SELECT bookings.booking_id, users.name, bookings.date,
                   bookings.time, bookings.guests, bookings.status
                   FROM bookings
                   JOIN users ON bookings.user_id = users.user_id''')
    all_bookings = cursor.fetchall()
    
    db.close()
    return render_template('admin.html', 
                         total_users=total_users,
                         total_orders=total_orders,
                         total_bookings=total_bookings,
                         all_orders=all_orders,
                         all_bookings=all_bookings)

@app.route('/place_order', methods=['POST'])
def place_order():
    if 'user_id' not in session:
        flash('Please login to place an order!',' error')
        return redirect('/')
    
    food_id = request.form['food_id']
    quantity = request.form['quantity']
    user_id = session['user_id']

    db= get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO orders (user_id , food_id , quantity) VALUES (%s,%s,%s)',(user_id, food_id, quantity))
    db.commit()
    db.close()

    flash('Order placed sucessfully!','success')
    return redirect('/food')

@app.route('/remove_order/<int:order_id>')
def remove_order(order_id):
    if 'user_id' not in session:
        return redirect('/')
    
    db= get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM orders WHERE order_id=%s AND user_id=%s',(order_id, session['user_id']))
    db.commit()
    db.close()

    flash("order removed!", "success")
    return redirect('/orders')

@app.route('/book_table' , methods = ['GET' , 'POST'])
def book_table():
    if 'user_id' not  in session:
        flash('Please login to book table', 'error')
        return redirect('/')
    
    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        guests = request.form['guests']
        user_id = session['user_id']

        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO bookings (user_id, date, time, guests) VALUES (%s, %s, %s, %s)',
                       (user_id, date, time, guests))
        db.commit()
        db.close()

        flash('Table booked successfull!','success')
        return redirect('/book_table')
    
    db= get_db()
    cursor = db.cursor()
    cursor.execute('SELECT bookings.booking_id , users.name, bookings.date, bookings.time, bookings.guests, bookings.status FROM  bookings JOIN users ON bookings.user_id = users.user_id WHERE  bookings.user_id =%s',(session['user_id'],))
    data = cursor.fetchall()
    db.close()
    return render_template('book_table.html' ,bookings = data)

@app.route('/cancel_booking/<int:booking_id>')
def cancel_booking(booking_id):
    if 'user_id' not in session:
        return redirect('/')
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM bookings WHERE booking_id=%s AND user_id=%s',
                   (booking_id, session['user_id']))
    db.commit()
    db.close()

    flash('Booking cancelled!', 'success')
    return redirect('/book_table')

@app.route('/add_category', methods=['POST'])
def add_category():
    if not session.get('is_admin'):
        return redirect('/')
    name = request.form['name']
    description = request.form['description']
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO categories (name, description) VALUES (%s, %s)', (name, description))
    db.commit()
    db.close()
    flash('Category added!', 'success')
    return redirect('/manage')

# DELETE CATEGORY
@app.route('/delete_category/<int:cat_id>')
def delete_category(cat_id):
    if not session.get('is_admin'):
        return redirect('/')
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM categories WHERE id=%s', (cat_id,))
    db.commit()
    db.close()
    flash('Category deleted!', 'success')
    return redirect('/manage')

# ADD FOOD
@app.route('/add_food', methods=['POST'])
def add_food():
    if not session.get('is_admin'):
        return redirect('/')
    name = request.form['name']
    price = request.form['price']
    description = request.form['description']
    cat_id = request.form['cat_id']
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO food (name, price, description, cat_id) VALUES (%s, %s, %s, %s)',
                   (name, price, description, cat_id))
    db.commit()
    db.close()
    flash('Food item added!', 'success')
    return redirect('/manage')

# DELETE FOOD
@app.route('/delete_food/<int:food_id>')
def delete_food(food_id):
    if not session.get('is_admin'):
        return redirect('/')
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM food WHERE food_id=%s', (food_id,))
    db.commit()
    db.close()
    flash('Food item deleted!', 'success')
    return redirect('/manage')

# MANAGE PAGE
@app.route('/manage')
def manage():
    if not session.get('is_admin'):
        flash('Access denied!', 'error')
        return redirect('/')
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM categories')
    categories = cursor.fetchall()
    cursor.execute('SELECT food.food_id, food.name, food.price, food.description, categories.name FROM food JOIN categories ON food.cat_id = categories.id')
    foods = cursor.fetchall()
    db.close()
    return render_template('manage.html', categories=categories, foods=foods)



if __name__ == '__main__':
    app.run(debug=True)