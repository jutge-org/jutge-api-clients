import jutge_api_client as j


def test_get_languages():
    jutge = j.JutgeApiClient()
    languages = jutge.tables.get_languages()
    assert isinstance(languages, dict)
    for language_id, language in languages.items():
        assert isinstance(language_id, str)
        assert isinstance(language.language_id, str)
        assert isinstance(language.own_name, str)
        assert isinstance(language.eng_name, str)
        assert language_id == language.language_id


def test_get_all():
    jutge = j.JutgeApiClient()
    tables = jutge.tables.get()
    assert isinstance(tables, j.AllTables)
    assert isinstance(tables.languages, dict)
    assert isinstance(tables.languages["ca"], j.Language)
    assert isinstance(tables.languages["ca"].language_id, str)
    assert isinstance(tables.languages["ca"].own_name, str)
    assert isinstance(tables.languages["ca"].eng_name, str)
    assert isinstance(tables.compilers, dict)
    assert isinstance(tables.compilers["Python3"], j.Compiler)
