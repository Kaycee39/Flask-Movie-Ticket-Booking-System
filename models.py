from flask_login import UserMixin
from datetime import datetime
from . import db
import enum

from werkzeug.security import generate_password_hash, check_password_hash

class TransactionMethod(enum.Enum):
  CASH = "cash"
  MPESA = "M-pesa"
class Hall(enum.Enum):
  HALL_A = "Hall A"
  HALL_B = "Hall B"
class Format(enum.Enum):
  two_D ="2D"
  three_D ="3D"
class AccountType(enum.Enum):
    EMPLOYEE = "1"
    CUSTOMER = "0"


class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), index=True, unique=True)
  email = db.Column(db.String(150), unique = True, index = True)
  password_hash = db.Column(db.String(150))
  time = db.Column(db.DateTime(), default = datetime.utcnow, index = True)

  #def set_password(self, password):
   #     self.password_hash = generate_password_hash(password)

  def check_password(self,password):
        return check_password_hash(self.password_hash,password)

class movies(db.Model):
  id = db.Column(db.Integer,primary_key=True)
  name = db.Column(db.String(50), index=True)
  genre = db.Column(db.String(50), index=True)
  time =db.Column(db.Integer, index=True)
  cast =db.Column(db.String(200), index=True)
  director =db.Column(db.String(50), index=True)
  preview =db.Column(db.String(200), index=True)
  photo =db.Column(db.String(300))  
  schedules = db.relationship("schedule", back_populates="movies")

class schedule(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50))
  date =db.Column(db.DateTime)
  quality = db.Column(db.String(50))
  hall = db.Column(db.String(50)) 
  price = db.Column(db.Integer)
  movie_id=db.Column(db.Integer,db.ForeignKey('movies.id'))
  movies = db.relationship('movies', back_populates = 'schedules')

class search(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64))
  

class personal(db.Model):
  id =db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50))
  email = db.Column(db.String(150))
  phone = db.Column(db.Integer)

class Transactions(db.Model):
  id =db.Column(db.Integer, primary_key=True, nullable =True)
  name = db.Column(db.String(50))
  amount = db.Column(db.Float(precision=2))
  phone = db.Column(db.Integer)
  transaction_time = db.Column(db.DateTime)
  payment_method = db.Column(db.Enum(TransactionMethod))
  