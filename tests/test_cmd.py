from pato_gui import about
from pato_gui.pom import db_order


def test_about():
    expected = {'__title__', '__author__', '__email__', '__version__', '__license__', '__copyright__', '__url__', '__help_url__'}
    actual = set(dir(about))
    assert actual.issuperset(expected), f'The actual names of the about module are {actual} but expected are {expected}'


def test_db_order1():
    dbs = ['prd', 'tst', 'acc', 'dev']
    dbs_sorted_actual = sorted(dbs, key=db_order)
    dbs_sorted_expected = ['dev', 'tst', 'acc', 'prd']
    assert dbs_sorted_actual == dbs_sorted_expected


def test_db_order2():
    dbs = ['d', 'a', 'b', 'c']
    dbs_sorted_actual = sorted(dbs, key=db_order)
    dbs_sorted_expected = ['a', 'b', 'c', 'd']
    assert dbs_sorted_actual == dbs_sorted_expected


def test_db_order3():
    dbs = ['orcl', 'tst']
    dbs_sorted_actual = sorted(dbs, key=db_order)
    dbs_sorted_expected = ['tst', 'orcl']  # dev, tst|test, acc, prd|prod have numbers 1 thru 4, the rest 256 + ascii first character
    assert dbs_sorted_actual == dbs_sorted_expected


def test_db_order4():
    dbs = ['bc_dev2', 'bc_dev', 'bc_acc', 'bc_prd']
    dbs_sorted_actual = sorted(dbs, key=db_order)
    dbs_sorted_expected = ['bc_dev', 'bc_acc', 'bc_prd', 'bc_dev2']  # dev, tst|test, acc, prd|prod have numbers 1 thru 4, the rest 256 + ascii first character
    assert dbs_sorted_actual == dbs_sorted_expected


if __name__ == '__main__':
    test_about()
    test_db_order1()
    test_db_order2()
    test_db_order3()
    test_db_order4()
