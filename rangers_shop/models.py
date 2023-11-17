from werkzeug.security import generate_password_hash #generates a unique password hash for extra security 
from flask_sqlalchemy import SQLAlchemy #this is our ORM (Object Relational Mapper)
from flask_login import UserMixin, LoginManager #helping us load a user as our current_user 
from datetime import datetime #put a timestamp on any data we create (Users, Products, etc)
import uuid #makes a unique id for our data (primary key)
from flask_marshmallow import Marshmallow


#instantiate all our classes
db = SQLAlchemy() #make database object
login_manager = LoginManager() #makes login object 
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve

    """
    return User.query.get(user_id) 

#
class User(db.Model, UserMixin): 
    #CREATE TABLE 
    user_id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow) 


    #INSERT INTO User() Values()
    def __init__(self, username, email, password, first_name="", last_name=""):
        self.user_id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email 
        self.password = self.set_password(password) 



    #methods for editting our attributes 
    def set_id(self):
        return str(uuid.uuid4()) #all this is doing is creating a unique identification token
    

    def get_id(self):
        return str(self.user_id) #UserMixin using this method to grab the user_id on the object logged in
    
    
    def set_password(self, password):
        return generate_password_hash(password) #hashes the password so it is secure (aka no one can see it)
    

    def __repr__(self):
        return f"<User: {self.username}>"

class Product(db.Model):
    prod_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String)
    description = db.Column(db.String(200))
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    # Playtime is the minutes to finish a game
    playtime = db.Column(db.Integer, nullable=False)

    def __init__(self, name, quantity, price, playtime, image ="", description = ""):
        self.prod_id = self.set_id()
        self.name = name
        self.quantity = quantity
        self.price = price
        self.playtime = playtime
        self.image = image
        self.description = description


    def set_id(self):
        return str(uuid.uuid4())
    

    def decremenet_quantity(self,amount):
        self.quantity -=int(amount)
        return self.quantity
    
    def incremenet_quantity(self, amount):
        self.quantity += int(amount)
        return self.quantity
    
    def __repr__(self):
        return f"<Product: {self.name}>"
    
class ProductSchema(ma.Schema):

    class Meta:
        fields=['prod_id', 'name', 'image', 'description', 'price','playtime']

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)