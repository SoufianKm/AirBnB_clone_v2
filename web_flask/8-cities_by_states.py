#!/usr/bin/python3
""" Script that starts a Flask web application """

from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states_route():
    """
    Cities by states: display a HTML page: (inside the tag BODY)
    Returns:
        html: template that lists all states sort by name A->Z
    """
    states = storage.all("State").values()
    return render_template("8-cities_by_states.html", states=states)


@app.teardown_appcontext
def close_db_storage(exception=None):
    """
    After each request remove the current SQLAlchemy Session:
    """
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
