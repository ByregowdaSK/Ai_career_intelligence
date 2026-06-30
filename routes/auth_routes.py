from flask import Blueprint, render_template, request, redirect, session

from models.user_model import get_user_by_email
from db import get_db_connection

from werkzeug.security import generate_password_hash, check_password_hash

import random
import re

from datetime import datetime

from flask_mail import Message
from extensions import mail

auth = Blueprint('auth', __name__)


# =========================
# LOGIN
# =========================

@auth.route('/login', methods=['GET', 'POST'])
def login():

    error = None

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        user = get_user_by_email(email)

        if user:

            # =========================
            # ADMIN & TEST USER
            # =========================

            if (
                user['email'] in ['admin@gmail.com', 'test@gmail.com']
                and user['password'] == password
            ):

                session['user_id'] = user['id']
                session['name'] = user['name']
                session['email'] = user['email']
                session['role'] = user['role']

                session['is_admin'] = (
                    user['role'] == 'admin'
                )

                # UPDATE LAST LOGIN

                conn = get_db_connection()
                cursor = conn.cursor()

                cursor.execute("""
                UPDATE tbl_user
                SET last_login = %s
                WHERE id = %s
                """, (datetime.now(), user['id']))

                conn.commit()

                cursor.close()
                conn.close()

                # ADMIN REDIRECT

                if user['role'] == 'admin':
                    return redirect('/admin')

                return redirect('/dashboard')

            # =========================
            # REGISTERED USERS
            # =========================

            elif check_password_hash(
                user['password'],
                password
            ):

                session['user_id'] = user['id']
                session['name'] = user['name']
                session['email'] = user['email']
                session['role'] = user['role']

                session['is_admin'] = (
                    user['role'] == 'admin'
                )

                # UPDATE LAST LOGIN

                conn = get_db_connection()
                cursor = conn.cursor()

                cursor.execute("""
                UPDATE tbl_user
                SET last_login = %s
                WHERE id = %s
                """, (datetime.now(), user['id']))

                conn.commit()

                cursor.close()
                conn.close()

                # ADMIN REDIRECT

                if user['role'] == 'admin':
                    return redirect('/admin')

                return redirect('/dashboard')

            else:
                error = "Invalid password"

        else:
            error = "User not found"

    return render_template(
        'login.html',
        error=error
    )


# =========================
# REGISTER
# =========================

@auth.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'GET':
        return render_template('register.html')

    name = request.form.get('name')

    email = request.form.get('email')

    password = request.form.get('password')

    confirm = request.form.get('confirm_password')

    # EMPTY VALIDATION

    if not name or not email or not password or not confirm:

        return render_template(
            'register.html',
            error="All fields are required"
        )

    # PASSWORD MATCH

    if password != confirm:

        return render_template(
            'register.html',
            error="Passwords do not match"
        )

    # EMAIL FORMAT

    if not re.match(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        email
    ):

        return render_template(
            'register.html',
            error="Invalid email format"
        )

    # PASSWORD LENGTH

    if len(password) < 6:

        return render_template(
            'register.html',
            error="Password must be at least 6 characters"
        )

    # DUPLICATE CHECK

    existing_user = get_user_by_email(email)

    if existing_user:

        return render_template(
            'register.html',
            error="Email already exists"
        )

    # HASH PASSWORD

    hashed_password = generate_password_hash(password)

    # INSERT USER

    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute(
    """
    INSERT INTO tbl_user
    (
        name,
        email,
        password,
        role,
        chatbot_usage,
        recommendation_count,
        resume_uploaded,
        resume_score
    )

    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """,
    (
        name,
        email,
        hashed_password,
        'student',
        0,
        0,
        0,
        0
    )
)

    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/login')


# =========================
# FORGOT PASSWORD
# =========================

@auth.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():

    message = None

    if request.method == 'POST':

        email = request.form['email']

        otp = str(
            random.randint(100000, 999999)
        )

        session['reset_otp'] = otp
        session['reset_email'] = email

        msg = Message(
            'Career AI Password Reset OTP',

            sender='yourgmail@gmail.com',

            recipients=[email]
        )

        msg.body = f'Your OTP is: {otp}'

        mail.send(msg)

        return redirect('/verify_otp')

    return render_template(
        'forgot_password.html',
        message=message
    )


# =========================
# VERIFY OTP
# =========================

@auth.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():

    error = None

    if request.method == 'POST':

        user_otp = request.form['otp']

        if user_otp == session.get('reset_otp'):

            return redirect('/reset_password')

        else:

            error = "Invalid OTP"

    return render_template(
        'verify_otp.html',
        error=error
    )


# =========================
# RESET PASSWORD
# =========================

@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_password():

    if request.method == 'POST':

        new_password = generate_password_hash(
            request.form.get('password')
        )

        email = session.get('reset_email')

        conn = get_db_connection()

        cur = conn.cursor()

        cur.execute(
            """
            UPDATE tbl_user
            SET password=%s
            WHERE email=%s
            """,
            (
                new_password,
                email
            )
        )

        conn.commit()

        cur.close()
        conn.close()

        session.pop('reset_otp', None)
        session.pop('reset_email', None)

        return redirect('/login')

    return render_template(
        'reset_password.html'
    )


# =========================
# LOGOUT
# =========================

@auth.route('/logout')
def logout():

    session.clear()

    return redirect('/login')