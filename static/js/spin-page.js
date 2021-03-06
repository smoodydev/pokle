
let games = [
    { "name": "Red/Blue", "img": "rb.png", "goals": ["Gym 1", "Gym 2", "Gym 3", "Gym 4", "Gym 5", "Gym 6", "Gym 7", "Gym 8", "Elite 4", "Defeat Mewtwo"], "max": 151 },
    { "name": "Yellow", "img": "y.png", "goals": ["Gym 1", "Gym 2", "Gym 3", "Gym 4", "Gym 5", "Gym 6", "Gym 7", "Gym 8", "Elite 4", "Defeat Mewtwo"], "max": 151 },
    { "name": "Gold/Silver", "img": "gs.png", "goals": ["Gym 1", "Gym 2", "Gym 3", "Gym 4", "Gym 5", "Gym 6", "Gym 7", "Gym 8", "Elite 4"], "max": 251 },
    { "name": "Crystal", "img": "crystal.png", "goals": ["Gym 1", "Gym 2", "Gym 3", "Gym 4", "Gym 5", "Gym 6", "Gym 7", "Gym 8", "Elite 4"], "max": 251 },
    { "name": "Ruby/Saphire", "img": "rs.png", "goals": ["Gym 1", "Gym 2", "Gym 3", "Gym 4", "Gym 5", "Gym 6", "Gym 7", "Gym 8", "Elite 4"], "max": 386 },
    { "name": "Emerald", "img": "emerald.png", "goals": ["Gym 1", "Gym 2", "Gym 3", "Gym 4", "Gym 5", "Gym 6", "Gym 7", "Gym 8", "Elite 4"], "max": 386 },
    { "name": "Diamond/Pearl", "img": "dp.png", "goals": ["Gym 1", "Gym 2", "Gym 3", "Gym 4", "Gym 5", "Gym 6", "Gym 7", "Gym 8", "Elite 4"], "max": 493 },
    { "name": "Platinum", "img": "plat.png", "goals": ["Gym 1", "Gym 2", "Gym 3", "Gym 4", "Gym 5", "Gym 6", "Gym 7", "Gym 8", "Elite 4"], "max": 493 },
    // {"name": "Black/White", "img":"bw.jpg"},
    // {"name": "X/Y", "img":"xy.jpg"},
    // {"name": "X/Y", "img":"xy.jpg"},

    { "name": "Fire Red/Leaf Green", "img": "frlg.png", "goals": ["Gym 1", "Gym 2", "Gym 3", "Gym 4", "Gym 5", "Gym 6", "Gym 7", "Gym 8", "Elite 4", "Defeat Mewtwo"], "max": 386 },
    { "name": "Heart Gold/Soul Silver", "img": "hgss.png", "goals": ["Gym 1", "Gym 2", "Gym 3", "Gym 4", "Gym 5", "Gym 6", "Gym 7", "Gym 8", "Elite 4"], "max": 493 },
    // {"name": "Omega Ruby/Alpha Saphire", "img":"oras.jpg"},
    // {"name": "Brilliant Diamond/Shining Pearl", "img":"bdsp.jpg"},

    // {"name": "Sword/Shield", "img":"ss.jpg", "goals": ["Gym 1", "Gym 2", "Gym 3", "Gym 4", "Gym 5", "Gym 6", "Gym 7", "Gym 8", "Elite 4"]},

];
let sec_length = 1000;
let interval = 300;
let seconds;
let game_show;
let goal_show;
let pokemon_show;
let random_Index;
let the_game;
let the_goal;
let the_pokemon;

function spinPokemon() {
    if (pokemon_show < 1) {
        console.log("Done!");
        $.post($SCRIPT_ROOT + '/get_spinned_details', {
            the_pokemon: the_pokemon,
            goal: the_goal,
            game: the_game["name"]
        }, function (data) {

            pokemon_name = data;

            $("#poke").html(
                `<div class="starterdiv" style="background-image: url('/static/gifs/${pokemon_name}.gif');">
                        </div>
                    
                    <div class="row">
                        <h1>${pokemon_name}</h1></div>`);
            $("#result").text(data.text_back);

        });
        games.splice(random_Index, 1);
        console.log(games)
        return false;
    } else {
        the_pokemon = Math.floor(Math.random() * the_game["max"] + 1);
        $("#poke").html(`<div class="row"><h1 style="padding-top: 30%">${the_pokemon}</h1></div>`)
        pokemon_show = pokemon_show - 1;

        setTimeout(spinPokemon, interval);
    }


}
function spinGoal() {
    if (goal_show < 1) {
        spinPokemon();
    } else {
        the_goal = the_game["goals"][Math.floor(Math.random() * the_game["goals"].length)];
        $("#goal").html(`<div class="row"><h1 style="padding-top: 30%">${the_goal}</h1></div>`)
        goal_show = goal_show - 1;

        setTimeout(spinGoal, interval);
    }


}

function spinGen() {
    if (game_show < 1) {

        spinGoal();
    } else {
        random_Index = Math.floor(Math.random() * games.length);
        the_game = games[random_Index];
        $("#game").html(`<div class="row"><img src="/static/img/${the_game["img"]}"/></div><div class="row"><h1>${the_game["name"]}</h1></div>`)
        game_show = game_show - 1;

        setTimeout(spinGen, interval);
    }


}

function countdownToStart() {
    if (seconds < 1) {
        $("#timeleft").html(`<p>Rolling...</p>`);
        spinGen()
    } else {
        $("#timeleft").html(`<p>${seconds}</p>`);
        seconds = seconds - 1;

        setTimeout(countdownToStart, sec_length);
    }

}


$("#spin").click(function () {
    seconds = 5;
    game_show = 10;
    goal_show = 10;
    pokemon_show = 10;
    countdownToStart();
});
