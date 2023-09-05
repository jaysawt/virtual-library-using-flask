from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.app_context().push()



#INSERTING VALUES INTO DATABASES USING sqlite3 (errors in queries are not visible in this)
# import sqlite3
# db = sqlite3.connect('books-collection.db')
# cursor = db.cursor()
# cursor.execute('CREATE TABLE books('
#                'id INT Primary key,title varchar(250) NOT NULL UNIQUE,author varchar(250) NOT NULL,rating FLOAT NOT NULL)')
# cursor.execute('INSERT INTO books VALUES(1,"Harry Poter","J.K. Rowlings",9.3)')
# db.commit()


#INSERTING VALUES AND CREATING DATABASE USING SQL ALCHEMY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#CREATING TABLE IN DATABASE


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), unique=True, nullable=False)
    author = db.Column(db.String(150), nullable=False)
    ratings = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'


# db.create_all()

# ----------CRUD OPERATIONS----------------------#
#
# # CREATE RECORD
# data = Books(title='Harry Potter', author='J.K Rowling', ratings=9.3)
# db.session.add(data)  # this is done so that the row is added only one time
# db.session.commit()
#
# #READ RECORD
# all_record = Books.query.all()
# print(all_record)
# particular_record = Books.query.filter_by(title='Harry Potter').first()
# print(particular_record.author)

# #UPDATE RECORD
# book_id = 1
# find_record_to_update = Books.query.get(book_id)
# find_record_to_update.title = 'Harry Potter and the chamber of secrets'
# db.session.commit()
#
# find_record_to_update_2 = Books.query.filter_by(title='Harry Potter and the chamber of secrets').first()
# find_record_to_update_2.title = 'Harry Potter and the Goblet of fire'
# db.session.commit()
#
# all_record = Books.query.all()
# print(all_record)
#
#
# #DELETE RECORD
# find_record_to_delete = Books.query.get(book_id)
# db.session.delete(find_record_to_delete)
# db.session.commit()

@app.route('/')
def home():
    data_from_database = db.session.query(Books).all()
    return render_template('index.html', items=data_from_database)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        add_record = Books(title=request.form['book'], author=request.form['author'], ratings=request.form['rating'])
        db.session.add(add_record)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')


@app.route('/edit/id=<int:srno>', methods=['GET', 'POST'])
def change(srno):
    if request.method == 'POST':
        change_rating = Books.query.get(srno)
        change_rating.ratings = request.form['changed_rating']
        db.session.commit()
        return redirect(url_for('home'))
    else:
        #book_id = request.args.get('id') this can be used instead of passing "srno" and then book_selected = Book.query.get(book_id) can be used to pass in book parameter
        data_of_database = db.session.query(Books).all()
        return render_template('edit_rating.html', book=data_of_database[srno-1])


@app.route('/delete/<int:num>')
def delete(num):
    record_delete = Books.query.get(num)
    db.session.delete(record_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

    # note: the sql alchemy gives unique key error because the app runs multiple times in debug=True mode and as a result
    #the row get added multiple times and the error is generated