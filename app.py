from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
from models import BookLinks, similar_books
import pandas as pd
import numpy as np
from googlesearch import search
from sqlalchemy import exc

#Initiate app
app = Flask(__name__)

#Select environment = "prod" or "dev"
ENV = 'dev'

#Route the app config according to prod or dev
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pass@localhost/bookrec'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace('postgres', 'postgresql')
    app.debug = False

#Turn off track modification for sql_alchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Initiate databaase
db = SQLAlchemy(app)

#Get book dataframe and the similarity matrix
book_df = pd.read_csv("data/books719.csv")
simsort = np.load('data/simsort.npy')

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

        if (len(book)<1 or len(number_rec)<0):
            return render_template('index.html',
             message='Please enter a book and number of recommendations')
        else:
            try:
                title = BookLinks([book])
                results = similar_books(title, book_df, int(number_rec), simsort)
                print(results)
                return render_template('success.html', results=results)

            except:
                try: 
                    data = Feedback(book, number_rec)
                    db.session.add(data)
                    db.session.commit()

                    return render_template('index.html',
                    message='This book is not in our database yet, but will be added soon! Please try another book.')
                except exc.IntegrityError:
                    db.session.rollback()
                    return render_template('index.html',
                    message='This book is not in our database yet, but will be added soon! Please try another book.')

if __name__ == '__main__':
    
    app.run()
