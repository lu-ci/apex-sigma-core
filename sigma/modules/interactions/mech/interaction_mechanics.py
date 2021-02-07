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

import secrets

import discord


async def get_interaction_list(db, intername):
    """
    Gets all interaction for the given interaction type name.
    :param db: The main database handler reference.
    :type db: sigma.core.mechanics.database.Database
    :param intername: The name of the interaction type.
    :type intername: str
    :return:
    :rtype: list[dict]
    """
    return await db[db.db_nam].Interactions.find({'name': intername, 'active': True}).to_list(None)


async def grab_interaction(db, intername):
    """
    Gets a single interaction for the given interaction type name.
    :param db: The main database handler reference.
    :type db: sigma.core.mechanics.database.Database
    :param intername: The name of the interaction type.
    :type intername: str
    :return:
    :rtype: dict
    """
    cache_key = f'interaction_cache_{intername}'
    interaction_cache = await db.cache.get_cache(cache_key) or {}
    fill = False if interaction_cache else True
    if fill:
        interaction_cache = await get_interaction_list(db, intername)
        await db.cache.set_cache(cache_key, interaction_cache)
    if interaction_cache:
        choice = interaction_cache.pop(secrets.randbelow(len(interaction_cache)))
        await db.cache.set_cache(cache_key, interaction_cache)
    else:
        choice = {'url': 'https://i.imgur.com/m59E4nx.gif', 'user_id': None, 'server_id': None, 'interaction_id': None}
    return choice


def target_check(usr, lookup):
    """
    Checks a user if they are the possible lookup target.
    :param usr: The user to check.
    :type usr: discord.Member
    :param lookup: The lookup query.
    :type lookup: str
    :return:
    :rtype: bool
    """
    return usr.display_name.lower() == lookup.lower() or usr.name.lower() == lookup.lower()


# message.mentions are not always in the correct order
def get_mentions(message):
    """
    Grabs mentions from a message.
    :param message: The message object.
    :type message: discord.Message
    :return:
    :rtype: list[discord.Member]
    """
    return list(filter(lambda x: x, [message.guild.get_member(i) for i in message.raw_mentions]))


def get_target(sigma, message):
    """
    Gets the target of the interaction.
    :param sigma: The client's member object.
    :type sigma: discord.Member
    :param message: The message of the interaction cause.
    :type message: discord.Message
    :return:
    :rtype: discord.Member
    """
    mentions = get_mentions(message)
    if mentions:
        if mentions[0].id == sigma.id and len(mentions) >= 2:
            target = mentions[1]
        else:
            target = mentions[0]
    else:
        if message.content:
            lookup = ' '.join(message.content.split(' ')[1:])
            user = discord.utils.find(lambda x: target_check(x, lookup), message.guild.members)
            target = user if user else message.author
        else:
            target = message.author
    return target


def get_author(sigma, message):
    """
    Gets the author of the interaction.
    :param sigma: The client's member object.
    :type sigma: discord.Member
    :param message: The message of the interaction cause.
    :type message: discord.Message
    :return:
    :rtype: discord.Member
    """
    mentions = get_mentions(message)
    if len(mentions) >= 2:
        if mentions[0].id == sigma.id:
            author = sigma
        else:
            author = message.author
    else:
        author = message.author
    return author


async def update_data(db, data, user, guild):
    """
    Updates the static data of an interaction
    if the guild and member that submitted it are found.
    :param db: The main database handler reference.
    :type db: sigma.core.mechanics.database.Database
    :param data: The interaction data document.
    :type data: dict
    :param user: The user that submitted it.
    :type user: discord.Member or discord.User
    :param guild: The guild that submitted it.
    :type guild: discord.Guild
    """
    if user:
        unam = data.get('user_name')
        if unam is None or unam != user.name:
            await db[db.db_nam].Interactions.update_many(
                {'user_id': data.get('user_id')}, {'$set': {'user_name': user.name}}
            )
    if guild:
        snam = data.get('server_name')
        if snam is None or snam != guild.name:
            await db[db.db_nam].Interactions.update_many(
                {'server_id': data.get('server_id')}, {'$set': {'server_name': guild.name}}
            )


async def make_footer(cmd, item):
    """
    Generates the footer for the embed with submitter details.
    :param cmd: The main command instance and reference.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param item: The interaction document item.
    :type item: dict
    :return:
    :rtype: str
    """
    uid = item.get('user_id')
    user = await cmd.bot.get_user(uid)
    username_fallback = item.get('user_name') or 'Unknown User'
    username = user.name if user else username_fallback
    sid = item.get('server_id')
    srv = await cmd.bot.get_guild(sid)
    servername_fallback = item.get('server_name') or 'Unknown Server'
    servername = srv.name if srv else servername_fallback
    await update_data(cmd.db, item, user, srv)
    react_id = item.get('interaction_id')
    footer = f'[{react_id}] | Submitted by {username} from {servername}.'
    return footer
