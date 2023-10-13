#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from models import HeroPower, Hero, Power
from flask_migrate import Migrate


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/cathy/Downloads/python-code-challenge-superheroes-1 (5) (1)/python-code-challenge-superheroes/code-challenge/app/db/dbheroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

class HeroesResource(Resource):
    def get(self):
        heroes = Hero.query.all()
        hero_list = []

        for hero in heroes:
            hero_data = {
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name
            }
            hero_list.append(hero_data)

        return hero_list, 200

class HeroResource(Resource):
    def get(self, id):
        hero = Hero.query.filter_by(id=id).first()
        if hero:
            hero_data = {
                "id": hero.id,
                "name": hero.name,
                "super_power": hero.super_power,
                "powers": []  
            }

            for hero_power in hero.powers:
                power_data = {
                    "id": hero_power.power.id,
                    "name": hero_power.power.name,
                    "description": hero_power.power.description
                }

                hero_data["powers"].append(power_data) 

            return hero_data, 200
        else:
            return {"error": "Hero not found"}, 404

class PowerResource(Resource):
    def get(self, id):
        power = Power.query.get(id)
        if power:
            power_data = {
                "id": power.id,
                "name": power.name,
                "description": power.description
            }
            return power_data, 200
        else:
            return {"error": "Power not found"}, 404

class PowersResource(Resource):
    def get(self):
        powers = Power.query.all()
        powers_list = []

        for power in powers:
            power_data = {
                "id": power.id,
                "name": power.name,
                "description": power.description
            }
            powers_list.append(power_data)

        return powers_list, 200

class PowerUpdateResource(Resource):
    def patch(self, id):
        hero_power = HeroPower.query.get(id)
        if hero_power:
            data = request.get_json()
            for key, value in data.items():
                setattr(hero_power, key, value)

            db.session.commit()
            return hero_power.to_dict(), 200
        else:
            return {"error": "Hero Power not found"}, 404

class HeroPowerResource(Resource):
    def post(self):
        data = request.get_json()
        new_strength = HeroPower(**data)
        db.session.add(new_strength)
        db.session.commit()
        return new_strength.to_dict(), 201

api.add_resource(HeroesResource, '/heroes')
api.add_resource(HeroResource, '/heroes/<int:id>')
api.add_resource(PowersResource, '/powers')
api.add_resource(PowerResource, '/powers/<int:id>')
api.add_resource(PowerUpdateResource, '/powers/<int:id>')
api.add_resource(HeroPowerResource, '/hero_powers')

if __name__ == '__main__':
    app.run(port=5555)
