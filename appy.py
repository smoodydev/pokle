import requests

def get_pokemon_data(limit=150):
    pk_list = {}
    
    # Loop through the first 'limit' Pokémon
    for pokemon_id in range(1, limit + 1):
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}/"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            name = data['name']
            types = [t['type']['name'] for t in data['types']]
            pk_list[name] = types
    
    return pk_list

# Call the function to get the Pokémon data
pokemon_data = get_pokemon_data()

# Print the result
print(pokemon_data)