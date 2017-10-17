try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os


def get_packages(pack):
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(pack)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]

setup(
    name='ticket_system',
    packages=get_packages('ticket_system'),
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-restful',
        'uwsgi',
        'psycopg2',
        'pylibmc',
    ]
)
