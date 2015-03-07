#!/usr/bin/env python
import os
import csv
import random
from datetime import date

from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import MigrateCommand
from flask.ext.script.commands import ShowUrls, Clean

from tasker import create_app, db, models

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
    return dict(app=app,
                db=db,
                user=models.User,
                task=models.Task,
                tracking=models.Tracking
                )


@manager.command
def test():
    """Run the tests."""
    import pytest
    exit_code = pytest.main([TEST_PATH, '--verbose'])
    return exit_code

@manager.command
def seed_stats():
    myusers = models.User.query.order_by(models.User.id.desc()).all()
    for user in myusers:
       tasks = models.Task.query.filter_by(t_user=user.id).all()
       for task in tasks:
            month = 1
            days = 31
            for month in range(1,3):
                for day in range(1,days):
                    r_date = date(2015,month,day)
                    r_value = random.randint(1,100)
                    stat = models.Tracking(user.id, task.id, r_date, r_value)
                    db.session.add(stat)
                days = 28
       db.session.commit()


if __name__ == '__main__':
    manager.run()
