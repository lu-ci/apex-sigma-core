# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
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

from .auto_responder import clean_word


async def auto_reactor(ev, message):
    if message.guild:
        if message.content:
            pfx = await ev.db.get_prefix(message)
            if not message.content.startswith(pfx):
                triggers = await ev.db.get_guild_settings(message.guild.id, 'ReactorTriggers') or {}
                arguments = message.content.split(' ')
                for arg in arguments:
                    arg = clean_word(arg)
                    if arg in triggers:
                        reaction = triggers[arg]
                        try:
                            await message.add_reaction(reaction)
                        except Exception:
                            pass
                        break
