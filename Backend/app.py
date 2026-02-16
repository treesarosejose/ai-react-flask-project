from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    # Create feedback table
    c.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            message TEXT,
            sentiment TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# --- SIMPLE SENTIMENT FUNCTION ---
def analyze_sentiment(text):
    text = text.lower()
    positive_words = ['good', 'great', 'happy', 'excellent', 'awesome', 'love']
    negative_words = ['bad', 'sad', 'terrible', 'awful', 'hate', 'poor']
    score = 0
    for word in positive_words:
        if word in text:
            score += 1
    for word in negative_words:
        if word in text:
            score -= 1
    if score > 0:
        return 'Positive'
    elif score < 0:
        return 'Negative'
    else:
        return 'Neutral'

# --- SIGNUP API ---
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data['username']
    password = data['password']
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return jsonify({"message": "Signup successful"})
    except:
        return jsonify({"message": "Username already exists"}), 400

# --- LOGIN API ---
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']
    if username == "admin" and password == "admin123":
        return jsonify({"message": "Admin login successful", "isAdmin": True})
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    if user:
        return jsonify({"message": "Login successful", "isAdmin": False})
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# --- FEEDBACK API ---
@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.json
    username = data['username']
    message = data['message']
    sentiment = analyze_sentiment(message)
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO feedback (username, message, sentiment) VALUES (?, ?, ?)",
              (username, message, sentiment))
    conn.commit()
    conn.close()
    return jsonify({"message": "Feedback saved", "sentiment": sentiment})

# --- ADMIN VIEW FEEDBACK API ---
@app.route('/admin/feedbacks', methods=['GET'])
def view_feedbacks():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT username, message, sentiment FROM feedback")
    all_feedback = c.fetchall()
    conn.close()
    return jsonify(all_feedback)

if __name__ == '__main__':
    app.run(debug=True)
