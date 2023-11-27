from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, MultipleFileField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange, ValidationError
from wtforms.widgets import TextArea

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class CreateAccountForm(FlaskForm): 
    name = StringField('Full Name', validators=[DataRequired()])                                     #username field with validators
    email = StringField('Email', validators=[DataRequired(), Email()])                                  #email field with validation to make sure that it is an actual email field
    username = StringField('Username', validators=[DataRequired()])                                     #username field with validators

    def validate_username(self,check):                                                                  #extra validator to make sure that every account's username is unique
        for user in self.usernameList:                                                                  #go through every username
            if check.data == user.username:                                                             #if the user's typed username already exists
                raise ValidationError('This username already exists')                                   #raise a validation error

    password = PasswordField('Password',validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])       #password that the user wants for the account, if the confirm and password are not equal validation error is also thrown
    confirm  = PasswordField('Repeat Password')                                                                                #retype password
    submit = SubmitField('Create Account')                                                                                     #submit the account

class Notebox(FlaskForm):
    note_name = StringField('Note Name: ', validators=[DataRequired()])
    
    def validate_note_name(self,check):                                                                 #extra validator to make sure that every note has a unique name
        for note in self.notelist:                                                                      #go through every note's name
            if check.data == note.note_name:                                                            #if the typed note name already exists 
                raise ValidationError('This note name already exists')                                  #raise a validation error
    
    note_body = StringField('Note', widget=TextArea())                                                  
    image_upload = MultipleFileField('Image', name='image')
    submit = SubmitField('Create Note')

class TableParams(FlaskForm):                                                                                                       #user can enter the paramters for their new table
    name = StringField('Table Name:', validators=[DataRequired()])                                                                  #user enters name for their table
    rows = IntegerField('Rows:', validators=[DataRequired(), NumberRange(min=1, message='Number must be greater than 0.')] )        #user enters a row value that is greater than 0
    columns = IntegerField('Columns:', validators=[DataRequired(), NumberRange(min=1, message='Number must be greater than 0.')] )  #user eneters a column value that is greater than 0
    submit = SubmitField('Save Table')

class updateName (FlaskForm):                                                                                           #user can update their username
    oldname = StringField('Please enter your current username', validators=[DataRequired()])                            #user must enter their current username

    def validate_oldname(self,check):                                                                                   #another function to add a validation check such that the current username matches what the user entered as their current username       
        if(check.data != self.username):                                                                                #self.username was passed in routes.py and is used to validate oldusername, and make sure the user enters the correct value
             raise ValidationError('the username you entered has to be same as current username')                                        #if they do not enter the correct value, the validation error is thrown

    newname = StringField('New username', validators=[DataRequired()])                                                  #user can enter their new username in this field                                

    def validate_newname(self,check):                                                                                   #another function to add a validation check such that the current username does not matche what the user entered as their wanted new username
        if(self.oldname.data == check.data):                                                                            #self.username was passed in routes.py and is used to validate newusername, and make sure the user enters the correct value
             raise ValidationError('New name cannot be the same as your old name')                                      #if they do not enter the correct value, the validation error is thrown
   
    submit = SubmitField('Update')                                                                                      #user can submit the form


class updatePassword (FlaskForm):                                                                                           #user can update password
    oldpassword = PasswordField('Please enter your current password', validators=[DataRequired()])                          #user must eneter their current password

    def validate_oldpassword(self,check):                                                                                   #another function to add a validation check such that the current password matches what the user entered as their current password                                 
        if(check.data != self.password):                                                                                    #self.password was passed in routes.py and is used to validate oldpassword, and make sure the user enters the correct value
             raise ValidationError('the password you entered has to be same as current password')                                       #if they do not enter the correct value, the validation error is thrown

    newpassword = PasswordField('New password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')]) #user can enter their new password which must equal to the later field confirm (user retypes their password twice)

    def validate_newpassword(self,check):                                                                                   #another function to add a validation check such that the current password does not matche what the user entered as their wanted newpassword
        if(self.oldpassword.data == check.data):                                                                            #self.password was passed in routes.py and is used to validate newpassword, and make sure the user enters the correct value
             raise ValidationError('New password cannot be the same as your old password')                                  #if they do not enter the correct value, the validation error is thrown

    confirm  = PasswordField('Repeat New Password')                                                                         #user repeats newpassword
   
    submit = SubmitField('Update')                                                                                          #user submits

class Editbox(FlaskForm):
    note_body = StringField('Note', widget=TextArea())
    image_upload2 = MultipleFileField('Images2', name='image2')
    save = SubmitField('Save Changes')
    
class NewNoteButton(FlaskForm):
    button = SubmitField('New Note')

class EditNoteButton(FlaskForm):
    button = SubmitField('Edit Note')
    
class DeleteNoteButton(FlaskForm):
    button = SubmitField('Delete Note')
    

                                                                                                                        
class DeleteProfile(FlaskForm):                                                                                             #form for user to delete their profile

    typepassword = PasswordField('Type your current password to confirm deletion', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match') ])#user types in a password which must equal to the confirm field

    def validate_typepassword(self,check):                                                                                  #another validation check for the typepassword field where routes.py sends in the user's current password and it is checked against the password entered in the form
        if(check.data != self.password):                                                                                    #self.password represents the user's password, and check.data is the typepassword that is entered by the user
             raise ValidationError('The password you typed does not match the your current password')                       #validation error is raised when they are not equal                                       

    confirm  = PasswordField('Repeat Current Password')                                                                         #user must type in their password again
    confirmDeletion = BooleanField('Confirm Deletion',validators=[DataRequired()])                                          #user must confirm the deletion
    submit = SubmitField('Delete Profile')                                                                                  #user can submit the form

                                                                                                                            
class  tableEntry(FlaskForm):                                                                                               #form for user to create an entry
    row = IntegerField('Row:')                                                                                              #cell row where entry is located
    column = IntegerField('Column:')                                                                                        #cell column where entry is located
    note = SelectField('Select a Note')                                                                                     #user must select a link to a note given in routes.py
    string =  StringField('Content:')                                                                                       #user enters any string they would like
    submit = SubmitField('Save Cell')                                                                                       #user can save cell

                                                                                                                            
class modifyParams(FlaskForm):                                                                                                      #form for user to modify paramaters
    rows = IntegerField('Rows:', validators=[DataRequired(), NumberRange(min=1, message='Number must be greater than 1.')] )        #user can modify the number of rows with validator to check that the number of rows is greater than one
    columns = IntegerField('Columns:', validators=[DataRequired(), NumberRange(min=1, message='Number must be greater than 1.')] )  #user can modify the number of columns with validator to check that the number of columns is greater than one
    submit = SubmitField('Save Changes')                                                                                            #user submits the form





