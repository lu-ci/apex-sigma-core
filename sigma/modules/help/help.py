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

from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.generic_responses import GenericResponse

LUCIA_IMAGE = 'https://i.imgur.com/KVgdtNg.png'
SIGMA_TITLE = 'Apex Sigma: The Database Giant'
PATREON_URL = 'https://www.patreon.com/luciascipher'
PAYPAL_URL = 'https://www.paypal.me/AleksaRadovic'
SUPPORT_URL = 'https://discordapp.com/invite/aEUCHwX'


# noinspection PyShadowingBuiltins
async def help(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        cmd_name = ''.join(pld.args).lower()
        if cmd_name in cmd.bot.modules.alts:
            cmd_name = cmd.bot.modules.alts[cmd_name]
        if cmd_name in cmd.bot.modules.commands:
            pfx = cmd.db.get_prefix(pld.settings)
            command = cmd.bot.modules.commands[cmd_name]
            usage = command.usage.replace('{pfx}', pfx).replace('{cmd}', command.name)
            title = f'📄 [{command.category.upper()}] {command.name.upper()} Usage and Information'
            response = discord.Embed(color=0x1B6F5F, title=title)
            response.add_field(name='Usage Example', value=f'`{usage}`', inline=False)
            response.add_field(name='Command Description', value=f'```\n{command.desc}\n```', inline=False)
            if command.alts:
                response.add_field(name='Command Aliases', value=f'```\n{", ".join(command.alts)}\n```')
        else:
            response = GenericResponse('Command not found.').not_found()
    else:
        response = discord.Embed(color=0x1B6F5F)
        response.set_author(name=SIGMA_TITLE, icon_url=user_avatar(cmd.bot.user), url=cmd.bot.cfg.pref.website)
        invite_url = f'https://discordapp.com/oauth2/authorize?client_id={cmd.bot.user.id}&scope=bot&permissions=8'
        support_text = f'**Add Me**: [Link]({invite_url})'
        support_text += f' | **Commands**: [Link]({cmd.bot.cfg.pref.website}/commands)'
        support_text += f' | **Support**: [Link]({SUPPORT_URL})'
        support_text += f'\nWanna help? **Patreon**: [Link]({PATREON_URL}) | **PayPal**: [Link]({PAYPAL_URL})'
        response.add_field(name='Help', value=support_text)
        response.set_thumbnail(url=user_avatar(cmd.bot.user))
        response.set_footer(text='© by Lucia\'s Cipher. Released under the GPLv3 license.', icon_url=LUCIA_IMAGE)
    await pld.msg.channel.send(embed=response)
