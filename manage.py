#!/usr/bin/env python
import os

from flask.ext.script import Manager, Server
from flask.ext.migrate import MigrateCommand
from flask.ext.script.commands import ShowUrls, Clean
from statful.models import Activity, Stat
from statful import create_app, db
from datetime import datetime, timedelta
import random


HERE = os.path.abspath(os.path.dirname(__file__))
TEST_PATH = os.path.join(HERE, 'tests')


app = create_app()
manager = Manager(app)
manager.add_command('server', Server())
manager.add_command('db', MigrateCommand)
manager.add_command('show-urls', ShowUrls())
manager.add_command('clean', Clean())


@manager.shell
def make_shell_context():
    """ Creates a python REPL with several default imports
        in the context of the app
    """

    return dict(app=app, db=db)


@manager.command
def test():
    """Run the tests."""
    import pytest
    exit_code = pytest.main([TEST_PATH, '--verbose'])
    return exit_code


@manager.command
def seed_activities():
    activity_tuple = [('clicker', 3), ('yes_no', 3), ('scale', 3)]
    names = [('Running a mile', 'mile'), ('Pull ups', 'reps'),
             ('Crunches', 'reps'), ('Eat breakfast', ""),
             ('write stories', ""), ('Commit to Github', ""),
             ('Teach class', ""), ('Make breakfast', ""),
             ('Read', "")]
    for activity_kind in activity_tuple:
        for kind in range(activity_kind[1]):
            activity = Activity(name=names[0][0],
                                type=activity_kind[0],
                                unit=names[0][1],
                                user_id=1
                                )
            names.pop(0)
            db.session.add(activity)
    db.session.commit()
    print("Activities seeded.")


@manager.command
def seed_stats():
    for activities_id in range(2, 5):
        for day in range(30):
            activity_date = datetime.today() - timedelta(days=day)
            clicker_stat = Stat(occurrences=random.randint(1, 10),
                                when=activity_date,
                                activity_id=activities_id)
            db.session.add(clicker_stat)
            yes_no_stat = Stat(yes_no=random.randint(0, 1),
                               when=activity_date,
                               activity_id=(activities_id+3))
            db.session.add(yes_no_stat)
            scale_stat = Stat(scale=random.randint(1, 5),
                              when=activity_date,
                              activity_id=(activities_id+6))
            db.session.add(scale_stat)
    db.session.commit()
    print("Stats seeded.")


if __name__ == '__main__':
    manager.run()
