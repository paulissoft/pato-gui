from utils import about
from utils.pom import db_order


def test_about():
    expected = {'__title__', '__author__', '__email__', '__version_info__', '__version__', '__license__', '__copyright__', '__url__', '__help_url__'}
    actual = set(dir(about))
    assert actual.issuperset(expected), f'The actual names of the about module are {actual} but expected are {expected}'


def test_db_order():
    dbs = ['prd', 'tst', 'acc', 'dev']
    dbs_sorted_actual = sorted(dbs, key=db_order)
    dbs_sorted_expected = ['dev', 'tst', 'acc', 'prd']
    assert dbs_sorted_actual == dbs_sorted_expected
    dbs = ['d', 'a', 'b', 'c']
    dbs_sorted_actual = sorted(dbs, key=db_order)
    dbs_sorted_expected = ['a', 'b', 'c', 'd']
    assert dbs_sorted_actual == dbs_sorted_expected


if __name__ == '__main__':
    test_about()
    test_db_order()
