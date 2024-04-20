#!/usr/bin/python3
""" Script that starts a Flask web application """

from flask import Flask, render_template
from models import *

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
@app.route('/states/<state_id>', strict_slashes=False)
def states(state_id=None):
    """
    Load all cities of a State: display a HTML page: (inside the tag BODY)
    Returns:
        html: template that lists all cities of a State sort by name A->Z
    """
    states = storage.all("State")
    if state_id is not None:
        state_id = 'State.' + state_id
    return render_template('9-states.html', states=states, state_id=state_id)


@app.teardown_appcontext
def close_db_storage(exception=None):
    """
    After each request remove the current SQLAlchemy Session:
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
