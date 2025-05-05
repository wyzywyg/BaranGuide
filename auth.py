from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps

auth_bp = Blueprint('auth', __name__)

# Path to JSON file for user data
USERS_FILE = 'users.json'

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def create_default_admin():
    users_file = 'users.json'
    users = {}
    
    # Load existing users if file exists
    if os.path.exists(users_file):
        with open(users_file, 'r') as f:
            users = json.load(f)
    
    # Check if admin account already exists
    admin_email = 'admin01-barangay@gmail.com'
    if admin_email not in users:
        # Create admin account
        users[admin_email] = {
            'full_name': 'Barangay Admin',
            'email': admin_email,
            'phone': '09123456789',
            'password': generate_password_hash('admin123'),
            'role': 'official',  # This will work with your existing code
            'created_at': datetime.now().isoformat(),
            'is_admin': True  # Additional flag to identify admin users
        }
        
        # Save to file
        with open(users_file, 'w') as f:
            json.dump(users, f, indent=4)
        
        print("Default admin account created successfully!")
    else:
        print("Admin account already exists")

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            flash('Please login to access this page', 'error')
            return redirect(url_for('auth.show_auth', form_type='login'))
        return f(*args, **kwargs)
    return decorated_function

# Role required decorator
def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_email' not in session:
                flash('Please login to access this page', 'error')
                return redirect(url_for('auth.show_auth', form_type='login'))
            
            users = load_users()
            user = users.get(session['user_email'])
            
            if not user or user['role'] != role:
                flash(f'Access denied. This page is only for {role}s', 'error')
                return redirect(url_for('home'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@auth_bp.route('/<form_type>')
def show_auth(form_type):
    # Validate form_type
    if form_type not in ['login', 'signup']:
        form_type = 'login'
    return render_template('auth.html', form_type=form_type)


@auth_bp.route('/login', methods=['POST'])
def login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            role = request.form.get('role', 'resident')
            
            users = load_users()
            user = users.get(email)
            
            if not user or not check_password_hash(user['password'], password):
                flash('Invalid email or password', 'error')
                return redirect(url_for('auth.show_auth', form_type='login'))
            
            # Store user data in session
            session['user_email'] = email
            session['user_role'] = user['role']
            session['user_name'] = user['full_name']
            session['is_admin'] = user.get('is_admin', False)
            
            # Admin handling
            if user.get('is_admin', False):
                flash('Login successful!', 'success')
                return redirect(url_for('admin_dashboard'))
            
            if user['role'] != role:
                flash(f'Please login as {user["role"]}', 'error')
                return redirect(url_for('auth.show_auth', form_type='login'))
            
            flash('Login successful!', 'success')
            
            # Redirect based on role
            if role == 'resident':
                return redirect(url_for('resident_dashboard'))
            else:
                return redirect(url_for('official_dashboard'))
        
        return redirect(url_for('auth.show_auth', form_type='login'))

@auth_bp.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form.get('fullName')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')
        role = request.form.get('role', 'resident')
        
        users = load_users()
        
        if email in users:
            flash('Email already exists', 'error')
            return redirect(url_for('auth.show_auth', form_type='signup'))
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('auth.show_auth', form_type='signup'))
        
        if len(password) < 8:
            flash('Password must be at least 8 characters', 'error')
            return redirect(url_for('auth.show_auth', form_type='signup'))
        
        # Create new user
        users[email] = {
            'full_name': full_name,
            'email': email,
            'phone': phone,
            'password': generate_password_hash(password),
            'role': role,
            'created_at': datetime.now().isoformat()
        }
        
        save_users(users)
        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('auth.show_auth', form_type='login'))
    
    return redirect(url_for('auth.show_auth', form_type='signup'))

@auth_bp.route('/logout')
def logout():
    # Clear the session
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('home'))

