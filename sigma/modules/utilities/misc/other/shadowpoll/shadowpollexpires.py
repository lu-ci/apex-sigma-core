import arrow
import discord

from sigma.modules.utilities.misc.reminders.remindme import convert_to_seconds


async def shadowpollexpires(cmd, message, args):
    if args:
        if len(args) == 2:
            poll_id = args[0].lower()
            time_input = args[1]
            try:
                exp_in = convert_to_seconds(time_input)
            except ValueError:
                exp_in = None
            except LookupError:
                exp_in = None
            if exp_in:
                poll_file = await cmd.db[cmd.db.db_cfg.database].ShadowPolls.find_one({'id': poll_id})
                if poll_file:
                    if poll_file['origin']['author'] == message.author.id:
                        end_stamp = arrow.utcnow().float_timestamp + exp_in
                        end_human = arrow.get(end_stamp).humanize()
                        end_datet = arrow.get(end_stamp).datetime
                        poll_file['settings'].update({'expires': end_stamp})
                        poll_coll = cmd.db[cmd.db.db_cfg.database].ShadowPolls
                        await poll_coll.update_one({'id': poll_id}, {'$set': poll_file})
                        title = f'⏰ Poll set to expire {end_human}.'
                        response = discord.Embed(color=0xff3333, title=title, timestamp=end_datet)
                    else:
                        response = discord.Embed(color=0xBE1931, title='⛔ You didn\'t make this poll.')
                else:
                    response = discord.Embed(color=0x696969, title='🔍 I couldn\'t find that poll.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Invalid time input.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Missing arguments.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Missing poll ID and expiration time.')
    await message.channel.send(embed=response)
