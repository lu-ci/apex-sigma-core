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

from sigma.core.mechanics.command import SigmaCommand


async def send_divorce(author: discord.Member, target: discord.Member, is_divorce):
    if is_divorce:
        splitup = discord.Embed(color=0xe75a70, title=f'💔 {author.name} has divorced you...')
    else:
        splitup = discord.Embed(color=0xe75a70, title=f'💔 {author.name} has canceled their proposal...')
    try:
        await target.send(embed=splitup)
    except discord.Forbidden:
        pass


async def divorce(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.mentions:
        target = message.mentions[0]
        if target.id != message.author.id:
            author_lookup = {'UserID': message.author.id}
            target_lookup = {'UserID': target.id}
            author_profile = await cmd.db[cmd.db.db_cfg.database].Profiles.find_one(author_lookup) or {}
            target_profile = await cmd.db[cmd.db.db_cfg.database].Profiles.find_one(target_lookup) or {}
            a_spouses = author_profile.get('Spouses') or []
            a_spouse_ids = [s.get('UserID') for s in a_spouses]
            t_spouses = target_profile.get('Spouses') or []
            t_spouse_ids = [s.get('UserID') for s in t_spouses]
            if message.author.id in t_spouse_ids and target.id in a_spouse_ids:
                current_kud = await cmd.db.get_currency(message.author, message.guild)
                current_kud = current_kud.get('current') or 0
                marry_stamp = discord.utils.find(lambda s: s.get('UserID') == target.id, a_spouses).get('Time')
                time_diff = arrow.utcnow().timestamp - marry_stamp
                div_cost = time_diff // 6
                if current_kud >= div_cost:
                    for sp in a_spouses:
                        if sp.get('UserID') == target.id:
                            a_spouses.remove(sp)
                    for sp in t_spouses:
                        if sp.get('UserID') == target.id:
                            t_spouses.remove(sp)
                    a_up_data = {'$set': {'Spouses': a_spouses}}
                    t_up_data = {'$set': {'Spouses': t_spouses}}
                    await cmd.db[cmd.db.db_cfg.database].Profiles.update_one(author_lookup, a_up_data)
                    await cmd.db[cmd.db.db_cfg.database].Profiles.update_one(target_lookup, t_up_data)
                    response = discord.Embed(color=0xe75a70, title=f'💔 You have divorced {target.name}...')
                    await send_divorce(message.author, target, True)
                    await cmd.db.rmv_currency(message.author, div_cost)
                else:
                    currency = cmd.bot.cfg.pref.currency
                    no_kud = f'❗ You don\'t have {div_cost} {currency} to get a divorce.'
                    response = discord.Embed(color=0xBE1931, title=no_kud)
            elif target.id in a_spouse_ids:
                for sp in a_spouses:
                    if sp.get('UserID') == target.id:
                        a_spouses.remove(sp)
                a_up_data = {'$set': {'Spouses': a_spouses}}
                await cmd.db[cmd.db.db_cfg.database].Profiles.update_one(author_lookup, a_up_data)
                response = discord.Embed(color=0xe75a70, title=f'💔 You have canceled the proposal to {target.name}...')
                await send_divorce(message.author, target, False)
            else:
                not_married = f'❗ You aren\'t married, nor have proposed, to {target.name}.'
                response = discord.Embed(color=0xBE1931, title=not_married)
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Can\'t divorce yourself.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ No user targeted.')
    await message.channel.send(embed=response)
