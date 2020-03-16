# You might need to add more of these import statements as you implement your controllers.
from app import app
from flask import render_template, session, request
from helpers import GENRES_LIST
from helpers import get_four_choices
import json

@app.route('/clear')
def clear():

    data = {}
    data['attempts'] = session['attempts']
    data['score'] = session['score']

    return render_template("clear.html", **data)
