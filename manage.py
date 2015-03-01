#!/usr/bin/env python
import os

from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import MigrateCommand
from flask.ext.script.commands import ShowUrls, Clean

from stat_tracker.app import create_app, db, models
from stat_tracker.generate_seed_data import create_specified_user, \
                                            create_items, create_action

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
def seed():
    """Seed database."""
    action_num = 27
    user = create_specified_user('zackjcooper@gmail.com', 'password', 'Zack')
    created_item_list = create_items(num=5, user_id=user.id)
    for item in created_item_list:
        create_action(item.id, num=action_num)
    action_count = len(created_item_list) * action_num
    print('Items: {} Actions: {}'.format(len(created_item_list), action_count))


if __name__ == '__main__':
    manager.run()
