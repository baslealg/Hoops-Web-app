import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server


os.system('dropdb hoops')
os.system('createdb hoops')
model.connect_to_db(server.app)
model.db.create_all()



# seeds test users from .json file
with open('data/testusers.json') as f:
    user_data = json.loads(f.read())

users_in_db = []
for user in user_data:
    db_user = crud.create_user(username=user['username'], password=user['password'])
    users_in_db.append(db_user)
model.db.session.add_all(users_in_db)
model.db.session.commit()


# seeds test games from .json file
with open('data/testgames.json') as f:
    game_data = json.loads(f.read())

games_in_db = []
for game in game_data:
    db_game = crud.create_game(game_title=game['game_title'], date_time=game['date_time'], max_players=game['max_players'], user=model.User.query.get(game['host_id']))
    games_in_db.append(db_game)
model.db.session.add_all(games_in_db)
model.db.session.commit()


# seeds test locations from .json file
with open('data/testlocations.json') as f:
    locations_data = json.loads(f.read())

locations_in_db = []
for location in locations_data:
    db_location = crud.create_location(game=model.Game.query.get(location['game_id']), address=location['address'], latitude=location['latitude'], longitude=location['longitude'])
    locations_in_db.append(db_game)
model.db.session.add_all(locations_in_db)
model.db.session.commit()


# seeds test usergames 
all_test_games = model.Game.query.all()
all_test_users = model.User.query.all()
usergames_in_db = []
for game in all_test_games:
        db_usergame = crud.Usergame(game=game, user= game.user)
        usergames_in_db.append(db_usergame)
model.db.session.add_all(usergames_in_db)
model.db.session.commit()


