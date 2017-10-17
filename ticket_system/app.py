# -*- coding: utf-8 -*-

from flask import Flask, g
from flask_restful import Api, Resource, reqparse
from werkzeug.exceptions import BadRequest

import controllers
from ticket_system.lib.Exception import ExceptionProjectBase
from db.DB import DBInit

app = Flask(__name__)
app.config.from_pyfile('config.py')

api = Api(app)


class TicketListAPI(Resource):
    def get(self):
        try:
            ticket_controller = controllers.TicketController()
            return {
                'status': 'ok',
                'data': ticket_controller.get_list()
            }
        except ExceptionProjectBase, e:
            return {
                'status': 'error',
                'message': e.message
            }

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('subject', type=unicode, required=True, help="You must specify 'subject'")
        parser.add_argument('text', type=unicode, required=True, help="You must specify 'text'")
        parser.add_argument('email', type=unicode, required=True, help="You must specify 'email'")

        try:
            args = parser.parse_args()
        except BadRequest, e:
            if hasattr(e, 'data') and isinstance(e.data, dict):
                e.data['status'] = 'error'
            raise e

        try:
            ticket_controller = controllers.TicketController()
            ticket_controller.create_ticket(**args)

        except ExceptionProjectBase, e:
            return {
                'status': 'error',
                'message': e.message
            }

        return {
            'status': 'ok',
            'message': "You create ticket"
        }


class TicketAPI(Resource):
    def get(self, id):
        try:
            ticket_controller = controllers.TicketController()
            return {
                'status': 'ok',
                'data': ticket_controller.get_by_id(id)
            }
        except ExceptionProjectBase, e:
            return {
                'status': 'error',
                'message': e.message
            }

    def put(self, id):
        return self.update(id)

    def post(self, id):
        return self.update(id)

    def update(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('status', type=unicode, required=True, help="You may update only 'status' field")

        try:
            args = parser.parse_args()
        except BadRequest, e:
            if hasattr(e, 'data') and isinstance(e.data, dict):
                e.data['status'] = 'error'
            raise e

        try:
            ticket_controller = controllers.TicketController()
            ticket_controller.update_status(id, args['status'])
        except ExceptionProjectBase, e:
            return {
                'status': 'error',
                'message': e.message
            }

        return {
            'status': 'ok',
            'message': "You update status for ticket %s" % id
        }


class CommentsListAPI(Resource):
    def post(self, ticket_id):
        parser = reqparse.RequestParser()

        parser.add_argument('text', type=unicode, required=True, help="You must specify 'text'")
        parser.add_argument('email', type=unicode, required=True, help="You must specify 'email'")

        try:
            args = parser.parse_args()
        except BadRequest, e:
            if hasattr(e, 'data') and isinstance(e.data, dict):
                e.data['status'] = 'error'
            raise e

        try:
            comment_controller = controllers.CommentController()
            comment_controller.create_comment(ticket_id=ticket_id, **args)
        except ExceptionProjectBase, e:
            return {
                'status': 'error',
                'message': e.message
            }

        return {
            'status': 'ok',
            'message': "You create comment for ticket: %s" % ticket_id
        }


api.add_resource(TicketListAPI, '/api/tickets', '/api/tickets/')
api.add_resource(TicketAPI, '/api/tickets/<int:id>')
api.add_resource(CommentsListAPI, '/api/tickets/<int:ticket_id>/comments', '/api/tickets/<int:ticket_id>/comments/')


@app.cli.command()
def initdb():
    """Initialize the database."""
    db_init = DBInit()
    db_init.run()
    print "Database successfully Initialized"


@app.teardown_appcontext
def close_db(error):
    if not hasattr(g, 'db'):
        return
    if not hasattr(g.db, 'close'):
        return
    g.db.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0')
