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
import secrets

import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.utilities.data_processing import user_avatar


def make_sugg_embed(msg: discord.Message, args: list, token: str):
    sugg_embed = discord.Embed(color=msg.author.color, timestamp=msg.created_at)
    sugg_embed.description = " ".join(args)
    author_name = f'{msg.author.name} [{msg.author.id}]'
    footer_content = f'[{token}] From {msg.guild.name}.'
    sugg_embed.set_author(name=author_name, icon_url=user_avatar(msg.author))
    sugg_embed.set_footer(icon_url=msg.guild.icon_url, text=footer_content)
    return sugg_embed


def make_sugg_data(msg: discord.Message, args: list, token: str):
    return {
        'suggestion': {'id': token, 'text': ' '.join(args)},
        'user': {'id': msg.author.id, 'name': msg.author.name},
        'guild': {'id': msg.guild.id, 'name': msg.guild.name},
        'timestamp': msg.created_at.timestamp()
    }


async def suggest(cmd: SigmaCommand, message: discord.Message, args: list):
    sugg_chn_id = cmd.cfg.get('channel')
    if sugg_chn_id:
        sugg_chn = discord.utils.find(lambda x: x.id == sugg_chn_id, cmd.bot.get_all_channels())
        if sugg_chn:
            if args:
                sugg_token = secrets.token_hex(4)
                sugg_msg = await sugg_chn.send(embed=make_sugg_embed(message, args, sugg_token))
                [await sugg_msg.add_reaction(r) for r in ['⬆', '⬇']]
                await cmd.db[cmd.db.db_nam].Suggestions.insert_one(make_sugg_data(message, args, sugg_token))
                response = discord.Embed(color=0x77B255, title=f'✅ Suggestion {sugg_token} submitted.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Cannot find suggestion channel.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Missing suggestion channel configuration.')
    await message.channel.send(embed=response)
