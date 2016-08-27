from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, UserMixin, RoleMixin

db = SQLAlchemy()

roles_users = db.Table('roles_users',
                db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
                db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))

class Connection(db.Model):
    __tablename__ = "connections"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    provider_id = db.Column(db.String(255))
    provider_user_id = db.Column(db.String(255))
    access_token = db.Column(db.String(255))
    secret = db.Column(db.String(255))
    display_name = db.Column(db.String(255))
    profile_url = db.Column(db.String(512))
    image_url = db.Column(db.String(512))
    rank = db.Column(db.Integer)

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(120))
    active = db.Column(db.Boolean())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

class Role(db.Model, RoleMixin):
    __tablename__ = "roles"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class Landmark(db.Model):
    __tablename__ = "landmark"

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
    __tablename__ = "landmark_groups"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(10000))
    landmark_id = db.Column(db.Integer, db.ForeignKey('landmark.id'))

    # def __init__(self, name, description, landmark_id)
