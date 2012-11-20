from datetime import datetime
from pyramid.response import Response
from pyramid.view import view_config, notfound_view_config
import transaction

from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    )

from sqlalchemy.exc import DBAPIError
from sqlalchemy import desc, asc

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
      t.updated = now
    else:
      t = Thread(now, now)
    DBSession.add(t)
    DBSession.flush()
    p = Post(t.id, now, request.params['msg'])
    DBSession.add(p)
    url = request.route_url('board') 
    return HTTPFound(location=url)

  latest_threads = DBSession.query(Thread).order_by(desc(Thread.updated)).limit(5)
  return {'latest_threads':latest_threads}

@view_config(route_name='thread', renderer='thread.mak')
def thread(request):
  thread_id = request.matchdict['thread_id']
  thread = DBSession.query(Thread).get(thread_id)
  if thread is None:
    raise HTTPNotFound(comment='No such thread.').exception
  return {'thread':thread}

@view_config(route_name='home', renderer='home.mak')
def my_view(request):
    return {}

@notfound_view_config(renderer='404.mak')
def notfound(context, request):
  msg =  request.exception.comment
  return {'message':msg}
