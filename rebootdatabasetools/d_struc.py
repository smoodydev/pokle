import csv
from main import db



import csv

@app.route("/tryread")
def insert():
    last = ""
    with open('All_Pokemon.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                print(f'\t{row[0]} {row[1]} {row[2]} {row[3]} {row[14]} {row[41]} {row[42]} ')
                line_count += 1
            elif line_count < 5:
            # else:
                
                entry = {
                    "number": row[0],
                    "name": row[1],
                    "type_one":row[2],
                    "type_two":row[3],
                    "generation":int(float(row[14])),
                    "height":row[41],
                    "weight":row[42]
                }
                mongo.db.pokemon.insert_one(entry)
                print(f'\t{row[0]} {row[1]} {row[2]} {row[3]} {row[14]} {row[41]} {row[42]} ')
                line_count += 1
            
        print(f'Processed {line_count} lines.')
    return "tried"



@app.route("/insertmoves")
def insertmoves():
    with open('moves.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
        
            print(row)
            the_move = {
                "m_id": line_count+1,
                "name": row[0],
                "move_type": row[1]
            }
            mongo.db.moves.insert_one(the_move)
            
            # print(f'\t{row[0]} {row[1]} {row[2]} {row[3]}')
                
            line_count += 1
        print(f'Processed {line_count} lines.')
    return "tried"


@app.route("/insertpartners")
def insertpartners():
    line_count = 0
    with open('partners.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            moves = row[2].split(",")
            
            partner_entry = {
                "p_id": line_count+1,
                "name": row[0],
                "tier": int(row[1]),
                "moves": [],
                "evolves": int(row[3])
            }


            for m in moves:
                move_details = mongo.db.moves.find_one({"m_id": int(m)})
                partner_entry["moves"].append([move_details["name"], move_details["move_type"]])
            mongo.db.partners.insert_one(partner_entry)
            
            # print(f'\t{row[0]} {row[1]} {moves} {row[3]}')
                
            line_count += 1

        print(f'Processed {line_count} lines.')

    return "tried"


