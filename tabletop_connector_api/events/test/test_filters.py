from tabletop_connector_api.events.filters import unpack_from_list


def test_unpack_from_list_not_packed():
    d = {"a": 1}
    unpack_from_list(d, "a")

    assert d["a"] == 1


def test_unpack_from_list_packed():
    d = {"a": [1]}
    unpack_from_list(d, "a")

    assert d["a"] == 1
