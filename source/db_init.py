from os import mkdir
from classes import db

mkdir("../data")
db.create_all()
