from flask import request, jsonify
from models import app
from functions import create_user, get_all_users, get_user, update_user, delete_user
from functions import create_author, get_all_authors, get_author, update_author, delete_author
from functions import create_book, get_all_books, get_book, update_book, delete_book

@app.route("/api/user", methods=["GET", "POST"])
def users_read_create():
  if request.method == "GET":
    return get_all_users()
  if request.method == "POST":
    return create_user(username=request.form['username'], email=request.form['email'])

@app.route("/api/user/<id>", methods=["GET", "PUT", "DELETE"])
def one_user(id):
  if request.method == "GET":
    return get_user(id)
  if request.method == "PUT":
    return update_user(id, request.form['username'], request.form['email'])
  if request.method == "DELETE":
    return delete_user(id)

@app.route("/api/author", methods=["GET", "POST"])
def authors_read_create():
  if request.method == "GET":
    return get_all_authors()
  if request.method == "POST":
    return create_author(name=request.form['name'])

@app.route("/api/author/<id>", methods=["GET", "PUT", "DELETE"])
def one_author(id):
  if request.method == "GET":
    return get_author(id)
  if request.method == "PUT":
    return update_author(id, request.form['name'])
  if request.method == "DELETE":
    return delete_author(id)

@app.route("/api/book", methods=["GET", "POST"])
def books_read_create():
  if request.method == "GET":
    return get_all_books()
  if request.method == "POST":
    return create_book(request.form['title'], request.form['author'])

@app.route("/api/book/<id>", methods=["GET", "PUT", "DELETE"])
def one_book(id):
  if request.method == "GET":
    return get_book(id)
  if request.method == "PUT":
    return update_book(id, request.form['title'], request.form['author'])
  if request.method == "DELETE":
    return delete_book(id)



if __name__ == '__main__':
    app.run(debug=True)