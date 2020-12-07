import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(base_dir, 'db.sqlite')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # deprecated

database = SQLAlchemy(app)
metadata = database.MetaData()
migrate = Migrate(app, database)

@app.before_first_request
def load_sig_db():
    """
    Before first request we'll make sure signatures are loaded.
    This will only pull in new signatures (by title) on each start,
    and existing signatures won't be updated.
    """
    from web.utils import load_signatures
    load_signatures()

from web import routes, models
