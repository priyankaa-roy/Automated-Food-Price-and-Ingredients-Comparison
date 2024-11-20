from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure MySQL
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'lionKing0'
app.config['MYSQL_DB'] = 'employee_db_sample'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Routes

@app.route('/')
def index():
    return render_template('index.html')

# from flask import render_template, redirect, url_for

@app.route('/login', methods=['POST'])
def login():
    message = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check user credentials in the database
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()
        cur.close()

        if user:
            # Redirect to the dashboard with the username
            # return render_template('dashboard.html', username=username)
            return render_template('dashboard.html', username=username)
        else:
            message = 'Invalid credentials'

    return render_template('index.html', message=message)


@app.route('/registration_form')
def registration_form():
    return render_template('registration_form.html')

@app.route('/register', methods=['POST'])
def register():
    # Get form data
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm-password']

    # Basic form validation
    if password != confirm_password:
        return "Password and Confirm Password do not match. Please try again."

    # Save user data to the database
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
    mysql.connection.commit()
    cur.close()

    return f"User {username} registered successfully!"

@app.route('/user_details', methods=['GET', 'POST'])
def user_details():
    if request.method == 'POST':
        filter_username = request.form.get('filter', '')
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, username, email FROM users WHERE username LIKE %s", (f'%{filter_username}%',))
        users = cur.fetchall()
        cur.close()
    else:
        # If it's a GET request or no filter is provided, fetch all users
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, username, email FROM users")
        users = cur.fetchall()
        cur.close()

    return render_template('user_details.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)

    