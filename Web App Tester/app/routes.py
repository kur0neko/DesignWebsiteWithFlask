from flask import render_template
from flask import redirect
from flask import flash
from flask import session
from flask import request
from .forms import CreateAccountForm, LoginForm, Notebox, TableParams, updateName, updatePassword, SearchForm, NewNoteButton, EditNoteButton, Editbox, DeleteProfile
from app.models import User, Note, Table
from app import myapp_obj
from app import db

@myapp_obj.route("/")
def index():
		return render_template('index.html')

@myapp_obj.route("/home")																		#homepage 
def home():
	if 'user' in session:																		#check for user
		user = session['user']
		newnote = NewNoteButton() 																#create both 'New Note' and 'Edit Note' buttons
		editbutton = EditNoteButton()
		found_user = User.query.filter_by(username=session['user']).first()						#find the database entry with the same name as the user logged in
		if found_user:
			session['id'] = found_user.id														#make the session id equal to the id of the found entry

		note_list = {}																			#dictionary to hold the note_name, note_body, and edit button
		found_id = Note.query.filter_by(user_id = session['id']).all()							#find all entries under the id of the user's id
		if found_id:																						
			for note in found_id:																#if found any entries, for valueadd their note_body (content in box) and key as note_name
				note_list[f'{note.note_name}'] = (note.note_body, editbutton)
	else:
		return redirect('/login')
	return render_template('home.html',  user=user, note_list=note_list, newnote=newnote)

@myapp_obj.route("/login", methods=['GET', 'POST'])																#basic login function
def login():
	form = LoginForm()
	if form.validate_on_submit():
		found_user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
		if found_user:
			session['user'] = form.username.data
			print('you logged in! it worked!')
			return redirect('/home')
		else:
			return redirect('/createaccount')
	return render_template('login.html', form=form)

@myapp_obj.route('/logout')
def logout():
	session.pop("user", None)
	return redirect('/login')

@myapp_obj.route("/createaccount", methods=['GET', 'POST'])							#template for create account
def createaccount():
    form = CreateAccountForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        print('do something')
        print(f'this is the username of the user {form.username.data}')
        print(f'this is the password of the user {form.password.data}')
        u = User(username=form.username.data, password=form.password.data,
                 email=form.email.data)
        db.session.add(u)
        db.session.commit()
        return redirect('/')

    return render_template('createaccount.html', form=form)

@myapp_obj.route("/profile", methods=['GET', 'POST'])
def profile():
	if 'user' in session:
		user = session['user']
		found_user = User.query.filter_by(username=session['user']).first()
		if found_user:
			session['id'] = found_user.id
			
		changeName = updateName()
		changeName.username = found_user.username
		if changeName.validate_on_submit():
			found_user.username = changeName.newname.data
			session['user'] = found_user.username
			db.session.commit()
			return redirect('/profile')

		changePassword = updatePassword()
		changePassword.password = found_user.password
		if changePassword.validate_on_submit():
			found_user.password = changePassword.newpassword.data
			db.session.commit()
			return redirect('/profile')
		
		delete = DeleteProfile()
		delete.password = found_user.password
		if delete.validate_on_submit():
			db.session.delete(found_user)
			db.session.commit()
			print(Table.query.all()) #debug
			print(Note.query.all()) #debug
			return redirect('/logout')

	else:
		return redirect('/login')
	return render_template('profile.html', user = user, changeName = changeName, changePassword= changePassword, delete = delete)

@myapp_obj.route('/newnote', methods=['GET', 'POST'])
def newnote():
	if 'user' in session:																						#make sure user is logged in before proceeding, if not send back to login
		note = Notebox()																						
		if note.validate_on_submit():																			#once the note is submitted, functions are applied
			print('you submitted your note!')																	#check if note is submitted
			found_user = User.query.filter_by(username=session['user']).first()									#find the data entry with the same name as the logged-in user
			u = Note(note_body = note.note_body.data, note_name = note.note_name.data, owner=found_user)		#create new data entry, (owner=found_user) is one to many relationship --> id in users table connected to user-id in note tables
			db.session.add(u)
			db.session.commit()																					#add new data entry into the the database
			return redirect('/home')																			#send back to home
	else:
		return redirect('/login')
	return render_template('newnote.html', note= note)

@myapp_obj.route('/newtable', methods=['GET', 'POST'])
def newtable():
	if 'user' in session:

		user = session['user']
		found_user = User.query.filter_by(username=session['user']).first()
		if found_user:
			session['id'] = found_user.id
			
		table = TableParams()
		table_list = {}
		found_id = Table.query.filter_by(user_id = session['id']).all()
		if found_id:
			for dbtable in found_id:
				table_list[f'{dbtable.table_name}'] = (dbtable.numRows, dbtable.numColumns)
		
		if table.validate_on_submit():
			print('table creation')
			u = Table(table_name= table.name.data,  numRows = table.rows.data, numColumns = table.columns.data, user_id = session['id'])
			db.session.add(u)
			db.session.commit()
		
	else:
		return redirect('/login')
	return render_template('newtable.html', table = table, table_list = table_list)

@myapp_obj.route('/editnote/<notename>', methods=['GET', 'POST'])		#creation of edit note page/'<notename> for the name of the note being sent
def editnote(notename):
	if 'user' in session:
		found_user = Note.query.filter_by(note_name=notename).first()	#find the note in the database that matches the notename in the url
		if found_user:
			editnote = Editbox(note_body=found_user.note_body)			#if found, make the inital string in the box the same as the note_body string in the database

		if editnote.validate_on_submit():								#represents if the edited note is submitted, apply functions below
			found_user.note_body = editnote.note_body.data				#if validated make the changed string equal to the database note_body variable (the content)				
			db.session.commit()											#commit the changes to the database to change the string value
			return redirect('/profile')									#take back to profile page
	return render_template('editnote.html', editnote=editnote)			 

#function of flask that return dictionary
@myapp_obj.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


  #get data from submitted form 
   #Query the database
    #notes=notes.order_by(Note.note_name).all()
@myapp_obj.route('/search',methods=['GET', 'POST'])
def search():
    form=SearchForm()#
    if request.method == 'POST' and form.validate_on_submit():
         query = request.form.get('searched', '')     #searched=form.searched.data#
         result=Note.query.filter(Note.note_name.like('%' + query + '%')).all()
         return render_template("search.html",form =form,query=query, result=result)
    else:
        return render_template("search.html",message="error, Note is not found")
        
    
         