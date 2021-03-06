from contextlib import contextmanager
import redis


@contextmanager
def create_session():
    pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    r = redis.Redis(connection_pool=pool)
    try:
        yield r
    finally:
        del r


def clear_db():
    r = redis.Redis()
    return r.flushdb()


def display_db():
    db = dict()
    with create_session() as session:
        for i, x in enumerate(session.scan_iter()):
            db[i] = (x, session.lrange(x, 0, -1))
    print(db)
