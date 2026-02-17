from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
import pickle
import os

app = Flask(__name__)
CORS(app)

MODEL_PATH = 'sentiment_model.pkl'
DB_PATH = 'database.db'

# ---------------- DATABASE SETUP ----------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            text TEXT,
            Emotion TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ---------------- MODEL TRAINING ----------------
def train_model():
    """Load dataset, train or retrain sentiment model."""
    # Assume dataset: dataset.csv with columns: 'text', 'Emotion'
    df = pd.read_csv('feedback_dataset.csv')
    X = df['text']
    y = df['Emotion']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english')),
        ('clf', LogisticRegression(max_iter=1000))
    ])
    
    model.fit(X_train, y_train)

    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)

    print("Model trained and saved successfully.")

# Train automatically if not already trained
if not os.path.exists(MODEL_PATH):
    train_model()

# ---------------- LOAD MODEL ----------------
def load_model():
    with open(MODEL_PATH, 'rb') as f:
        return pickle.load(f)

model = load_model()

# ------------------ ROUTES ------------------

# ---------- SIGNUP ----------
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data['username']
    password = data['password']
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return jsonify({"message": "Signup successful"})
    except:
        return jsonify({"message": "Username already exists"}), 400

# ---------- LOGIN ----------
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']
    if username == "admin" and password == "admin123":
        return jsonify({"message": "Admin login successful", "isAdmin": True})
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    if user:
        return jsonify({"message": "Login successful", "isAdmin": False})
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# ---------- FEEDBACK + SENTIMENT ----------
@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.json
    username = data['username']
    text = data['text']

    Emotion = model.predict([text])[0]

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO feedback (username, text, Emotion) VALUES (?, ?, ?)",
              (username, text, Emotion))
    conn.commit()
    conn.close()

    return jsonify({"text": "Feedback saved", "Emotion": Emotion})

# ---------- ADMIN VIEW FEEDBACK ----------
@app.route('/admin/feedbacks', methods=['GET'])
def view_feedbacks():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT username, text, Emotion FROM feedback")
    all_feedback = c.fetchall()
    conn.close()
    feedback_list = [
        {"username": row[0], "text": row[1], "Emotion": row[2]} for row in all_feedback
    ]
    return jsonify(feedback_list)

# ---------- RETRAIN MODEL (ADMIN-ONLY) ----------
@app.route('/admin/retrain', methods=['POST'])
def retrain():
    train_model()
    return jsonify({"message": "Model retrained successfully"})

# ---------- HEALTH CHECK ----------
@app.route('/')
def home():
    return jsonify({"message": "Flask Emotion analysis API running"})

# ---------------- MAIN ENTRY ----------------
if __name__ == '__main__':
    app.run(debug=True)
