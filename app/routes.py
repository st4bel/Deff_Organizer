from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import *
from app.models import User, Organizer, LinkMember
import app.troop_parser as tp

@app.route("/")
@app.route("/index")
def index():
    return render_template("erklaerbaer.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Falscher Benutzername oder Passwort")
            return redirect(url_for("index"))
        login_user(user, remember = form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    admin = False
    if User.query.filter_by(is_admin = True).first() == None:
        admin = True
    form = RegristrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, is_admin = admin)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Benutzer {} erfolgreich erstellt".format(user.username))
        return redirect(url_for("index"))
    return render_template("register.html", form = form, admin = admin)

@app.route("/user")
@login_required
def user():
    user = User.query.filter_by(username = current_user.username).first_or_404()
    tables = user.tables
    return render_template("user.html", user = user, tables = tables)

@app.route("/import", methods=["GET", "POST"])
@login_required
def import_code():
    form = ImportForm()
    if form.validate_on_submit():
        text = form.text.data
        i, e = tp.parse_troops(text = text, has_bows = True, has_paladin = False)
        flash(str(e))
        return redirect(url_for("index"))
    return render_template("import.html", form = form)

@app.route("/create_table", methods=["GET", "POST"])
@login_required
def create_table():
    form = CreateTable()
    if form.validate_on_submit():
        o = Organizer(name = form.name.data, has_bows = form.has_bows.data, has_paladin = form.has_paladin.data, only_trusted = form.only_trusted.data)
        user = User.query.filter_by(username = current_user.username).first_or_404()
        member = LinkMember(is_admin = True, is_trusted = True)
        member.user = user
        member.table = o
        db.session.add(o, member)
        db.session.commit()
        return redirect("user")
    return render_template("create_table.html", form = form)

@app.route("/table/<tablename>")
@login_required
def table_overview(tablename):
    o = Organizer.query.filter_by(name = tablename).first_or_404()
    member = LinkMember.query.filter_by(user = current_user, table = o).first_or_404()
    return render_template("table_overview.html", member = member)

@app.route("/admin")
@login_required
def admin():
    if current_user.is_admin != True:
        flash("Please login as Admin!")
        return redirect(url_for("index"))
    return render_template("admin.html")
