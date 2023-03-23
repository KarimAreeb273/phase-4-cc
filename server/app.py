#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Restaurant, RestaurantPizza, Pizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

class Restaurants(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        restaurant_dict = [restaurant.to_dict() for restaurant in restaurants]
        response = make_response(restaurant_dict, 200)
        return response

class RestaurantById(Resource):
    def get(self, id):
        restaurants = Restaurant.query.filter(Restaurant.id == id).first()
        if not restaurants: 
            return make_response({"error": "Restaurant not found"}, 404)
        restaurant_dict = restaurants.to_dict(rules=('pizzas',))
        response = make_response(restaurant_dict, 200)
        return response
    
    def delete(self, id):
        restaurants = Restaurant.query.filter(Restaurant.id == id).first()
        if not restaurants: 
            return make_response({"error": "Restaurant not found"}, 404)
        db.session.delete(restaurants)
        db.session.commit()
        response = make_response({}, 200)
        return response

class Pizzas(Resource):
    def get(self):
        pizzas = Pizza.query.all()
        pizza_dict = [pizza.to_dict() for pizza in pizzas]
        response = make_response(pizza_dict, 200)
        return response

class RestaurantPizzas(Resource):
    def post(self):
        new = request.get_json()
        try:
            new_pizzas = RestaurantPizza (
                price = new['price'],
                pizza_id = new['pizza_id'],
                restaurant_id = new['restaurant_id']
            )

            db.session.add(new_pizzas)
            db.session.commit()

            new_pizzas_dict = new_pizzas.pizzas.to_dict()
            response = make_response(new_pizzas_dict, 201)
            return response
        except ValueError:
            return make_response ({"error": ["validation errors"]}, 400)

api.add_resource(Restaurants, '/restaurants')
api.add_resource(RestaurantById, '/restaurant/<int:id>')
api.add_resource(Pizzas, '/pizzas')
api.add_resource(RestaurantPizzas, '/restaurant_pizzas')
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
