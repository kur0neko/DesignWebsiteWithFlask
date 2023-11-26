from flask import render_template
from flask import redirect, url_for
from flask import flash
from flask import session
from flask import request, send_file
from .forms import CreateAccountForm, LoginForm, Notebox, TableParams, updateName, updatePassword, SearchForm, NewNoteButton, EditNoteButton, Editbox
from app.models import User, Note, Table, Image, TableEntries
from flask import request
from .forms import CreateAccountForm, LoginForm, Notebox, TableParams, updateName, updatePassword, SearchForm, NewNoteButton, EditNoteButton, Editbox, DeleteProfile, tableEntry
from app.models import User, Note, Table
from app import myapp_obj
from app import db
from io import BytesIO

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
		
		img_list = []																			#holds all images for each note																			#dictionary to hold the image name and id
		note_list = {}																			#dictionary to hold the note_name, note_body, and edit button
		found_id = Note.query.filter_by(user_id = session['id']).all()							#find all entries under the id of the user's id
		if found_id:																						
			for note in found_id:
				found_img = Image.query.filter_by(note_id=note.id).all()						#find all image with the same id as the note
				if found_img:
					img_dict = {}																#create a new dictionary for each note
					for img in found_img:														#if found, append all images into a dictionary
						imagename = img.imgname											 		#take the name of the image
						img_dict[imagename] = note.id											#to check values appended										
					img_list.append(img_dict)
					print(img_list)															
					note_list[f'{note.note_name}'] = [note.note_body, editbutton, note.id]		#if found any entries, for value add their note_body (content in box) and key as note_name	
				else:
					note_list[f'{note.note_name}'] = [note.note_body, editbutton]				#no images, do not have a list for the values


		table_list = Table.query.filter_by(user_id = session['id']).all()
		

	else:
		return redirect('/login')													
	return render_template('home.html',  user=user, note_list=note_list, newnote=newnote, img_list=img_list, table_list = table_list)

@myapp_obj.route("/login", methods=['GET', 'POST'])												#basic login function
def login():
	form = LoginForm()
	if form.validate_on_submit():
		found_user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
		if found_user:
			session['user'] = form.username.data
			print('you logged in! it worked!')
			db.session.commit()
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

@myapp_obj.route('/newnote', methods=['GET','POST'])
def newnote():
	if 'user' in session:																						#make sure user is logged in before proceeding, if not send back to login
		note = Notebox()																						
		if note.validate_on_submit():																			#once the note is submitted, functions are applied
			print('you submitted your note!')																	#check if note is submitted
			found_user = User.query.filter_by(username=session['user']).first()									#find the data entry with the same name as the logged-in user
			u = Note(note_body=note.note_body.data, note_name=note.note_name.data, owner=found_user)			#create new data entry, (owner=found_user) is one to many relationship --> id in users table connected to user-id in note tables
			db.session.add(u)																					#add new data entry into the the database
			db.session.commit()		
			

			for image in request.files.getlist('image'):														#grabs all images from the image_upload attribute																					#test for all images inside												
				mimetype = image.mimetype																		#grab type of image
				print(mimetype)
				if mimetype == 'application/octet-stream':
					print('this is an empty image field')
				else:
					i = Image(img=image.read(), mimetype=mimetype, imgname=image.filename, note=u)				#import into database (Image Table)
					db.session.add(i)																				
			
			db.session.commit()																					#commit changes from Image
			return redirect('/home')																			#send back to home
	else:
		return redirect('/login')
	return render_template('newnote.html', note=note)

@myapp_obj.route('/newtable', methods=['GET', 'POST'])
def newtable():
	if 'user' in session:

		user = session['user']
		found_user = User.query.filter_by(username=session['user']).first()
		if found_user:
			session['id'] = found_user.id
			
		table = TableParams()
	
		if table.validate_on_submit():
			print('table creation')
			u = Table(table_name= table.name.data,  numRows = table.rows.data, numColumns = table.columns.data, user_id = session['id'])
			db.session.add(u)
			db.session.commit()
			redirecttest = url_for('edittable', table_id=u.id)
			return redirect(redirecttest)
		
	else:
		return redirect('/login')
	return render_template('newtable.html', table = table)

@myapp_obj.route('/edittable/<table_id>', methods=['GET', 'POST'])	
def edittable(table_id):
	if 'user' in session:
		thisTable = Table.query.filter_by(id=table_id).first()	
			 
		tableEnt = tableEntry()
       
		notes = Note.query.filter(Note.user_id == session['id']).all()
		tableEnt.note.choices = [(note.id, note.note_name) for note in notes]

		entryList = TableEntries.query.filter(TableEntries.table_id == thisTable.id).all()
		if tableEnt.validate_on_submit():
			entry = TableEntries.query.filter(TableEntries.entryRow == tableEnt.row.data, TableEntries.entryColumn == tableEnt.column.data, TableEntries.table_id == thisTable.id).first()

			if entry:
				entry.entryRow = tableEnt.row.data
				entryColumn = tableEnt.column.data
				entry.entry_String =  tableEnt.string.data
				entry.entry_Note = tableEnt.note.data
			
			else:
				u = TableEntries(entryRow = tableEnt.row.data, entryColumn = tableEnt.column.data,
				entry_String =  tableEnt.string.data, 
				entry_Note = int(tableEnt.note.data), 
				table_id = thisTable.id)
				db.session.add(u)

			entryList = TableEntries.query.filter(TableEntries.table_id == thisTable.id).all()
			db.session.commit()
			redirecttest = url_for('edittable', table_id = table_id)
			return redirect(redirecttest)
	else:
		return redirect('/login')
	return render_template('edittable.html', thisTable = thisTable, tableEnt = tableEnt, entryList = entryList, notes = notes)

	


@myapp_obj.route('/search', methods=['GET','POST'])
def search():
    if 'user' in session:
        UserID = session.get('id')  
        keyword = request.args.get('searched', '')
        note_results = search_notes(UserID, keyword)
        return render_template('search.html', keyword=keyword, note_results=note_results)
    else:
        return redirect('/home')


@myapp_obj.route('/editnote/<notename>', methods=['GET', 'POST'])		#creation of edit note page/'<notename> for the name of the note being sent
def editnote(notename):
	if 'user' in session:
		found_note = Note.query.filter_by(note_name=notename).first()											#find the note in the database that matches the notename in the url
		if found_note:
			editnote = Editbox(note_body=found_note.note_body)													#if found, make the inital string in the box the same as the note_body string in the database

		if editnote.validate_on_submit():																		#represents if the edited note is submitted, apply functions below
			found_note.note_body = editnote.note_body.data														#if validated make the changed string equal to the database note_body variable (the content)																							
			db.session.commit()																					#commit the changes to the database to change the string value

			for image2 in request.files.getlist('image2'):
				mimetype = image2.mimetype		
				if mimetype == 'application/octet-stream':
					print('this is an empty image field')
				else:																														
					i2 = Image(img=image2.read(), mimetype=mimetype, imgname=image2.filename, note=found_note)			
					db.session.add(i2)
					db.session.commit()
				
				return redirect('/home')
			return redirect('/home')																#take back to profile page
	return render_template('editnote.html', editnote=editnote)			 

def search_notes(userID,keyword):
     result = Note.query.filter(userID == Note.user_id, Note.note_name.ilike(f'%{keyword}%')).all()
     return result
    
@myapp_obj.route('/download/<img_name>', methods=['GET'])													#used to receive the image name for download
def download(img_name):
	found_img = Image.query.filter_by(imgname=img_name).first()												#find the data entry with same name as the image name
	return send_file(BytesIO(found_img.img), download_name=found_img.imgname, as_attachment=True)			#use send file, change read data into image, download w/name of image as attachment
 
