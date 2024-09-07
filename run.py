from app import create_app, db
from app.models import User, Event, Attendee, Registration

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Event': Event, 'Attendee': Attendee, 'Registration': Registration}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)