from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import Enum

db = SQLAlchemy()

class PetType(str, Enum):
    DOG = "perro"
    CAT = "gato"

class FoodType(str, Enum):
    DRY = "seca"
    WET = "humeda"
    MIXED = "mixta"

class Pet(db.Model):
    __tablename__ = 'pets'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    raza = db.Column(db.String(100), nullable=False)
    peso = db.Column(db.String(20), nullable=False)
    edad = db.Column(db.String(20), nullable=False)
    tipo_comida = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'tipo': self.tipo,
            'raza': self.raza,
            'peso': self.peso,
            'edad': self.edad,
            'tipo_comida': self.tipo_comida,
            'created_at': self.created_at.isoformat()
        }
