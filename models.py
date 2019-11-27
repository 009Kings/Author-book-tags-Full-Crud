from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kingkong@localhost/flasktoot1'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True)
  email = db.Column(db.String(120), unique=True)

  def __init__(self, username, email):
    self.username = username
    self.email = email

class Author(db.Model):
  __tablename__ = 'authors'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255))

  books = db.relationship("Book", back_populates="author", lazy="dynamic")

class Book(db.Model):
  __tablename__ = 'books'

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(255))
  author_id = db.Column(db.Integer, db.ForeignKey("authors.id"))

  author = db.relationship("Author", back_populates="books")

class UserSchema(ma.Schema):
  class Meta:
    # Fields to expose
    fields = ('id', 'username', 'email')

class AuthorSchema(ma.ModelSchema):
  class Meta:
    model = Author
    fields = ('id', 'name', 'books')
  
  books = ma.List(ma.HyperlinkRelated("one_book"))

  links = ma.Hyperlinks({
    'self': ma.URLFor('author', id='<id>'),
    'collection': ma.URLFor('author'),
  })


# Defining via model or table schema
class BookSchema(ma.TableSchema):
  class Meta:
    table = Book.__table__
    fields = ('id', 'title', 'author')
  
  author = ma.Nested(AuthorSchema)

  links = ma.Hyperlinks({
    'self': {
      'href': ma.URLFor('book', id='<id>'),
      'title': 'book_detail'
    },
    'collection': ma.URLFor('book'),
  })

# If we want to reference the hyper link instead of nest the model
# class BookSchema(ma.ModelSchema):
#   class Meta:
#     model = Book
#     fields = ('id', 'title', 'author')
  
#   author = ma.HyperlinkRelated("one_author")
#   # author = ma.Nested(AuthorSchema)

#   links = ma.Hyperlinks({
#     'self': {
#       'href': ma.URLFor('book', id='<id>'),
#       'title': 'book_detail'
#     },
#     'collection': ma.URLFor('book'),
#   })

user_schema = UserSchema()
users_schema = UserSchema(many=True)
author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)
book_schema = BookSchema()
books_schema = BookSchema(many=True)

# --------- Sum Seed data --------- #
# author = Author(name="Chuck Paluhniuk")
# author_schema = AuthorSchema()
# book = Book(title="Fight Club", author=author)
# db.session.add(author)
# db.session.add(book)
# db.session.commit()

db.create_all()