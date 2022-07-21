from flask import Flask, render_template, request, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired

# Create a Flask instance
app = Flask(__name__)
app.config['SECRET_KEY'] = "My secret key for movies buddy"

# Create a Form Class for homepage

class ButtonForm(FlaskForm):
    submit = SubmitField("Find a movie")

# Create a Form Class for input
class StringForm(FlaskForm):
    s = 

@app.route('/', methods=['GET', 'POST'])
def home():
    form = ButtonForm()
    return render_template('index.html', form=form)

selected = []
@app.route('/options', methods=['GET', 'POST'])

def options():
    # return request.method 
    if request.method == "POST":
        global selected
        selected = request.form.getlist('options')

        if len(selected) > 0:
            return redirect(url_for('input1'))
    return render_template('options.html')

@app.route('/input', methods=['GET', 'POST'])
def input1():
    print(selected)
    return render_template('input.html', selected=selected)


if __name__ == '__main__':               # this should always be at the end
    app.run(debug=True, host="0.0.0.0")