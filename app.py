from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from google import genai
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "super_secret_key_chatbot"

API_KEY = "YOUR_API_KEY_HERE"
client = genai.Client(api_key=API_KEY)

def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()
user_chats = {}

@app.route("/")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            data = request.get_json()
            if not data:
                return jsonify({"status": "error", "message": "Invalid data format!"})
                
            email = data.get("email")
            password = data.get("password")
            
            if not email or not password:
                return jsonify({"status": "error", "message": "Email and password cannot be empty!"})
                
            hashed_password = generate_password_hash(password)
            
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                conn.close()
                session["user"] = email
                return jsonify({"status": "success", "message": "Email already registered. Logging you in..."})
            
            cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_password))
            conn.commit()
            conn.close()
            
            session["user"] = email
            return jsonify({"status": "success", "message": "Account created successfully!"})
            
        except Exception as e:
            return jsonify({"status": "error", "message": f"Server Error: {str(e)}"})
            
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            data = request.get_json()
            email = data.get("email")
            password = data.get("password")
            
            if not email or not password:
                return jsonify({"status": "error", "message": "Please fill in all fields!"})
                
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            user = cursor.fetchone()
            conn.close()
            
            if user and check_password_hash(user[2], password):
                session["user"] = email
                return jsonify({"status": "success"})
            else:
                return jsonify({"status": "error", "message": "Invalid Email or Password!"})
        except Exception as e:
            return jsonify({"status": "error", "message": f"Server Error: {str(e)}"})
            
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/get_response", methods=["POST"])
def get_response():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401
        
    user_email = session["user"]
    user_message = request.json.get("message")
    
    if not user_message:
        return jsonify({"error": "Message is empty"}), 400

    if user_email not in user_chats:
        system_instruction = (
            "You are a helpful AI assistant. By default, you must always respond in clear and professional English. "
            "However, if the user explicitly writes to you in Roman English, Urdu, or any other language, "
            "you must flexibly adapt and reply back in that exact same language style."
        )
        config = {'system_instruction': system_instruction}
        user_chats[user_email] = client.chats.create(model='gemini-2.5-flash', config=config)

    try:
        response = user_chats[user_email].send_message(user_message)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": f"ERROR: {str(e)}"}), 200

@app.route("/new_chat", methods=["POST"])
def new_chat():
    if "user" in session:
        user_email = session["user"]
        system_instruction = (
            "You are a helpful AI assistant. By default, you must always respond in clear and professional English. "
            "However, if the user explicitly writes to you in Roman English, Urdu, or any other language, "
            "you must flexibly adapt and reply back in that exact same language style."
        )
        config = {'system_instruction': system_instruction}
        user_chats[user_email] = client.chats.create(model='gemini-2.5-flash', config=config)
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)