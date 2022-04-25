function get_pokemon() {
    let the_pokemon = $(`#pokemon_entered`).val().toLowerCase();
   
    if (pokemonNames.includes(the_pokemon)) {
        return the_pokemon;
    }
    return false;

}


function try_word() {
    let the_pokemon = get_pokemon();
    if (the_pokemon) {
        $.post($SCRIPT_ROOT, {
            pokemon: the_pokemon
        }, function (data) {
            if(data.correct){
                console.log(data.correct);
                $("#the_img").removeClass("shadow");
                $("#banner").html("It's "+data.name+"!")
            }
            // if (data.validated) {
            //     pk = data.result;
                
            //     // wordsent = "";
            //     // paintCells(data.result, word_attempt);
            //     // $("#result").text("Result for " + word_attempt);
            //     // attempt++;
            //     // letter_index = 0;
            //     // attempt_array.push(data.result);
            //     // if (data.result == "y".repeat(num_letters)){
            //     //     alert("You are a Wiener!")
            //     //     openWinModal();
            //     // }
            //     make_type_card(pk.types, "correctTypes");
            //     make_type_card(pk.not_types, "guessedTypes");
            //     if (data.code ==2){
            //         $("#thepkimg").attr("src", "static/gifs/"+pk.name.toLowerCase()+".gif");
            //         $("#correctHeight").html("Height: "+pk.height+"m")
            //         $("#correctWeight").html("Weight: "+pk.weight+"kg")
                    
            //     }
            //     else{
            //         $("#guessedPokemon").append(make_pokemon_card(pk));
            //     }
                
            //     // $("#guessedTypes").append(make_type_card(pk.not_types));
            // }
            else {
                $("#result").text(data.text_back);
            }
        });
    }
}



$('#enter').bind('click', function () {
    try_word();
    return false;
});