import pytest

from reel2bits import create_app
from models import db as _db
from dbseed import make_db_seed
import os


@pytest.yield_fixture(scope='session')
def app():
    cfg = os.getenv('CONFIGTEST', 'tests/config_test.py')
    app = create_app(cfg)
    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.yield_fixture(scope='session')
def db(app):
    _db.create_all()
    make_db_seed(_db)

    yield _db

    _db.drop_all()


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


@pytest.yield_fixture(scope='function')
def session(db):
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection)
    session = db.create_scoped_session(options=options)

    db.session = session

    yield session

    transaction.rollback()
    connection.close()
    session.remove()