from enum import unique

from app import db


class User(db.Model) :
    id = db.Column(db.Interger, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Item(db.Model) :
    id = db.Column(db.Interger, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)