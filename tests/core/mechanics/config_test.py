from sigma.core.mechanics.config import DiscordConfig, DatabaseConfig, PreferencesConfig


class TestConfiguration(object):

    @staticmethod
    def test_dsc_default():
        dsc = DiscordConfig({})
        assert dsc.raw == {}
        assert dsc.token == 'You got no token, son!'
        assert dsc.owners == [137951917644054529]
        assert dsc.bot is True

    @staticmethod
    def test_db_default():
        db = DatabaseConfig({})
        assert db.raw == {}
        assert db.database == 'sigma'
        assert db.auth is False
        assert db.host == '127.0.0.1'
        assert db.port == 27017
        assert db.username == 'user'
        assert db.password == 'pass'

    @staticmethod
    def test_pref_default():
        pref = PreferencesConfig({})
        assert pref.raw == {}
        assert pref.dev_mode is False
        assert pref.status_rotation is True
        assert pref.prefix == '>>'
        assert pref.currency == 'Kud'
        assert pref.currency_icon == '⚜'
        assert pref.website == 'https://lucia.moe/sigma'
        assert pref.text_only is False
        assert pref.music_only is False
        assert pref.movelog_channel is None
        assert pref.errorlog_channel is None
