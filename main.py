import os
from flask import Flask, redirect, jsonify, render_template, request, flash, session
from flask_sqlalchemy import SQLAlchemy
import random
from utils import weakness_check, compare_pokemon
import csv

if os.path.exists("env.py"):
    import env

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = os.environ.get("SECRETKEY", "SomeSecret")


db = SQLAlchemy(app)



# Pokemon Class
class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    name = db.Column(db.String(80), unique=True, nullable=False)
    generation = db.Column(db.Integer)
    type_one = db.Column(db.String(80), nullable=False)
    type_two = db.Column(db.String(80), nullable=False)
    height = db.Column(db.Float)
    weight =  db.Column(db.Float)

    def __init__(self, number, name, generation, type_one, type_two, height, weight):   
        self.number = number
        self.name = name
        self.generation = generation
        self.type_one = type_one
        self.type_two = type_two
        self.height = height
        self.weight = weight

    def to_dict(self):
        as_dict = {
            "name": self.name,
            "generation":self.generation,
            "type_one": self.type_one,
            "type_two": self.type_two,
            "height":self.height,
            "weight":self.weight
        }
        return as_dict


moves = db.Table('moves',
    db.Column('move_id', db.Integer, db.ForeignKey('move.id'), primary_key=True),
    db.Column('partner_id', db.Integer, db.ForeignKey('partner.id'), primary_key=True)
)  

class Partner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    tier = db.Column(db.Integer)
    moves = db.relationship('Move', secondary=moves, lazy='subquery',
      backref=db.backref('partners', lazy=True))
    evolves_id = db.Column(db.Integer, nullable=True)
    
    def __init__(self, name, moves, tier, evolves_id):   
        self.name = name
        self.tier = tier
        self.evolves_id = evolves_id
        
    def add_moves(self, moves_in):
        for move in moves_in:
            self.moves.append(Move.query.filter(Move.id==int(move)).first())
 
  
    def to_dict(self):
        as_dict = {
            "name": self.name,
            "moves":self.moves,
            "tier": self.tier,
            "evolves_id": self.evolves_id,
        }
        return as_dict


class Move(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    move_type = db.Column(db.String(80), unique=False, nullable=False)
    
    def __init__(self, name, move_type):   
        self.name = name
        self.move_type = move_type
   


def get_pokemon(pokemon):
    is_pokemon = Pokemon.query.filter(Pokemon.name==pokemon).first()
    if (is_pokemon):
        is_pokemon = is_pokemon.to_dict()
    return is_pokemon


def new_pokemon(gen=False):
    if gen:
        allPokemon = Pokemon.query.filter(Pokemon.generation <= gen)
    else:
        allPokemon = Pokemon.query.all()
    
    random_number = random.randint(0, len(list(allPokemon)))
    the_pokemon = allPokemon[random_number]
    pokemon_dict = {
        "name": the_pokemon.name,
        "number": the_pokemon.number,
        "generation": the_pokemon.generation, 
        "type_one": the_pokemon.type_one, 
        "type_two": the_pokemon.type_two, 
        "height": the_pokemon.height, 
        "weight": the_pokemon.weight
        
    }
    session["pokemon"] = pokemon_dict
    session["attempts"] = []
    
    
    return pokemon_dict

@app.route("/picknew")
def start_new():
    partners = Partner.query.filter(Partner.tier==0)
    return render_template("picknew.html", partners=partners)

@app.route("/selectpartner/<partner_id>")
def selectpartner(partner_id):

    selected_partner = Partner.query.get(partner_id)
    pokemon = selected_partner.to_dict()
    if pokemon["tier"]==0:
        partner_dict = {
            "name": pokemon["name"],
            "tier": pokemon["tier"],
            "moves": []
        }

        for x in pokemon["moves"]:
            partner_dict["moves"].append([x.name, x.move_type])
        
        session["partner"] = partner_dict
    
    return redirect("/")


@app.route("/new")
def new():
    new_pokemon(2)
    if "complete" in session:
        session.pop("complete")
    session.pop("attempts")
    return redirect("/")

@app.route('/guess_pokemon', methods=["POST"])
def guess_pokemon():
    word = request.form["pokemon"].capitalize()
    
    if ("complete" not in session):
        is_pokemon = get_pokemon(word)
        if is_pokemon:
            
            the_pokemon = session["pokemon"]
            print(the_pokemon)
            
            if word == the_pokemon["name"]:
                text_back = "You are a winner!"
                result = the_pokemon
                result["types"] = [the_pokemon["type_one"], the_pokemon["type_two"]]
                code = 2
                session["complete"] = True
            elif 'attempts' in session:
                attempts = session.get("attempts")
                attempts.append(word)
                session["attempts"] = attempts
                text_back = "The server received the word "+ word
                result = compare_pokemon(the_pokemon, is_pokemon)
                code = 1
            else:
                session["attempts"] = [word]
                code = 1
                text_back = "The server received the word "+ word
                result = compare_pokemon(the_pokemon, is_pokemon)
            # if "user" in session:
            #     updating = {"word":session["word"], "current_attempts": session["attempts"]}
            #     mongo.db.useraccount.update_one({"username": session["user"]}, {"$set" : updating})
            #     if "complete" in session:
            #         score = len(session["attempts"])
            #         mongo.db.useraccount.update_one({"username": session["user"]},{"$inc": {"score": 5 if score <= 3 else 7-score}})
            
            
            return jsonify(validated=True, result=result, code=code, text_back=text_back)
        else:
            return jsonify(validated=False, text_back="Not a Valid Pokemon")
    else:
        print("completed")
        text_back = "You have already completed this word"
    return jsonify(validated=False, text_back=text_back)

@app.route('/use_move', methods=["POST"])
def use_move():
    move_slot = request.form["move_slot"]
    try:
        attack_type = session["partner"]["moves"][int(move_slot)]
        print(attack_type)
        pokemon = session["pokemon"]

        effectiveness = weakness_check([pokemon["type_one"], pokemon["type_two"]], attack_type)
        result = {
            "move_details": attack_type,
            "val": effectiveness
        }
        return jsonify(validated=True, result=result)
    except:
        return jsonify(validated=False, text_back="Something unclear happened")


@app.route('/')
def index():
    if not all([key in session for key in ["pokemon", "attempts", "partner"]]):
        print("SHEEE")
        new_pokemon(1)
        if "partner" not in session:
            return redirect("picknew")
        
    pokemon = "pokemon"


    return render_template("index.html", pokemon=pokemon)


@app.route('/data')
def data():
    moves = Move.query.all()
    partners = Partner.query.all()
    return render_template("aaa.html", moves=moves, partners=partners)



if __name__ == '__main__':
    db.create_all()
    app.run(host=os.environ.get('IP', "0.0.0.0"),
            port=int(os.environ.get('PORT', 5000)),
            debug=True)