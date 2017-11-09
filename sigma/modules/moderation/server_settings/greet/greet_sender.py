import discord

from sigma.core.utilities.data_processing import movement_message_parser


async def greet_sender(ev, member):
    greet_active = ev.db.get_guild_settings(member.guild.id, 'Greet')
    if greet_active is True or greet_active is None:
        greet_dm = ev.db.get_guild_settings(member.guild.id, 'GreetDM')
        if greet_dm:
            target = member
        else:
            greet_channel_id = ev.db.get_guild_settings(member.guild.id, 'GreetChannel')
            if greet_channel_id is None:
                target = None
            else:
                target = discord.utils.find(lambda x: x.id == greet_channel_id, member.guild.channels)
        if target:
            current_greeting = ev.db.get_guild_settings(member.guild.id, 'GreetMessage')
            if current_greeting is None:
                current_greeting = 'Hello {user_mention}, welcome to {server_name}.'
            greeting_text = movement_message_parser(member, current_greeting)
            await target.send(greeting_text)
