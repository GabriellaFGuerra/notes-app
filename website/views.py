from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db

views = Blueprint('views', __name__)

@login_required
@views.route('/', methods=['GET', 'POST'])

def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='danger')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    return render_template('home.html', user=current_user)

@views.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    note = Note.query.get(id)
    if request.method == 'POST':
        note.data = request.form.get('note')

        if len(note.data) < 1:
            flash('Note is too short!', category='danger')
        else:
            flash('Note updated!', category='success')
            db.session.commit()
            return redirect(url_for('views.home'))
    return render_template('home.html', user=current_user)

@views.route('/delete/<int:id>')
def delete(id):
    note = Note.query.get(id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('views.home'))