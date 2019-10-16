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
from sigma.core.mechanics.caching import MemoryCacher
from sigma.core.mechanics.config import CacheConfig

FETCH_HELPER_CACHE = None


def get_fetch_helper(bot):
    """
    Gets a static fetch helper instance.
    :param bot: The main client instance.
    :type bot: sigma.core.sigma.ApexSigma
    :return:
    :rtype: FetchHelper
    """
    global FETCH_HELPER_CACHE
    if not FETCH_HELPER_CACHE:
        FETCH_HELPER_CACHE = FetchHelper(bot)
    return FETCH_HELPER_CACHE


class FetchHelper(object):
    __slots__ = ('bot', 'db', 'cache')

    def __init__(self, bot):
        """
        Helps fetch functions by caching some results.
        :param bot: The bot instance.
        :type bot: sigma.core.sigma.ApexSigma
        """
        self.bot = bot
        self.db = self.bot.db
        self.cache = MemoryCacher(CacheConfig({}))

    async def get_object_doc(self, variant, oid):
        """
        Grabs an object from the database or cache instance.
        :param variant: The type of object to grab.
        :type variant: str
        :param oid: The ID of the object.
        :type oid: int
        :return: None or dict
        """
        coll = self.db[self.db.db_nam][f'{variant.title()}Objects']

    async def fetch_user(self, uid):
        """
        Fetches and caches a user.
        :param uid: The user ID.
        :type uid: int
        :return:
        :rtype: None or discord.User
        """
        return None

    async def fetch_channel(self, cid):
        """
        Fetches and caches a user.
        :param cid: The channel ID.
        :type cid: int
        :return:
        :rtype: None or discord.TextChannel
        """
        return None

    async def fetch_guild(self, gid):
        """
        Fetches and caches a user.
        :param gid: The guild ID.
        :type gid: int
        :return:
        :rtype: None or discord.Guild
        """
        return None

    @staticmethod
    def make_role_data(rol):
        """
        Makes a data dict for storage for a role.
        :param rol: The role to store.
        :type rol: discord.Role
        :return: dict
        """
        data = {
            "hoist": rol.hoist,
            "name": rol.name,
            "mentionable": rol.mentionable,
            "color": rol.color,
            "position": rol.position,
            "id": str(rol.id),
            "managed": rol.managed,
            "permissions": rol.permissions.value
        }
        return data

    @staticmethod
    def make_emoji_data(emj):
        """
        Makes a data dict for storage for a custom emoji.
        :param emj: The emoji to store.
        :type emj: discord.Emoji
        :return:
        """
        data = {
            "available": emj.available,
            "managed": emj.managed,
            "name": emj.name,
            "roles": [FetchHelper.make_role_data(role) for role in emj.roles],
            "require_colons": emj.require_colons,
            "animated": emj.animated,
            "id": str(emj.id)
        }
        return data

    @staticmethod
    def make_guild_data(gld):
        """
        Makes a data dict for storage for a guild.
        :param gld: The guild to store.
        :type gld: discord.Guild
        :return: dict
        """
        data = {
            "mfa_level": gld.mfa_level,
            "application_id": None,
            "description": gld.description,
            "icon": gld.icon,
            "afk_timeout": gld.afk_timeout,
            "system_channel_id": str(gld.system_channel.id) if gld.system_channel else None,
            "default_message_notifications": gld.default_notifications,  # TODO: Fix enum storage.
            "widget_enabled": 0,  # Warning: UNUSED. Treating as if always zero.
            "afk_channel_id": str(gld.afk_channel.id) if gld.afk_channel else None,
            "premium_subscription_count": gld.premium_subscription_count,
            "explicit_content_filter": gld.explicit_content_filter,  # TODO: Fix enum storage.
            "max_presences": gld.max_presences,
            "id": str(gld.id),
            "features": gld.features,
            "preferred_locale": "en-US",
            "verification_level": gld.verification_level,  # TODO: Fix enum storage.
            "name": gld.name,
            "roles": [FetchHelper.make_role_data(role) for role in gld.roles],
            "widget_channel_id": None,  # Warning: UNUSED. Treating as if always disabled.
            "region": gld.region,  # TODO: Fix enum storage.
            "embed_channel_id": None,  # Warning: UNUSED. Treating as if always None.
            "system_channel_flags": gld.system_channel_flags.value,
            "banner": gld.banner,
            "premium_tier": gld.premium_tier,
            "splash": gld.splash,
            "max_members": gld.max_members,
            "emojis": [FetchHelper.make_emoji_data(emoji) for emoji in gld.emojis],
            "embed_enabled": False,  # Warning: UNUSED. Treating as if always False.
            "vanity_url_code": None,  # Warning: Async function that makes an API call. Not worth awaiting.
            "owner_id": str(gld.owner_id)
        }
        return data
