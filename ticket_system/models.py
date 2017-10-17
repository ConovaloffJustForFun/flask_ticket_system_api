# -*- coding: utf-8 -*-
"""
One of the test goal: create project without ORM
"""

import abc
import time
from datetime import datetime

import psycopg2.extras

from db.DB import DB
from ticket_system.lib.Validate import Validate
from ticket_system.lib.Exception import ExceptionValidate, ExceptionBusinessLogicCorrupt


class BaseModel(object):
    def __init__(self):
        self.db = DB()

    @abc.abstractmethod
    def save(self):
        return


class Ticket(BaseModel):
    def __init__(self):
        BaseModel.__init__(self)
        self.id = None
        self.date_create = None
        self.date_change = None
        self.subject = None
        self.text = None
        self.email = None
        self.status = None

        self._fields = ['id', 'date_create', 'date_change', 'subject', 'text', 'email', 'status']

    def __iter__(self):
        for field_name in self._fields:
            value = getattr(self, field_name)
            if isinstance(value, datetime):
                timestamp = int(time.mktime(value.timetuple()))
                yield (field_name, timestamp)
            else:
                yield (field_name, value)

    def validate_email(self):
        return Validate.email(self.email)

    def validate_status(self):
        if self.status in ('open', 'answer_ready', 'answer_wait', 'close'):
            return True

        return False

    def update(self):
        if not self.validate_status():
            raise ExceptionValidate("Valid value for status: 'open', 'answer_ready', 'answer_wait', 'close'")

        self.db.execute("""
          UPDATE
            ticket
          SET
            status = %(status)s,
            date_change = NOW()
          WHERE
            id = %(id)s;
          """, {'status': self.status, 'id': self.id})

    def save(self):
        if not self.validate_email():
            raise ExceptionValidate("not valid email: %s" % self.email)

        self.db.execute("""
          INSERT INTO ticket
            (subject, text, email)
          VALUES
            (%(subject)s, %(text)s, %(email)s);
          """, {'subject': self.subject, 'text': self.text, 'email': self.email})


class TicketContainer:
    def __init__(self):
        pass

    @classmethod
    def get_all(cls):
        db = DB().get_db()
        cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM ticket")

        ticket_row_list = cur.fetchall()
        ticket_list = []
        for ticket_row in ticket_row_list:
            ticket = Ticket()
            for column_name in ticket_row._index:
                setattr(ticket, column_name, ticket_row[column_name])
            ticket_list.append(ticket)

        return ticket_list

    @classmethod
    def get_by_id(cls, id):
        db = DB().get_db()
        cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM ticket WHERE id = %(id)s", {'id': id})

        ticket_row = cur.fetchone()
        if ticket_row is None:
            return None

        ticket = Ticket()
        for column_name in ticket_row._index:
            setattr(ticket, column_name, ticket_row[column_name])

        return ticket


class Comment(BaseModel):
    def __init__(self):
        BaseModel.__init__(self)

        self.id = None
        self.ticket_id = None
        self.date_create = None
        self.email = None
        self.text = None

        self._fields = ['id', 'ticket_id', 'date_create', 'text', 'email']

    def save(self):
        if not self.validate_email():
            raise ExceptionValidate("not valid email: %s" % self.email)

        self.db.execute("""
          INSERT INTO comment
            (ticket_id, text, email)
          VALUES
            (%(ticket_id)s, %(text)s, %(email)s);
          """, {'ticket_id': self.ticket_id, 'text': self.text, 'email': self.email})

    def validate_email(self):
        return Validate.email(self.email)

    def __iter__(self):
        for field_name in self._fields:
            value = getattr(self, field_name)
            if isinstance(value, datetime):
                timestamp = int(time.mktime(value.timetuple()))
                yield (field_name, timestamp)
            else:
                yield (field_name, value)


class CommentContainer:
    def __init__(self):
        pass

    @classmethod
    def get_by_ticket_id(cls, ticket_id):
        db = DB().get_db()
        cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM comment WHERE ticket_id = %(ticket_id)s", {'ticket_id': ticket_id})

        comment_row_list = cur.fetchall()

        comment_list = []
        for comment_row in comment_row_list:
            comment = Comment()
            for column_name in comment_row._index:
                setattr(comment, column_name, comment_row[column_name])
            comment_list.append(comment)

        return comment_list
