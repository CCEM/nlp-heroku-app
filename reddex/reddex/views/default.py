"""."""
from pyramid.view import view_config
from reddex.scripts.sentiment_reddex import evaluate_comments
from pyramid.response import Response
from reddex.models import SubReddit


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
    print('made it here')
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
        print('receieved comments', comments_dict)
        # update_db(comments_dict)
        print('back from update')
        for item in comments_dict:
            response[item] = evaluate_comments(comments_dict[item])
        print('response composed')
        print('sent')
        return response
    else:
        return 'get request'


@view_config(route_name='test_db', renderer='../templates/testdb.jinja2')
def testdb_view(request):
    """."""
    entries = request.dbsession.query(SubReddit).all()
    return {'db': entries}


# def update_db(data):
#     """"."""
#     print('updating dB', data)
#     return data
