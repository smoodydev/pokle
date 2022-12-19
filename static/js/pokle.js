let pokemon_types = [
    "Normal", "Fire", "Water", "Grass", "Electric", "Ice", "Fighting", "Poison", "Ground", "Flying", "Psychic", "Bug", "Rock", "Ghost", "Dark", "Dragon", "Steel", "Fairy"
];
let min_height = 0;
let max_height = 99999;
let min_weight = 0;
let max_weight = 99999;

function getPokemon() {
    let the_pokemon = $(`#pokemon_entered`).val().toLowerCase();

    if (pokemonNames.includes(the_pokemon)) {
        return the_pokemon;
    }
    return false;

}

function make_type_card(types, section) {
    for (let type in types) {
        if (types[type] != "") {
            if (!$("#" + section + " ." + types[type].toLowerCase()).length) {
                $("#" + section).append(`<div class="typebadge ${types[type].toLowerCase()}">
                ${types[type].toUpperCase()}
            </div>`);
            }

        }
    }


}

function make_attack_card(move, move_result) {
    return `<div class="c4 md1"><p>Used ${move_result.move_details[0]}</p>
    <div class="effective effective-${move_result.val}">x${move_result.val}</div>
    <div class="typebadge ${move_result.move_details[1]}">${move_result.move_details[1].toUpperCase()}
    </div>`
}

function make_pokemon_card(the_pokemon) {
    let height, weight = "";
    let height_in = parseFloat(the_pokemon.height[1]);
    let weight_in = parseFloat(the_pokemon.weight[1]);
    if (the_pokemon.height[0]) {
        height = "Taller";
        if (height_in > min_height) {
            min_height = height_in;
            $("#tallerThan").html(min_height)
        }
    } else {
        height = "Shorter"
        if (height_in < max_height) {
            max_height = height_in;
            $("#shorterThan").html(max_height)
        }
    }

    if (the_pokemon.weight[0]) {
        weight = "Heavier"
        if (weight_in > min_weight) {
            min_weight = weight_in
            $("#heavierThan").html(min_weight);
        }


    } else {
        weight = "Lighter"
        if (the_pokemon.weight[1] < max_weight) {
            max_weight = weight_in
            $("#lighterThan").html(max_weight);
        }
    }
    return `
    <div class="c4 md1 soften">
        <img src="static/gifs/${the_pokemon.name.replaceAll(" ", "-").toLowerCase()}.gif"><p>${the_pokemon.name}</p><p>${height}<p><p>${weight}<p>
    </div>`;
}

function openWinModal(pokemon) {
    $("#winModalTitle").html("You did it!");
    $("#winModalImage").html(`<img src="static/gifs/${pokemon.replaceAll(" ", "-").toLowerCase()}.gif">`);
    $("#winModalMessage").html("You found " + pokemon);
    $("#winModal").show();
}

function closeModal() {
    $("#winModal").hide();
}


function generateTypeCards() {
    pokemon_types.forEach(function (type) {
        $("#typeCards").append(`
        <div id="type-card-${type}" class="typebadge ${type.toLowerCase()}">
            ${type}
        </div>`);

    });
}
generateTypeCards();

function removeTypeCard(types) {
    types.forEach(function (type) {
        $("#type-card-" + type).remove();
    })

}

function guessPokemon() {
    let the_pokemon = getPokemon();
    if (the_pokemon) {
        $.post($SCRIPT_ROOT + '/guess_pokemon', {
            pokemon: the_pokemon
        }, function (data) {
            if (data.code) {
                pk = data.result;
                make_type_card(pk.types, "correctTypes");
                removeTypeCard(pk.types.concat(pk.not_types));
                if (data.code == 2) {
                    $("#thepkimg").attr("src", "static/gifs/" + pk.name.toLowerCase() + ".gif");
                    $("#correctHeight").html("Height: " + pk.height + "m");
                    $("#correctWeight").html("Weight: " + pk.weight + "kg");
                    openWinModal(pk.name);
                }
                else {
                    $("#guessedPokemon").append(make_pokemon_card(pk));
                }

            }
            else {
                $("#result").text(data.text_back);
            }
        });
    }
}

$('.usemove').bind('click', function () {
    let slotUsed = this.id;
    $.post($SCRIPT_ROOT + '/use_move', {
        move_slot: this.id
    }, function (data) {
        if (data.validated) {
            move_result = data.result;
            $("typemul#tm_" + slotUsed).html("x"+move_result["val"]);
            $("#guessedPokemon").append(make_attack_card(this.innerhtml, move_result));
        }
        else {
            $("#result").text(data.text_back);
        }
    });
    return false;
});


$('#enter').bind('click', function () {
    guessPokemon();
    console.log("Loaded")
    return false;
});

$('.modalCloseBtn button').bind('click', function () {
    closeModal();
    return false;
});