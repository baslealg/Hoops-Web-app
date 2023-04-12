from model import db, User, Location, Game, Usergame, connect_to_db
from flask import jsonify

def create_user(username, password):
    """Create and return a new user."""

    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()

    return user


def create_game(game_title, date_time, max_players, user):
    """Create and return a new game."""

    game = Game(game_title=game_title, date_time=date_time, max_players=max_players, user=user)
    db.session.add(game)
    db.session.commit()

    return game

"""currently this function gets all games but once google maps incorped it will get games by zipcode"""
def get_games():
    all_games = Game.query.all()
    return all_games

def create_usergame(game, user):
    """Create and return a new usergame."""
    usergame_check = Usergame.query.filter_by(game=game, user=user).first()
    if usergame_check == None:
        usergame = Usergame(game=game, user=user)
        db.session.add(usergame)
        db.session.commit()
        return usergame

def create_location(game, address, latitude, longitude):
    """Create and return a location."""
    location = Location(game=game, address=address, latitude=latitude, longitude=longitude)

    return location


def get_num_players(game_id):
    num_players = db.session.query(Usergame).filter_by(game_id=game_id).count()
    return num_players


if __name__ == '__main__':
    from server import app
    connect_to_db(app)