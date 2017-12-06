import discord


def count_votes(poll_file):
    vote_coll = {}
    for vote in poll_file['votes'].keys():
        vote_index = poll_file['votes'].get(vote)
        if vote_index in vote_coll:
            curr = vote_index.get(vote_coll)
        else:
            curr = 0
        curr += 1
        vote_coll.update({vote_index: curr})
    return vote_coll


def make_bar(points, total):
    fill = (points // total) * 10
    empty = 10 - fill
    bar = f'[{fill * "▣"}{empty * "▢"}]'
    return bar


async def shadowpollstats(cmd, message, args):
    if args:
        poll_id = args[0].lower()
        poll_file = cmd.db[cmd.db.db_cfg.database].ShadowPolls.find_one({'id': poll_id})
        if poll_file:
            author = poll_file['origin']['author']
            active = poll_file['settings']['active']
            visible = poll_file['settings']['visible']
            if author == message.author.id or visible:
                total = len(list(poll_file['votes']))
                vote_coll = count_votes(poll_file)
                loop_index = 0
                output = f'Total Votes: {total}'
                for option in poll_file['poll']['answers']:
                    loop_index += 1
                    if loop_index in vote_coll:
                        points = vote_coll.get(loop_index)
                    else:
                        points = 0
                    if len(option) > 10:
                        option = option[:7] + '...'
                    bar = make_bar(points, total)
                    stat_line = f'[8] {bar} {int((points / total) * 100)}% - {option}'
                    output += f'\n{stat_line}'
                response = discord.Embed(color=0xF9F9F9, title=f'📊 Poll {poll_id} Statistics.')
                response.description = f'```\n{output}\n```'
            else:
                response = discord.Embed(color=0xFFCC4D, title='🔒 You can\'t view this poll\'s stats.')
        else:
            response = discord.Embed(color=0x696969, title='🔍 I couldn\'t find that poll.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Missing poll ID.')
    await message.channel.send(embed=response)
