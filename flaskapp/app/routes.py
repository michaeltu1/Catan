from flask import Flask, render_template

flask_app = Flask(__name__)


@flask_app.route('/')
def home():
    return render_template('home.html')


@flask_app.route('/about')
def about():
    return render_template('about.html')


# app = flask_app.wsgi_app

if __name__ == '__main__':
    # app = flask_app.wsgi_app
    flask_app.run(debug=True)
