import random
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from movieSuggester import getMovies

# Create a Flask instance
app = Flask(__name__)
app.config['SECRET_KEY'] = "My secret key for movies buddy"

selected = []
genres = ""
minimumUserRating = ""
streamingServices = []

# Create a Form Class for homepage

class ButtonForm(FlaskForm):
    submit = SubmitField("Find a movie")


@app.route('/', methods=['GET', 'POST'])
def home():
    form = ButtonForm()
    return render_template('index.html', form=form)


@app.route('/options', methods=['GET', 'POST'])
def options():
    # return request.method 
    if request.method == "POST":
        global selected
        selected = request.form.getlist('options')

        if len(selected) > 1:
            return redirect(url_for('input1'))
        if len(selected) == 1:
            return redirect(url_for('selectedMovie'))  

    return render_template('options.html')


@app.route('/input', methods=['GET', 'POST'])
def input1():
    print("My selected list:", selected)

    global genres, minimumUserRating, streamingServices

    if request.method == "POST":
        genres = request.form.get("genre")
        minimumUserRating = request.form.get("minimumUserRating")
        streamingServices = request.form.getlist("streamingservices")

        return redirect(url_for('selectedMovie'))

    return render_template('input.html', selected=selected)


@app.route('/discover', methods=['GET', 'POST'])
def selectedMovie():

    if genres == "" and minimumUserRating == "" and streamingServices == []:
        movies = getMovies("", "", [])
        print("Yes, I am here")
    else:
        movies = getMovies(genres, minimumUserRating, streamingServices)
    
    movieNumber = random.randint(0, len(movies["results"]) - 1)
    selectedMovie = movies["results"][movieNumber]
    movieT = selectedMovie["title"]
    # print("Genres list:", genres)
    # print("rating list:", minimumUserRating)
    # print("ss list:", streamingServices)
    # movieT = "MAybe"

    return render_template('selectedMovie.html', movieTitle=movieT)

if __name__ == '__main__':               # this should always be at the end
    app.run(debug=True, host="0.0.0.0")