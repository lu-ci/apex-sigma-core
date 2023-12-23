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

from sigma.core.mechanics.incident import get_incident_core
from sigma.core.utilities.event_logging import log_event


async def notify(pld, target, verb, action):
    """
    Notifies the offender of punishment via direct message.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    :type target: discord.Member
    :type verb: str
    :type action: str
    """
    guild_icon = str(pld.msg.guild.icon.url) if pld.msg.guild.icon else None
    to_target = discord.Embed(color=0x696969)
    to_target.add_field(name=f'🔨 You have been {action}.', value='Reason: Accruing too many warnings.')
    to_target.set_footer(text=f'{verb.title()}: {pld.msg.guild.name}.', icon_url=guild_icon)
    try:
        await target.send(embed=to_target)
    except (discord.Forbidden, discord.HTTPException):
        pass


async def make_incident(db, pld, trg, action):
    """
    Makes and reports an incident for an Auto-Punishment.
    :type db: sigma.core.mechanics.database.Database
    :type pld: sigma.core.mechanics.payload.CommandPayload
    :type trg: discord.Member
    :type action: str
    """
    icore = get_incident_core(db)
    incident = icore.generate(action)
    incident.set_location(pld.msg.guild)
    incident.set_moderator(pld.msg.author)
    incident.set_target(trg)
    incident.set_reason('Auto-Punished by Sigma')
    await icore.save(incident)
    icon = '🔊' if 'un' in action else '🔇'
    incident_embed = incident.to_embed(icon, 0x696969)
    await icore.report(pld.msg.guild, incident_embed)


async def auto_textmute(cmd, pld, target):
    """
    Auto-Textmutes a user and logs it appropriately.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :type pld: sigma.core.mechanics.payload.CommandPayload
    :type target: discord.Member
    """
    mute_list = pld.settings.get('muted_users') or []
    if target.id not in mute_list:
        await notify(pld, target, 'on', 'text-muted')
        mute_list.append(target.id)
        await cmd.db.set_guild_settings(pld.msg.guild.id, 'muted_users', mute_list)

        # importing locally to avoid function name confusion/overwrites
        from sigma.modules.moderation.messages.textmute import generate_log_embed
        # spoof the message author as Sigma (feels wrong but hey, it works)
        pld.msg.author = pld.msg.guild.me
        log_embed = generate_log_embed(pld.msg, target, 'Auto-Punished by Sigma')
        await log_event(cmd.bot, pld.settings, log_embed, 'log_mutes')


async def auto_hardmute(cmd, pld, target):
    """
    Auto-Hardmutes a user and logs it appropriately.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :type pld: sigma.core.mechanics.payload.CommandPayload
    :type target: discord.Member
    """
    await notify(pld, target, 'on', 'hard-muted')
    for channel in pld.msg.guild.channels:
        if isinstance(channel, discord.TextChannel) or isinstance(channel, discord.CategoryChannel):
            try:
                await channel.set_permissions(target, send_messages=False, add_reactions=False)
            except (discord.Forbidden, discord.NotFound):
                pass
    # importing locally to avoid function name confusion/overwrites
    from sigma.modules.moderation.punishments.hardmute import generate_log_embed
    # spoof the message author as Sigma (feels wrong but hey, it works)
    pld.msg.author = pld.msg.guild.me
    log_embed = generate_log_embed(pld.msg, target, 'Auto-Punished by Sigma')
    await log_event(cmd.bot, pld.settings, log_embed, 'log_mutes')


async def auto_kick(cmd, pld, target):
    """
    Auto-Kicks a user and logs it appropriately.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :type pld: sigma.core.mechanics.payload.CommandPayload
    :type target: discord.Member
    """
    await notify(pld, target, 'from', 'kicked')
    await target.kick(reason='Auto-Punished by Sigma')
    # importing locally to avoid function name confusion/overwrites
    from sigma.modules.moderation.punishments.kick import generate_log_embed
    # spoof the message author as Sigma (feels wrong but hey, it works)
    pld.msg.author = pld.msg.guild.me
    log_embed = generate_log_embed(pld.msg, target, 'Auto-Punished by Sigma')
    await log_event(cmd.bot, pld.settings, log_embed, 'log_kicks')


async def auto_softban(cmd, pld, target):
    """
    Auto-Softbans a user and logs it appropriately.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :type pld: sigma.core.mechanics.payload.CommandPayload
    :type target: discord.Member
    """
    await notify(pld, target, 'from', 'soft-banned')
    await target.ban(reason='Auto-Punished by Sigma', delete_message_days=1)
    await target.unban()
    # importing locally to avoid function name confusion/overwrites
    from sigma.modules.moderation.punishments.ban import generate_log_embed
    # spoof the message author as Sigma (feels wrong but hey, it works)
    pld.msg.author = pld.msg.guild.me
    log_embed = generate_log_embed(pld.msg, target, 'Auto-Punished by Sigma')
    await log_event(cmd.bot, pld.settings, log_embed, 'log_kicks')


async def auto_ban(cmd, pld, target):
    """
    Auto-Bans a user and logs it appropriately.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :type pld: sigma.core.mechanics.payload.CommandPayload
    :type target: discord.Member
    """
    await notify(pld, target, 'from', 'banned')
    await target.ban(reason='Auto-Punished by Sigma', delete_message_days=1)
    # importing locally to avoid function name confusion/overwrites
    from sigma.modules.moderation.punishments.ban import generate_log_embed
    # spoof the message author as Sigma (feels wrong but hey, it works)
    pld.msg.author = pld.msg.guild.me
    log_embed = generate_log_embed(pld.msg, target, 'Auto-Punished by Sigma')
    await log_event(cmd.bot, pld.settings, log_embed, 'log_kicks')


async def auto_punish(cmd, pld, target, action, duration):
    """
    Auto-Punishes a user in accordance with the guild's settings.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :type pld: sigma.core.mechanics.payload.CommandPayload
    :type target: discord.Member
    :type action: str
    :type duration: int or None
    """
    if pld.msg.guild:
        await make_incident(cmd.db, pld, target, action)
        action_funcs = {
            'textmute': auto_textmute,
            'hardmute': auto_hardmute,
            'kick': auto_kick,
            'softban': auto_softban,
            'ban': auto_ban
        }
        action_func = action_funcs.get(action)
        await action_func(cmd, pld, target)
        if duration:
            endstamp = arrow.get(arrow.utcnow().int_timestamp + duration).timestamp
            doc_data = {'server_id': pld.msg.guild.id, 'user_id': target.id, 'time': endstamp}
            await cmd.db.col[f'{action.title()}ClockworkDocs'].insert_one(doc_data)
