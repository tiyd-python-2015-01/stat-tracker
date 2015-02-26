from faker import Factory
from .models import Bookmark, User, BookmarkUser, Click
import random
from stat_tracker.app import db


def create_user(user_id=1):
    fake = Factory.create()

    email = fake.email()
    name = fake.name()
    password = fake.password()
    if user_id == 0:
        user = User(id=0, email=email, name=name, password=password)
    else:
        user = User(email=email, name=name, password=password)
    db.session.add(user)
    db.session.commit()


def create_bookmarks(num=30):
    fake = Factory.create()
    for _ in range(1, num+1):
        title = fake.company()
        description = fake.text(max_nb_chars=40)
        url = fake.url()
        bookmark = Bookmark(title=title,
                            description=description,
                            url=url)
        db.session.add(bookmark)
    db.session.commit()

def user_to_bookmark(user_id, bookmark_user_num=10, bookmark_count=30 ):
    for counter in range(1, bookmark_user_num+1):
        bookmark_user = BookmarkUser(user_id=user_id,
                                     item_id=random.randint(1,bookmark_count))
        db.session.add(bookmark_user)
    db.session.commit()


def click_creation(user_count, click_count=1000):
    fake=Factory.create()
    for num in range(0,user_count+1):
        for count in range(0,click_count):
            item_id = random.randint(1,30)
            timestamp = fake.date_time_between(start_date="-30d",
                                               end_date="now")
            click = Click(item_id = item_id,
                          user_id = num,
                          timestamp = timestamp,
                          user_ip_address = fake.ipv4(),
                          user_agent =fake.user_agent())
            db.session.add(click)
    db.session.commit()
    return user_count * click_count

def create_specified_user(email, password, name):
    user = User(email=email, name=name, password=password)
    db.session.add(user)
    db.session.commit()
