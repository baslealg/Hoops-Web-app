from model import db, User, Location, Game, Usergame, connect_to_db


def create_user(username, password):
    """Create and return a new user."""

    user = User(username=username, password=password)

    return user


def create_game(game_title, date_time, max_players, user):
    """Create and return a new game."""

    game = Game(game_title=game_title, date_time=date_time, max_players=max_players, user=user)


    return game

"""currently this function gets all games but once google maps incorped it will get games by zipcode"""
def get_games():
    all_games = Game.query.all()
    return all_games

def create_usergame(game, user):
    """Create and return a new usergame."""
    usergame = Usergame(game=game, user=user)

    return usergame

def create_location(game, address, latitude, longitude):
    """Create and return a location."""
    location = Location(game=game, address=address, latitude=latitude, longitude=longitude)

    return location

if __name__ == '__main__':
    from server import app
    connect_to_db(app)