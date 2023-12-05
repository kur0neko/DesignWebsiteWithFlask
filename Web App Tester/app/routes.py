from flask import render_template
from flask import redirect, url_for
from flask import flash
from flask import session
from flask import request, send_file
from app.models import User, Note, Table, Image, TableEntries
from .forms import CreateAccountForm, LoginForm, Notebox, TableParams, updateName, updatePassword, NewNoteButton, EditNoteButton, Editbox, DeleteProfile, tableEntry, modifyParams, DeleteNoteButton, TranslateBox ,DeleteTableButton
from app.models import User, Note, Table
from app import myapp_obj
from app import db
from io import BytesIO
import requests

@myapp_obj.route("/")
def index():																					#index page
		return render_template('index.html')

@myapp_obj.route("/home", methods=['GET', 'POST'])																		#homepage 
def home():
	if 'user' in session:																		#check for user
		user = session['user']
		newnote = NewNoteButton() 																#create both 'New Note' and 'Edit Note' buttons
		editbutton = EditNoteButton()
		deleteButton=DeleteNoteButton()
		found_user = User.query.filter_by(username=session['user']).first()						#find the database entry with the same name as the user logged in
		if found_user:
			session['id'] = found_user.id														#make the session id equal to the id of the found entry

		languages = [                                                                         # dictionary of languages to be used by googletrans library
        ('ar', 'arabic'),
        ('bn', 'bengali'),
        ('zh-cn', 'chinese (simplified)'),
        ('zh-tw', 'chinese (traditional)'),
        ('nl', 'dutch'),
        ('en', 'english'),
        ('fr', 'french'),
        ('de', 'german'),
        ('hi', 'hindi'),
        ('ga', 'irish'),
        ('it', 'italian'),
        ('ja', 'japanese'),
        ('ko', 'korean'),
        ('la', 'latin'),
        ('pt', 'portuguese'),
        ('ro', 'romanian'),
        ('es', 'spanish'),
        ('sv', 'swedish'),
        ('th', 'thai'),
        ('tr', 'turkish'),
        ('vi', 'vietnamese'),
        ('cy', 'welsh')
        ]

		translated = TranslateBox()                                                                     #create the flask form
		translated.destLang.choices = languages                                                         #set the flask form choices to these languages
		valid = True
		overuse = False
		
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
					note_list[f'{note.note_name}'] = [note.note_body, editbutton, deleteButton, note.id]		#if found any entries, for value add their note_body (content in box) and key as note_name	
				else:
					note_list[f'{note.note_name}'] = [note.note_body, editbutton, deleteButton]				#no images, do not have a list for the values
				
				if translated.validate_on_submit(): 
					print('here')                                                                               #translation was sucessfully submited
					text = note.note_body                                                                 #get the text from the note box
					print(text)                                                                                 #debug
					print(translated.destLang.data)                                                             #debug
					if text:
						APIkey = str(myapp_obj.config.get('GOOGLE_TRANSLATE_SECRET_KEY'))                                           
						newBody = translateThis(text, translated.destLang.data, APIkey)                         #call translating method
						if newBody == 'nulloveruseGOOGLE_TRANSLATE_SECRET_KEY12282004':                         #make sure that when API key is overused sen use a message
							overuse = True
						elif newBody:
							note.note_body = newBody                                                      #if validated make the changed string equal to the database note_body variable (the content)                                                                                            
							db.session.commit()                                                                 #commit the changes
							return redirect('/home')                                                            #go back home   
						else:
							valid = False

		table_list = Table.query.filter_by(user_id = session['id']).all() 						# create a list of all tables that belong to the current user

		UserID = session.get('id')  
		keyword = request.args.get('searched')
		note_results = search_notes(UserID, keyword)
	
	else:
		return redirect('/login')													
	return render_template('home.html',  user=user, note_list=note_list, newnote=newnote, img_list=img_list, table_list = table_list, note_results = note_results, keyword = keyword, translated = translated, overuse = overuse, valid = valid)


def translateThis(text, dest1, apiKey):                                                 #translate method
    
    parameters = {'q': text,'target': dest1,'key': apiKey}								#paramaters needed for the request to google translate api
    print(apiKey)																		#debug
    response = requests.post("https://translation.googleapis.com/language/translate/v2", params=parameters)	#request the google translate API, not using the credentials methods because that will leak more private information than just the API Key
    print(response.status_code)															#print if the request to API was sucessful. 200 means sucess, 403 means failure
    if response.status_code == 200:
        translation = response.json()													#get the response if request worked
        print(translation)                                                              #debug
        translated = translation['data']['translations'][0]['translatedText']           #get translation
        detectedLanguage = translation['data']['translations'][0]['detectedSourceLanguage'] #get detected language
        if detectedLanguage == dest1:                                                   #detect the language and check if its equal to source
            translated = None                                                           #send message NONE to route
    else:
        translated = 'nulloveruseGOOGLE_TRANSLATE_SECRET_KEY12282004'               #if API overrequested make sure to not let user do more
    return translated                                                               #return the text from the translation


@myapp_obj.route("/login", methods=['GET', 'POST'])													#template for login
def login():
    form = LoginForm()																				#create login form
    if form.validate_on_submit():																	#validate the form if found
        found_user = User.query.filter_by(username=form.username.data).first()						#find the corresponding username
        if found_user:
            print(f'Found user: {found_user.username}')												#if the username is found
            if found_user.check_password(form.password.data):										#check the corresponding password
                session['user'] = form.username.data												#set the session
                flash('Login successful!', 'success')												#flash a message
                return redirect('/home')															#redirect to home
            else:
                print('Invalid password')															#otherwise print an invalid message
        else:
            print('User not found')																	#debug

        flash('Invalid username or password. Please try again.', 'danger')							#flash a message if invalid login
        return redirect('/login')																	#redirect to login
    return render_template('login.html', form=form)													#render the template

@myapp_obj.route('/logout')																		#template for logging out
def logout():
	session.pop("user", None)																	#pop the user session
	return redirect('/')																		#redirect to the index page

@myapp_obj.route("/createaccount", methods=['GET', 'POST'])
def createaccount():
    username_list = User.query.all()														#get a list of all the users
    form = CreateAccountForm()																#create the create account form
    form.usernameList = username_list														#get a username list and make it a variable for the form

    if form.validate_on_submit():															#if the form is validated
        u = User(username=form.username.data, email=form.email.data)						#create a user
        u.set_password(form.password.data)  												# Hash the password
        db.session.add(u)																	# add the changes 
        db.session.commit()																	#commit the changes
        flash('Account created successfully!', 'success')									#debug
        return redirect('/')																#redirect to index
	

    return render_template('createaccount.html', form=form)									#render the template




@myapp_obj.route("/profile", methods=['GET', 'POST'])
def profile():
	if 'user' in session:															#check if the user is in session (i.e logged in)
		user = session['user']														#set the user to the current session's user
		found_user = User.query.filter_by(username=session['user']).first()			#find the corresponding user in the User database

		if found_user:																#if this user exists (which will always be true, but better safe than sorry)
			session['id'] = found_user.id											#set the session id to the found user's id
		
		username_list = User.query.all()											#query all usernames
		changeName = updateName()													#create the form so the user can update their username
		changeName.usernameList =  username_list									#create username_list for the change Name for that can be used later for validation
		changeName.username = found_user.username									#create a variable for the changeName form so that it can be used in the validation in forms.py
		if changeName.validate_on_submit():											#check if the form was validated
			found_user.username = changeName.newname.data							#change the user's username to the new username
			session['user'] = found_user.username									#change the session's username to this new username as well
			db.session.commit()														#commit the changes
			return redirect('/profile')												#redirect to the profile

		changePassword = updatePassword()											#create the form so the user can update their password
		changePassword.password = found_user.password								#create a variable for the changePassword form so that it can be used in the validation in forms.py
		if changePassword.validate_on_submit():										#check if the form was validated
			found_user.password = changePassword.newpassword.data					#change the user's password to the new password
			db.session.commit()														#commit the changes
			return redirect('/profile')												#redirect to the profile
		
		delete = DeleteProfile()													#create the form so that the user can delete their profile
		delete.password = found_user.password										#create a variable for the form so that it can be used in forms.py for validation
		if delete.validate_on_submit():												#check if form validated
			db.session.delete(found_user)											#delete the user from the database
			db.session.commit()														#commit the changes
			print(Table.query.all()) 												#debug to see if cascading delete occurs
			print(Note.query.all()) 												#debug to see if cascading delete occurs
			return redirect('/logout')												#simply logout of the account which no longer exists, which will basically redirect us to login

	else:
		return redirect('/login')													#if user is not in session redirect to login
	return render_template('profile.html', user = user, changeName = changeName, changePassword= changePassword, delete = delete)

@myapp_obj.route('/newnote', methods=['GET','POST'])
def newnote():
	if 'user' in session:																						#make sure user is logged in before proceeding, if not send back to login
		note = Notebox()
		notelist1 = Note.query.filter(Note.user_id == session['id']).all()
		note.notelist = notelist1																						
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
	if 'user' in session: 																						#check if user is in session

		user = session['user'] 																					# set the user to the current session's user
		found_user = User.query.filter_by(username=session['user']).first() 									# find the corresponding user in the User database
		if found_user: 																							# if this user exists (which will always be true, but better safe than sorry)
			session['id'] = found_user.id 																		# set the session id to the found user's id
			
		table = TableParams() 																					# create form which use will input paramaters for their table
	
		if table.validate_on_submit():
			print('table creation') 																			# debug
			u = Table(table_name= table.name.data,  
						numRows = table.rows.data, 
						numColumns = table.columns.data, 
						user_id = session['id']) 																# create new Table 
			db.session.add(u) 																					# add it to database
			db.session.commit() 																				# commit the changes
			redirecttest = url_for('edittable', table_id=u.id) 													# get url for editing this specific table
			return redirect(redirecttest) 																		# redirect to the url found above
		
	else:
		return redirect('/login') 																				# if a current session is not found return to the login page. 
	return render_template('newtable.html', table = table)

@myapp_obj.route('/edittable/<table_id>', methods=['GET', 'POST'])												#we use dynamic routes here because we want each edit table webpage to be assigned to a single table
def edittable(table_id):
	if 'user' in session: 																						#check if user is in session
		thisTable = Table.query.filter_by(id=table_id).first()													# find the table that corresponds to the table_id in the route
			 
		tableEnt = tableEntry() 																				# create the form for entering a value into the table
       
		notes = Note.query.filter(Note.user_id == session['id']).all() 											#get all the notes that belongs to the session's user
		tableEnt.note.choices = [(note.id, note.note_name) for note in notes]  									# set the choices for note selection in the form to the list of notes
		tableEnt.note.choices.insert(0,(None, ' ')) 															# insert an option to select no note at index 0 of the selections

		entryList = TableEntries.query.filter(TableEntries.table_id == thisTable.id).all() 						# get a list of all the entries for this table
		if tableEnt.validate_on_submit(): 																		# when form is sucessfully submitted

			entry = TableEntries.query.filter(TableEntries.entryRow == tableEnt.row.data, 
												TableEntries.entryColumn == tableEnt.column.data, 
												TableEntries.table_id == thisTable.id).first() 					#get the entry for the specified flask form in the cell

			if entry: 																							# if there is already an entry, dont create a new entry into the database, instead just modify it
				entry.entryRow = tableEnt.row.data
				entryColumn = tableEnt.column.data
				entry.entry_String =  tableEnt.string.data
				entry.entry_Note = tableEnt.note.data
			
			else: 																								# if there is no entry, create a new entry and commit it into the database
				u = TableEntries(entryRow = tableEnt.row.data, entryColumn = tableEnt.column.data,
				entry_String =  tableEnt.string.data, 
				entry_Note = tableEnt.note.data, 
				table_id = thisTable.id)
				db.session.add(u)

			entryList = TableEntries.query.filter(TableEntries.table_id == thisTable.id).all() 					#update entry list
			db.session.commit() 																				# commit all the cganges
			redirecttest = url_for('edittable', table_id = table_id)
			return redirect(redirecttest) 																		#redirect to the same webpage with all the changes
		
		newsize = modifyParams() 																				#user form for changing the rows and columns 
		
		if newsize.validate_on_submit():																		#if form is validated

			if newsize.rows.data > thisTable.numRows:															#check if the new rows is greater than the original rows
				thisTable.numRows = newsize.rows.data															#change numRows of the table
			
			if newsize.columns.data > thisTable.numColumns:														#check if the new columns is greater than the original columns
				thisTable.numColumns = newsize.columns.data														#change numColumns of the table
			
			if newsize.rows.data < thisTable.numRows:															#check if new rows is less than the current numRows
				change = thisTable.numRows - newsize.rows.data													#find the difference between the two
				for i in range(change):																			#iterate through that change
					x = thisTable.numRows - i -1																#We want to delete the outside rows, so we calculate a new value with an offset
					entryList = TableEntries.query.filter(TableEntries.entryRow == x).all() 					#we query all the entries that are in a row that must be deleted
					for entry in entryList:																		#we delete all those entries
						db.session.delete(entry)	
					thisTable.numRows = newsize.rows.data														#we change the value of numRows correspondingly
			
			if newsize.columns.data < thisTable.numColumns:														#check if new columns is less than the current numColumns
				change = thisTable.numColumns - newsize.columns.data											#find the difference between the two 
				for i in range(change):																			#iterate through that change
					x = thisTable.numColumns - i -1																#We want to delete the outside columns, so we calculate a new value with an offset 
					entryList = TableEntries.query.filter(TableEntries.entryColumn == x).all() 					#we query all the enteries that are in the row that must be deleted
					for entry in entryList:																		#we delete all those entries
						db.session.delete(entry)																
					thisTable.numColumns = newsize.columns.data													#we change the value of numColumns correspondingly

			db.session.commit()																					#we commit these changes
			redirecttest = url_for('edittable', table_id = table_id)											#we redirect to the same webpage so we can see the changes
			return redirect(redirecttest)																		

	else:
		return redirect('/login')																				#if user is not in a session redirect them back to the login page
	return render_template('edittable.html', thisTable = thisTable, tableEnt = tableEnt, entryList = entryList, notes = notes, newsize= newsize) # render the template, this way these variables can be used in other files

	


@myapp_obj.route('/search', methods=['GET','POST']) 															#creating instance template'/search', accept POST and GET form
def search():
    if 'user' in session:																						#If the user is logged in, in the session
        UserID = session.get('id')  																			#save the user ID from database which will use later on to verified who is logged in to use search.
        keyword = request.args.get('searched', '')																#Get string argument that user enter from search bar by GET(required to use equest.args.get in order to work correctly)
        note_results = search_notes(UserID, keyword)															#call function to pass userID and keyword that user search.
        return render_template('search.html', keyword=keyword, note_results=note_results)						#function will return query which will use to select* from Note where(userID==User.id) Render this page template
    else:
        return redirect('/home')																				#if user not in the session not login just return to home page


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
    
     result = Note.query.filter(userID == Note.user_id, 
	 (Note.note_name.ilike(f'%{keyword}%') | (Note.note_body.ilike(f'%{keyword}%')))).all()           #return the query select Note that have the userID matched to current user logged in, search only the files that this user has in her/his session.
     return result  																						  #note that "ilike" will allow to find all case sensitive as well. Fetch all file that have similar name or case sensitive
    
@myapp_obj.route('/download/<img_name>', methods=['GET'])													#used to receive the image name for download
def download(img_name):
	found_img = Image.query.filter_by(imgname=img_name).first()												#find the data entry with same name as the image name
	return send_file(BytesIO(found_img.img), download_name=found_img.imgname, as_attachment=True)			#use send file, change read data into image, download w/name of image as attachment
 
 
@myapp_obj.route('/deleteNote/<notename>', methods=['POST', 'GET'])													#used to receive the image name for download
def deleteNote(notename):
    #check if the current user it the real owner                                                              	#function deleteNote is function will remove note by notename
    if 'user' in session:																					    #First create instance template /deleteNote accept POST and GET forms
        found_note = Note.query.filter_by(note_name=notename).first()											#first check if the user is logged in in the session
        if found_note:																							#find the note of the user that logged in, if the notename match to the database note name
            #note = Note.query.get_or_404(found_note)                                                           #If found hode the value of Notename inside found_note, If found_note is have  notename
            db.session.delete(found_note)																		#delete the notedata out of the database
            db.session.commit()																					#Commit the current transaction in database
    return redirect('/home')																					#then redirect to home page

@myapp_obj.route('/deleteTable/<table_id>', methods=['GET', 'POST'])
def deleteTable(table_id):
    if 'user' in session: 																						#check if user is in session
        found_table = Table.query.filter_by(id=table_id).first()																				# create the form for entering a value into the table
        #notes = Note.query.filter(Note.user_id == session['id']).all()
        if found_table:
            db.session.delete(found_table)
            db.session.commit()	
    return redirect('/home')




