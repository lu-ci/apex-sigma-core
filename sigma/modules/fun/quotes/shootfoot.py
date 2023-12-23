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

from sigma.core.utilities.generic_responses import GenericResponse


async def get_all_sf(db):
    """
    :type db: sigma.core.mechanics.database.Database
    :rtype: list
    """
    joke_docs = await db.cache.get_cache('shoot_foot_docs')
    if joke_docs is None:
        joke_docs = await db.col.ShootFootData.find().to_list(None)
        await db.cache.set_cache('shoot_foot_docs', joke_docs)
    return joke_docs


async def shootfoot(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    lang = ' '.join(pld.args).lower() if pld.args else None
    if lang:
        joke_doc = await cmd.db.col.ShootFootData.find_one({'lang_low': lang})
        if not joke_doc:
            joke_docs = await get_all_sf(cmd.db)
            for joke_doc_item in joke_docs:
                alts = joke_doc_item.get('alts') or []
                if lang in alts:
                    joke_doc = joke_doc_item
                    break
    else:
        all_docs = await get_all_sf(cmd.db)
        joke_doc = secrets.choice(all_docs)
    if joke_doc:
        joke = secrets.choice(joke_doc.get('methods'))
        foot_lang = joke_doc.get('lang')
        response = discord.Embed(color=0xbf6952, title=f'🔫 How to shoot yourself in the foot with {foot_lang}...')
        response.description = joke
    else:
        response = GenericResponse(f'I don\'t know how to do it in {lang}.').not_found()
    await pld.msg.channel.send(embed=response)
