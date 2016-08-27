from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, value):
        return check_password_hash(self.password, value)

    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    def is_active(self):
        return True

    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % self.username


class Landmark(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    lat = db.Column(db.Float(10, 6))
    lng = db.Column(db.Float(10, 6))
    name = db.Column(db.String(100))
    group = db.relationship('Group', backref='Landmark')

    def __init__(self, lat, lng, name, group):
        self.lat = lat
        self.lng = lng
        self.name = name
        self.group = group


    def is_nearby(self, lat, lng):
        # 'SELECT id, ( 3959 * acos( cos( radians(37) ) * cos( radians( lat ) ) * cos( radians( lng ) - radians(-122) ) + sin( radians(37) ) * sin( radians( lat ) ) ) ) AS distance FROM markers HAVING distance < 25 ORDER BY distance LIMIT 0 , 20;'
        nearby = False
        if self.lat > lat[0] and self.lat < lat[1]:
            if self.lng > lng[0] and self.lng < lng[1]:
                nearby = True
        return nearby


    def get_id(self):
        return self.id


class Group(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(10000))


User_Group = db.Table('user_group',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
)
