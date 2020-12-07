from web import database

"""
class Users(database.Model):
    __tablename__ = 'users'
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(64), index=True, unique=True)
    email = database.Column(database.String(120), index=True, unique=True)
    password_hash = database.Column(database.String(128))

    def __repr__(self):
        return '<Users {}>'.format(self.username)
"""

class Signatures(database.Model):
    __tablename__ = 'signatures'
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String, index=True, unique=True)
    description = database.Column(database.String)
    author = database.Column(database.String)
    date = database.Column(database.String)
    modified = database.Column(database.String)
    tactic = database.Column(database.String)
    technique = database.Column(database.String)
    subtechnique = database.Column(database.String)
    operating_system = database.Column(database.String)
    dvquery = database.Column(database.String)
    false_positives = database.Column(database.String)
    tags = database.Column(database.String)
    references = database.Column(database.String)

    def __repr__(self):
        return '<Signature: {}>'.format(self.title)
