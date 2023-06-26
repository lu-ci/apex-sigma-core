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
import arrow
import discord

HOME_GUILD_ID = 200751504175398912
HOURS_TO_APPEAR = [9, 23]
MIN_DELAY = 22 * 3600


def shown_today(pld):
    """
    :type pld: sigma.core.mechanics.payload.MessagePayload
    :rtype: bool
    """
    shown = False
    now = arrow.utcnow()
    last_stamp = pld.settings.get('donation_timestamp', 0)
    if now.float_timestamp - last_stamp < MIN_DELAY:
        shown = True
    return shown


async def should_show(db, pld):
    """
    :type db: sigma.core.mechanics.database.SigmaDatabase
    :type pld: sigma.core.mechanics.payload.MessagePayload
    :rtype: bool
    """
    # show = False
    # if not shown_today(pld):
    #     now = arrow.utcnow()
    #     if now.hour in HOURS_TO_APPEAR:
    #         show = True
    show = not shown_today(pld)
    if show:
        await db.set_guild_settings(pld.msg.guild.id, 'donation_timestamp', arrow.utcnow().float_timestamp)
    return show


async def donate_cta(ev, pld):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    :param pld: The event payload data to process.
    :type pld: sigma.core.mechanics.payload.MessagePayload
    """
    if not pld.msg.author.bot:
        if pld.msg.guild.id != HOME_GUILD_ID:
            if await should_show(ev.db, pld):
                title = 'I would like to ask for your financial support~'
                response = discord.Embed(color=0x1B6F5F, title=title)
                response.description = 'Hello dear user, Alex the creator of Sigma is in a bit of financial trouble.'
                response.description += ' If you could help him out, it would be greatly appreciated.'
                response.description += ' At the moment he pays for everything as the current donations don\'t cover'
                response.description += ' the costs of running the bot.'
                response.description += ' You can donate either via [Patreon](https://www.patreon.com/luciascipher)'
                response.description += ' or [PayPal](https://www.paypal.me/AleksaRadovic).'
                response.description += ' Thank you for your support! <3'
                response.set_footer(text='This message appears only once per day.')
                await pld.msg.channel.send(embed=response)
