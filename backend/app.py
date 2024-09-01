from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
import pyrebase
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

# Firebase Configuration
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

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

# Configure Gemini LLM
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# App Secret Key
app.secret_key = os.getenv("FLASK_SECRET_KEY", 'secret')

# ----------------------------------------
# Routes
# ----------------------------------------

@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html', title="Welcome to Stock Up")

@app.route('/home', methods=['GET', 'POST'])
def home():
    """Home page with an option to select ingredients"""
    return render_template('home.html', title="Home")

@app.route('/shelf-alert')
def shelf_alert():
    """Shelf Alert Page"""
    return render_template('shelf-alert.html', title="Shelf Alert")

@app.route('/gourmet-goals')
def gourmet_goals():
    """Gourmet Goals Page"""
    return render_template('gourmet-goals.html', title="Gourmet Goals")

@app.route('/fridgepeek')
def fridgepeek():
    """Fridge Peek Page"""
    return render_template('fridgepeek.html', title="Fridge Peek")

@app.route('/recipie-genie')
def recipie_genie():
    """Recipe Genie Page"""
    return render_template('recipie-genie.html', title="Recipe Genie")

@app.route('/shop-smart')
def shop_smart():
    """Shop Smart Page"""
    return render_template('shop-smart.html', title="Shop Smart")

# ----------------------------------------
# User Authentication (Signup/Signin)
# ----------------------------------------

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User Signup"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = auth.create_user_with_email_and_password(email, password)
            flash('Signup successful! Please log in.', 'success')
            return redirect(url_for('signin')) 
        except Exception as e:
            flash(f'Signup failed: {str(e)}', 'error')
            return redirect(url_for('signup'))

    return render_template('signup.html', title="Signup")

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    """User Signin"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))  
        except Exception as e:
            flash(f'Login failed: {str(e)}', 'error')
            return redirect(url_for('signin'))

    return render_template('signin.html', title="Signin")

# ----------------------------------------
# Recipe Generator using Gemini LLM
# ----------------------------------------
@app.route('/generate-recipes', methods=['POST'])
def generate_recipes():
    data = request.get_json()
    ingredients = data.get('ingredients', [])

    # Format ingredients for LLM prompt
    ingredients_list = ", ".join(ingredients)
    prompt = f"Generate tasty indian recipes using the following ingredients: {ingredients_list}. Separate the response using '-----------' as a divider for multiple recipes.Provide the recipes including ingredients and steps."

    try:
        # Generate the completion using the correct method
        response = genai.generate_text(prompt=prompt)  # Ensure this is the correct method

        # Print the response to understand its structure
        print("API Response:", response)

        # Extract the text from the response
        recipes_text = ""
        if hasattr(response, 'result'):
            recipes_text = response.result.strip()
        elif hasattr(response, 'candidates') and response.candidates:
            recipes_text = response.candidates[0].text.strip()  # Adjust based on actual response structure
        else:
            raise ValueError("Unexpected response format")

        # Example parsing logic
        recipes = parse_recipes(recipes_text)

        # Print recipes to terminal
        print("Generated Recipes:")
        for recipe in recipes:
            print(f"Recipe Name: {recipe['name']}")
            print(f"Ingredients: {recipe['ingredients']}")
            print(f"Steps: {recipe['steps']}")
            print("-----------")

        return jsonify({'recipes': recipes})
    
    except Exception as e:
        print(f"Error generating recipes: {e}")
        return jsonify({'error': 'Failed to generate recipes'}), 500
def parse_recipes(text):
    """
    Parses the text from the response into a list of recipe dictionaries.
    Handles cases where multiple recipes are provided, each with a name, ingredients, and steps.
    """
    recipes = []
    recipe = None
    ingredients_section = False
    steps_section = False
    
    lines = text.split('\n')
    for line in lines:
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Identify recipe name (## 1. Recipe Name format)
        if line.startswith("## "):
            if recipe:  # If a recipe already exists, append it before starting a new one
                recipes.append(recipe)
            
            # Start a new recipe
            recipe_name = line[3:].strip()  # Remove the "## " and get the recipe name
            recipe = {
                'name': recipe_name,
                'ingredients': [],
                'steps': []
            }
            ingredients_section = False
            steps_section = False

        # Identify the start of the ingredients section
        elif line.lower().startswith("### ingredients"):
            ingredients_section = True
            steps_section = False

        # Identify the start of the steps section
        elif line.lower().startswith("### steps"):
            ingredients_section = False
            steps_section = True

        # Collect ingredients
        elif ingredients_section:
            recipe['ingredients'].append(line)

        # Collect steps
        elif steps_section:
            recipe['steps'].append(line)

    # Append the last recipe after the loop ends
    if recipe:
        recipes.append(recipe)
    
    return recipes

if __name__ == '__main__':
    app.run(debug=True)