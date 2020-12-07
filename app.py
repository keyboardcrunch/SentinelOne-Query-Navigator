from web import app, database
from web.models import Signatures

@app.shell_context_processor
def make_shell_context():
    """
    Auto-create database and tables.
    """
    return {'database': database, 'Signatures': Signatures}
