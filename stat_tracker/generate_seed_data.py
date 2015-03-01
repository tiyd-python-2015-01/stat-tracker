from faker import Factory
from .models import User, Item, Action
import random
import datetime
from stat_tracker.app import db


def create_specified_user(email, password, name):
    user = User(email=email, name=name, password=password)
    db.session.add(user)
    db.session.commit()
    return user


def create_items(num=5, user_id=1):
    fake = Factory.create()
    created_list = []
    for _ in range(1, num+1):
        name = fake.text(max_nb_chars=10)
        goal = fake.text(max_nb_chars=20)
        description = fake.text(max_nb_chars=30)
        item = Item(user_id = user_id,
                    name = name,
                    goal = goal,
                    description = description)
        db.session.add(item)
        db.session.commit()
        created_list.append(item)
    return created_list

def create_action(item_id, num=27):
    fake = Factory.create()
    date = datetime.datetime(2015,1,1)
    for _ in range(1, num+1):
        value = random.randint(1,10)
        logged_at = fake.date_time_between(start_date="-30d", end_date="now")
        action = Action(item_id=item_id, value=value, logged_at=logged_at)
        db.session.add(action)
        date += datetime.timedelta(days=1)
    db.session.commit()
