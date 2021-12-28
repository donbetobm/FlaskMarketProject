from flask_login import login_manager
from sqlalchemy.orm import backref
from market import db, login_manager
from market import bycrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    #relationship between two tables; lazy allows SQLite to grab all the items related to the user in once
    items = db.relationship('Item', backref='owned_user', lazy=True)

    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f'${str(self.budget)[:-3]},{str(self.budget)[-3:]}'
        else:
            return f"${self.budget}"

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plaint_text_password):
        self.password_hash = bycrypt.generate_password_hash(plaint_text_password).decode('UTF-8')

    # this built in function takes the password hash stored and the actual password that it's been entered
    # then, checks if they match and returns True or False
    def check_password_correction(self, attempted_password):
        return bycrypt.check_password_hash(self.password_hash, attempted_password)

    def can_purchase(self, item_obj):
        return self.budget >= item_obj.price

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    #create relationship so SQLalchemy is able to know which user own an item
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))    
    def __repr__(self):
        return f'Item {self.name}'

    def buy(self, user):
        self.owner = user.id
        # subtract the current object price from the users object
        user.budget -= self.price
        db.session.commit()