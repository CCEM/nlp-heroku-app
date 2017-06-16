"""."""
from pyramid.view import view_config
from reddex.scripts.sentiment_reddex import evaluate_comments
from pyramid.response import Response
from reddex.models import SubReddit
from datetime import datetime
from pyramid.httpexceptions import HTTPNotFound
import operator


@view_config(route_name='home', renderer='../templates/home.jinja2')
def home_view(request):
    """Get data from DB and render on home view."""
    session = request.dbsession
    distinct_subs = session.query(SubReddit.name).distinct()
    distinct_subs = [sub[0] for sub in distinct_subs]
    averages_dict = {}
    views_dict = {}
    neutral5 = positive5 = negative5 = None
    for sub in distinct_subs:
        sub_medians = session.query(
            SubReddit.median
        ).filter(SubReddit.name == sub).all()
        sub_medians = [median[0] for median in sub_medians]
        views_dict[sub] = len(sub_medians)
        averages_dict[sub] = sum(sub_medians) / len(sub_medians)
        sorted_list_of_tuples = sorted(averages_dict.items(),
                                       key=operator.itemgetter(1))[::-1]
        positive5 = sorted_list_of_tuples[0:5]
        negative5 = sorted_list_of_tuples[-5:][::-1]
        neutral_start = int(len(sorted_list_of_tuples) / 2) - 2
        neutral_end = int(len(sorted_list_of_tuples) / 2) + 3
        neutral5 = sorted_list_of_tuples[neutral_start:neutral_end]

    return {
        'neutral': neutral5,
        'positive': positive5,
        'negative': negative5,
        'views': views_dict
    }


@view_config(route_name='about', renderer='../templates/about.jinja2')
def about_view(request):
    """Render about view."""
    if request.method != 'GET':
        raise HTTPNotFound
    return {}


@view_config(route_name='inbound', renderer='json')
def inbound_api(request):
    """Accept good POST request and send back data."""
    # request.response = Response()
    # request.response.headerlist = []
    # request.response.headerlist.extend(
    #     (
    #         ('Access-Control-Allow-Origin',
    #          'chrome-extension://lcajaahlihccgekhidmjiedlkcdpedpo'),
    #         ('Content-Type', 'application/json')
    #     )
    # )
    if request.method == 'POST':
        try:
            response = {}
            comments_dict = dict(request.POST)
            sub = comments_dict.pop('url', None)
            for item in comments_dict:
                response[item] = evaluate_comments(comments_dict[item])

            new_entry = SubReddit(
                name=sub,
                mean=sum(response.values()) / len(response),
                median=sorted(list(response.values()))
                [(int(len(response) / 2))],
                date=datetime.now()
            )

            request.dbsession.add(new_entry)
            return response
        except TypeError:
            return 'Invalid input.'
    else:
        raise HTTPNotFound
