"""
Apex Sigma: The Database Giant Discord Bot.
Copyright (C) 2019  Lucia's Cipher

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from sigma.core.mechanics.config import DatabaseConfig, DiscordConfig, PreferencesConfig, CacheConfig


class TestConfiguration(object):

    @staticmethod
    def test_dsc_default():
        dsc = DiscordConfig({})
        assert dsc.raw == {}
        assert dsc.token is None
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
        assert pref.website == 'https://luciascipher.com/sigma'
        assert pref.text_only is False
        assert pref.music_only is False
        assert pref.movelog_channel is None
        assert pref.errorlog_channel is None

    @staticmethod
    def test_cache_default():
        cache = CacheConfig({})
        assert cache.raw == {}
        assert cache.type is None
        assert cache.time == 300
        assert cache.size == 1000000
        assert cache.host == '127.0.0.1'
        assert cache.port == 6379
