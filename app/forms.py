from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")

class RegristrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Repeat Password", validators=[DataRequired(),EqualTo("password")])
    email = StringField("Email",validators=[DataRequired(), Email()])
    submit = SubmitField("Register")

    def validate_username(self, username): #function with validate_* become stock validators for flask
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Username already in use")
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Email already in use")

class ImportForm(FlaskForm):
    text = TextAreaField(validators=[DataRequired()])
    submit = SubmitField("Importieren")

class CreateTable(FlaskForm):
    name = StringField("Name der neuen Tabelle z.B. W100 -ES-", validators=[DataRequired()])
    has_bows = BooleanField("Spielwelt hat Bögen?")
    has_paladin = BooleanField("Spielwelt hat Paladin")
    only_trusted = BooleanField("Nur vertrauenswürdige Stammesmember können alle Daten sehen?")
    submit = SubmitField("Erstellen")
