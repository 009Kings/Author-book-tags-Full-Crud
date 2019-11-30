from flask import request, jsonify, redirect
from models import app, db, User, user_schema, users_schema, Author, author_schema, authors_schema, Book, book_schema, books_schema, Tag, tags_schema

def add_tag(book_id, tag_name):
  if book_id:
    try:
      book = Book.query.filter_by(id=book_id).one()
      tag = Tag.query.filter_by(tag=tag_name).one_or_none()
      if not tag:
        tag = Tag(tag=tag_name)
      if book and tag:
        book.tags.append(tag)
        db.session.commit()
        return redirect(f"/api/book/{book_id}")
      else:
        return jsonify(message='Problem in adding Tag')
    except Exception as err:
      print("💥", err)
      return jsonify(message='Problem adding tag')
  else:
    try:
      tag = Tag.query.filter_by(tag=tag_name).one_or_none()
      if not tag:
        db.session.add(Tag(tag=tag_name))
        db.session.commit()
      return redirect('/api/tag')
    except Exception as err:
      print("💥", err)
      return jsonify(message='Problem adding tag')

def remove_tag(book_id, tag):
  try:
    book = Book.query.filter_by(id=book_id).one_or_none()
    tag = Tag.query.filter_by(tag=tag).one_or_none()
    if book and tag:
      book.tags.remove(tag)
      db.session.commit()
      return redirect(f"/api/book/{book_id}")
    else:
      return jsonify(message=f"problem removing tag {tag} from book at id {book_id}")
  except Exception as err:
    print("💥", err)
    return jsonify(message='Problem removing tag from book')

def get_all_tags():
  try:
    all_tags = Tag.query.all()
    return tags_schema.jsonify(all_tags, many=True)
  except Exception as err:
    print("💥", err)
    return jsonify(message='Problem getting all tags')

def delete_tag(tag_id):
  try:
    tag = Tag.query.get(tag_id)
    if tag:
      db.session.delete(tag)
      db.session.commit()
    return redirect("/api/tag")
  except Exception as err:
    print("💥", err)
    return jsonify(message=f'Problem deleting tag at id {tag_id}')

def create_book(title, author):
  new_book = Book(title=title, author_id=author)
  try:
    existing = Book.query.filter_by(title=title).filter_by(author_id=author).one_or_none()
    if not existing:
      db.session.add(new_book)
      db.session.commit()
      return book_schema.dump(new_book)
    else:
      return jsonify(message='Book already exists')
  except Exception as err:
    print("💥", err)
    return jsonify(message='Problem creating new book')

def get_all_books():
  all_books = Book.query.all()
  if all_books:
    result = books_schema.dump(all_books)
    return jsonify(result)
  else: 
    return jsonify(message='No books')

def get_book(id):
  book = Book.query.get(id)
  print("📖", book.tags[0].id)
  if book:
    return book_schema.jsonify(book)
  else:
    return jsonify(message='Error getting book at {}'.format(id))

def update_book(id, title, author):
  try:
    book = Book.query.get(id)
    book.title = title
    book.author = author
    db.session.commit()

    return redirect(f'/api/book/{id}')
  except Exception as err:
    print("💥", err)
    return jsonify(message='Error updating author at {}'.format(id))

def delete_book(id):
  try:
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()

    return redirect('/api/book')
  except Exception as err:
    print("💥", err)
    return jsonify(message='Error deleting book at {}'.format(id))

def create_author(name):
  new_author = Author(name=name)
  try:
    db.session.add(new_author)
    db.session.commit()
    return author_schema.dump(new_author)
  except Exception as err:
    print("💥", err)
    return jsonify(message='Problem creating new author')

def get_all_authors():
  all_authors = Author.query.all()
  if all_authors:
    return authors_schema.jsonify(all_authors, many=True)
  else: 
    return jsonify(message='No authors')

def get_author(id):
  author = Author.query.get(id)
  if author:
    # for book in author.books.all():
    #   print("📖", book.title)
    return author_schema.jsonify(author, many=False)
  else:
    return jsonify(message='Error getting author at {}'.format(id))

def update_author(id, name):
  try:
    author = Author.query.get(id)
    author.name = name
    db.session.commit()

    return redirect(f'/api/author/{id}')
  except Exception as err:
    print("💥", err)
    return jsonify(message='Error updating author at {}'.format(id))

def delete_author(id):
  try:
    author = Author.query.get(id)
    db.session.delete(author)
    db.session.commit()

    return redirect('/api/author')
  except Exception as err:
    print("💥", err)
    return jsonify(message='Error deleting author at {}'.format(id))

def create_user(username, email):
  new_user = User(username, email)
  try:
    db.session.add(new_user)
    db.session.commit()
    return user_schema.dump(new_user)
  except Exception as err:
    print("💥", err)
    return jsonify(message='User already exists')

def get_all_users():
  all_users = User.query.all()
  if all_users:
    result = users_schema.dump(all_users)
    return jsonify(result)
  else: 
    return jsonify(message='No users')

def get_user(id):
  user = User.query.get(id)
  if user:
    return user_schema.jsonify(user)
  else:
    return jsonify(message='Error getting user at {}'.format(id))

def update_user(id, username, email):
  try:
    user = User.query.get(id)
    user.email = email
    user.username = username
    db.session.commit()

    return redirect(f'/api/user/{id}')
  except Exception as err:
    print("💥", err)
    return jsonify(message='Error updating user at {}'.format(id))

def delete_user(id):
  try:
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/api/user')
  except Exception as err:
    print("💥", err)
    return jsonify(message='Error deleting user at {}'.format(id))
