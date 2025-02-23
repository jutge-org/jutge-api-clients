import jutge_api_client as j


def test_get_time():
    jutge = j.JutgeApiClient()
    time = jutge.misc.get_time()
    assert isinstance(time, object)
    assert isinstance(time, j.Time)
    assert isinstance(time.full_time, str)
    assert isinstance(time.int_timestamp, int)
    assert isinstance(time.float_timestamp, float)
    assert isinstance(time.time, str)
    assert isinstance(time.date, str)


def test_get_fortune():
    jutge = j.JutgeApiClient()
    fortune = jutge.misc.get_fortune()
    assert isinstance(fortune, str)


def test_get_homepage_stats():
    jutge = j.JutgeApiClient()
    stats = jutge.misc.get_homepage_stats()
    assert isinstance(stats, object)
    assert isinstance(stats, j.HomepageStats)
    assert isinstance(stats.users, int)
    assert isinstance(stats.problems, int)
    assert isinstance(stats.submissions, int)


def test_get_logo():
    jutge = j.JutgeApiClient()
    logo = jutge.misc.get_logo()
    assert isinstance(logo, object)
    assert isinstance(logo, j.Download)
    assert isinstance(logo.name, str)
    assert isinstance(logo.type, str)
    assert isinstance(logo.data, bytes)
    assert logo.name == "jutge.png"
    assert logo.type == "image/png"
    # PNG files start with an 8-byte signature: 89 50 4E 47 0D 0A 1A 0A
    signature = [0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]
    assert logo.data[:8] == bytes(signature), "The logo has not a PNG signature"
