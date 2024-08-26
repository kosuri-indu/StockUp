from flask import Flask, request, render_template, redirect, url_for, flash
import pyrebase

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

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

@app.route('/savysaver')
def savysaver():
    return render_template('savysaver.html')

@app.route('/shelf-alert')
def shelf_alert():
    return render_template('shelf-alert.html')

@app.route('/gourmet-goals')
def gourmet_goals():
    return render_template('gourmet-goals.html')

@app.route('/look-whats-chilling')
def look_whats_chilling():
    return render_template('look-whats-chilling.html')

@app.route('/recipie-genie')
def recipie_genie():
    return render_template('recipie-genie.html')

@app.route('/calorie-crunch')
def calorie_crunch():
    return render_template('calorie-crunch.html')

@app.route('/shop-smart')
def shop_smart():
    return render_template('shop-smart.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            # Create a new user
            user = auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('home')) 
        except Exception as e:
            flash('Signup failed. Please try again.', 'error')
            return redirect(url_for('signup'))

    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('home'))  
        except Exception as e:
            flash('Login failed. Please check your credentials.', 'error')
            return redirect(url_for('signin'))

    return render_template('signin.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
