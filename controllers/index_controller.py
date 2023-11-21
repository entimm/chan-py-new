from flask import Blueprint, url_for, redirect

blueprint = Blueprint('index', __name__)


@blueprint.route('/')
def index():
    return redirect(url_for('chart.view'))