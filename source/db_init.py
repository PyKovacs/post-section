from os import mkdir
from app import db

mkdir("../data")
db.create_all()
