import os
from flask import Flask, redirect, jsonify, render_template, request, flash, session, send_file, url_for
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


@app.route("/aaa")
def run_an_update():
    print("Hello")
    all_partners = mongo.db.partners.find()
    for partner in all_partners:
        print(partner["_id"])
        mongo.db.partners.update_one({"_id": ObjectId(partner["_id"])}, {"$set": {"evolves" : int(partner["evolves"])}})
    return render_template("index.html")


# Helper Functions
def get_pokemon(pokemon):
    is_pokemon = mongo.db.pokemon.find_one({"name": {"$regex": pokemon, "$options": "i"}})
    return is_pokemon


def new_pokemon(gen=False):
    if gen:
        allPokemon = mongo.db.pokemon.find({"generation": {"$lte": gen}})
    else:
        allPokemon = mongo.db.pokemon.find()
    
    list_pokemon = list(allPokemon)
    random_number = random.randint(0, len(list_pokemon)-1)
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
    print(pokemon)
    partner_dict = {
            "name": pokemon["name"],
            "tier": pokemon["tier"],
            "moves": []
        }

    for x in pokemon["moves"]:
        partner_dict["moves"].append([x[0], x[1]])
    session["partner"] = partner_dict


def evolve_partner():
    if "partner" in session:
        evolution_id = mongo.db.partners.find_one({"name": session["partner"]["name"]})
        if evolution_id:
            evolution = mongo.db.partners.find_one({"p_id": int(evolution_id["evolves"])})
            if evolution:
                set_partner(evolution)

        

# Inital Route - Once Only
@app.route("/picknew")
def start_new():
    partners = mongo.db.partners.find({"tier": 0})
    return render_template("picknew.html", partners=partners)


@app.route("/selectpartner/<partner_id>")
def selectpartner(partner_id):
    pokemon = mongo.db.partners.find_one({"_id": ObjectId(partner_id)})
    if int(pokemon["tier"])==0:
        set_partner(pokemon)

        partner_dict = {
            "name": pokemon["name"],
            "tier": pokemon["tier"],
            "moves": []
        }

        for x in pokemon["moves"]:
            partner_dict["moves"].append([x[0], x[1]])
        
        session["partner"] = partner_dict
    
        return redirect(url_for("pokle"))
    else:
        return redirect("/picknew")


@app.route("/partnercode/<partnercode>/<p_id>")
def use_partner_code(partnercode, p_id):
    code = mongo.db.partnercodes.find_one({"partnercode": partnercode})
    pokemon = mongo.db.partners.find_one({"p_id": int(p_id)})
    if code and pokemon:
        set_partner(pokemon)
        return redirect(url_for("pokle"))
    else:
        return "code not valid"


# Reset
@app.route("/new")
def new():
    if "complete" in session:
        session.pop("complete")
    if "attempts" in session:
        session.pop("attempts")
    return redirect(url_for("pokle"))


# play
@app.route('/guess_pokemon', methods=["POST"])
def guess_pokemon():
    word = request.form["pokemon"]
    print(word)
    if ("complete" not in session):
        is_pokemon = get_pokemon(word)
        if is_pokemon:
            
            the_pokemon = session["pokemon"]
            print(the_pokemon)
            
            if word.lower() == the_pokemon["name"].lower():
                text_back = "You are a winner!"
                result = the_pokemon
                result["types"] = [the_pokemon["type_one"], the_pokemon["type_two"]]
                code = 2
                session["complete"] = True
                if "experience" in session["partner"]:
                    session["partner"]["experience"] = session["partner"]["experience"] + 1
                    if session["partner"]["experience"] >= (session["partner"]["tier"] + (session["partner"]["tier"] * 3)):
                        evolve_partner()
                else:
                     session["partner"]["experience"] = 1
                
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
            
            print("A")
            return jsonify(validated=True, result=result, code=code, text_back=text_back)
        else:
            print("b")
            return jsonify(validated=False, text_back="Not a Valid Pokemon")
    else:
        print("C")
        text_back = "You have already completed this word"
    return jsonify(validated=False, text_back=text_back)


@app.route('/use_move', methods=["POST"])
def use_move():
    move_slot = request.form["move_slot"]
    try:
        attack_type = session["partner"]["moves"][int(move_slot)]
        pokemon = session["pokemon"]

        effectiveness = weakness_check([pokemon["type_one"], pokemon["type_two"]], attack_type)
        result = {
            "move_details": attack_type,
            "val": effectiveness
        }
        return jsonify(validated=True, result=result)
    except:
        return jsonify(validated=False, text_back="Something unclear happened")





@app.route("/")
def splash_landing():
    return render_template("splash.html")

@app.route("/summerfest")
def summer_landing():
    summer = mongo.db.summerfest.find()
    players = mongo.db.useraccount.find().sort("score", -1)
    return render_template("summer.html", summer=summer, players=players)


@app.route("/spin_page")
def spin_page():
    return render_template("spin.html")

@app.route("/get_spinned_details", methods=["POST"])
def get_spinned_details():
    pokemon_back = list(mongo.db.pokemon.find({"number":str(request.form["the_pokemon"])}))
    if "name" in session:
        if session["name"] == "admin":
            mongo.db.summerfest.insert_one({"game":request.form["game"], "goal":request.form["goal"], "pokemon":(pokemon_back[0]["name"]).lower()})
    return (pokemon_back[0]["name"]).lower()


@app.route("/poklegen/<gen>")
def set_pokle_gen(gen):
    session["gens"] = int(gen)
    if "complete" in session:
        session.pop("complete")
    session.pop("attempts")
    return redirect(url_for("pokle"))


# Main
@app.route('/pokle')
def pokle():
    if not all([key in session for key in ["pokemon", "attempts", "partner"]]):
        if "partner" not in session:
            return redirect("picknew")
        if "gens" in session:
            new_pokemon(session["gens"])
        else:
            new_pokemon(1)
        
    
    return render_template("index.html")


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
    return the_pokemon["name"]


@app.route('/remember/', methods=["GET","POST"])
def guess():
    if "remember" not in session:
        session["remember"] = get_random_for_guessing()
    pokemon = session["remember"]
    
    if request.method == "POST":

        guess = request.form["pokemon_entered"].capitalize()
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
            mongo.db.remember.update_one({"name": pokemon}, {"$inc":{"image_issue":1}})
        else:
            print("NOPE")
            mongo.db.remember.find_one_and_update({"name": pokemon}, {'$push': {'guessed': guess}, "$inc":{"count":1, "wrong":1}})

        
        session["remember"] = get_random_for_guessing()
    else:
        print("Something")

    return render_template("guess.html")


@app.route('/whos-that-pokemon/', methods=["GET","POST"])
def whos_that_pokemon():
    if request.method == "POST":
        result = {
            "correct": False
        }
        guess = request.form["pokemon"].capitalize()
        if guess == session["guess"]:
            result["correct"] = True
            result["name"] = session["guess"]
        return jsonify(result)

    session["guess"] = get_random_for_guessing()

    
    return render_template("whos_that_poke.html")


@app.route('/issue')
def issue():
    pokemon = session["guess"]
    if mongo.db.remember.find_one({"name": pokemon}):
        mongo.db.remember.update_one({"name": pokemon}, {"$inc":{"image":1}})
    else:
        mongo.db.remember.insert_one(
            {
                "name": pokemon,
                "count":0,
                "wrong":0,
                "guessed":[],
                "image_issue": 1
            }
        )
    
    return redirect(url_for("whos-that-pokemon"))


@app.route("/remember_img/")
def img_getter_remember():
    string_pk = "static/gifs/" + session["remember"]+ ".gif"
    return send_file(string_pk.lower(), mimetype='image/gif')

@app.route("/guess_img/")
def img_getter_guess():
    string_pk = "static/gifs/" + session["guess"]+ ".gif"
    return send_file(string_pk.lower(), mimetype='image/gif')


@app.route("/post-times", methods=["GET", "POST"])
def post_times():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        account_exist = mongo.db.useraccount.find_one({"username": username})

        if (account_exist):
            if account_exist["password"] == password:
                account_id = account_exist["_id"]

            else:
                account_exist = False
        else:
            account_exist = mongo.db.useraccount.insert_one({"username":username, "password":password})
            account_id = account_exist.inserted_id
        if account_exist:
            link_in = request.form.get("link_url")
            igt_time = request.form.get("igt_time")
            selected_run = request.form.get("select-run")
            mongo.db.summerfestrun.insert_one({
                "link": link_in,
                "igt_time":float(igt_time.replace(":", ".")),
                "selected_run": ObjectId(selected_run),
                "user": {"_id": account_id, "username": username},
                "checked": False
            })
        
        
    summer = mongo.db.summerfest.find()
    return render_template("postboard.html", summer=summer)



@app.route("/admincheat")
def admincheat():
    if os.environ.get("admin") and os.environ.get("admin") != "nope":
        if request.args.get("cheat") ==  os.environ.get("admin"):
            session["name"] = "admin"
        return render_template("splash.html")
    return redirect("pokle")


@app.route("/updatebest")
def update_best_times():
    runs = list(mongo.db.summerfest.find())
    for run in runs:
        best_time = 999.99
        if "best_time" in run:
            best_time = run["best_time"]
        if "players" in run:
            players = run["players"]
        else:
            players = []
        run_times = mongo.db.summerfestrun.find({"selected_run": run["_id"], "checked":False})
        for times in run_times:
            igt_time = times["igt_time"]
            if igt_time < best_time:
                best_time = igt_time
                players = [times["user"]]
            elif igt_time == best_time:
                players.append(times["user"])
            mongo.db.summerfestrun.update_one({"_id": times["_id"]}, {"$set": {"checked": True}})
        if players:
            mongo.db.summerfest.update_one({"_id":run["_id"]}, {"$set": {"best_time": best_time, "players": players}})
    print("ready?")
    return "hello"


score_chart = [30, 20, 15, 10, 9, 8, 7, 5, 3, 1]
@app.route("/updatebest/hard")
def update_best_times_hard():
    players = {}
    players
    game_runs = list(mongo.db.summerfest.find())
    for game in game_runs:
        if "best_time" in game:
            run_times = mongo.db.summerfestrun.find({"selected_run": game["_id"]}).sort("igt_time")[:10]
            last_time = game["best_time"]
            skip_point = 0
            for i, run in enumerate(run_times):
                
                if run["user"]["_id"] in players:
                    players[run["user"]["_id"]]["score"] = players[run["user"]["_id"]]["score"] + score_chart[i+skip_point]
                else:
                    players[run["user"]["_id"]] = {"score": score_chart[i+skip_point], "username":run["user"]["username"]}

                if float(run["igt_time"]) == last_time and last_time != game["best_time"]:
                    skip_point =+ 1
    for key, data in players.items():

        mongo.db.useraccount.update_one({"_id": ObjectId(key)}, {"$set": {"score": data["score"]}})
    
    return "hello"

    



if __name__ == '__main__':
    app.run(host=os.environ.get('IP', "0.0.0.0"),
            port=int(os.environ.get('PORT', 5000)),
            debug=os.path.exists("env.py"))