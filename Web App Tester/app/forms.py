from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.widgets import TextArea

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class CreateAccountForm(FlaskForm):
    name = StringField('Full name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Repeat Password')
    submit = SubmitField('Create Account')

class Notebox(FlaskForm):
    note_name = StringField('Note Name: ', validators=[DataRequired()])
    note_body = StringField('Note', widget=TextArea())
    submit = SubmitField('Save Note')

class Editbox(FlaskForm):
    note_body = StringField('Note', widget=TextArea())
    save = SubmitField('Save Changes')
    
class NewNoteButton(FlaskForm):
    button = SubmitField('New Note')

class EditNoteButton(FlaskForm):
    hidden = HiddenField('Hidden')
    button = SubmitField('Edit Note')
