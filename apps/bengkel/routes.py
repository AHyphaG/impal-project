from flask import render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user,
    login_required
)

from apps import db, login_manager
from apps.bengkel import blueprint

from apps.authentication.util import verify_pass


@blueprint.route('/bengkel')
@login_required(role="ANY")
def bengkel():
    return render_template('bengkel/bengkel.html')


