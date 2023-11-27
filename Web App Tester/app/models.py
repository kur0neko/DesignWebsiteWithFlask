from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    noter = db.relationship('Note', backref ='owner', lazy = 'dynamic', cascade = 'all')
    tabler = db.relationship('Table', backref ='owner', lazy = 'dynamic', cascade = 'all') #build the relationship between the table and the user, so when a user is deleted their is a cascading delete 


    def __repr__(self):
       return f'{self.id}: {self.username}'

class Note(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    note_name = db.Column(db.String(15), unique=True)
    note_body = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<note {self.id}: {self.note_name}>'
    
    images = db.relationship('Image', backref ='note', lazy = 'dynamic')


class Table(db.Model):                                          #model for table 

    id = db.Column(db.Integer, primary_key=True)                #table id/primary key
    table_name = db.Column(db.String(15))                       #name of table
    numRows = db.Column(db.Integer)                             #number of rows
    numColumns = db.Column(db.Integer)                          #number of columns
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))   #foriegn key which allows user to have one to many relationship with table  

    def __repr__(self):
        return f'<table {self.id}: {self.table_name}>'          #define a string rep of the table itself


class TableEntries(db.Model):                                   #model for table entries
    id = db.Column(db.Integer, primary_key=True)                #primary key for the table which is id
    entryRow = db.Column(db.Integer)                            #entryRow is the row of the cell's entry
    entryColumn = db.Column(db.Integer)                         #column of the cell's entry
    entry_String = db.Column(db.String(1000))                   #string that user types in the cell
    entry_Note = db.Column(db.Integer)                          #id of the note in the cell
    table_id = db.Column(db.Integer, db.ForeignKey('table.id')) #foriegn key to reresent the one to many relationship the table has to the table enteries

    def __repr__(self):
        return f'<tableEntr {self.id}: {self.entry_String}>'    #define a string rep of the table entries
    
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.LargeBinary)
    mimetype = db.Column(db.Text, nullable=False)
    imgname = db.Column(db.String(100), nullable=False)
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'))
    def __repr__(self):
        return f'<image {self.img}: {self.id}>'