active_guilds = [138067606119645184, 200751504175398912, 198184144986046470]


async def just_monika(ev, message):
    if message.content:
        if message.guild:
            if message.guild.id in active_guilds:
                args = message.content.split()
                triggered = False
                for arg in args:
                    if arg.lower() in ['sayori', 'yuri', 'natsuki', 'natsu']:
                        triggered = True
                        break
                if triggered:
                    await message.channel.send('**JUST MONIKA** <:lcMonika:375975016359264257>')
