# src\models.py

from .init_app import db, ma

# Class to create database model
class VoteCount(db.Model):
    """ This class will create the model for the data with the following key values.
            id : primary key (auto generated)
            candidate : name of the candidate (string, unique, nallable)
            votes : number of votes (integer)
            
            tablename : voteCount"""

    __tablename__ = 'voteCount'
    id = db.Column(db.Integer, primary_key = True)
    candidate = db.Column(db.String(200), unique = True, nullable = False)
    votes = db.Column(db.Integer)

    def __init__(self, candidate, votes):
        self.candidate = candidate
        self.votes = votes

# Create schema for the model
class VoteCountSchema(ma.Schema):
    """ This class is used to define the model schema to
        speify the fields need to show from the tabel"""
    class Meta:
        fields = ('id', 'candidate', 'votes')