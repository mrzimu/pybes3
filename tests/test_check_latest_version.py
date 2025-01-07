from pybes3._check_latest_version import check_latest_version, get_all_tags, get_latest_version


def test_get_all_tags():
    tags = get_all_tags()
    assert len(tags) > 0


def test_get_latest_version():
    tags1 = ["v0.1.0", "v0.1.1"]
    latest_version1 = get_latest_version(tags1)
    assert latest_version1 == (0, 1, 1, 0)

    tags2 = ["v0.1.0", "v0.1.0.1"]
    latest_version2 = get_latest_version(tags2)
    assert latest_version2 == (0, 1, 0, 1)

    tags3 = ["v0.1.0", "v0.1.0.1", "v0.1.0.2"]
    latest_version3 = get_latest_version(tags3)
    assert latest_version3 == (0, 1, 0, 2)

    tags4 = ["v0.1.0", "v0.1.0.1", "v0.1.0.2", "v0.2.0"]
    latest_version4 = get_latest_version(tags4)
    assert latest_version4 == (0, 2, 0, 0)

    # v0.3 should be ignored
    tags5 = ["v0.1.0", "v0.1.0.1", "v0.1.0.2", "v0.2.0", "v0.3"]
    latest_version5 = get_latest_version(tags5)
    assert latest_version5 == (0, 2, 0, 0)


def test_check_latest_version(capsys):
    test_current_version1 = (99, 99, 99, 99)
    check_latest_version(test_current_version1)
    captured = capsys.readouterr()
    assert captured.out == ""

    test_current_version2 = (0, 1, 0, 1)
    check_latest_version(test_current_version2)
    captured = capsys.readouterr()
    assert len(captured.out) > 0
