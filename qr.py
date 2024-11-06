# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import pyqrcode
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    qr_code_valid_until = db.Column(db.DateTime, nullable=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists!', 'danger')
            return redirect(url_for('register'))

        # Heslo generováno zde, uživatel si ho ale nenastavuje
        password = 'your_temp_password'  # Mùžete generovat náhodné heslo
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        expiration_time = datetime.utcnow() + timedelta(minutes=5)
        new_user = User(username=username, password=password_hash, qr_code_valid_until=expiration_time)
        db.session.add(new_user)
        db.session.commit()

        qr_code_data = f"http://dev.spsejecna.net:20489/verify/{username}"
        qr_code = pyqrcode.create(qr_code_data)
        qr_code.png(f'static/images/{username}_qr.png', scale=5)
        flash('Account created! Please scan the QR code to proceed.', 'success')
        return render_template('display_qr.html', qr_code=f'{username}_qr.png')

    return render_template('register.html')

@app.route('/verify/<username>', methods=['GET', 'POST'])
def verify(username):
    user = User.query.filter_by(username=username).first_or_404()
    
    # Zkontrolujeme, zda platnost QR kódu nevypršela
    if datetime.utcnow() > user.qr_code_valid_until:
        flash('QR code has expired.', 'danger')
        return redirect(url_for('register'))

    if request.method == 'POST':
        password = request.form['password']
        # Zkontrolujeme, zda heslo odpovídá hashovanému heslu v databázi
        if bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid password.', 'danger')

    return render_template('login.html', username=username)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082, debug=True)  # zmìòte port podle potøeby
