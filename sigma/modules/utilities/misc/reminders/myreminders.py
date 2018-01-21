from sigma.core.mechanics.command import SigmaCommand
import arrow
import discord

from sigma.core.utilities.data_processing import get_image_colors
from sigma.core.utilities.data_processing import user_avatar


async def myreminders(cmd: SigmaCommand, message: discord.Message, args: list):
    here = False
    if args:
        if args[-1].lower() == 'here':
            here = True
    if here:
        lookup_data = {'UserID': message.author.id, 'ChannelID': message.channel.id}
    else:
        lookup_data = {'UserID': message.author.id}
    all_reminders = cmd.db[cmd.db.db_cfg.database].Reminders.find(lookup_data)
    reminder_count = await all_reminders.count()
    all_reminders = await all_reminders.to_list(None)
    if reminder_count:
        if reminder_count == 1:
            ender = 'reminder'
        else:
            ender = 'reminders'
        if here:
            reminder_list_title = f'You have {reminder_count} pending {ender} in #{message.channel.name}.'
        else:
            reminder_list_title = f'You have {reminder_count} pending {ender}.'
        reminder_list = ''
        for reminder in all_reminders:
            human_time = arrow.get(reminder['ExecutionStamp']).humanize(arrow.utcnow())
            channel = discord.utils.find(lambda x: x.id == reminder['ChannelID'], cmd.bot.get_all_channels())
            if channel:
                chan_name = f'**#{channel.name}**'
                srv_name = f'**{channel.guild.name}**'
            else:
                chan_name = '*{No Channel}*'
                srv_name = '*{No Server}*'
            rem_id = reminder['ReminderID']
            reminder_list += f'\n`{rem_id}` in {chan_name} on {srv_name} {human_time}'
        strip_clr = await get_image_colors(user_avatar(message.author))
        response = discord.Embed(color=strip_clr)
        response.set_author(name=f'{message.author.display_name}\'s Reminders', icon_url=user_avatar(message.author))
        response.add_field(name='Reminder Count', value=reminder_list_title, inline=False)
        response.add_field(name='Reminder List', value=reminder_list, inline=False)
    else:
        response = discord.Embed(color=0x696969, title='🔍 You have no pending reminders.')
    await message.channel.send(embed=response)
