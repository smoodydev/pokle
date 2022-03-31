import csv
from main import db


@app.route("/insertmoves")
def insertmoves():
    db.session.query(Move).delete()
    db.session.query(Partner).delete()
    db.session.commit()
    last = ""
    with open('moves.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
        
            print(row)
            db.session.add(Move(name=row[0], move_type=row[1]))
            db.session.commit()
            
            # print(f'\t{row[0]} {row[1]} {row[2]} {row[3]}')
                
            line_count += 1
        print(f'Processed {line_count} lines.')
    return "tried"


@app.route("/insertpartners")
def insertpartners():
    db.session.query(Partner).delete()
    db.session.commit()
    last = ""
    with open('partners.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
        
            print(row)
            db.session.add(Partner(name=row[0], tier=int(row[1]), moves=list(row[2]), evolves_id=int(row[3])))
            db.session.commit()
            moves_in = row[2].split(",")
            print(type(moves_in))

            partner = Partner.query.filter(Partner.name==row[0]).first()
            print(partner)
            partner.add_moves(moves_in)
            print(partner, moves_in)
            print(f'\t{row[0]} {row[1]} {row[2]} {row[3]}')
                
            line_count += 1

        print(f'Processed {line_count} lines.')

    return "tried"

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
            else:
                db.session.add(Pokemon(number=int(float(row[0])), name=row[1],    type_one=row[2],  type_two=row[3],  generation=int(float((row[14]))), height=row[41],  weight=row[42] ))
                db.session.commit()
                print(f'\t{row[0]} {row[1]} {row[2]} {row[3]} {row[14]} {row[41]} {row[42]} ')
                line_count += 1
        print(f'Processed {line_count} lines.')
    return "tried"

