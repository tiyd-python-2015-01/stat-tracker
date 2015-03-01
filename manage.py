#!/usr/bin/env python
import os

from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import MigrateCommand
from flask.ext.script.commands import ShowUrls, Clean

from stattracker import create_app, db, models
from stattracker.models import Enterprise, Stat

import datetime
import random


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
def seed(activity, unit):
    """Seed first user with activities and stats"""
    e = Enterprise(ent_name=activity, ent_unit=unit, user_id=1)
    db.session.add(e)
    db.session.commit()
    today = datetime.datetime.now().date()
    day = datetime.timedelta(days=1)
    date = today - day
    seeds = random.randint(20, 60)
    for x in range(seeds):
        db.session.add(Stat(value=random.randint(0, 10), recorded_at=date, enterprise_id=e.id))
        db.session.commit()
        date = date - day
    print("{} stats added.".format(seeds))


if __name__ == '__main__':
    manager.run()
