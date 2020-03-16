# You might need to add more of these import statements as you implement your controllers.
from app import app
from flask import render_template, session, request
from helpers import GENRES_LIST
from helpers import get_four_choices
import billboard
import random
from utility import get_preview_url


@app.route('/question')
def question():
    data = {}

    genre = request.args.get('genre')
    username = request.args.get('username')

    session['username'] = username

    data['genre'] = genre
    session['genre'] = genre
    # genre = 'hot-100'
    chart = billboard.ChartData(genre)
    song_nums = get_four_choices(chart)

    song_list = []
    for num in song_nums:
        temp = {}
        temp['song'] = chart[num]
        temp['index'] = num
        song_list.append(temp)

    correct_index = random.sample(range(4), 1)
    correct_song_index = song_nums[correct_index[0]]

    session['answer'] = correct_song_index
    data['songs'] = song_list

    session['correct_title'] = song_list[correct_index[0]]['song'].title
    session['correct_artist'] = song_list[correct_index[0]]['song'].artist

    found_working_song = False

    song_preview = {}
    while (found_working_song == False):
        song_preview = get_preview_url(song_list[correct_index[0]]['song'].title, song_list[correct_index[0]]['song'].artist)
        if 'error' not in song_preview:
            found_working_song = True

    data['preview'] = song_preview

    data['attempts'] = str(session['attempts'])
    data['score'] = str(session['score'])

    return render_template("question.html", **data)
