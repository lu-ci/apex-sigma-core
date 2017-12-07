import discord

from sigma.core.utilities.data_processing import movement_message_parser


async def bye_sender(ev, member):
    bye_active = await ev.db.get_guild_settings(member.guild.id, 'Bye')
    if bye_active is True or bye_active is None:
        bye_channel_id = await ev.db.get_guild_settings(member.guild.id, 'ByeChannel')
        if bye_channel_id is None:
            target = None
        else:
            target = discord.utils.find(lambda x: x.id == bye_channel_id, member.guild.channels)
        if target:
            current_goodbye = await ev.db.get_guild_settings(member.guild.id, 'ByeMessage')
            if current_goodbye is None:
                current_goodbye = '{user_name} has left {server_name}.'
            goodbye_text = movement_message_parser(member, current_goodbye)
            await target.send(goodbye_text)
