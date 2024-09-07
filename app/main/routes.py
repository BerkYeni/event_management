from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app import db
from app.main import bp
from app.models import Event, Attendee, Registration
from app.forms import EventForm, AttendeeRegistrationForm, AttendeeManagementForm

@bp.route('/')
@bp.route('/index')
def index():
    events = Event.query.order_by(Event.date.asc()).all()
    return render_template('index.html', title='Home', events=events)

@bp.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(title=form.title.data,
                      description=form.description.data,
                      date=form.date.data,
                      location=form.location.data,
                      organizer=current_user)
        db.session.add(event)
        db.session.commit()
        flash('Your event has been created!', 'success')
        return redirect(url_for('main.index'))
    return render_template('create_event.html', title='Create Event', form=form)

@bp.route('/event/<int:id>')
def event(id):
    event = Event.query.get_or_404(id)
    return render_template('event.html', title=event.title, event=event)

@bp.route('/event/<int:id>/register', methods=['GET', 'POST'])
def register_for_event(id):
    event = Event.query.get_or_404(id)
    form = AttendeeRegistrationForm()
    if form.validate_on_submit():
        attendee = Attendee(name=form.name.data, email=form.email.data)
        db.session.add(attendee)
        registration = Registration(event=event, attendee=attendee)
        db.session.add(registration)
        db.session.commit()
        flash('You have successfully registered for this event!', 'success')
        return redirect(url_for('main.event', id=event.id))
    return render_template('register_for_event.html', title='Register for Event', form=form, event=event)

@bp.route('/manage_attendees/<int:event_id>')
@login_required
def manage_attendees(event_id):
    event = Event.query.get_or_404(event_id)
    if event.organizer != current_user:
        flash('You do not have permission to manage attendees for this event.', 'danger')
        return redirect(url_for('main.index'))
    registrations = Registration.query.filter_by(event_id=event_id).all()
    return render_template('manage_attendees.html', title='Manage Attendees', event=event, registrations=registrations)

@bp.route('/edit_attendee/<int:registration_id>', methods=['GET', 'POST'])
@login_required
def edit_attendee(registration_id):
    registration = Registration.query.get_or_404(registration_id)
    if registration.event.organizer != current_user:
        flash('You do not have permission to edit this attendee.', 'danger')
        return redirect(url_for('main.index'))
    form = AttendeeManagementForm()
    if form.validate_on_submit():
        registration.attendee.name = form.name.data
        registration.attendee.email = form.email.data
        db.session.commit()
        flash('Attendee information has been updated.', 'success')
        return redirect(url_for('main.manage_attendees', event_id=registration.event_id))
    elif request.method == 'GET':
        form.name.data = registration.attendee.name
        form.email.data = registration.attendee.email
    return render_template('edit_attendee.html', title='Edit Attendee', form=form, registration=registration)

@bp.route('/delete_attendee/<int:registration_id>', methods=['POST'])
@login_required
def delete_attendee(registration_id):
    registration = Registration.query.get_or_404(registration_id)
    if registration.event.organizer != current_user:
        flash('You do not have permission to delete this attendee.', 'danger')
        return redirect(url_for('main.index'))
    db.session.delete(registration)
    db.session.commit()
    flash('Attendee has been removed from the event.', 'success')
    return redirect(url_for('main.manage_attendees', event_id=registration.event_id))