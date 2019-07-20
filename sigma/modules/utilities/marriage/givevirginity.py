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

from sigma.core.utilities.dialogue_controls import bool_dialogue
from sigma.core.utilities.generic_responses import error


class UserVirginity(object):
    __slots__ = ('raw', 'empty', 'user_id', 'first', 'virgin', 'virginities')

    def __init__(self, raw):
        self.raw = {} if raw is None else raw
        self.empty = raw is None
        self.user_id = self.raw.get('user_id')
        self.first = self.raw.get('first')
        self.virgin = self.raw.get('virgin') or True
        self.virginities = self.raw.get('virginities') or []

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'first': self.first,
            'virgin': self.virgin,
            'virginities': self.virginities
        }

    async def save(self, db):
        """
        :param db: The database instance.
        :type db: sigma.core.mechanics.database.Database
        :return:
        :rtype:
        """
        data = self.to_dict()
        if self.empty:
            await db[db.db_nam].Virginity.insert_one(data)
        else:
            await db[db.db_nam].Virginity.update_one({'user_id': self.user_id}, {'$set': data})


async def givevirginity(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.mentions:
        target = pld.msg.mentions[0]
        av = UserVirginity(await cmd.db[cmd.db.db_name].Virginity.find_one({'user_id': pld.msg.author.id}))
        if av.empty:
            av.user_id = pld.msg.author.id
        if av.virgin:
            tv = UserVirginity(await cmd.db[cmd.db.db_name].Virginity.find_one({'user_id': target.id}))
            if tv.empty:
                tv.user_id = target.id
            question = f'Do you accept {pld.msg.author.name}\'s virginity?'
            if tv.virgin:
                question = f'Do you accept {pld.msg.author.name}\'s virginity in exchange for your own?'
            question = discord.Embed(color=0xF9F9F9, title=f'❔ {question}')
            success, timeout = await bool_dialogue(cmd.bot, pld.msg, question)
            if success:
                av.virgin = False
                av.first = target.id
                tv.virginities.append(pld.msg.author.id)
                congrats_title = f'🎉 Congrats, you are no longer a child! ... apparently.'
                if tv.virgin:
                    tv.virgin = False
                    tv.first = pld.msg.author.id
                    av.virginities.append(target.id)
                    congrats_title = f'🎉 Congrats, you are no longer children! ... apparently.'
                await av.save(cmd.db)
                await tv.save(cmd.db)
                response = discord.Embed(color=0x66CC66, title=congrats_title)
            else:
                if timeout:
                    response = discord.Embed(color=0x696969, title=f'🕙 {target.name} didn\'t respond.')
                else:
                    response = discord.Embed(color=0xBE1931, title=f'❌ {target.name} rejected you.')
        else:
            response = error('You are not a virgin.')
    else:
        response = error('No user mentioned.')
    await pld.msg.channel.send(embed=response)
