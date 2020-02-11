from flask import Flask, escape, url_for, request, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import click

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
# 这个不是很理解
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(20))

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(10))

@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop')
def initdb(drop):
    if(drop):
        db.drop_all()
    db.create_all()
    click.echo('Initialized database')

@app.cli.command()
def forge():
    """fake data"""
    db.create_all()
    name = 'frostant'
    movies = [
        {'title':'My love','year':'2000'},
        {'title':'My frost','year':'2001'},
        {'title':'My dream','year':'2002'},
        {'title':'My her','year':'2003'},
    ]
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)
    
    db.session.commit()
    click.echo('Done')

@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)
# 相当于全局变量

@app.errorhandler(404)
def  page_not_found(e):
    return render_template('404.html'),404

@app.route('/')
def index():
    movies = Movie.query.all()
    return render_template('index.html',movies=movies)

