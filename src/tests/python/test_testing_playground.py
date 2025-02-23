import jutge_api_client as j


def test_inc():
    """Checks that passing objects in and out of endpoints works."""

    jutge = j.JutgeApiClient()
    input = j.TwoInts(a=1, b=2)
    output = jutge.testing.playground.inc(input)
    assert output.a == input.a + 1
    assert output.b == input.b + 1


def test_add3i():
    """Checks that inlining the parameters works."""

    jutge = j.JutgeApiClient()
    s = jutge.testing.playground.add3i(1, 2, 3)
    assert s == 6


def test_negate():
    """Checks that ifiles and ofiles work."""

    jutge = j.JutgeApiClient()
    download = jutge.misc.get_logo()
    download.write("logo.png")
    file = open("logo.png", "rb")
    download = jutge.testing.playground.negate(file)
    download.write("negated_logo.png")
    # PNG files start with an 8-byte signature: 89 50 4E 47 0D 0A 1A 0A
    signature = [0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]
    assert download.data[:8] == bytes(signature), "The logo has not a PNG signature"
