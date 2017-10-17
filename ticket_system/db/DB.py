import psycopg2
from flask import g
from flask import current_app as app


class DB:
    def __init__(self):
        pass

    def execute(self, *args, **kwargs):
        db = self.get_db()
        cur = db.cursor()
        cur.execute(*args, **kwargs)
        db.commit()
        cur.close()

    def get_db(self):
        if not hasattr(g, 'db'):
            g.db = self.connect_db()

        return g.db

    def connect_db(self):
        db_conf = app.config.get('DATABASE')
        conn = psycopg2.connect(**db_conf)

        return conn


class DBInit(DB):
    def __init__(self):
        DB.__init__(self)

    def run(self):
        db = self.get_db()
        with app.open_resource('db/schema.sql', mode='r') as f:
            db.cursor().execute(f.read())
        db.commit()
