# You might need to add more of these import statements as you implement your controllers.
from app import app
from flask import render_template, session, request
from helpers import GENRES_LIST
from helpers import get_four_choices
import json

@app.route('/', methods=['POST', 'get'])
def index():

    if 'attempts' not in session:
        session['attempts'] = 0
    if 'score' not in session:
        session['score'] = 0

    data = {}

    if request.method == 'POST':
        data['tits'] = 'tits'
        if request.form['desicion'] == 'yes':
            session['attempts'] = 0
            session['score'] = 0

    genres = []

    counter = 0
    for genre in GENRES_LIST:
        temp = {}
        temp['genre'] = genre
        temp['chart_title'] = GENRES_LIST.values()[counter]
        genres.append(temp)
        counter += 1

    data['genres'] = genres
    data['attempts'] = str(session['attempts'])
    data['score'] = str(session['score'])

    return render_template("index.html", **data)
