from .init_app import db, ma

# create database model
class VoteCount(db.Model):
    __tablename__ = 'voteCount'
    id = db.Column(db.Integer, primary_key = True)
    candidate = db.Column(db.String(200), unique = True, nullable = False)
    votes = db.Column(db.Integer)

    def __init__(self, candidate, votes):
        self.candidate = candidate
        self.votes = votes

# create schema for the model
class VoteCountSchema(ma.Schema):
    class Meta:
        fields = ('id', 'candidate', 'votes')