const intervalID = setInterval(checkOption, 500);

function checkOption() {
    console.log("Checking");
    let option = $("#pokemonToGuess").text()
    console.log(option);
    if (option != ""){
        $("#pokemon_entered").val($("#pokemonToGuess").text());
        $("#pokemonToGuess").text("")
        $("button#enter").click()
    }
    

    
}