import os
import sys
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )
from ..models import SubReddit
from datetime import datetime


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    settings['sqlalchemy.url'] = os.environ.get('DATABASE_URL')

    engine = get_engine(settings)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    # session_factory = get_session_factory(engine)

    # with transaction.manager:
    #     import random
    #     dbsession = get_tm_session(session_factory, transaction.manager)
    #     test_subs = ['test1', 'test2', 'test3', 'test4', 'test5',
    #                  'test6', 'test7', 'test8', 'test9', 'test10']
    #     holder = []
    #     for sub in test_subs:
    #         for _ in range(5):
    #             new_entry = SubReddit(
    #                 name=sub,
    #                 mean=random.uniform(-1, 1),
    #                 median=random.uniform(-1, 1),
    #                 date=datetime.now()
    #             )
    #             holder.append(new_entry)
    #
    #
    #     dbsession.add_all(holder)
