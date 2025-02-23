import jutge_api_client as j


def test_inc():
    """Checks that passing objects in and out of endpoints works."""

    jutge = j.JutgeApiClient()
    input = j.TwoInts(a=1, b=2)
    output = jutge.playground.inc(input)
    assert output.a == input.a + 1
    assert output.b == input.b + 1


def test_add3i():
    """Checks that inlining the parameters works."""

    jutge = j.JutgeApiClient()
    s = jutge.playground.add3i(1, 2, 3)
    assert s == 6
