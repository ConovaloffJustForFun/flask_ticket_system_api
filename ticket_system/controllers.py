# -*- coding: utf-8 -*-

from ticket_system.lib.Exception import ExceptionNotFound, ExceptionBusinessLogicCorrupt

import models
from lib.Cache import CacheContainer


class TicketController:
    def get_list(self):

        cache_key = 'ticket:all'
        cache = CacheContainer().get_cache()
        cache_result = cache.get(cache_key)
        if cache_result is not None:
            return cache_result

        result = []

        ticket_list = models.TicketContainer.get_all()
        for ticket in ticket_list:
            ticket_dict = dict(ticket)

            comment_list = models.CommentContainer.get_by_ticket_id(ticket.id)
            comment_list_dict = []
            for comment in comment_list:
                comment_list_dict.append(dict(comment))

            ticket_dict['comments'] = comment_list_dict
            result.append(ticket_dict)

        cache.set(cache_key, result)
        return result

    def create_ticket(self, subject, text, email):
        ticket = models.Ticket()
        ticket.subject = subject
        ticket.text = text
        ticket.email = email

        ticket.save()

        cache_key = 'ticket:all'
        CacheContainer().get_cache().delete(cache_key)

    def get_by_id(self, id):
        cache_key = 'ticket:%s' % id
        cache = CacheContainer().get_cache()
        cache_result = cache.get(cache_key)
        if cache_result is not None:
            return cache_result

        ticket = models.TicketContainer.get_by_id(id)
        if ticket is None:
            raise ExceptionNotFound('Ticket with id %s not found' % id)

        comment_list = models.CommentContainer.get_by_ticket_id(ticket.id)
        comment_list_dict = []
        for comment in comment_list:
            comment_list_dict.append(dict(comment))

        ticket_dict = dict(ticket)
        ticket_dict['comments'] = comment_list_dict

        cache.set(cache_key, ticket_dict)
        return ticket_dict

    def update_status(self, id, status):
        ticket = models.TicketContainer.get_by_id(id)
        if ticket.status == 'open' and status not in ('answer_ready', 'close'):
            raise ExceptionBusinessLogicCorrupt(
                "Ticket in the status 'open' and can go only into state 'close' or 'answer_ready'"
            )
        elif ticket.status == 'answer_ready' and status not in ('answer_wait', 'close'):
            raise ExceptionBusinessLogicCorrupt(
                "Ticket in status 'answer_ready' and can go only into state 'answer_wait' or 'close'"
            )
        elif ticket.status == 'close':
            raise ExceptionBusinessLogicCorrupt(
                "Ticket in the status 'close' and not allowed to change the status"
            )
        # This is not in task, but in the future it may be needed.
        # elif self._status == 'answer_wait' and status not in ('answer_ready', 'close'):
        #     raise ExceptionBusinessLogicCorrupt(
        #         "Ticket in status 'answer_wait' and can go only into state 'answer_ready' or 'close'"
        #     )

        ticket.status = status
        ticket.update()

        cache_key = 'ticket:%s' % id
        CacheContainer().get_cache().delete(cache_key)


class CommentController:
    def create_comment(self, ticket_id, text, email):
        ticket = models.TicketContainer.get_by_id(ticket_id)
        if not ticket:
            raise ExceptionNotFound('Ticket not found')

        if ticket.status == 'close':
            raise ExceptionBusinessLogicCorrupt('Not allowed to add comments for a closed ticket')

        comment = models.Comment()
        comment.ticket_id = ticket.id
        comment.text = text
        comment.email = email

        comment.save()

        cache_key = 'ticket:%s' % ticket_id
        CacheContainer().get_cache().delete(cache_key)
