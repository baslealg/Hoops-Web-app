from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import model
import crud
from flask import Flask
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')

@app.route('/games')
def games_page():
    games = crud.get_games()
    print(games)
    return render_template('games.html', games=games)

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        return "Account created successfully!"
    else:
        return render_template('create_account.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        # Get the user's email and password from the form data
        username = request.form['username']
        password = request.form['password']

        # Query the database for a user with matching email and password
        user = model.User.query.filter_by(username=username, password=password).first()

        if user:
            
            return redirect('/dashboard')
        else:
            # If no matching user is found, display an error message
            error = "Incorrect email or password. Please try again."


    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    """View dashboard"""

    return render_template('dashboard.html')


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)