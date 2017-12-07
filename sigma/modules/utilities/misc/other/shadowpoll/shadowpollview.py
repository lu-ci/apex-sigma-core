import arrow
import discord

from sigma.core.utilities.data_processing import user_avatar


async def shadowpollview(cmd, message, args):
    if args:
        poll_id = ''.join(args).lower()
        poll_file = await cmd.db[cmd.db.db_cfg.database].ShadowPolls.find_one({'id': poll_id})
        if poll_file:
            active = poll_file['settings']['active']
            visible = poll_file['settings']['visible']
            author_id = poll_file['origin']['author']
            if active or visible or author_id == message.author.id:
                response = discord.Embed(color=0xF9F9F9, title=poll_file['poll']['question'])
                author = discord.utils.find(lambda x: x.id == author_id, cmd.bot.get_all_members())
                if author:
                    response.set_author(name=author.name, icon_url=user_avatar(author))
                else:
                    response.set_author(name=f'{author_id}', icon_url='https://i.imgur.com/QnYSlld.png')
                expiration = poll_file['settings']['expires']
                if expiration is not None:
                    exp_dt = arrow.get(expiration).datetime
                    exp_hum = arrow.get(expiration).humanize()
                    response.set_footer(text=f'Expires {exp_hum}')
                    response.timestamp = exp_dt
                else:
                    created = poll_file['created']
                    cre_dt = arrow.get(created).datetime
                    cre_hum = arrow.get(created).humanize()
                    response.set_footer(text=f'Created {cre_hum}')
                    response.timestamp = cre_dt
                loop_index = 0
                answer_lines = []
                for answer in poll_file['poll']['answers']:
                    loop_index += 1
                    answer_line = f'**{loop_index}**: {answer}'
                    answer_lines.append(answer_line)
                answers = '\n'.join(answer_lines)
                response.description = answers
            else:
                response = discord.Embed(color=0xFFCC4D, title='🔒 That poll is not active.')
        else:
            response = discord.Embed(color=0x696969, title='🔍 I couldn\'t find that poll.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ No poll ID given.')
    await message.channel.send(embed=response)
