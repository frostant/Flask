from flask import Flask, escape, url_for, request, render_template
app = Flask(__name__)

name = 'frostant'
movies = [
    {'title':'My love','year':'2000'},
    {'title':'My frost','year':'2001'},
    {'title':'My dream','year':'2002'},
    {'title':'My her','year':'2003'},
]

@app.route('/')
def index():
    return render_template('index.html',name=name,movies=movies)

