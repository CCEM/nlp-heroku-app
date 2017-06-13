"""."""
from pyramid.view import view_config
from reddex.scripts.sentiment_reddex import evaluate_comments
from pyramid.response import Response


@view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
def my_view(request):
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
        for item in comments_dict:
            response[item] = evaluate_comments(comments_dict[item])
        return response
