from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    usergames = db.relationship("Usergame", back_populates="user")
    games = db.relationship("Game", back_populates="user")

    def __repr__(self):
        return f'<User user_id={self.user_id} username={self.username}>'

class Game(db.Model):
    """A game."""
    __tablename__ = 'games'

    game_id = db.Column(db.Integer, primary_key=True)
    game_title = db.Column(db.String, nullable=False)
    date_time = db.Column(db.DateTime)
    max_players = db.Column(db.Integer, nullable=False)
    host_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    user = db.relationship("User", back_populates="games")
    usergames = db.relationship("Usergame", back_populates="game")
    location = db.relationship("Location", uselist=False, back_populates="game")

    def __repr__(self):
        return f'<Game game_id={self.game_id} game_title={self.game_title}>'

class Usergame(db.Model):
    """A usergame"""
    __tablename__ = 'usergames'

    usergame_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    game_id = db.Column(db.Integer, db.ForeignKey('games.game_id'))


    game = db.relationship("Game", back_populates="usergames")
    user = db.relationship("User", back_populates="usergames")

    def __repr__(self):
            return f'<Usergame usergame_id={self.rating_id}>'

class Location(db.Model):
    """A location."""

    __tablename__ = 'locations'

    location_id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.game_id'))
    address = db.Column(db.String, nullable=False)
    latitude = db.Column(db.String, nullable=False)
    longitude = db.Column(db.String, nullable=False)

    game = db.relationship("Game", back_populates="location")

    def __repr__(self):
        return f'<Location location_id={self.location_id} game_id={self.game_id}>'
    

def connect_to_db(flask_app, db_uri="postgresql:///hoops", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
