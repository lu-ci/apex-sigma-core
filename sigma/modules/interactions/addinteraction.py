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


async def addinteraction(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        if len(args) >= 2:
            reaction_name = args[0]
            allowed_reactions = []
            for command in cmd.bot.modules.commands:
                if cmd.bot.modules.commands[command].category.lower() == 'interactions':
                    allowed_reactions.append(command)
            if reaction_name.lower() in allowed_reactions:
                reaction_url = '%20'.join(args[1:])
                if reaction_url.startswith('http'):
                    if reaction_url.endswith('.gif'):
                        exist_check = await cmd.db[cmd.db.db_nam]['Interactions'].find_one({'URL': reaction_url})
                        if not exist_check:
                            reaction_id = secrets.token_hex(4)
                            lookup = {'Name': reaction_name.lower()}
                            inter_count = await cmd.db[cmd.db.db_nam]['Interactions'].count_documents(lookup) + 1
                            title = f'✅ Added **{reaction_name.lower()}** number **{inter_count}**.'
                            response = discord.Embed(color=0x77B255, title=title)
                            log_msg = None
                            if 'log_ch' in cmd.cfg:
                                log_ch_id = cmd.cfg['log_ch']
                                log_ch = discord.utils.find(lambda x: x.id == log_ch_id, cmd.bot.get_all_channels())
                                if log_ch:
                                    author = f'{message.author.name}#{message.author.discriminator}'
                                    data_desc = f'Author: {author}'
                                    data_desc += f'\nAuthor ID: {message.author.id}'
                                    data_desc += f'\nGuild: {message.guild.name}'
                                    data_desc += f'\nGuild ID: {message.guild.id}'
                                    data_desc += f'\nReaction URL: [Here]({reaction_url})'
                                    data_desc += f'\nReaction ID: {reaction_id}'
                                    log_resp_title = f'🆙 Added {reaction_name.lower()} number {inter_count}'
                                    log_resp = discord.Embed(color=0x3B88C3)
                                    log_resp.add_field(name=log_resp_title, value=data_desc)
                                    log_resp.set_thumbnail(url=reaction_url)
                                    log_msg = await log_ch.send(embed=log_resp)
                            reaction_data = {
                                'Name': reaction_name.lower(),
                                'user_id': message.author.id,
                                'server_id': message.guild.id,
                                'URL': reaction_url,
                                'ReactionID': reaction_id,
                                'MessageID': log_msg.id if log_msg else None
                            }
                            await cmd.db[cmd.db.db_nam]['Interactions'].insert_one(reaction_data)
                        else:
                            response = discord.Embed(color=0xBE1931, title=f'❗ Reaction already exists.')
                    else:
                        response = discord.Embed(color=0xBE1931, title=f'❗ Reaction URL must end with .gif.')
                else:
                    response = discord.Embed(color=0xBE1931, title=f'❗ Invalid URL.')
            else:
                response = discord.Embed(color=0xBE1931, title=f'❗ No such interaction was found.')
        else:
            response = discord.Embed(color=0xBE1931, title=f'❗ Not enough arguments.')
    else:
        response = discord.Embed(color=0xBE1931, title=f'❗ Nothing inputted.')
    await message.channel.send(embed=response)
