from flask import render_template
from flask import redirect
from flask import flash
from flask import session
from flask import request
from .forms import CreateAccountForm, LoginForm, Notebox, TableParams, updateName, updatePassword, SearchForm
from app.models import User, Note, Table
from app import myapp_obj
from app import db

@myapp_obj.route("/")
def index():
		return render_template('index.html')

@myapp_obj.route("/home")
def home():
		return render_template('home.html')

from flask import flash

@myapp_obj.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        found_user = User.query.filter_by(username=form.username.data).first()
        if found_user:
            print(f'Found user: {found_user.username}')
            if found_user.check_password(form.password.data):
                session['user'] = form.username.data
                flash('Login successful!', 'success')
                return redirect('/home')
            else:
                print('Invalid password')
        else:
            print('User not found')

        flash('Invalid username or password. Please try again.', 'danger')
        return redirect('/login')
    return render_template('login.html', form=form)



@myapp_obj.route('/logout')
def logout():
	session.pop("user", None)
	return redirect('/login')

@myapp_obj.route("/createaccount", methods=['GET', 'POST'])
def createaccount():
    form = CreateAccountForm()
    if form.validate_on_submit():
        u = User(username=form.username.data, email=form.email.data)
        u.set_password(form.password.data)  # Hash the password
        db.session.add(u)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect('/')
    return render_template('createaccount.html', form=form)



@myapp_obj.route("/profile", methods=['GET', 'POST'])
def profile():
	if 'user' in session:
		user = session['user']
		found_user = User.query.filter_by(username=session['user']).first()
		if found_user:
			session['id'] = found_user.id

		note_list = {}
		found_id = Note.query.filter_by(user_id = session['id']).all()
		if found_id:
			for note in found_id:
				note_list[f'{note.note_name}'] = (note.note_body)

		found_user = User.query.filter_by(id = session['id']).first()
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
			found_user.password = changeName.newpassword.data
			db.session.commit()
			return redirect('/profile')
	
	else:
		return redirect('/login')
	return render_template('profile.html', user=user, note_list=note_list, changeName = changeName, changePassword= changePassword)

@myapp_obj.route('/newnote', methods=['GET', 'POST'])
def newnote():
	if 'user' in session:
		note = Notebox()
		if note.validate_on_submit():
			print('you submitted your note!')
			found_user = User.query.filter_by(username=session['user']).first()
			u = Note(note_body = note.note_body.data, note_name = note.note_name.data, owner=found_user)
			db.session.add(u)
			db.session.commit()
			return redirect('/profile')
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
    form=SearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        searched=form.searched.data
        #notes=Note.filter(Note.note_name.like('%'+notes.searched+'%')).all()
        result = Note.query.filter(Note.note_name.like(searched)).all()
        return render_template("search.html",form =form, searched=searched,result=result)
    else:
        return render_template("search.html")
        
    
         