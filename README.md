Install
============

    # edit config.py
    vi ./ticket_system/config.py

    FLASK_APP=ticket_system/app.py flask initdb

    uwsgi --socket 0.0.0.0:8000 --protocol=http -w wsgi

API
============

    # Create ticket
    curl -d 'subject=Ticket Subject&text=Text for ticket&email=my@email.com' localhost:8000/api/tickets/
    curl -d 'subject=Ticket Subject 2&text=Text for ticket2&email=my@email.com' localhost:8000/api/tickets/

    # Read ticket list
    curl localhost:8000/api/tickets/

    # Read specific ticket
    curl localhost:8000/api/tickets/1

    # Update ticket status
    curl -X PUT -d 'status=answer_ready' localhost:8000/api/tickets/1

    # Create comment for specific ticket
    curl -d 'text=Text of comment for this ticket&email=my@email.com' localhost:8000/api/tickets/1/comments/
