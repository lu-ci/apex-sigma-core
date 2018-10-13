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


async def send_proposal(author: discord.Member, target: discord.Member, is_proposal):
    if is_proposal:
        proposal = discord.Embed(color=0xf9f9f9, title=f'💍 {author.name} has proposed to you!')
    else:
        proposal = discord.Embed(color=0xf9f9f9, title=f'💍 {author.name} has accepted your proposal!')
    try:
        await target.send(embed=proposal)
    except discord.Forbidden:
        pass


async def marry(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.mentions:
        target = message.mentions[0]
        author = message.author
        if target.id != author.id:
            if not target.bot:
                author_upgrades = await cmd.db.get_profile(author.id, 'upgrades') or {}
                target_upgrades = await cmd.db.get_profile(target.id, 'upgrades') or {}
                author_limit = 10 + (author_upgrades.get('harem') or 0)
                target_limit = 10 + (target_upgrades.get('harem') or 0)
                a_spouses = await cmd.db.get_profile(message.author.id, 'spouses') or []
                a_spouse_ids = [s.get('user_id') for s in a_spouses]
                t_spouses = await cmd.db.get_profile(target.id, 'spouses') or []
                t_spouse_ids = [s.get('user_id') for s in t_spouses]
                a_limited = True if len(a_spouses) >= author_limit else False
                t_limited = True if len(t_spouses) >= target_limit else False
                if not a_limited and not t_limited:
                    if target.id not in a_spouse_ids:
                        a_spouses.append({'user_id': target.id, 'time': arrow.utcnow().timestamp})
                        await cmd.db.set_profile(message.author.id, 'spouses', a_spouses)
                        if author.id not in t_spouse_ids:
                            response = discord.Embed(color=0xe75a70, title=f'💟 You proposed to {target.name}!')
                            await send_proposal(author, target, True)
                        else:
                            congrats_title = f'🎉 Congrats to {author.name} and {target.name}!'
                            response = discord.Embed(color=0x66cc66, title=congrats_title)
                            await send_proposal(author, target, False)
                    else:
                        if author.id in t_spouse_ids:
                            married_error = f'❗ You and {target.name} are already married.'
                            response = discord.Embed(color=0xBE1931, title=married_error)
                        else:
                            response = discord.Embed(color=0xBE1931, title=f'❗ You already proposed to {target.name}.')
                else:
                    limited = author if a_limited else target
                    response = discord.Embed(color=0xe75a70, title=f'💔 {limited.name} has too many spouses.')
            else:
                response = discord.Embed(color=0xe75a70, title='💔 Machines aren\'t that advanced yet.')
        else:
            response = discord.Embed(color=0xe75a70, title='💔 You love yourself too much.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ No user targeted.')
    await message.channel.send(embed=response)
