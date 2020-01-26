from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password_hash = db.Column(db.String(128))

    def __repr(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Organizer(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    only_trusted = db.Column(db.Boolean)
    has_bows = db.Column(db.Boolean)

    link_members = db.relationship("Member", backref = "organizer", lazy = "dynamic")
    link_flex = db.relationship("Flex", backref = "organizer", lazy = "dynamic")
    link_extern = db.relationship("Extern", backref = "organizer", lazy = "dynamic")

    def __repr__(self):
        return "<Organizer {}>".format(self.name)




class Member(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    organizer_id = db.Column(db.Integer, db.ForeignKey("organizer.id"))
    is_admin = db.Column(db.Boolean)
    is_trusted = db.Column(db.Boolean)

class Flex(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    organizer_id = db.Column(db.Integer, db.ForeignKey("organizer.id"))
    spear = db.Column(db.Integer)
    sword = db.Column(db.Integer)
    bow = db.Column(db.Integer)
    skav = db.Column(db.Integer)

class Extern(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    organizer_id = db.Column(db.Integer, db.ForeignKey("organizer.id"))
    acceptor_id = db.Column(db.Integer, db.ForeignKey("user.id"))
