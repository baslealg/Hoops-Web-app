from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from model import connect_to_db, db
import model
import crud
from flask import Flask
from jinja2 import StrictUndefined
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/', methods=['GET', 'POST'])
def homepage():
    """View homepage."""
    google_maps_api_key = os.environ.get('GOOGLE_MAPS_AUTH_TOKEN')
    session['zipcode'] = 10001
    if request.method == 'POST':
        zipcode = request.form['zip_code']
        if not crud.is_valid_city(zipcode):
            flash("Not a valid zipcode", error)
        else:
            session['zipcode'] = zipcode
            return redirect('/games')
    return render_template('homepage.html', google_maps_api_key=google_maps_api_key)

@app.route('/games', methods=['GET', 'POST'])
def games_page():
    google_maps_api_key = os.environ.get('GOOGLE_MAPS_AUTH_TOKEN')
    if request.method == 'POST':
        zipcode = request.form['zip_code']
        if not crud.is_valid_city(zipcode):
            flash("Not a valid zipcode or city")
        else:
            session['zipcode'] = zipcode
    games = crud.get_games(session['zipcode'])
    games_num_players = {}
    for game in games:
        games_num_players[game.game_id] = crud.get_num_players(game.game_id)
    return render_template('games.html', games=games, games_num_players= games_num_players, google_maps_api_key=google_maps_api_key)

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        phone_number = request.form['phone_number']
        if crud. is_valid_phone_number(phone_number):
            crud.send_welcome_message(phone_number)
            user = crud.create_user(username=username, password=password, phone_number=phone_number)
            session['logged_in_user'] = user.user_id
            flash("Account created successfully!")
            return redirect('/dashboard')
        else:
            flash('Please enter a valid phone number')
            return render_template('create_account.html')
    else:
        return render_template('create_account.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = model.User.query.filter_by(username=username, password=password).first()

        if user:
            session['logged_in_user'] = user.user_id
            flash('succesfully logged in!')
            return redirect('/dashboard')
        else:
            flash('Incorrect username or password')


    return render_template('login.html',)

@app.route('/dashboard')
def dashboard():
    """View dashboard"""
    user = model.User.query.get(session['logged_in_user'])
    return render_template('dashboard.html', user=user)

@app.route('/create_game', methods=['GET', 'POST'])
def create_game():
    if request.method == 'POST':
        game_title = request.form['game_title']
        iso_string = request.form['date_time']
        date_time = datetime.fromisoformat(iso_string)
        max_players = request.form['max_players']
        location = request.form['location']
        if crud.is_valid_city(location):
            lat, lng = crud.location_lat_long(location)
            user = model.User.query.get(session['logged_in_user'])
            print('***********************************************************************', date_time)
            game =crud.create_game(game_title=game_title, date_time=date_time, max_players=max_players, user=user)
            location_game = crud.create_location(game=game, address=location, latitude=lat, longitude=lng)
            user_game = crud.create_usergame(game=game, user=user)
            flash('Successfully created a game!')
            return redirect('/dashboard')
        else:
           flash('Invalid Location', 'error')
           return render_template('create_game.html') 
    else:
        return render_template('create_game.html')
    

@app.route('/join_game/<game_id>')
def join_game(game_id):
    if 'logged_in_user' not in session:
        flash('Please log in or create an account')
        return redirect('/login')
    else:
        user = model.User.query.get(session['logged_in_user'])
        game = model.Game.query.get(game_id)
        usergame = crud.create_usergame(game, user)
        phone_number = int(user.phone_number)
        game_title = game.game_title
        game_time = game.date_time
        crud.send_join_game_message(game_title=game_title, game_time=game_time, phone_number=phone_number)
        flash('Succesfully joined game!')
        return redirect('/dashboard')

@app.route('/api/locations')
def get_locations():
    locations = model.Location.query.all()
    locations_list = []
    for location in locations:
        location_dict = {
            'location_id': location.location_id,
            'game_id': location.game_id,
            'address': location.address,
            'latitude': location.latitude,
            'longitude': location.longitude
        }
        locations_list.append(location_dict)
    return jsonify(locations_list)


@app.route('/api/zipcode')
def get_zipcode():
    if session['zipcode']:
        return jsonify({'zipcode': session['zipcode']})

@app.route('/logout')
def logout():
    session.pop('logged_in_user', None)
    flash('Succesfully Logged Out')
    return redirect('/')

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)