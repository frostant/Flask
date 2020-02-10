from flask import Flask
app = Flask(__name__)

@app.route('/hello/<name>')
# @ 相当于连接下面一个函数
def hello_name(name):
    return 'Hello %s!' % name

@app.route('/blog/<int:postID>/')
def show_blog(postID):
    return 'Blog ID is %d' % postID


if __name__ == '__main__':
    app.run(debug = True)

# 注意 app.route()末尾加个/更稳定