import os


from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, flash, session,request,redirect,url_for
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import current_app
from flask import request



from . import db
from .forms import moviesForm,scheduleForm,SearchForm,Personalinfo,paymentForm,Payment
from .models import movies,schedule,search,personal,Transactions,TransactionMethod
from .mpesa import send_money_request

admin = Blueprint('admin', __name__)
#---------------------------------------------------------------------------------------
@admin.route('/', methods=["GET", "POST"])

def home():
    
    return render_template("index.html")

#--------------------------------------------------------------------------
@admin.route('/add_movies', methods = ["GET","POST"])

def addmovies():
    form = moviesForm()
    if form.is_submitted():
        if form.validate_on_submit():
            name = form.name.data
            genre =form.genre.data
            time =form.time.data
            cast =form.cast.data
            director = form.director.data
            preview=form.preview.data

            f = form.file_photo.data
            filename = secure_filename(f.filename)
            basedir = os.path.abspath(os.path.dirname(__file__))
            loc = os.path.join(current_app.config['UPLOAD_FOLDER'], 'photos', filename)
            f.save(os.path.join(basedir,loc))

            movie = movies(
                name = name,
                time = time,
                genre =genre,
                cast =cast,
                director=director,
                preview = preview,
                photo = loc
            )
            print("yew")
            try:
                db.session.add(movie)
                db.session.commit()
                print ("added")
            except Exception as e:
                # for resetting non-commited .add()
                db.session.rollback()
                db.session.flush()
                print("failed") 
                flash('Database Error: Failed to add')
                print(e)
            else:
                        # on successful saving
                flash(' successful.')
                return redirect(url_for('admin.addmovies'))
        else:
            flash("form not validated") 
            

    return render_template ("admin/add_movies.html", form=form)
#-------------------------------------------------------------------------------
@admin.route('/movie_details', methods=["GET","POST"])
def movie_details():

    Movies = movies.query.all()

    return render_template("admin/movie_details.html", movies = Movies)
#---------------------------------------------------------------------------
@admin.route('/schedule_shows', methods = ["GET","POST"])
def schedule_shows():
    form = scheduleForm()
    if form.is_submitted():
        if form.validate_on_submit():
            name = form.name.data
            movie_id = form.movie_id.data
            date =form.date.data
            quality =form.quality.data
            hall = form.hall.data
            price = form.price.data

            

            schedules = schedule(
                name = name,
                movie_id=movie_id,         
                date = date,
                quality = quality,
                hall = hall,
                price = price
            )
            print ("yes")
            try:
                db.session.add(schedules)
                db.session.commit()
                print ("added")
            except Exception as e:
                # for resetting non-commited .add()
                db.session.rollback()
                db.session.flush()
                    
                flash('Database Error: Failed to add schedules')
                print(e)
            else:
                        # on successful saving
                flash(' successful.')
        else:
            flash("form not validated") 

    return render_template("admin/schedule_shows.html",form = form)

#-------------------------------------------------------------
@admin.route('/view_scheduled_shows')
def scheduled_shows():
    Schedules=schedule.query.all()
    return render_template("admin/view_scheduled_shows.html", schedule =Schedules)
#-------------------------------------------------------------------------------





'''@admin.route('/bookings?schedules_name=<name>')
def bookings(name):
    Schedules=schedule.query.get(name)
    print(Schedules)
    Movies = movies.query.filter(movies.name==name).all()
    print(Movies)

    return render_template("admin/bookings.html", schedule = Schedules, movies = Movies)

@admin.route('/bookings', methods = ["GET","POST"])
def search_movie():
   
    form = SearchForm()
    if form.is_submitted():
        if form.validate_on_submit():
            movie_name = form.name.data
            movie_name = "%{}%".format(movie_name)
            Movies = movies.query.filter(movies.name.like(movie_name)).all()
            if Movies:
                return  render_template("admin/bookings.html", movies = Movies, form=form) 
            else:
                flash ("no such movie  was found")
                return  render_template("admin/bookings.html", form=form) 
        else: 
            flash("form not validated")
    return render_template("admin/bookings.html", form=form)
'''

#--------------------------------------------------------------------------------
@admin.route('/personal_info', methods =["GET","POST"])
def personal_info():
    form = Personalinfo()
    if form.is_submitted():
        if form.validate_on_submit():
            name = form.name.data
           
            email =form.email.data
            phone =form.phone.data
            

            personalinformation = personal(
                
                name = name,
                
                email =email,
                phone =phone
            )
            print ("yes")
            try:
                db.session.add(personalinformation)
                db.session.commit()
                print ("added")
            except Exception as e:
                # for resetting non-commited .add()
                db.session.rollback()
                db.session.flush()
                    
                flash('Database Error: Failed to add')
                print(e)
            else:
                        # on successful saving
                flash(' successful.')
        else:
            flash("form not validated") 

    return render_template ("admin/personal_info.html", form=form)

#--------------------------------------------------------------------------------
@admin.route('/pay_ticket', methods =["GET","POST"])
def pay():
    form = paymentForm()
    if form.is_submitted():
        if form.validate_on_submit():
            name = form.name.data
           
            amount =form.amount.data
           
            payment_method = form.payment_method.data

            
            
            pay = Transactions(
                
                name = name,
                
                amount =amount,
                payment_method = TransactionMethod.CASH.name,
                transaction_time = datetime.now()
            )
            print ("yes")
            try:
                db.session.add(pay)
                db.session.commit()
                print ("added")
            except Exception as e:
                # for resetting non-commited .add()
                db.session.rollback()
                db.session.flush()
                    
                flash('Database Error: Failed to add')
                print(e)
            else:
                        # on successful saving
                flash(' successful.')
            print("yes")
        else:
            flash("form not validated") 

    return render_template ("admin/pay_ticket.html", form=form)

#---------------------------------------------------------------------------
@admin.route('/view_bookings', methods=["GET","POST"])
def view_bookings():
    payments=Transactions.query.all()
    return render_template("admin/view_bookings.html",Transactions =payments)

# --------------------------------------------------------------------
@admin.route('/pay_mpesa', methods =["GET","POST"])
def paympesa():
    form = Payment()
    if form.is_submitted():
        if form.validate_on_submit():
            name = form.name.data
            phone = form.phone.data
            amount = form.amount.data
            if amount > 0:
            # create  object
                send_money_request(amount, phone) # send mpesa request
                
                pay = Transactions(
                    
                    name = name,
                    phone = phone,
                    amount =amount,
                    transaction_time = datetime.now()
                )


                try:
                    db.session.add(pay)
                    db.session.commit()
                except Exception as e:
                    # for resetting non-commited .add()
                    db.session.rollback()
                    db.session.flush()
                    print("Failed to add ")
                    flash('Database Error: Failed to process transaction')
                    print(e)
                else:
                    # on successful saving
                    flash('successful')
            
            else:
                flash("Amount has to be greater than zero")
            
        else:
            flash("form not validated") 

    return render_template ("admin/pay_mpesa.html", form=form)
#-------------------------------------------------------------------------------
@admin.route('/delete?id=<id>')
def delete(id):
        schedules_to_delete =schedule.query.get(id)
        try:
            db.session.delete(schedules_to_delete)
            db.session.commit()
        except:
            print("delete")

        return redirect (url_for("admin.scheduled_shows"))
        

#---------------------------------------------------------------------
@admin.route('/delete_movies?id=<id>')
def delete_movies(id):
        movies_to_delete =movies.query.get(id)
        try:
            db.session.delete(movies_to_delete)
            db.session.commit()
        except:
            print("delete")

        return redirect (url_for("admin.movie_details"))
