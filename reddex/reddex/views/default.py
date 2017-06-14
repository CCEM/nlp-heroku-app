"""."""
from pyramid.view import view_config
from reddex.scripts.sentiment_reddex import evaluate_comments
from pyramid.response import Response
from reddex.models import SubReddit
import threading


@view_config(route_name='home', renderer='../templates/home.jinja2')
def home_view(request):
    """."""
    # try:
    #     query = request.dbsession.query(MyModel)
    #     one = query.filter(MyModel.name == 'one').first()
    # except DBAPIError:
    #     return Response(db_err_msg, content_type='text/plain', status=500)
    return {}


@view_config(route_name='about', renderer='../templates/about.jinja2')
def about_view(request):
    """."""
    # try:
    #     query = request.dbsession.query(MyModel)
    #     one = query.filter(MyModel.name == 'one').first()
    # except DBAPIError:
    #     return Response(db_err_msg, content_type='text/plain', status=500)
    return {}


@view_config(route_name='inbound', renderer='json')
def inbound_api(request):
    """."""
    request.response = Response()
    request.response.headerlist = []
    request.response.headerlist.extend(
        (
            ('Access-Control-Allow-Origin', '*'),
            ('Content-Type', 'application/json')
        )
    )
    if request.method == 'POST':
        response = {}
        comments_dict = dict(request.POST)
        sub = comments_dict.pop('url', None)
        for item in comments_dict:
            response[item] = evaluate_comments(comments_dict[item])
        thread = threading.Thread(target=update_db, args=(request, response, sub))
        thread.daemon = True
        thread.start()
        return response
    else:
        return 'get request'


@view_config(route_name='testdb', renderer='../templates/testdb.jinja2')
def testdb_view(request):
    """."""
    entries = request.dbsession.query(SubReddit).all()
    return {'db': entries}


def update_db(request, data, sub):
    """"."""
    new_entry = SubReddit(
        name=sub,
        mean=sum(data.values())/len(data),
        median=sorted(list(data.values()))[(int(len(data)/2))]
    )
    request.dbsession.add(new_entry)
    return
