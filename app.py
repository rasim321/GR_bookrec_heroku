from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pass@localhost/bookrec'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace('postgres', 'postgresql')
    app.debug = False

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
    __tablename__ = 'book_requests'
    id = db.Column(db.Integer, primary_key=True)
    book = db.Column(db.String, unique=True)
    number_rec = db.Column(db.Integer)

    def __init__(self, book, number_rec):
        self.book = book
        self.number_rec = number_rec


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        book = request.form['name_book']
        number_rec = request.form['number_rec']
        print(book, number_rec)

        if (book == '' or number_rec == ''):
            return render_template('index.html',
             message='Please enter a book and number of recommendations')
        else:
            data = Feedback(book, number_rec)
            db.session.add(data)
            db.session.commit()

            return render_template('success.html')

if __name__ == '__main__':
    
    app.run()
