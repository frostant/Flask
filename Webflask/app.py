from flask import Flask, escape, url_for, request, render_template
from flask import redirect, flash
from flask_sqlalchemy import SQLAlchemy
import os
import click

app = Flask(__name__)
# app.send_file_max_age_default = timedelta(seconds=1)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
app.config['SECRET_KEY'] = 'dev' # 等同于 app.secret_key = 'dev'
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
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

@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year)>4:
            flash('Invalid change')
            return redirect(url_for('edit',movie_id=movie_id))
        movie.title = title
        movie.year = year
        db.session.commit()
        flash('Item updated')
        return redirect(url_for('index'))
    return render_template('edit.html',movie=movie)

@app.route('/movie/delete/<int:movie_id>', methods=['GET', 'POST'])
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted')
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form.get('title')
        year = request.form.get('year')
        if not title or not year or len(year) >4:
            flash('Invalid input. ')
            return redirect(url_for('index'))
        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash('Item created')
        return redirect(url_for('index'))

    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html',movies=movies)

