from sqlalchemy import create_engine, Column, Integer, String, select , Float, Text ,ForeignKey, DateTime, types
from sqlalchemy.orm import declarative_base,relationship, backref
from sqlalchemy.orm import Session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime



engine = create_engine("sqlite:///flask.db", echo=True, future=True)
Base = declarative_base()
session = Session(engine)


def create_db():
    Base.metadata.create_all(engine)


class Store(Base):
    __tablename__ = 'stores'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    address = Column(String(100), nullable=False)

    def __init__(self, name, address):
        self.name = name
        self.address = address

class Station(Base):
    __tablename__ = 'stations'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    address = Column(String(100), nullable=False)

    def __init__(self, name, address):
        self.name = name
        self.address = address


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    namezh = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    descriptionzh = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    image = Column(String(100), nullable=False)

class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', backref=backref('order', lazy=True))

class OrderItem(Base):
    __tablename__ = "OrderItem"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    order = relationship('Order', backref=backref('items', lazy=True))
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    product = relationship('Product', backref=backref('order', lazy=True))
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

class Customer(Base):
    __tablename__ = "Customer"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    address = Column(Text, nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

class Promotion(Base):
    __tablename__ = "Promotion"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    discount = Column(Float, nullable=False)
    products = relationship('Product', secondary='product_promotion', backref=backref('promotion', lazy=True))


class Inventory(Base):
    __tablename__ = "Inventory"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    product = relationship('Product', backref=backref('inventory', lazy=True))
    quantity = Column(Integer, nullable=False)

class Feedback(Base):
    __tablename__ = 'Feedback'
    id = Column(Integer, primary_key=True)
    content = Column(String(255), nullable=False)
    rating = Column(Integer, nullable=False)

class cart(Base):
    __tablename__ = 'cart'
    id = Column(Integer, primary_key=True) 
    product_id = Column(Integer) 
    quantity = Column(Integer)

class News(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(String(2000), nullable=False)
    author = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class Return(Base):
    __tablename__ = 'returns'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    reason = Column(String(100), nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class Coupon(Base):
    __tablename__ = 'coupons'
    id = Column(Integer, primary_key=True)
    code = Column(String(50), unique=True, nullable=False)
    discount = Column(Float, nullable=False)
    expires_at = Column(DateTime, nullable=False)

class Shipping(Base):
    __tablename__ = 'shippings'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class Checkout(Base):
    __tablename__ = 'checkout'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class Favorite(Base):
    __tablename__ = 'favorites'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)