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

book_tags = db.Table('book_tags',
  db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True),
  db.Column('book_id', db.Integer, db.ForeignKey('books.id'), primary_key=True)
)

class Book(db.Model):
  __tablename__ = 'books'

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(255))
  author_id = db.Column(db.Integer, db.ForeignKey("authors.id"))

  author = db.relationship("Author", back_populates="books")
  tags = db.relationship("Tag", secondary=book_tags, 
            back_populates="books", lazy="subquery", 
            cascade="all,delete")

class Tag(db.Model):
  __tablename__ = 'tags'

  id = db.Column(db.Integer, primary_key=True)
  tag = db.Column(db.String(50), unique=True)

  books = db.relationship("Book", secondary=book_tags, 
              back_populates="tags", cascade="delete")

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

class TagSchema(ma.TableSchema):
  class Meta:
    table = Tag.__table__
    fields = ['tag']

# Defining via model or table schema
# class BookSchema(ma.TableSchema):
#   class Meta:
#     table = Book.__table__
#     fields = ('id', 'title', 'author')
  
#   author = ma.Nested(AuthorSchema)

#   links = ma.Hyperlinks({
#     'self': {
#       'href': ma.URLFor('book', id='<id>'),
#       'title': 'book_detail'
#     },
#     'collection': ma.URLFor('book'),
#   })

# If we want to reference the hyper link instead of nest the model
class BookSchema(ma.ModelSchema):
  class Meta:
    model = Book
    fields = ('id', 'title', 'author', 'tags')
  
  author = ma.HyperlinkRelated("one_author")
  tags = ma.List(ma.Nested(TagSchema))

  links = ma.Hyperlinks({
    'self': {
      'href': ma.URLFor('book', id='<id>'),
      'title': 'book_detail'
    },
    'collection': ma.URLFor('book'),
  })

user_schema = UserSchema()
users_schema = UserSchema(many=True)
author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)
book_schema = BookSchema()
books_schema = BookSchema(many=True)
tag_schema = TagSchema()
tags_schema = TagSchema(many=True)

# --------- Sum Seed data --------- #
author = Author.query.filter_by(name="Chuck Paluhniuk").one()
# author_schema = AuthorSchema()
book = Book(title="Fight Club", author=author)
# db.session.add(author)
db.session.add(book)
jrrt = Author.query.filter_by(name="J.R.R. Tolkien").one()
jrrt_books = [
  Book(title="The Hobbit", author=jrrt),
  Book(title="The Lord of the Rings", author=jrrt),
  Book(title="The Silmarillion", author=jrrt),
]
db.session.add_all(jrrt_books)
db.session.commit()
tag = Tag(tag="fantasy")
lotr = db.session.query(Book).filter_by(author_id=2).all()
for book in lotr:
  book.tags.append(tag)
lotr.tags.append(tag)
db.session.commit()

db.create_all()