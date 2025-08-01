from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    if current_user.is_authenticated: 
        return redirect(url_for('main.dashboard'))
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) 
    
    login_user(user, remember=remember)
    return redirect(url_for('main.dashboard'))

@auth.route('/logout')
@login_required
def logout(): 
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup')
def signup():
    if current_user.is_authenticated: 
        return redirect(url_for('main.dashboard'))
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    first_name = request.form.get('first_name')
    surname = request.form.get('surname')
    password = request.form.get('password')

    # Check if user already exists
    user = User.query.filter_by(email=email).first()
    if user: 
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))
    
    # Create new user
    new_user = User(
        email=email,
        first_name=first_name,
        surname=surname,
        password=generate_password_hash(password, method='pbkdf2:sha256')
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('auth.login'))
    except Exception as e:
        db.session.rollback()
        flash(f'Registration failed: {str(e)}')
        return redirect(url_for('auth.signup'))
