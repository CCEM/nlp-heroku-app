"""Setup for server/web page of reddex extension."""
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_jinja2',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'ipython',
    'pyramid_ipython'
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest',
    'pytest-cov',
    'tox',
]

setup(
    name='reddex',
    version='0.0',
    description='Reddex',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='Carlos Cadena, Chris Hudson, Ely Paysinger, Morgan Numura',
    author_email='cs.cadena@gmail.com, c.ahudson84@yahoo.com, paysinger@gmail.com, morgan.nomura@gmail.com',
    url='this will be a link to chrome store?',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'testing': tests_require,
    },
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = reddex:main',
        ],
        'console_scripts': [
            'initdb = reddex.scripts.initializedb:main',
        ],
    },
)
