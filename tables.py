from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app


class packagesdetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    packagename = db.Column(db.String(100), unique=False, nullable=False)
    Description = db.Column(db.String(300), unique=False, nullable=False)
    version = db.Column(db.String(10), unique=False, nullable=False)

    def __init__(self, packagename, Description, version):
        self.packagename = packagename
        self.Description = Description
        self.version = version
# db.create_all()


class repositoriesdetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    repositoriename = db.Column(db.String(100), unique=False, nullable=False)
    branchname = db.Column(db.String(100), unique=False, nullable=False)
    activestatus = db.Column(db.Boolean, unique=False, nullable=True)
    accountname = db.Column(db.String(20), unique=False, nullable=False)

    def __init__(self, repositoriename, branchname, activestatus, accountname):
        self.repositoriename = repositoriename
        self.branchname = branchname
        self.activestatus = activestatus
        self.accountname = accountname
# db.create_all()
