from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    noter = db.relationship('Note', backref ='owner', lazy = 'dynamic')

    def __repr__(self):
       return f'{self.id}: {self.username}'

class Note(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    note_name = db.Column(db.String(15))
    note_body = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<note {self.id}: {self.note_name}>'

