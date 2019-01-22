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

import discord
from cryptography.fernet import InvalidSignature, InvalidToken

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import error
from sigma.modules.utilities.mathematics.nodes.encryption import get_encryptor


async def encrypt(cmd: SigmaCommand, pld: CommandPayload):
    text = False
    cipher = get_encryptor(cmd.bot.cfg)
    if cipher:
        if pld.args:
            if pld.args[-1] == ':t':
                text = True
                crypt_text = ' '.join(pld.args[:-1]).encode('utf-8')
            else:
                crypt_text = ' '.join(pld.args).encode('utf-8')
            try:
                ciphered = cipher.encrypt(crypt_text).decode('utf-8')
            except InvalidToken:
                ciphered = None
            except InvalidSignature:
                ciphered = None
            if ciphered:
                if text:
                    response = ciphered
                else:
                    response = discord.Embed(color=0xe75a70)
                    response.add_field(name='💟 Text Encrypted', value=ciphered)
            else:
                response = error('The token or key are incorrect.')
        else:
            response = error('Nothing to decrypt.')
    else:
        response = error('You don\'t posses a key.')
    if text:
        await pld.msg.channel.send(response)
    else:
        await pld.msg.channel.send(embed=response)
