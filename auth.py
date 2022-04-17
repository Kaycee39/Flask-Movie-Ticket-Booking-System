

from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_manager ,login_user, logout_user, login_required, current_user
from .models import User,AccountType

from . import db
from .forms import RegistrationForm,LoginForm
from .models import User


auth = Blueprint('auth', __name__)

@auth.route('/sign_up', methods = ['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password_hash =form.password1.data
    
        user=User(
            name = name,
            email= email,
            password_hash = generate_password_hash(password_hash, method='sha256')
           
            
        )
        
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.log_in'))
    return render_template('auth/sign_up.html', form=form)
    #We first check if the form is valid and then create a new user object with
    #the username, email, and password data from the submitted form.
    #Then we add the data to the database and redirect the user to the login page.

#an error may occur saying 'werkzeug.routing.BuildError:
#  Could not build url for endpoint 'auth.log_in'. 
# Did you mean 'auth.login' instead?'
#solution:
#This is expected behavior since your login endpoint
#  is part of your auth blueprint. When using
#  url_for you should use route endpoint name rather than view function name(in this case def log_in ):
# ie they shouldnt match with the url for and the login function

@auth.route('/log_in', methods=['GET', 'POST'])
def log_in():
    

    form = LoginForm()
    if form.is_submitted():

        if form.validate_on_submit():
            
            user = User.query.filter_by(email = form.email.data).first()
            if user is not None and user.check_password(form.password.data):
                login_user(user)
                next = request.args.get("next")
                session['username'] = user.name
                session['user_id'] = user.id
                return redirect(next or url_for('admin.home'))
            else:
                
                flash('Invalid email address or Password.')
        else:
            
            flash("Invalid email or address")
     
    return render_template('auth/log_in.html', form=form)

