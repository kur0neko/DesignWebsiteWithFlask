from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, MultipleFileField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange, ValidationError
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
    
    def validate_note_name(self,check):
        for note in self.notelist:
            if check.data == note.note_name:
                raise ValidationError('This note name already exists')
    
    note_body = StringField('Note', widget=TextArea())
    image_upload = MultipleFileField('Image', name='image')
    submit = SubmitField('Create Note')

class TableParams(FlaskForm):
    name = StringField('Table Name:', validators=[DataRequired()])
    rows = IntegerField('Rows:', validators=[DataRequired(), NumberRange(min=1, message='Number must be greater than 1.')] )
    columns = IntegerField('Columns:', validators=[DataRequired(), NumberRange(min=1, message='Number must be greater than 1.')] )
    submit = SubmitField('Save Table')

class updateName (FlaskForm):
    oldname = StringField('Old username', validators=[DataRequired()])

    def validate_oldname(self,check):
        if(check.data != self.username):
             raise ValidationError('oldname has to be same as current username')

    newname = StringField('New username', validators=[DataRequired()])

    def validate_newname(self,check):
        if(self.oldname.data == check.data):
             raise ValidationError('New name cannot be the same as your old name')
   
    submit = SubmitField('Update')

class updatePassword (FlaskForm):
    oldpassword = PasswordField('Old password', validators=[DataRequired()])

    def validate_oldpassword(self,check):
        if(check.data != self.password):
             raise ValidationError('old password has to be same as current password')

    newpassword = PasswordField('New password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])

    def validate_newpassword(self,check):
        if(self.oldpassword.data == check.data):
             raise ValidationError('New password cannot be the same as your old password')

    confirm  = PasswordField('Repeat New Password')
   
    submit = SubmitField('Update')

class Editbox(FlaskForm):
    note_body = StringField('Note', widget=TextArea())
    image_upload2 = MultipleFileField('Images2', name='image2')
    save = SubmitField('Save Changes')
    
class NewNoteButton(FlaskForm):
    button = SubmitField('New Note')

class EditNoteButton(FlaskForm):
    button = SubmitField('Edit Note')
    
class SearchForm(FlaskForm):
    searched = StringField('searched', validators=[DataRequired()])
    submit = SubmitField("submit")

class DeleteProfile(FlaskForm):

    typepassword = PasswordField('Type your current password to confirm deletion', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match') ])

    def validate_typepassword(self,check):
        if(check.data != self.password):
             raise ValidationError('The password you typed does not match the your current password')

    confirm  = PasswordField('Repeat New Password')
    confirmDeletion = BooleanField('Confirm Deletion',validators=[DataRequired()])
    submit = SubmitField('Delete Profile')

class  tableEntry(FlaskForm):

    row = IntegerField('Row:')
    column = IntegerField('Column:')
    note = SelectField('Select a Note')
    string =  StringField('Content:')
    submit = SubmitField('Save Cell')

class modifyParams(FlaskForm):
    rows = IntegerField('Rows:', validators=[DataRequired(), NumberRange(min=1, message='Number must be greater than 1.')] )
    columns = IntegerField('Columns:', validators=[DataRequired(), NumberRange(min=1, message='Number must be greater than 1.')] )
    submit = SubmitField('Save Changes')





