function get_pokemon() {
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
                $("#"+section).append(`<div class="typebadge ${types[type].toLowerCase()}">
                ${types[type].toUpperCase()}
            </div>`);
            }

        }
    }


}

function make_attack_card(move, move_result){
    return `<div class="c4 md1"><p>Used ${move_result.move_details[0]}</p>
    <div class="effective effective-${move_result.val}">x${move_result.val}</div>
    <div class="typebadge ${move_result.move_details[1]}">${move_result.move_details[1].toUpperCase()}
    </div>`
}

function make_pokemon_card(the_pokemon) {
    let height, weight = "";
    if (the_pokemon.height[0]){
        height = "Taller";
        if (the_pokemon.height[1] > $("#tallerThan").text()){
            min_height = the_pokemon.height[1];
            $("#tallerThan").html(the_pokemon.height[1])
        }
       
        
    }else{
        height = "Shorter"
        if (the_pokemon.height[1] < $("#shorterThan").text()){
            max_height = the_pokemon.height[1];
            $("#shorterThan").html(the_pokemon.height[1])
        }
   
        
    }
    
    if (the_pokemon.weight[0]){
        weight = "Heavier"
        if (the_pokemon.weight[1] < $("#heavierThan").text()){
            $("#heavierThan").html(the_pokemon.weight[1]);
        }
    }else{
        weight = "Lighter"
        if (the_pokemon.weight[1] < $("#lighterThan").text()){
            $("#lighterThan").html(the_pokemon.weight[1]);
        }
        
    }
    return `
    <div class="c4 md1">
        <img src="static/gifs/${the_pokemon.name.toLowerCase()}.gif"><p>${the_pokemon.name}</p><p>${height}<p><p>${weight}<p>
    </div>`
}

function try_word() {
    let the_pokemon = get_pokemon();
    if (the_pokemon) {
        $.post($SCRIPT_ROOT + '/guess_pokemon', {
            pokemon: the_pokemon
        }, function (data) {
            if (data.validated) {
                pk = data.result;
                
                // wordsent = "";
                // paintCells(data.result, word_attempt);
                // $("#result").text("Result for " + word_attempt);
                // attempt++;
                // letter_index = 0;
                // attempt_array.push(data.result);
                // if (data.result == "y".repeat(num_letters)){
                //     alert("You are a Wiener!")
                //     openWinModal();
                // }
                make_type_card(pk.types, "correctTypes");
                make_type_card(pk.not_types, "guessedTypes");
                if (data.code ==2){
                    $("#thepkimg").attr("src", "static/gifs/"+pk.name.toLowerCase()+".gif");
                    $("#correctHeight").html("Height: "+pk.height+"m")
                    $("#correctWeight").html("Weight: "+pk.weight+"kg")
                    
                }
                else{
                    $("#guessedPokemon").append(make_pokemon_card(pk));
                }
                
                // $("#guessedTypes").append(make_type_card(pk.not_types));
            }
            else {
                $("#result").text(data.text_back);
            }
        });
    }
}

$('.usemove').bind('click', function () {
    $.post($SCRIPT_ROOT + '/use_move', {
            move_slot: this.id
        }, function (data) {
            if (data.validated) {
                move_result = data.result;
                $("#guessedPokemon").append(make_attack_card(this.innerhtml, move_result));
            }
            else {
                $("#result").text(data.text_back);
            }
        });
    return false;
});


$('#enter').bind('click', function () {
    try_word();
    return false;
});