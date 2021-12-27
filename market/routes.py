import re
from market import app
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market', methods = ['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    if request.method == 'POST':
        purchased_item = request.form.get("purchased_item")
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            p_item_object.owner = current_user.id
            # subtract the current object price from the users object
            current_user.budget -= p_item_object.price
            db.session.commit()
            flash(f"Thank you for your purchase {p_item_object.name}")
    if request.method == 'GET':
        items = Item.query.filter_by(owner=None)
        return render_template('market.html', items = items, purchase_form = purchase_form)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    #create the instance
    form = RegisterForm()
    if form.validate_on_submit():
        #below this if statement, you're going to put what you want to happen when someone hits submit
        user_to_create = User(username=form.username.data,
        email_address=form.email_address.data,
        password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created succesfully, you are now logged in as {user_to_create.username}', category="success")
        return redirect(url_for('market_page'))
    if form.errors != {}: #if there are not error from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        #we want to know if the user exists and if the email and password is correct
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data
            ):
            login_user(attempted_user)
            flash(f'Now you are logged in as: {attempted_user.username}', category="succes")
            return redirect(url_for('market_page'))
        else:
            flash('Username or password did not match, try again', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been log out', category='info')
    return redirect(url_for("home_page"))

