"""Assign web url routes to the names of different pages."""


def includeme(config):
    """Assign web url routes to the names of different pages."""
    config.add_static_view('static', 'reddex:static')
    config.add_route('home', '/')
    config.add_route('inbound', '/inbound')
    config.add_route('about', '/about')
    config.add_route('db_test', '/testdb')
