from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange
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

class TableParams(FlaskForm):
    name = StringField('Table Name:', validators=[DataRequired()])
    rows = IntegerField('Rows:', validators=[DataRequired(), NumberRange(min=1, message='Number must be greater than 1.')] )
    columns = IntegerField('Columns:', validators=[DataRequired(), NumberRange(min=1, message='Number must be greater than 1.')] )
    submit = SubmitField('Save Table')



