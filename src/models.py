from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship, declarative_base


db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    firstname = db.Column(db.String(250), nullable=False)
    lastname = db.Column(db.String(250), nullable=False)

   
    def __repr__(self):
        return  self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(250), nullable=False)
    species = db.Column(db.String(250), nullable=False)
   

    def __repr__(self):
        return  self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    population = db.Column(db.Integer)
    terrain = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return  self.name 

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "terrain":self.terrain
            # do not serialize the password, its a security breach
        }
   

class FavoriteCharacter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    character_id = db.Column(db.Integer, db.ForeignKey("character.id"))
    usuario = relationship("Usuario")
    character = relationship("Character")
    

    def __repr__(self):
        return  self.usuario_id

    def serialize(self):
        return {
           "id": self.character.id,
            "name": self.character.name,
            "gender": self.character.gender
            # do not serialize the password, its a security breach
        }


class FavoritePlanet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"))
    usuario = relationship("Usuario")
    planet = relationship("Planet")

    def __repr__(self):
        return self.usuario_id

    def serialize(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "planet_id": self.planet_id,
            "planet":self.planet.serialize()
            # do not serialize the password, its a security breach
        }