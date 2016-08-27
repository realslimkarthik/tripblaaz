from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask.ext.security import current_user, login_required

from travel_tracker.extensions import cache
from travel_tracker.models import User

main = Blueprint('main', __name__)


@main.route('/')
@login_required
@cache.cached(timeout=1000)
def home():
    return render_template('index.html')


@main.route('/terms_conditions')
def terms_conditions():
    return render_template('terms_conditions.html')

@main.route('/dashboard')
@login_required
def get_dashboard():
    return render_template('dashboard.html')
