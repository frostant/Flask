from flask import Flask, url_for, escape
app = Flask(__name__)

# @app.route('/hello')
# def hello_world():
#     return 'hellosssd_frostant'
# @app.route('/')
@app.route('/home/<name>')
def hello(name):
    return 'User%s ' % escape(name) 
    # return '<h1>Hello Totoros!</h1><img src="http://helloflask.com/totoro.gif">'

app.add_url_rule('/list/', 'hellos', hello)

# def hello_mine():
#     return 'hello mine!'
# app.add_url_rule('/','mine',hello_mine)

if __name__ == '__main__':
    app.debug = True
    app.run()

