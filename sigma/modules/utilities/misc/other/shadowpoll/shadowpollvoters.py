import discord


async def shadowpollvoters(cmd, message, args):
    if args:
        poll_id = args[0].lower()
        poll_file = cmd.db[cmd.db.db_cfg.database].ShadowPolls.find_one({'id': poll_id})
        if poll_file:
            author = poll_file['origin']['author']
            if author == message.author.id:
                votes = poll_file['votes']
                if votes:
                    response = discord.Embed(color=0xF9F9F9, title=f'📨 Poll {poll_id} Voters')
                    voter_lines = []
                    members = cmd.bot.get_all_members()
                    options_dict = {}
                    loop_index = 0
                    for option in poll_file['poll']['answers']:
                        loop_index += 1
                        options_dict.update({loop_index: option})
                    for voter_id in poll_file['votes'].keys():
                        voter_id = int(voter_id)
                        voter = discord.utils.find(lambda x: x.id == voter_id, members)
                        voter_choice = options_dict.get(poll_file['votes'].get(str(voter_id)))
                        if voter:
                            voter_line = f'{voter.name}#{voter.discriminator} - {voter_choice}'
                        else:
                            voter_line = f'{voter_id} - {voter_choice}'
                        voter_lines.append(voter_line)
                    response.description = '\n'.join(voter_lines)
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ Nobody voted yet.')
            else:
                response = discord.Embed(color=0xBE1931, title='⛔ You didn\'t make this poll.')
        else:
            response = discord.Embed(color=0x696969, title='🔍 I couldn\'t find that poll.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Missing poll ID.')
    await message.channel.send(embed=response)
