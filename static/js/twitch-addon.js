const intervalID = setInterval(checkOption, 500);

function checkOption() {
    console.log("Checking");
    let pkOption = $("#pokemonToGuess").text()
    console.log(pkOption);
    if (pkOption != ""){
        $("#pokemon_entered").val($("#pokemonToGuess").text());
        $("#pokemonToGuess").text("")
        $("button#enter").click()
    }
    let moveOption = $("#useMove").text()
    if (moveOption != ""){
        $("#useMove").text("");
        $(".usemove#"+moveOption).click();
    }

    
}