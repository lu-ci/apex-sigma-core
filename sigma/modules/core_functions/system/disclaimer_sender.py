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

from sigma.core.mechanics.event import SigmaEvent

disclaimer = """
```md
# Sigma Info

## Help

* Sigma's help command is ">>help" by default.
* For any additional help or information you can hop on the official server and ask.
* Sigma is an open source project, if you have any concerns about how what functions you can check it out.

## Apex Sigma Usage Rules

You are NOT allowed to:
* Use Sigma to damage communities or users.
* Actively attempt to overload or damage the bot's functionality.
* Automate or bot any and all commands in any way. This includes, but is not limited to botting and using macros.

## Disclaimer
* By using Sigma you comply with various user data being stored.
* Only data needed for the functionality of a command is stored.

> Not complying will result in the user or guild being blacklisted.
```
"""


async def disclaimer_sender(_ev: SigmaEvent, guild: discord.Guild):
    try:
        await guild.owner.send(disclaimer)
    except discord.Forbidden:
        if guild.system_channel:
            try:
                await guild.system_channel.send(disclaimer)
            except discord.Forbidden:
                pass
