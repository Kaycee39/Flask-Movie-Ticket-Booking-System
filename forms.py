from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,IntegerField, DateTimeLocalField, SelectField,DateTimeField, TextAreaField,FloatField
from wtforms.validators import DataRequired,Email,EqualTo, ValidationError
from flask_wtf.file import FileField, FileRequired, FileAllowed
from .models import TransactionMethod,Hall,Format




class RegistrationForm(FlaskForm):
    name = StringField('username', validators =[DataRequired()])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password1 = PasswordField('Password', validators = [DataRequired()])
    password2 = PasswordField('Confirm Password', validators = [DataRequired(),EqualTo('password1')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class moviesForm(FlaskForm):
    name = StringField('name', validators =[DataRequired()])
    id = IntegerField('id',validators =[DataRequired()])
    genre = StringField('genre', validators =[DataRequired()])
    time = IntegerField('time', validators =[DataRequired()])
    preview = TextAreaField('preview', validators = [DataRequired()])
    cast = TextAreaField('cast', validators = [DataRequired()])
    director =StringField('director', validators =[DataRequired()])
    file_photo = FileField(validators =[FileAllowed(['jpg','png','gif','jpeg','pdf','webp'],'only image files are allowed!'),FileRequired('File was empty')])
    update = SubmitField('update')

class scheduleForm(FlaskForm):
    name =StringField('name', validators =[DataRequired()])
    movie_id=IntegerField('id',validators =[DataRequired()])
    date =DateTimeLocalField('date', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    quality = SelectField('select quality', choices =[(Format.two_D.name,Format.two_D.value),(Format.three_D.name,Format.three_D.value)], validators=[DataRequired()],)
    hall = SelectField('select hall', choices =[(Hall.HALL_A.name,Hall.HALL_A.value),(Hall.HALL_B.name,Hall.HALL_B.value)], validators=[DataRequired()],)
    price =IntegerField('id',validators =[DataRequired()])
    update = SubmitField('submit')

    def validate_date(form, field):
        if field.data < datetime.now():
            raise ValidationError("The date cannot be in the past!")


            
class SearchForm(FlaskForm):
  name= StringField('search', [DataRequired()])
  submit = SubmitField('Search')

class Personalinfo(FlaskForm):
    name = StringField('name', [DataRequired()])
    email = StringField('Email', validators=[DataRequired(),Email()])
    phone = IntegerField('phone',validators =[DataRequired()])
    

class paymentForm(FlaskForm):
    name = StringField('name', [DataRequired()])
    amount = FloatField('amount',validators =[DataRequired()])
    payment_method = SelectField('Select Payment Method', validators=[DataRequired()], choices = [(TransactionMethod.CASH.name,TransactionMethod.CASH.value),(TransactionMethod.MPESA.name,TransactionMethod.MPESA.value)])
    submit = SubmitField('Make Deposit')

class Payment(FlaskForm):
    name = StringField('name', [DataRequired()])
    amount = FloatField('amount',validators =[DataRequired()])
    phone = IntegerField('phone',validators =[DataRequired()])
    submit = SubmitField('Make Deposit')
