from flask import Flask, request, jsonify, url_for, Blueprint
from models import db, User, Person, Planet, Favorite
from utils import generate_sitemap, APIException

api = Blueprint('api', __name__)

@api.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    users_list = list(map(lambda user: user.serialize(), users))
    return jsonify(users_list), 200

@api.route('/user', methods=['POST'])
def create_user():
    rb = request.get_json()
    new_user = User(
        email=rb["email"], 
        password=rb["password"],
        is_active=True
        )
    db.session.add(new_user)
    db.session.commit()
    return f"User was created", 200


@api.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    planets_list = list(map(lambda planet: planet.serialize(), planets))
    return jsonify(planets_list), 200


@api.route('/planet', methods=['POST'])
def create_planet():
    rb = request.get_json()
    new_planet = Planet(
        planet_name=rb["planet_name"], 
        climate=rb["climate"],
        terrain=rb["terrain"]
        )
    db.session.add(new_planet)
    db.session.commit()
    return f"Planet was created", 200


@api.route('/planets/<int:id>', methods=['GET'])
def get_planet(id):
    planet = Planet.query.get(id)
    if planet is None:
        raise APIException("Planet not found", 404)
    return jsonify(planet.serialize()), 200


@api.route('/people', methods=['GET'])
def get_people():
    people = Person.query.all()
    people_list = list(map(lambda person: person.serialize(), people))
    return jsonify(people_list), 200


@api.route('/person', methods=['POST'])
def create_person():
    rb = request.get_json()
    new_person = Person(
        character_name=rb["character_name"], 
        height=rb["height"],
        haircolor=rb["haircolor"]
        )
    db.session.add(new_person)
    db.session.commit()
    return f"Person was created", 200


@api.route('/people/<int:id>', methods=['GET'])
def get_person(id):
    person = Person.query.get(id)
    if person is None:
        raise APIException("Person not found", 404)
    return jsonify(person.serialize()), 200


@api.route('/users/favorites/<int:user_id>', methods=['GET'])
def get_user_favorites(user_id):
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    favorites_list = list(map(lambda favorite: favorite.serialize(), favorites))
    return jsonify(favorites_list), 200


@api.route('/favorite/people/<int:person_id>', methods=['POST'])
def create_character_favorite(person_id):
    rb = request.get_json()
    new_favorite = Favorite(
        person_id=person_id, 
        user_id=rb["user_id"]
        )
    db.session.add(new_favorite)
    db.session.commit()
    return f"Favorite person was created", 200


@api.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def create_planet_favorite(planet_id):
    rb = request.get_json()
    new_favorite = Favorite(
        planet_id=planet_id, 
        user_id=rb["user_id"]
        )
    db.session.add(new_favorite)
    db.session.commit()
    return f"Favorite planet was created", 200


@api.route('/favorite/people/<int:id>', methods=['DELETE'])
def delete_character_favorite(person_id):
    rb = request.get_json()
    favorite = Favorite(person_id=person_id, user_id=rb["user_id"])
    if favorite is None:
        raise APIException("Favorite person not found", 404)
    db.session.delete(favorite)
    db.session.commit()
    return f"Favorite person was deleted", 200


@api.route('/favorite/planet/<int:id>', methods=['DELETE'])
def delete_planet_favorite(planet_id):
    rb = request.get_json()
    favorite = Favorite(planet_id=planet_id, user_id=rb["user_id"])
    if favorite is None:
        raise APIException("Favorite planet not found", 404)
    db.session.delete(favorite)
    db.session.commit()
    return f"Favorite planet was deleted", 200