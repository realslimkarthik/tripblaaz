from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask.ext.login import login_user, logout_user, login_required

from travel_tracker.extensions import cache
from travel_tracker.forms import LoginForm, RegisterForm
from travel_tracker.models import User

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


@main.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'success')

    return redirect(url_for('.home'))
