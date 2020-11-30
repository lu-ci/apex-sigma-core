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

> In a nutshell: Don't be an asshole.
> Breaking these might get you blacklisted.

## Disclaimer

> We're required to state our privacy and security policy.
> In short, it's the following.

* No personal data is ever seen, let alone stored.
* Only data needed for functionality is stored, nothing more.
* Nobody other than the staff maintaining the bot will have access to any data.
* We pledge to never share any details of any kind with external persons or organizations.
* Not for legal, not for monetary, not for any reason, ever.
```
"""


async def disclaimer_sender(_ev, pld):
    """
    :param _ev: The main event instance referenced.
    :type _ev: sigma.core.mechanics.event.SigmaEvent
    :param pld: The event payload data to process.
    :type pld: sigma.core.mechanics.payload.GuildPayload
    """
    try:
        await pld.guild.owner.send(disclaimer)
    except (discord.Forbidden, discord.HTTPException):
        if pld.guild.system_channel:
            try:
                await pld.guild.system_channel.send(disclaimer)
            except discord.Forbidden:
                pass
