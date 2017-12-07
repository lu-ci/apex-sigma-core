import arrow
import discord

from sigma.core.utilities.data_processing import user_avatar


async def reminderinfo(cmd, message, args):
    if args:
        rem_id = args[0].lower()
        lookup_data = {'UserID': message.author.id, 'ReminderID': rem_id}
        reminder = await cmd.db[cmd.db.db_cfg.database].Reminders.find_one(lookup_data)
        if reminder:
            execution_stamp = reminder['ExecutionStamp']
            text_message = reminder['TextMessage']
            timestamp = arrow.get(execution_stamp).datetime
            human_time = arrow.get(execution_stamp).humanize(arrow.utcnow())
            auth_title = f'{message.author.display_name}\'s Reminder: {rem_id}'
            channel = discord.utils.find(lambda x: x.id == reminder['ChannelID'], cmd.bot.get_all_channels())
            if channel:
                chan_name = f'**#{channel.name}**'
                srv_name = f'**{channel.guild.name}**'
            else:
                chan_name = '*{No Channel}*'
                srv_name = '*{No Server}*'
            location_text = f'Executes in {chan_name} on {srv_name} {human_time}.'
            response = discord.Embed(color=0x66CC66, timestamp=timestamp)
            response.add_field(name='🏛 Location', value=location_text, inline=False)
            response.add_field(name='🗒 Reminder Text', value=text_message, inline=False)
            response.set_author(name=auth_title, icon_url=user_avatar(message.author))
        else:
            response = discord.Embed(color=0x696969, title=f'🔍 Reminder `{rem_id}` not found.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ No reminder ID inputted.')
    await message.channel.send(embed=response)
