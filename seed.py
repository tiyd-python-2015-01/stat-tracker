from faker import Factory
from random import randint, random
from datetime import date, timedelta

from stat_tracker.models import User, Activity, Timestamp

ACTIVITIES = ["Run a Mile",
              "Read Something",
              "Work Out",
              "Make Dinner",
              "Water Plants",
              "Remember Birthdays",
              "Call Mom",
              "Set Alarm",
              "Practice Instruments",
              "Study",
              "Laundry"]

def seed(db):
    """
    Seeds the database but commented out to avoid running accidentally
    :param db
    :return:
    """
    users = db.session.query(User).all()
    # for user in users:
    #     num_of_activities = randint(0,len(ACTIVITIES)-1)
    #     count = 0
    #     while count < num_of_activities:
    #         activity = Activity(name=ACTIVITIES[randint(0, len(ACTIVITIES)-1)],
    #                             creator=user.id,
    #                             activity_type="Once A Day")
    #
    #         if not Activity.query.filter_by(name=activity.name, creator=activity.creator).first():
    #             db.session.add(activity)
    #             count += 1

    # today = date.today()
    # last_sixty_days = [today - timedelta(days=i) for i in range(60)]
    # last_sixty_days = [day.strftime("%Y-%m-%d") for day in last_sixty_days]
    # activities = db.session.query(Activity).all()
    #
    # for activity in activities:
    #     random_percent = random()
    #
    #     for day in last_sixty_days:
    #         if random() < random_percent:
    #             timestamp = Timestamp(timestamp=day,
    #                                   activity_id=activity.id,
    #                                   actor_id=activity.creator)
    #             if not Timestamp.query.filter_by(timestamp=day, activity_id=activity.id).first():
    #                 db.session.add(timestamp)
    #
    # db.session.commit()


def trim_seeds(db):
    """
    Removes 30% of randomly selected timestamps.
    :param db:
    :return:
    """
    timestamps = Timestamp.query.all()
    for timestamp in timestamps:
        if random() < 0.3:
            db.session.delete(timestamp)
    db.session.commit()