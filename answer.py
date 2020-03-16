# You might need to add more of these import statements as you implement your controllers.
from app import app
from flask import render_template, request, session
from helpers import GENRES_LIST
from helpers import get_four_choices
from bs4 import BeautifulSoup as bs
import requests
from firebase import firebase

@app.route('/answer', methods=['post'])
def answer():
    genre_ints = get_four_choices(GENRES_LIST)

    guess = str(request.form['guess'])
    answer = str(session['answer'])

    genre = session['genre']
    username = session['username']

    correct_song_title = session['correct_title']
    correct_song_artist = session['correct_artist']

    # youtube video
    base = "https://www.youtube.com/results?search_query="
    qstring = correct_song_title.replace(" ", "+") + "+" + correct_song_artist.replace(" ", "+")
    final_q = base+qstring
    vid = requests.get(base+qstring)
    vid_page = vid.text
    soup = bs(vid_page, 'html.parser')
    vids = soup.findAll('a', attrs={'class':'yt-uix-tile-link'})
    video = vids[0]['href']
    video = video[9:]

    # leaderboard

    db_cursor = firebase.FirebaseApplication('https://leaderboard183.firebaseio.com/', None)

    data = {}

    data['query'] = final_q

    data['video'] = "https://www.youtube.com/embed/"+video

    if guess == answer:
        session['score'] += 1
        data['is_correct'] = 1

        players = db_cursor.get('/score', None)
        if username not in players:
            db_cursor.put('/score', username, 1)
        else:
            player_score = players[username]
            db_cursor.put('/score', username, player_score + 1)

    else:
        data['is_correct'] = 0

    session['attempts'] += 1

    players = db_cursor.get('/tries', None)
    if username not in players:
        db_cursor.put('/tries', username, 1)
    else:
        player_score = players[username]
        db_cursor.put('/tries', username, player_score + 1)

    scores = db_cursor.get('/score', None)
    data['leaderboard'] = []

    for key, value in sorted(scores.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        data['leaderboard'].append("%s: %s" % (key, value))

    data['correct'] = str(session['answer'])
    data['guess'] = str(guess)

    data['genre'] = genre
    data['username'] = username
    data['correct_title'] = correct_song_title
    data['correct_artist'] = correct_song_artist

    data['score'] = str(session['score'])
    data['attempts'] = str(session['attempts'])

    return render_template("answer.html", **data)
