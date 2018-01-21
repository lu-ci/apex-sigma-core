import discord


async def wipeawards(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        uid = args[0]
        try:
            uid = int(uid)
        except ValueError:
            uid = None
        if uid:
            lookup = {'UserID': uid}
            collections = ['CurrencySystem', 'Cookies', 'ExperienceSystem', 'Inventory']
            for collection in collections:
                await cmd.db[cmd.db.db_cfg.database][collection].delete_one(lookup)
            target = discord.utils.find(lambda x: x.id == uid, cmd.bot.get_all_members())
            if target:
                unam = f'{target.name}#{target.discriminator}'
            else:
                unam = str(uid)
            response = discord.Embed(color=0x696969, title=f'🗑 Wiped {unam}\'s property.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Invalid Guild ID.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ No Guild ID was inputted.')
    await message.channel.send(embed=response)
