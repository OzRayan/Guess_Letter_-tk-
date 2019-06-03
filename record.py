#!/usr/bin/env python3

import datetime

from peewee import *


db = SqliteDatabase('in.db')


class Entry(Model):
    """Entry Model"""
    timestamp = DateTimeField(default=datetime.datetime.now)
    level = CharField(max_length=50)
    points = IntegerField()

    class Meta:
        database = db


def add_entry(level, points):
    """Add new record"""
    if level == 3:
        text = 'Hard'
    elif level == 2:
        text = 'Medium'
    else:
        text = 'Easy'
    Entry.create(level=text,
                 points=points)


def search():
    """Returns all the queries"""
    return Entry.select().order_by(Entry.points.desc())


def delete():
    """Deletes the lowest point query"""
    Entry.select().order_by(Entry.points.asc())[0].delete_instance()


db.connect()
db.create_tables([Entry], safe=True)
