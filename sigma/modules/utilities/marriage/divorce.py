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
from sigma.core.mechanics.payload import CommandPayload


async def send_divorce(author: discord.Member, target: discord.Member, is_divorce):
    if is_divorce:
        splitup = discord.Embed(color=0xe75a70, title=f'💔 {author.name} has divorced you...')
    else:
        splitup = discord.Embed(color=0xe75a70, title=f'💔 {author.name} has canceled the proposal...')
    try:
        await target.send(embed=splitup)
    except discord.Forbidden:
        pass


async def divorce(cmd: SigmaCommand, pld: CommandPayload):
    message, args = pld.msg, pld.args
    target = None
    is_id = False
    tid = None
    if message.mentions:
        target = message.mentions[0]
        tid = target.id
    else:
        if args:
            try:
                target = tid = int(args[0])
                is_id = True
            except ValueError:
                target = None
    if tid:
        if tid != message.author.id:
            a_spouses = pld.profile.get('spouses') or []
            a_spouse_ids = [s.get('user_id') for s in a_spouses]
            if is_id:
                t_spouses = await cmd.db.get_profile(target, 'spouses') or []
            else:
                t_spouses = await cmd.db.get_profile(target.id, 'spouses') or []
            t_spouse_ids = [s.get('user_id') for s in t_spouses]
            if message.author.id in t_spouse_ids and tid in a_spouse_ids:
                current_kud = await cmd.db.get_resource(message.author.id, 'currency')
                current_kud = current_kud.current
                marry_stamp = discord.utils.find(lambda s: s.get('user_id') == tid, a_spouses).get('time')
                time_diff = arrow.utcnow().timestamp - marry_stamp
                div_cost = int(time_diff * 0.004)
                if current_kud >= div_cost:
                    for sp in a_spouses:
                        if is_id:
                            if sp.get('user_id') == target:
                                a_spouses.remove(sp)
                        else:
                            if sp.get('user_id') == target.id:
                                a_spouses.remove(sp)
                    for sp in t_spouses:
                        if sp.get('user_id') == message.author.id:
                            t_spouses.remove(sp)
                    await cmd.db.set_profile(message.author.id, 'spouses', a_spouses)
                    if is_id:
                        await cmd.db.set_profile(target, 'spouses', t_spouses)
                    else:
                        await cmd.db.set_profile(target.id, 'spouses', t_spouses)
                    if is_id:
                        div_title = f'💔 You have divorced {target}...'
                    else:
                        div_title = f'💔 You have divorced {target.name}...'
                    response = discord.Embed(color=0xe75a70, title=div_title)
                    if not is_id:
                        await send_divorce(message.author, target, True)
                    await cmd.db.del_resource(message.author.id, 'currency', div_cost, cmd.name, message)
                else:
                    currency = cmd.bot.cfg.pref.currency
                    no_kud = f'❗ You don\'t have {div_cost} {currency} to get a divorce.'
                    response = discord.Embed(color=0xBE1931, title=no_kud)
            elif tid in a_spouse_ids:
                for sp in a_spouses:
                    if sp.get('user_id') == tid:
                        a_spouses.remove(sp)
                await cmd.db.set_profile(message.author.id, 'spouses', a_spouses)
                if is_id:
                    canc_title = f'💔 You have canceled the proposal to {target}...'
                else:
                    canc_title = f'💔 You have canceled the proposal to {target.name}...'
                response = discord.Embed(color=0xe75a70, title=canc_title)
                if not is_id:
                    await send_divorce(message.author, target, False)
            elif message.author.id in t_spouse_ids:
                for sp in t_spouses:
                    if sp.get('user_id') == message.author.id:
                        t_spouses.remove(sp)
                if is_id:
                    await cmd.db.set_profile(target, 'spouses', t_spouses)
                else:
                    await cmd.db.set_profile(target.id, 'spouses', t_spouses)
                if is_id:
                    canc_title = f'💔 You have rejected {target}\'s proposal...'
                else:
                    canc_title = f'💔 You have rejected {target.name}\'s proposal...'
                response = discord.Embed(color=0xe75a70, title=canc_title)
                if not is_id:
                    await send_divorce(message.author, target, False)
            else:
                if is_id:
                    not_married = f'❗ You aren\'t married, nor have proposed, to {target}.'
                else:
                    not_married = f'❗ You aren\'t married, nor have proposed, to {target.name}.'
                response = discord.Embed(color=0xBE1931, title=not_married)
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Can\'t divorce yourself.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ No user targeted.')
    await message.channel.send(embed=response)
