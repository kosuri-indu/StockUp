from flask import Flask, request, render_template, redirect, url_for, flash
import pyrebase

app = Flask(__name__)

# Firebase configuration
config = {
  "apiKey": "AIzaSyACxgHHyCly6LNi7ZSDzKNLPmavl8Y3l_E",
  "authDomain": "stock-up-7292b.firebaseapp.com",
  "projectId": "stock-up-7292b",
  "storageBucket": "stock-up-7292b.appspot.com",
  "messagingSenderId": "258250115065",
  "appId": "1:258250115065:web:5864c628e1beee634b9f28",
  "measurementId": "G-8M3Q5B6LPD",
  "databaseURL": "https://stock-up-7292b-default-rtdb.firebaseio.com/"
}

# Initialize Pyrebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

# Secret key for flash messages
app.secret_key = 'secret'

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            # Create a new user
            user = auth.create_user_with_email_and_password(email, password)
            flash('Account created successfully')
            return redirect(url_for('new'))  # Redirect to the index route
        except Exception as e:
            # Handle error if the email already exists or other errors
            flash(f'Error: {str(e)}')
            return redirect(url_for('signup'))

    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            flash('Sign in successful')
            return redirect(url_for('new'))  
        except Exception as e:
            flash(f'Error: {str(e)}')
            return redirect(url_for('signin'))

    return render_template('signin.html')

@app.route('/new', methods=['GET', 'POST'])
def new():
    return render_template('new.html')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
