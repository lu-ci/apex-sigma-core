# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2018  Lucia's Cipher
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import arrow
import discord
from humanfriendly.tables import format_pretty_table as boop

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.utilities.data_processing import paginate, user_avatar


async def spouses(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.mentions:
        target = message.mentions[0]
    else:
        target = message.author
    profile = await cmd.db[cmd.db.db_nam].Profiles.find_one({'user_id': target.id}) or {}
    splist = profile.get('spouses', [])
    spcount = len(splist)
    page = args[0] if args else 1
    splist, page = paginate(splist, page, 5)
    starter = 'You are' if target.id == message.author.id else f'{target.name} is'
    mid = 'have' if target.id == message.author.id else 'has'
    if splist:
        spdata = []
        all_members = cmd.bot.get_all_members()
        for sp in splist:
            spmemb = discord.utils.find(lambda m: m.id == sp.get('user_id'), all_members)
            spmemb = spmemb.name if spmemb else sp.get('user_id')
            sp_profile = await cmd.db[cmd.db.db_nam].Profiles.find_one({'user_id': sp.get('user_id')}) or {}
            sp_spouses = sp_profile.get('spouses') or []
            sp_spouse_ids = [s.get('user_id') for s in sp_spouses]
            sp_status = 'Married' if target.id in sp_spouse_ids else 'Proposed'
            spdata.append([spmemb, sp_status, arrow.get(sp.get('time')).humanize().title()])
        spbody = boop(spdata, ['Name', 'Status', 'Since'])
        upgrades = await cmd.db.get_profile(target.id, 'upgrades') or {}
        limit = 10 + (upgrades.get('harem') or 0)
        stats = f'[Page {page}] {target.name}\'s harem has {spcount}/{limit} people in it.'
        response = discord.Embed(color=0xf9f9f9)
        response.set_author(name=f'{starter} married to...', icon_url=user_avatar(target))
        response.add_field(name='Stats', value=stats, inline=False)
        response.add_field(name='Spouse List', value=f'```hs\n{spbody}\n```')
    else:
        if page == 1:
            response = discord.Embed(color=0xe75a70, title=f'💔 {starter} not married, nor {mid} proposed, to anyone.')
        else:
            response = discord.Embed(color=0xe75a70, title=f'💔 {starter.split()[0]} {mid} nobody on page {page}.')
    await message.channel.send(embed=response)
