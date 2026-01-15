# server/models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

# Naming convention for database constraints
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)

# --------------------------
# Models
# --------------------------

class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'
    serialize_rules = ('-reviews.customer',)  # avoid recursion

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)

    reviews = db.relationship('Review', back_populates='customer')
    items = association_proxy('reviews', 'item')  # association proxy


class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'
    serialize_rules = ('-reviews.item',)  # avoid recursion

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    price = db.Column(db.Float)

    reviews = db.relationship('Review', back_populates='item')


class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'
    serialize_rules = ('-customer.reviews', '-item.reviews',)  # avoid recursion

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)

    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    customer = db.relationship('Customer', back_populates='reviews')
    item = db.relationship('Item', back_populates='reviews')

    def __repr__(self):
        return f'<Review {self.id}, Customer {self.customer_id}, Item {self.item_id}>'
