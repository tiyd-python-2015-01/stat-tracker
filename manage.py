import csv
from datetime import datetime
from random import randint

from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import MigrateCommand
from flask.ext.script.commands import ShowUrls, Clean

from stat_tracker import create_app, db, bcrypt, models


app = create_app()

manager = Manager(app)
manager.add_command('server', Server())
manager.add_command('db', MigrateCommand)
manager.add_command('show-urls', ShowUrls())
manager.add_command('clean', Clean())


@manager.shell
def make_shell_context():
    return dict(app=app, db=db)


@manager.command
def seed_users():
    users_added = 0
    users_updated = 0

    with open('users.csv') as csvfile:
        csv_items = csv.DictReader(csvfile)
        for row in csv_items:
            user = models.User.query.filter_by(email=row['email']).first()
            if user is None:
                user = models.User()
                users_added += 1
            else:
                users_updated += 1
            for key, value in row.items():
                if key == 'password':
                    setattr(user, 'encrypted_password',
                            bcrypt.generate_password_hash(value))
                else:
                    setattr(user, key, value)
            db.session.add(user)
        db.session.commit()
    print("{} users added, {} users updated.".format(users_added,
                                                     users_updated))




if __name__ == '__main__':
    manager.run()
