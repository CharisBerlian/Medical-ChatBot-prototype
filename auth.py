import sqlite3
import hashlib
import os

DB_PATH = "user_data.db"

def init_auth_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Create the users table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            full_name TEXT,
            age INTEGER,
            email TEXT
        )
    ''')
    conn.commit()
    conn.close()

def ensure_db_connection():
    """Ensure database and table exist before any operation"""
    init_auth_db()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username: str, password: str, full_name: str = "", age: int = 0, email: str = "") -> bool:
    ensure_db_connection()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    if c.fetchone():
        conn.close()
        return False  # already exists
    c.execute("""
        INSERT INTO users (username, password, full_name, age, email) 
        VALUES (?, ?, ?, ?, ?)
    """, (username, hash_password(password), full_name, age, email))
    conn.commit()
    conn.close()
    return True

def login_user(username: str, password: str) -> dict:
    ensure_db_connection()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    hashed = hash_password(password)
    c.execute("""
        SELECT username, full_name, age, email 
        FROM users 
        WHERE username = ? AND password = ?
    """, (username, hashed))
    result = c.fetchone()
    conn.close()
    
    if result:
        return {
            "username": result[0],
            "full_name": result[1],
            "age": result[2],
            "email": result[3]
        }
    return None

