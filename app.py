from flask import Flask, render_template, request, redirect, url_for, flash 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Secret Key"

ENV = 'prod'

if ENV =='dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/bookstore'
else: # ENV = 'prod'
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://qasrejmhctbuen:65e3a5c223e13d3bfec557977d1f51ff20f6ea6ad4a46bde49833acda4d2672d@ec2-18-235-97-230.compute-1.amazonaws.com:5432/de019m5hdiju8'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30))
    title = db.Column(db.String(40))
    category = db.Column(db.String(100))

    def __init__(self,author,title,category):
        self.author = author
        self.title = title
        self.category = category
        

@app.route('/')
def index():
    all_data = Book.query.order_by(Book.id).all()

    return render_template('index.html', books = all_data)

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        author = request.form['author']
        title = request.form['title']
        category = request.form['category']

        data = Book(author, title, category)
        db.session.add(data)
        db.session.commit()

        flash("Book added!", 'success')

        return redirect(url_for('index'))

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        data = Book.query.get(request.form.get('id'))  # this is a hidden id we created in index.html
        data.author = request.form['author']
        data.title = request.form['title']
        data.category = request.form['category']

        db.session.commit()
        flash(f'Book {data.title} has been updated', 'success')

        return redirect(url_for('index'))

@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    data = Book.query.get(id)
    # data.title = Book.query.get(Book.title).filter(Book.id == id)
    db.session.delete(data)
    db.session.commit()
    flash('Book has been deleted', 'warning')

    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run()