from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class LinkMember(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key = True)
    organizer_id = db.Column(db.Integer, db.ForeignKey("organizer.id"), primary_key = True)
    is_admin = db.Column(db.Boolean)
    is_trusted = db.Column(db.Boolean)
    user = db.relationship("User", back_populates = "tables")
    table = db.relationship("Organizer", back_populates = "users")

    def __repr__(self):
        return "<Member User {} in Table {}>".format(self.user.username, self.table.name)

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    tables = db.relationship("LinkMember", back_populates = "user")
#    table_intern = db.relationship("LinkIntern", back_populates = "user")
#    table_extern = db.relationship("LinkExtern", back_populates = "user")

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Organizer(db.Model):
    __tablename__ = "organizer"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    only_trusted = db.Column(db.Boolean)
    has_bows = db.Column(db.Boolean)
    has_paladin = db.Column(db.Boolean)
    users = db.relationship("LinkMember", back_populates = "table")
#    intern = db.relationship("LinkIntern", back_populates = "table")
#    extern = db.relationship("LinkExtern", back_populates = "table")
    def __repr__(self):
        return "<Organizer {}>".format(self.name)

#class LinkIntern(db.Model):
#    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key = True)
#    organizer_id = db.Column(db.Integer, db.ForeignKey("organizer.id"), primary_key = True)
#    spear = db.Column(db.Integer)
#    sword = db.Column(db.Integer)
#    bow = db.Column(db.Integer)
#    skav = db.Column(db.Integer)
##    paladin = db.Column(db.Integer)
#    user = db.relationship("User", back_populates = "tables_intern")
#    table = db.relationship("Organizer", back_populates = "intern")
#    def __repr__(self):
#        return "<Internal Deff from {} in Table {}>".format(self.user.username, self.table.name)

#class LinkExtern(db.Model):
#    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key = True)
#    organizer_id = db.Column(db.Integer, db.ForeignKey("organizer.id"), primary_key = True)
#
#    user = db.relationship("User", back_populates = "tables_extern")
#    table = db.relationship("Organizer", back_populates = "extern")
#
#    def __repr__(self):
#        return "<External Deff from {} to  in Table {}>".format(self.user.username, self.table.name)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
