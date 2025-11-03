# user.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import sqlite3

# ==========================
# Blueprint Setup
# ==========================
user_bp = Blueprint('user', __name__, template_folder='templates')

# ==========================
# Database Helper
# ==========================
def get_db():
    conn = sqlite3.connect('procurement.db')
    conn.row_factory = sqlite3.Row
    return conn


# ==========================
# LOGIN REQUIRED DECORATOR
# ==========================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("⚠️ Please log in to continue.", "warning")
            return redirect(url_for('user.login'))
        return f(*args, **kwargs)
    return decorated_function


# ==========================
# REGISTER FUNCTION
# ==========================
@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        email = request.form['email'].strip()

        if not username or not password or not email:
            flash("All fields are required!", "danger")
            return redirect(url_for('user.register'))

        hashed_pw = generate_password_hash(password)

        conn = get_db()
        cur = conn.cursor()

        # Check if user already exists
        cur.execute("SELECT * FROM users WHERE email = ?", (email,))
        existing_user = cur.fetchone()
        if existing_user:
            flash("Email already registered!", "warning")
            conn.close()
            return redirect(url_for('user.register'))

        # Insert new user
        cur.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                    (username, email, hashed_pw))
        conn.commit()
        conn.close()

        flash("✅ Registration successful! Please login.", "success")
        return redirect(url_for('user.login'))

    return render_template('register.html')


# ==========================
# LOGIN FUNCTION
# ==========================
@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password'].strip()

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash(f"👋 Welcome {user['username']}!", "success")
            return redirect(url_for('user.dashboard'))
        else:
            flash("Invalid credentials!", "danger")

    return render_template('login.html')


# ==========================
# LOGOUT FUNCTION
# ==========================
@user_bp.route('/logout')
@login_required
def logout():
    session.clear()
    flash("👋 You have been logged out successfully.", "info")
    return redirect(url_for('user.login'))


# ==========================
# USER DASHBOARD
# ==========================
@user_bp.route('/dashboard')
@login_required
def dashboard():
    username = session.get('username')
    return render_template('dashboard.html', username=username)


# ==========================
# USERS LIST (ADMIN VIEW)
# ==========================
@user_bp.route('/users')
@login_required
def users():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, username, email FROM users")
    all_users = cur.fetchall()
    conn.close()
    return render_template('users.html', users=all_users)
