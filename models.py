from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy import DateTime, func
#from sqlalchemy import ForeignKey


db = SQLAlchemy()

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_power'

    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'), primary_key=True)
    power_id = db.Column(db.Integer, db.ForeignKey('power.id'), primary_key=True)
    strength = db.Column(db.String)
    
    updated_at = db.Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    serialize_rules = ("-hero.powers", "-power.heroes")

    @validates('strength')
    def validate_strength(self, key, strength):
        if strength not in ['Average', 'Weak', 'Strong']:
            raise ValueError("Input Strengths: Strong, Weak, Average")

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'
    serialize_rules = ("-powers.hero")
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_power = db.Column(db.String)
    created_at = db.Column(DateTime, default=func.current_timestamp())
    updated_at = db.Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Define the relationship with HeroPower
    powers = db.relationship('HeroPower', back_populates='hero')

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'
    serialize_rules = ("-heroes.power")
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    heroes = db.relationship('HeroPower', back_populates='power')
    created_at = db.Column(DateTime, default=func.current_timestamp())
    updated_at = db.Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

