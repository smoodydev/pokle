import os
from flask import Flask, redirect, jsonify, render_template, request, flash, session, send_file
from flask_pymongo import PyMongo, ObjectId
import random
from utils import weakness_check, compare_pokemon


if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get('DATABASE')

app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRETKEY", "SomeSecret")

mongo = PyMongo(app)
app.templates = ""



# Helper Functions


def get_pokemon(pokemon):
    is_pokemon = mongo.db.pokemon.find_one({"name": pokemon})
    return is_pokemon


def new_pokemon(gen=False):
    if gen:
        allPokemon = mongo.db.pokemon.find({"generation": gen})
    else:
        allPokemon = mongo.db.pokemon.find()
    
    list_pokemon = list(allPokemon)
    random_number = random.randint(0, len(list_pokemon))
    the_pokemon = list_pokemon[random_number]

    pokemon_dict = {
        "name": the_pokemon["name"],
        "number": the_pokemon["number"],
        "generation": the_pokemon["generation"], 
        "type_one": the_pokemon["type_one"], 
        "type_two": the_pokemon["type_two"], 
        "height": the_pokemon["height"], 
        "weight": the_pokemon["weight"]
        
    }
    session["pokemon"] = pokemon_dict
    session["attempts"] = []
    
    
    return pokemon_dict


def set_partner(pokemon):
    partner_dict = {
            "name": pokemon["name"],
            "tier": pokemon["tier"],
            "moves": []
        }

    for x in pokemon["moves"]:
        partner_dict["moves"].append([x[0], x[1]])
    session["partner"] = partner_dict



# Inital Route - Once Only
@app.route("/picknew")
def start_new():
    partners = mongo.db.partners.find({"tier": "0"})
    return render_template("picknew.html", partners=partners)


@app.route("/selectpartner/<partner_id>")
def selectpartner(partner_id):
    pokemon = mongo.db.partners.find_one({"_id": ObjectId(partner_id)})
    print(pokemon)
    if int(pokemon["tier"])==0:
        set_partner(pokemon)
        # print("TIER IS RIGHT")
        # partner_dict = {
        #     "name": pokemon["name"],
        #     "tier": pokemon["tier"],
        #     "moves": []
        # }

        # for x in pokemon["moves"]:
        #     partner_dict["moves"].append([x[0], x[1]])
        
        # session["partner"] = partner_dict
    
    return redirect("/")

@app.route("/partnercode/<partnercode>/<p_id>")
def use_partner_code(partnercode, p_id):
    code = mongo.db.partnercodes.find_one({"partnercode": partnercode})
    pokemon = mongo.db.partners.find_one({"p_id": int(p_id)})
    print(code)
    print(pokemon)
    if code and pokemon:
        set_partner(pokemon)
        return redirect("/")
    else:
        return "code not valid"


# Reset
@app.route("/new")
def new():
    new_pokemon(4)
    if "complete" in session:
        session.pop("complete")
    session.pop("attempts")
    return redirect("/")


# play
@app.route('/guess_pokemon', methods=["POST"])
def guess_pokemon():
    word = request.form["pokemon"].title()
    
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
        print(pokemon)

        effectiveness = weakness_check([pokemon["type_one"], pokemon["type_two"]], attack_type)
        result = {
            "move_details": attack_type,
            "val": effectiveness
        }
        return jsonify(validated=True, result=result)
    except:
        return jsonify(validated=False, text_back="Something unclear happened")


# Main
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
    moves = mongo.db.moves.find()
    partners = mongo.db.partners.find()
    return render_template("aaa.html", moves=moves, partners=partners)


def get_random_for_guessing():
    allPokemon = mongo.db.pokemon.find()
    list_pokemon = list(allPokemon)
    random_number = random.randint(0, len(list_pokemon))
    the_pokemon = list_pokemon[random_number]
    print(the_pokemon)
    return the_pokemon["name"]


@app.route('/remember/', methods=["GET","POST"])
def guess():
    if "remember" not in session:
        session["remember"] = get_random_for_guessing()
    pokemon = session["remember"]
    
    if request.method == "POST":
        print(pokemon)
        print("got a response")
        guess = request.form["pokemon_entered"].capitalize()
        print(guess)
        if mongo.db.remember.find_one({"name": pokemon}):
            print("FOund")
        else:
            mongo.db.remember.insert_one(
                {
                    "name": pokemon,
                    "count":0,
                    "wrong":0,
                    "guessed":[],
                    "image_issue": 0
                }
            )
        if guess == "Nope":
            print("nope")
            mongo.db.remember.update_one({"name": pokemon}, {"$inc":{"count":1, "wrong":1}} )
        elif guess == pokemon:
            print("Pokemon Right")
            mongo.db.remember.update_one({"name": pokemon}, {"$inc":{"count":1, "correct":1}})
            print("did Right?")
        elif guess == "image":
            mongo.db.remember.update_one({"name": pokemon}, {"$inc":{"image":1}})
        else:
            print("NOPE")
            mongo.db.remember.find_one_and_update({"name": pokemon}, {'$push': {'guessed': guess}, "$inc":{"count":1, "wrong":1}})

        
        session["remember"] = get_random_for_guessing()
    else:
        print("Something")

    return render_template("guess.html")


# @app.route('/whos-that-pokemon/', methods=["GET","POST"])
# def whos_that_pokemon():
#     if request.method == "POST":
#         print("got a response")

#     if "guess" not in session:
#         session["guess"] = "Hello"

#     else:
#         print("Something")
#     return render_template("guess.html")


@app.route("/guess_img/")
def img_getter():
    string_pk = "static/gifs/" + session["remember"]+ ".gif"
    print(string_pk)
    return send_file(string_pk.lower(), mimetype='image/gif')


if __name__ == '__main__':
    app.run(host=os.environ.get('IP', "0.0.0.0"),
            port=int(os.environ.get('PORT', 5000)),
            debug=True)