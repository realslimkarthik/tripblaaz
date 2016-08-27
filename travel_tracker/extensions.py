from flask.ext.cache import Cache
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask_assets import Environment

from travel_tracker.models import User

# Setup flask cache
cache = Cache()

# init flask assets
assets_env = Environment()

debug_toolbar = DebugToolbarExtension()
