Install
============

    git clone https://github.com/ConovaloffJustForFun/flask_ticket_system_api.git
    cd flask_ticket_system_api/

    # install pip and dev lib
    apt-get install python-pip libmemcached-dev postgresql-server-dev-all

    # installing dependencies
    python setup.py install

    # edit config.py
    vi ./ticket_system/config.py

    # initialize database
    FLASK_APP=ticket_system/app.py flask initdb

    # start server
    uwsgi --socket 0.0.0.0:8000 --protocol=http -w wsgi

TMP
============
Probably you can use test server fot view how this api work:

    85.143.219.32:8000/api/tickets/


API
============

    # Create ticket
    curl -d 'subject=Ticket Subject&text=Text for ticket&email=my@email.com' 85.143.219.32:8000/api/tickets/
    curl -d 'subject=Ticket Subject 2&text=Text for ticket2&email=my@email.com' 85.143.219.32:8000/api/tickets/

    # Read ticket list
    curl 85.143.219.32:8000/api/tickets/

    # Read specific ticket
    curl 85.143.219.32:8000/api/tickets/1

    # Update ticket status
    curl -X PUT -d 'status=answer_ready' 85.143.219.32:8000/api/tickets/1

    # Create comment for specific ticket
    curl -d 'text=Text of comment for this ticket&email=my@email.com' 85.143.219.32:8000/api/tickets/1/comments/

Knowledge issues
============
    
    # after
    python setup.py install
    
    # you may get error:
    Installed /usr/local/lib/python2.7/dist-packages/Flask_RESTful-0.3.6-py2.7.egg
    error: The 'flask' distribution was not found and is required by ticket-system
    
    # then simply run the installation again
    python setup.py install
    
    # https://github.com/pallets/flask/issues/1106
    


TODO
============
  * Cache as decorator for controller methods
  * SQLAlchemy and ORM
