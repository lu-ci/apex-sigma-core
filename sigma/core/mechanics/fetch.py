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

import discord

FETCH_HELPER_CACHE = None


def get_fetch_helper(bot):
    """
    Gets a static fetch helper instance.
    :type bot: sigma.core.sigma.ApexSigma
    :rtype: FetchHelper
    """
    global FETCH_HELPER_CACHE
    if not FETCH_HELPER_CACHE:
        FETCH_HELPER_CACHE = FetchHelper(bot)
    return FETCH_HELPER_CACHE


class SaveResponse(enumerate):
    skipped = 0
    updated = 1
    inserted = 2

    @staticmethod
    def describe(responses, variant):
        """
        Describes a list of save responses.
        :type responses:  list
        :type variant: str
        :rtype: str
        """
        skp_count = upd_count = ins_count = 0
        for response in responses:
            if response == SaveResponse.skipped:
                skp_count += 1
            elif response == SaveResponse.updated:
                upd_count += 1
            elif response == SaveResponse.inserted:
                ins_count += 1
        return f'Inserted {ins_count}, updated {upd_count}, and skipped {skp_count} {variant}s.'


class FetchHelper(object):
    __slots__ = ('bot', 'state', 'cache')

    def __init__(self, bot):
        """
        Helps fetch functions by caching some results.
        :type bot: sigma.core.sigma.ApexSigma
        """
        self.bot = bot
        # noinspection PyProtectedMember
        self.state = self.bot._connection
        self.cache = self.bot.cache

    async def get_object_doc(self, variant, oid):
        """
        Grabs an object from the database or cache instance.
        :type variant: str
        :type oid: int
        :rtype: None or dict
        """
        cache_key = f'document_{variant}_{oid}'
        data = await self.cache.get_cache(cache_key)
        return data

    async def save_object_doc(self, variant, data):
        """
        Checks if an object with the given ID exists in the object storage.
        :type variant: str
        :type data: dict
        :rtype: int
        """
        oid = data["id"]
        cache_key = f'document_{variant}_{oid}'
        doc = await self.get_object_doc(variant, oid)
        if doc:
            if '_id' in doc:
                del doc['_id']
            response = SaveResponse.updated
        else:
            response = SaveResponse.inserted
        if doc != data:
            await self.cache.set_cache(cache_key, data)
        else:
            response = SaveResponse.skipped
        return response

    async def fetch_user(self, uid):
        """
        Fetches and caches a user.
        :type uid: int
        :rtype: None or discord.User
        """
        result = None
        data = await self.get_object_doc('user', uid)
        if data:
            result = discord.User(state=self.state, data=data)
        return result

    async def fetch_channel(self, cid):
        """
        Fetches and caches a user.
        :type cid: int
        :rtype: None or discord.TextChannel
        """
        result = None
        data = await self.get_object_doc('channel', cid)
        if data:
            gdat = await self.get_object_doc('guild', data['guild_id'])
            if gdat:
                gdat = await self.fetch_guild(gdat['id'])
                if gdat:
                    result = discord.TextChannel(state=self.state, guild=gdat, data=data)
        return result

    async def fetch_guild(self, gid):
        """
        Fetches and caches a user.
        :type gid: int
        :rtype: None or discord.Guild
        """
        result = None
        data = await self.get_object_doc('guild', gid)
        if data:
            result = discord.Guild(state=self.state, data=data)
        return result

    @staticmethod
    def enum_to_val(enm):
        """
        Converts an enumerable to an integer.
        :rtype: int
        """
        return enm.value if 'value' in dir(enm) else enm

    @staticmethod
    def make_user_data(usr):
        """
        Makes a data dict for storage for a user.
        :type usr: discord.Member or discord.User
        :rtype: dict
        """
        data = {
            "username": usr.name,
            "discriminator": usr.discriminator,
            "id": str(usr.id),
            "avatar": usr.avatar,
            "bot": usr.bot
        }
        return data

    @staticmethod
    def make_channel_data(chn):
        """
        Makes a data dict for storage for a channel.
        :type chn: discord.TextChannel
        :rtype: dict
        """
        data = {
            "guild_id": str(chn.guild.id),
            "name": chn.name,
            "last_pin_timestamp": "2019-07-08T19:12:37.790000+00:00",  # Warning: Unimportant dummy data.
            "parent_id": str(chn.category_id) if chn.category_id else None,
            "nsfw": chn.is_nsfw(),
            "type": FetchHelper.enum_to_val(chn.type),
            "id": str(chn.id)
        }
        return data

    @staticmethod
    def make_role_data(rol):
        """
        Makes a data dict for storage for a role.
        :type rol: discord.Role
        :rtype: dict
        """
        data = {
            "hoist": rol.hoist,
            "name": rol.name,
            "mentionable": rol.mentionable,
            "color": rol.color.value,
            "position": rol.position,
            "id": str(rol.id),
            "managed": rol.managed,
            "permissions": rol.permissions.value
        }
        return data

    @staticmethod
    def make_emoji_data(emoji):
        """
        Makes a data dict for storage for a custom emoji.
        :type emj: discord.Emoji
        :rtype: dict
        """
        data = {
            "available": emoji.available,
            "managed": emoji.managed,
            "name": emoji.name,
            "roles": [FetchHelper.make_role_data(role) for role in emoji.roles],
            "require_colons": emoji.require_colons,
            "animated": emoji.animated,
            "id": str(emoji.id)
        }
        return data

    @staticmethod
    def make_guild_data(gld):
        """
        Makes a data dict for storage for a guild.
        :type gld: discord.Guild
        :rtype: dict
        """
        data = {
            "mfa_level": gld.mfa_level,
            "application_id": None,
            "description": gld.description,
            "icon": gld.icon,
            "afk_timeout": gld.afk_timeout,
            "system_channel_id": str(gld.system_channel.id) if gld.system_channel else None,
            "widget_enabled": 0,  # Warning: UNUSED. Treating as if always zero.
            "afk_channel_id": str(gld.afk_channel.id) if gld.afk_channel else None,
            "premium_subscription_count": gld.premium_subscription_count,
            "max_presences": gld.max_presences,
            "id": str(gld.id),
            "features": gld.features,
            "preferred_locale": "en-US",
            "name": gld.name,
            "roles": [FetchHelper.make_role_data(role) for role in gld.roles],
            "widget_channel_id": None,  # Warning: UNUSED. Treating as if always disabled.
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
