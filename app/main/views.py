from datetime import datetime
from flask import render_template, session, redirect, url_for

from . import main
from .forms import NameForm
from .. import db
from ..models import User

@main.route('/', methods=['GET', 'POST'])
def index():
  form = NameForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.name.data).first()
    if user is None:
      user = User(username = form.name.data)
      db.session.add(user)
      session['known'] = False
    else:
      session['known'] = True
    old_name = session.get('name')
    # if old_name is not None and old_name != form.name.data:
    #   flash("Looks like you have changed your name!")
    session['name'] = form.name.data
    form.name.data = ''
    return redirect(url_for('.index'))
  return render_template('index.html',
                          current_time = datetime.utcnow(),
                          form=form, name=session.get('name'),
                          known = session.get('known', False))