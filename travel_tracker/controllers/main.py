from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask.ext.login import login_user, logout_user, login_required

from travel_tracker.extensions import cache
from travel_tracker.forms import LoginForm, RegisterForm, CreateGroupForm
from travel_tracker.models import db, User, Group, Landmark, User_Group
from travel_tracker.utils.object_formatter import generate_landmark_json

main = Blueprint('main', __name__)


@main.route('/')
@cache.cached(timeout=1000)
def home():
    return render_template('index.html')


@main.route('/terms_conditions')
def terms_conditions():
    return render_template('terms_conditions.html')


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if request.method == 'POST' and form.validate_on_submit():

        flash('Logged in successfully.', 'success')
        return redirect(request.args.get('next') or url_for('.home'))

    return render_template('register.html', form=form)


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).one()
        login_user(user)

        flash('Logged in successfully.', 'success')
        return redirect(request.args.get('next') or url_for('.home'))

    return render_template('login.html', form=form)


@main.route('/dashboard')
@login_required
def get_dashboard():

    return render_template('dashboard.html')

@main.route('/add_group', methods=['POST'])
@login_required
def add_group():
    form = CreateGroupForm()
    params = request.args
    user_id = params['user_id']
    landmarks = params['landmarks']
    group_name = params['group_name']
    description = params['description']

    if form.validate_on_submit():
        landmark_names = []
        new_group = Group(name=group_name, description=description)
        db.session.add(new_group)
        for landmark in landmarks:
            new_landmark = Landmark(name=landmark['name'], lat=landmark['lat'], lng=landmark['lng'], group=new_group.id)
            landmark_names.append(landmark['name'])
            db.session(new_landmark)
        db.session.commit()

        flash('Created a new Group {group_name} with landmarks {landmarks}'.format(group_name=group_name, landmarks=landmark_names))
        return (generate_landmark_json(new_group.id))
    return


@main.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'success')

    return redirect(url_for('.home'))
