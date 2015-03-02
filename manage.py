import os
from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import MigrateCommand
from flask.ext.script.commands import ShowUrls,Clean
from stat_tracker import create_app, db, models
from faker import Factory
from random import randint
from random import choice
fake = Factory.create()

#Don't know what this does.
HERE = os.path.abspath(os.path.dirname(__file__))

app = create_app()
manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('server', Server())
manager.add_command('show-urls', ShowUrls())
manager.add_command('clean', Clean())

manager.shell
def make_shell_context():
    """ Creates a python REPL with several default imports
        in the context of the app
    """

    return dict(app=app, db=db)


activities = [("Stairs Climbed","Stairs"), ("Glasses of water","Glasses"),
              ("Vegetables Eaten", "Vegetables"), ("Hugs Given","Hugs"),
              ("Coding Lines Finished", "Coding Lines")]


@manager.command
def make_activities():
    a_counter = 1

    for _ in range(1,5):
        b_counter = 0
        for activity in activities:
            activity = models.Activity(user_id = a_counter,
                                       title = activities[b_counter][0],
                                       unit = activities[b_counter][1])
            db.session.add(activity)
            db.session.commit()
            b_counter +=1
        b_counter = 0
        a_counter +=1
@manager.command
def make_instances():
    activity_id = [activity.id for activity in models.Activity.query.all()]
    for _ in range(1000):
        instance = models.Instance(user_id = randint(1,4),
                                   activity_id = choice(activity_id),
                                   date = fake.date_time_between(start_date="-30d", end_date="now").date()    ,
                                   freq = randint(1,15))
        db.session.add(instance)
        db.session.commit()

if __name__ == '__main__':
    manager.run()
