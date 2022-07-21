from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.validators import DataRequired

# Create a Flask instance
app = Flask(__name__)
app.config['SECRET_KEY'] = "My secret key for movies buddy"

selected_genre = []

# Create a Form Class for homepage

class ButtonForm(FlaskForm):
    submit = SubmitField("Find a movie")

# Create a Form Class for input
class OptionsForm(FlaskForm):
    submit = SubmitField("Find a movie")

@app.route('/', methods=['GET', 'POST'])
def home():
    form = ButtonForm()
    return render_template('index.html', form=form)

@app.route('/input', methods=['GET', 'POST'])
def user_input():
    form = OptionsForm()
    return render_template('input.html', form=form)



if __name__ == '__main__':               # this should always be at the end
    app.run(debug=True, host="0.0.0.0")