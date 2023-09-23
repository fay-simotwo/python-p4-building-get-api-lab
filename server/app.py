#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define your models
class Bakery(db.Model):
    __tablename__ = 'bakeries'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255))
    description = db.Column(db.Text)

    def __init__(self, name, location, description):
        self.name = name
        self.location = location
        self.description = description

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'description': self.description
        }

class BakedGood(db.Model):
    __tablename__ = 'baked_goods'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float)
    bakery_id = db.Column(db.Integer, db.ForeignKey('bakeries.id'))
    
    bakery = db.relationship('Bakery', backref='baked_goods')

    def __init__(self, name, price, bakery):
        self.name = name
        self.price = price
        self.bakery = bakery

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'bakery_id': self.bakery_id
        }

# Routes for your API
@app.route('/')
def index():
    return '<h1>Bakery API</h1>'

@app.route('/bakeries')
def get_bakeries():
    bakeries = Bakery.query.all()
    bakery_list = [bakery.serialize() for bakery in bakeries]
    return jsonify(bakery_list)

@app.route('/bakeries/<int:id>')
def get_bakery_by_id(id):
    bakery = Bakery.query.get(id)
    if bakery:
        return jsonify(bakery.serialize())
    else:
        return jsonify({'message': 'Bakery not found'}), 404

@app.route('/baked_goods')
def get_baked_goods():
    baked_goods = BakedGood.query.all()
    baked_good_list = [baked_good.serialize() for baked_good in baked_goods]
    return jsonify(baked_good_list)

if __name__ == '__main__':
    app.run(debug=True)
