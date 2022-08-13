type_chart = {
    "normal" : {
        "weak": ["fighting"],
        "res": [],
        "immune": ["ghost"]

    },
    "fire" : {
        "weak": ["water", "ground", "rock"],
        "res": ["fire", "grass", "ice", "bug", "steel", "fairy"],
        "immune": []
        
    }, 
    "water" : {
        "weak": ["electic", "grass"],
        "res": ["fire", "water", "ice", "steel"],
        "immune": []
        
    }, 
    "electric" : {
        "weak": ["groond"],
        "res": ["electric", "flying", "steel"],
        "immune": []
        
    }, 
    "grass" : {
        "weak": ["fire", "ice","poison", "flying", "bug"],
        "res": ["water", "electric", "grass", "ground"],
        "immune": []
        
    }, 
    "ice" : {
        "weak": ["fire", "fighting", "rock", "steel"],
        "res": ["ice"],
        "immune": []
        
    }, 
    "fighting" : {
        "weak": ["flying", "psychic", "fairy"],
        "res": ["bug", "rock", "dark"],
        "immune": []
        
    }, 
    "poison" : {
        "weak": ["ground", "psychic"],
        "res": ["grass", "fighting", "poison", "bug", "fairy"],
        "immune": []
        
    }, 
    "ground" : {
        "weak": ["water", "grass", "ice"],
        "res": ["poison", "rock"],
        "immune": ["electric"]
        
    }, 
    "flying" : {
        "weak": ["electric", "ice", "rock"],
        "res": ["grass", "fighting", "bug"],
        "immune": ["ground"]
        
    }, 
    "psychic" : {
        "weak": ["bug", "ghost", "dark"],
        "res": ["fighting", "psychic"],
        "immune": []
        
    }, 
    "bug" : {
        "weak": ["fire", "flying", "rock"],
        "res": ["grass", "fighting", "ground"],
        "immune": []
        
    }, 
    "rock" : {
        "weak": ["water", "grass", "fighting", "ground", "steel"],
        "res": ["normal", "fire", "poison", "flying"],
        "immune": []
        
    }, 
    "ghost" : {
        "weak": ["ghost", "dark", "fairy"],
        "res": ["poison", "bug"],
        "immune": ["normal", "fighting"]
        
    }, 
    "dragon" : {
        "weak": ["ice", "dragon", "fairy"],
        "res": ["fire", "water", "electric", "grass"],
        "immune": []
        
    }, 
    "dark" : {
        "weak": ["fighting", "bug", "fairy"],
        "res": ["ghost", "dark"],
        "immune": ["psychic"]
        
    }, 
    "steel" : {
        "weak": ["fire", "fighting", "ground"],
        "res": ["normal", "grass", "ice", "flying", "psychic", "bug", "rock", "dragon", "steel", "fairy"],
        "immune": ["poison"]
        
    }, 
    "fairy" : {
        "weak": ["poison", "steel"],
        "res": ["fighting", "bug", "dark"],
        "immune": ["dragon"]
        
    }
}


def weakness_check(poke_types, attack):
    effectiveness = 1
    print(attack)
    for poke_type in poke_types:
        type_check = poke_type.lower()
        if type_check != "":
            if attack[1] in type_chart[type_check]["weak"]:
                effectiveness = effectiveness*2
            if attack[1] in type_chart[type_check]["res"]:
                effectiveness = effectiveness*0.5
            if attack[1] in type_chart[type_check]["immune"]:
                effectiveness = effectiveness*0
    return effectiveness




def compare_pokemon(should, guess):
    types = []
    not_types = []
    should_types = [should["type_one"], should["type_two"]]
    if guess["type_one"] in should_types:
        types.append(guess["type_one"])
    else:
        not_types.append(guess["type_one"])
    if guess["type_two"] in should_types:
        types.append(guess["type_two"])
    else:
        not_types.append(guess["type_two"])
    
    guess["height"] = float(guess["height"])
    should["height"] = float(should["height"])
    guess["weight"] = float(guess["weight"])
    should["weight"] = float(should["weight"])

    height = [1, guess["height"]] if should["height"] > guess["height"] else [0,guess["height"]]
    weight = [1, guess["weight"]] if should["weight"] > guess["weight"] else [0,guess["weight"]]

    dict_back = {
        "name": guess["name"], 
        "types": types,
        "not_types": not_types,
        "height": height,
        "weight": weight
 
    }

    return dict_back

