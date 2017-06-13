"""."""
from pyramid.view import view_config
from reddex.scripts.sentiment_reddex import evaluate_comments


@view_config(route_name='home', renderer='../templates/home.jinja2')
def my_view(request):
    """."""
    # try:
    #     query = request.dbsession.query(MyModel)
    #     one = query.filter(MyModel.name == 'one').first()
    # except DBAPIError:
    #     return Response(db_err_msg, content_type='text/plain', status=500)
    return {}


@view_config(route_name='about', renderer='../templates/about_us.jinja2')
def about_view(request):
    """."""
    # try:
    #     query = request.dbsession.query(MyModel)
    #     one = query.filter(MyModel.name == 'one').first()
    # except DBAPIError:
    #     return Response(db_err_msg, content_type='text/plain', status=500)
    return {}


@view_config(route_name='inbound', renderer='json')
def inbound_view(request):
    """."""
    if request.method == 'POST':
        response = {'headers': {'Access-Control-Allow-Origin': '*'}}
        comments_dict = dict(request.POST)
        for item in comments_dict:
            response[item] = evaluate_comments(comments_dict[item])
        return response
