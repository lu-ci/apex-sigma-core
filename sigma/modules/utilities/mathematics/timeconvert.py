import arrow
import discord


async def timeconvert(cmd, message, args):
    if args:
        conv_input = ' '.join(args).split('>')
        if len(conv_input) == 2:
            from_pieces = conv_input[0].split()
            if len(from_pieces) == 2:
                from_time = from_pieces[0]
                from_zone = from_pieces[1]
                to_zone = conv_input[1]
                from_string = f'{arrow.utcnow().format("YYYY-MM-DD")} {from_time}:00'
                from_arrow = arrow.get(arrow.get(from_string).datetime, from_zone)
                to_arrow = from_arrow.to(to_zone)
                time_out = to_arrow.format('YYYY-MM-DD HH:mm:ss (ZZ GMT)')
                response = discord.Embed(color=0x696969, title=f'🕥 {time_out}')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Invalid first argument.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Invalid input arguments.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)
