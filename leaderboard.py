from app import app
from flask import render_template, request, session

@app.route('/leaderboard')
def leaderboard():

    username = str(request.form['username'])
    session['info'] = username

    data['info'] = str(session['info'])

return render_template("leaderboard.html", **data)
