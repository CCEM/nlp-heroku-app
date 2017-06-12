"""."""
from pyramid.view import view_config


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
    if request.method == 'POST':
        return request.POST
