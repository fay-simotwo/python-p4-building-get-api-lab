from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Bakery(db.Model, SerializerMixin):
    __tablename__ = 'bakeries'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255))
    description = db.Column(db.Text)

    def __init__(self, name, location, description):
        self.name = name
        self.location = location
        self.description = description

class BakedGood(db.Model, SerializerMixin):
    __tablename__ = 'baked_goods'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float)
    bakery_id = db.Column(db.Integer, db.ForeignKey('bakeries.id'))
    
    # Define a relationship to link BakedGoods to their respective Bakeries
    bakery = db.relationship('Bakery', backref='baked_goods')

    def __init__(self, name, price, bakery):
        self.name = name
        self.price = price
        self.bakery = bakery
