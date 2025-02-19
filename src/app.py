"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Usuario, Character, Planet, FavoriteCharacter, FavoritePlanet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#crear un nuevo usuario
@app.route('/usuarios', methods=['POST'])
def create_usuario():
    data = request.json
    if not all(key in data for key in ["username", "email", "password", "firstname", "lastname"]):
        return jsonify({"error": "Faltan datos"}), 404
    
#guardar los datos en la BDD
    nuevo_usuario = Usuario(
        username=data["username"],
        email=data["email"],
        password=data["password"],
        firstname=data["firstname"],
        lastname=data["lastname"]
    )
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify(nuevo_usuario.serialize()), 201
   
# obtener todos los usuarios 
@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([usuario.serialize() for usuario in usuarios]), 200

# Eliminar un usuario
@app.route('/usuarios/<int:id>', methods=["DELETE"])
def delete_usuario(id):
    usuario = Usuario.query.get(id)

    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    db.session.delete(usuario)
    db.session.commit()

    return jsonify({"msg": "Usuario eliminado correctamente"}), 200


# actualizar los usuarios
@app.route('/usuarios/<int:id>', methods=['PUT'])
def change_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({"error": "usuario no encontrado"}), 404

    data = request.json
    if "username" in data:
        usuario.username = data["username"]
    if "email" in data:
        usuario.email = data["email"]
    if "password" in data:
        usuario.password = data["password"]
    if "firstname" in data:
        usuario.firstname = data["firstname"]
    if "lastname" in data:
        usuario.lastname = data["lastname"]

    db.session.commit()
    return jsonify(usuario.serialize()), 200

# obtener favoritos de un usuario
@app.route('/usuarios/<int:id>/favorites', methods=['GET'])
def get_favorites(id):
    favorites_planets = FavoritePlanet.query.filter_by(usuario_id=id).all()
    favorites_characters = FavoriteCharacter.query.filter_by(usuario_id=id).all()
 
    if not favorites_characters and not favorites_planets:
        return jsonify({"error": "Este usuario no tiene favoritos"}), 404

    # Serializar los datos de los favoritos de personajes y planetas
    return jsonify({
        "planets": [fav.planet.serialize() for fav in favorites_planets],  # Devolver detalles del planeta
        "characters": [fav.character.serialize() for fav in favorites_characters]  # Devolver detalles del personaje
    }), 200

#crear un nuevo personaje
@app.route('/characters', methods=['POST'])
def create_character():
    data = request.json
    if not all(key in data for key in ["name", "gender", "specie"]):
        return jsonify({"error": "Faltan datos"}), 404
    
#guardar los datos en la BDD
    nuevo_character = Character(
        name=data["name"],
        gender=data["gender"],
        specie=data["specie"]
        )
    db.session.add(nuevo_character)
    db.session.commit()
    return jsonify(nuevo_character.serialize()), 201

# obtener todos los personajes (character)
@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    return jsonify([character.serialize() for character in characters]), 200

#obtener personajes por id
@app.route('/characters/<int:id>', methods=['GET'])
def get_character(id):
    character = Character.query.get(id)
    if not character:
        return jsonify({"error": "Personaje no encontrado"}), 404
    return jsonify(character.serialize()), 200

#deletar un personaje
@app.route('/characters/<int:id>', methods=["DELETE"])
def delete_character(id):
    character = Character.query.get(id)

    if not character:
        return jsonify({"error":"personaje no encontrado"}), 404

    db.session.delete(character)
    db.session.commit()

    return jsonify({"msg": "Personaje eliminado correctamente"}), 200

# Actualizar un personaje
@app.route('/characters/<int:id>', methods=['PUT'])
def change_character(id):
    character = Character.query.get(id)
    if not character:
        return jsonify({"error": "Personaje no encontrado"}), 404

    data = request.json
    if "name" in data:
        character.name = data["name"]
    if "gender" in data:
        character.gender = data["gender"]
    if "specie" in data:
        character.specie = data["specie"]

    db.session.commit()
    return jsonify(character.serialize()), 200

#crear un nuevo planet
@app.route('/planets', methods=['POST'])
def create_planet():
    data = request.json
    if not all(key in data for key in ["name", "population", "terrain"]):
        return jsonify({"error": "Faltan datos"}), 404
    
#guardar los datos en la BDD
    nuevo_planet = Planet(
        name=data["name"],
        population=data["population"],
        terrain=data["terrain"]
        )
    db.session.add(nuevo_planet)
    db.session.commit()
    return jsonify(nuevo_planet.serialize()), 201
 
# obtener todos los planetas
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200


#obtener planetas por id
@app.route('/planets/<int:id>', methods=['GET'])
def get_planet(id):
    planet = Planet.query.get(id)
    if not planet:
        return jsonify({"error": "Planeta no encontrado"}), 404
    return jsonify(planet.serialize()), 200

#deletar un planeta
@app.route('/planets/<int:id>', methods=["DELETE"])
def delete_planet(id):
    planet = Planet.query.get(id)

    if not planet:
        return jsonify({"error":"planeta no encontrado"}), 404

    db.session.delete(planet)
    db.session.commit()

    return jsonify({"msg": "Planeta eliminado correctamente"}), 200

# Actualizar un planeta
@app.route('/planets/<int:id>', methods=['PUT'])
def change_planet(id):
    planeta = Planet.query.get(id)
    if not planeta:
        return jsonify({"error": "Planeta no encontrado"}), 404

    data = request.json
    if "name" in data:
        planeta.name = data["name"]
    if "population" in data:
        planeta.climate = data["population"]
    if "terrain" in data:
        planeta.terrain = data["terrain"]

    db.session.commit()
    return jsonify(planeta.serialize()), 200


# Agregar planeta favorito a un usuario
@app.route('/usuarios/<int:id>/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(id, planet_id):
    usuario = Usuario.query.get(id)
    planet = Planet.query.get(planet_id)

    if not usuario or not planet:
        return jsonify({"error": "Usuario o planeta no encontrado"}), 404

    favorite = FavoritePlanet(usuario_id=id, planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()
    
    return jsonify({"msg": "Planeta agregado a favoritos"}), 201

#agregar personaje favorito a un usuario
@app.route('/usuarios/<int:id>/favorite/character/<int:character_id>', methods=['POST'])
def add_favorite_character(id, character_id):
    usuario = Usuario.query.get(id)
    character = Character.query.get(character_id)

    if not usuario or not character:
        return jsonify({"error": "Usuario o personaje no encontrado"}), 404

    favorite = FavoriteCharacter(usuario_id=id, character_id=character_id)
    db.session.add(favorite)
    db.session.commit()
    
    return jsonify({"msg": "Personaje agregado a favoritos"}), 201

#eliminar un planet favorito de un usuario
@app.route('/usuarios/<int:id>/favorite/planet/<int:planet_id>', methods=["DELETE"])
def delet_favorite_planet(id, planet_id):
    usuario = Usuario.query.get(id)
    favorite = FavoritePlanet.query.filter_by(usuario_id=id, planet_id=planet_id).first()

    if not favorite:
        return jsonify({"error": "favorito no encontrado"}), 404
    
    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"msg": "Planeta eliminado de favoritos"}), 200

#eliminar un personaje favorito de un usuario
@app.route('/usuarios/<int:id>/favorite/character/<int:character_id>', methods=["DELETE"])
def delet_favorite_character(id, character_id):
    usuario = Usuario.query.get(id)
    favorite = FavoriteCharacter.query.filter_by(usuario_id=id, character_id=character_id).first()

    if not favorite:
        return jsonify({"error": "favorito no encontrado"}), 404
    
    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"msg": "Personaje eliminado de favoritos"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
