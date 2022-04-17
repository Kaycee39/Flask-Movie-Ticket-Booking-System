from flask import Flask, session, redirect, url_for
from flask import render_template
from flask import request
from flask import Blueprint
from flask import flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



from . import db
from .forms import SearchForm,Payment,Personalinfo,paymentForm
from .models import movies,schedule,Transactions,personal,TransactionMethod
from .mpesa import send_money_request



customer = Blueprint('customer', __name__)

#-----------------------------------------------------------------------------------
@customer.route('/home', methods=["GET", "POST"])

def home():
    print("before")
    Movies = movies.query.all()
    print(Movies)       
    return render_template("customer/index.html", movies = Movies)

#--------------------------------------------------------------------------------------
@customer.route('/bookings?id=<id>', methods=["GET","POST"])
def bookings(id):
    schedules = schedule.query.filter(schedule.movie_id == id).all()
    print(id)
    print(schedules)
    return render_template("customer/book_info.html", schedules = schedules)

#-------------------------------------------------------------------------

@customer.route('/pay_cust_mpesa', methods =["GET","POST"])
def paycustmpesa():
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

    return render_template ("customer/pay_cust_mpesa.html", form=form)


#_-------------------------------------------
@customer.route('/cust_personal_info', methods =["GET","POST"])
def cust_personal_info():
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

    return render_template ("customer/cust_personal_info.html", form=form, personalinformation=personal)

#-----------------------------------------------------------
@customer.route('/pay_cash_ticket', methods =["GET","POST"])
def pay_cash_ticket():
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

    return render_template ("customer/pay_cash_ticket.html", form=form)