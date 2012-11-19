from datetime import datetime
from pyramid.response import Response
from pyramid.view import view_config
import transaction

from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    )

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Thread,
    Post,
    )

@view_config(route_name='board', renderer='board.mak')
def board(request):
  if 'form.submitted' in request.params:
    now = datetime.now()
    if 'thread_id' in request.params:
      t = DBSession.query(Thread).get(request.params['thread_id'])
      if t is None:
        return HTTPNotFound('No such thread')
    else:
      t = Thread(now, now)
      DBSession.add(t)
      DBSession.flush()
    p = Post(t.id, now, request.params['msg'])
    DBSession.add(p)
    url = request.route_url('board') 
    return HTTPFound(location=url)

  latest_threads = DBSession.query(Thread).order_by(Thread.updated).limit(5)
  return {'latest_threads':latest_threads}

@view_config(route_name='thread', renderer='thread.mak')
def thread(request):
  thread_id = request.matchdict['thread_id']
  thread = DBSession.query(Thread).get(thread_id)
  if thread is None:
    return HTTPNotFound('No such thread')
  return {'thread':thread}

@view_config(route_name='home', renderer='home.mak')
def my_view(request):
    return {}

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_immago_db" script
    to initialize your database tables.  Check your virtual 
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

