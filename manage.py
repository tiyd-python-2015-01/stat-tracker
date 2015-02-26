#!/usr/bin/env python
import os

from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import MigrateCommand
from flask.ext.script.commands import ShowUrls, Clean

from urlybird.app import create_app, db, models
from urlybird.generate_seed_data import create_user, create_bookmarks, create_specified_user
from urlybird.generate_seed_data import user_to_bookmark, click_creation

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
def seed(num_users=3):
    """Seed database."""
    total_bookmarks = 10*num_users
    create_bookmarks(total_bookmarks)
    create_user(0)
    for counter in range(1, num_users+1):
        create_user()
        user_to_bookmark(user_id=counter, bookmark_user_num=10,
                         bookmark_count=total_bookmarks)
    clicks_added = click_creation(user_count=num_users)

    create_specified_user('zackjcooper@gmail.com', 'password', 'Zack')
    user_to_bookmark(user_id=4, bookmark_user_num=10,
                     bookmark_count=total_bookmarks)
    print('Users: {} Bookmarks: {} Clicks: {}'.format(num_users,
                                                     total_bookmarks,
                                                     clicks_added))

if __name__ == '__main__':
    manager.run()
