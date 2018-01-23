import secrets

import arrow
import discord

from sigma.core.utilities.data_processing import user_avatar


def convert_to_seconds(time_input):
    indent_list = time_input.split(':')
    if len(indent_list) == 3:
        output = (3600 * int(indent_list[0])) + (60 * int(indent_list[1]) + int(indent_list[2]))
    elif len(indent_list) == 2:
        output = (60 * int(indent_list[0]) + int(indent_list[1]))
    elif len(indent_list) == 1:
        output = int(indent_list[0])
    else:
        raise LookupError
    return output


async def remindme(cmd, message, args):
    if args:
        time_req = args[0]
        try:
            in_seconds = convert_to_seconds(time_req)
            upper_limit = 7776000
            if in_seconds <= upper_limit:
                rem_count = await cmd.db[cmd.db.db_cfg.database].Reminders.find({'UserID': message.author.id}).count()
                rem_limit = 15
                if rem_count < rem_limit:
                    if len(args) > 1:
                        text_message = ' '.join(args[1:])
                    else:
                        text_message = 'No reminder message set.'
                    execution_stamp = arrow.utcnow().timestamp + in_seconds
                    timestamp = arrow.get(execution_stamp).datetime
                    if in_seconds < 60:
                        time_diff = f'In {in_seconds} seconds'
                    else:
                        time_diff = arrow.get(execution_stamp + 5).humanize(arrow.utcnow())
                    reminder_id = secrets.token_hex(2)
                    reminder_data = {
                        'ReminderID': reminder_id,
                        'UserID': message.author.id,
                        'CreationStamp': arrow.utcnow().timestamp,
                        'ExecutionStamp': execution_stamp,
                        'ChannelID': message.channel.id,
                        'ServerID': message.guild.id,
                        'TextMessage': text_message
                    }
                    await cmd.db[cmd.db.db_cfg.database]['Reminders'].insert_one(reminder_data)
                    response = discord.Embed(color=0x66CC66, timestamp=timestamp)
                    response.description = text_message
                    response.set_author(name=f'Reminder {reminder_id} Created', icon_url=user_avatar(message.author))
                    response.set_footer(text=f'Executes: {time_diff.title()}')
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ You already have 15 reminders pending.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Reminders have a limit of 90 days.')
        except LookupError:
            response = discord.Embed(color=0xBE1931, title='❗ Please use the format HH:MM:SS.')
        except ValueError:
            response = discord.Embed(color=0xBE1931, title='❗ Inputted value is invalid.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ No arguments inputted.')
    await message.channel.send(embed=response)
