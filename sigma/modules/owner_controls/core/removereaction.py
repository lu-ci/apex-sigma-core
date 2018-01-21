from sigma.core.mechanics.command import SigmaCommand
import discord


async def removereaction(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        lookup = args[0].lower()
        interaction_item = await cmd.db[cmd.db.db_cfg.database].Interactions.find_one({'ReactionID': lookup})
        if interaction_item:
            await cmd.db[cmd.db.db_cfg.database].Interactions.delete_one(interaction_item)
            response = discord.Embed(color=0, title=f'🔥 Reaction `{lookup}` has been removed.')
        else:
            response = discord.Embed(color=0xBE1931, title=f'❗ Reaction not found.')
    else:
        response = discord.Embed(color=0xBE1931, title=f'❗ Nothing inputed.')
    await message.channel.send(embed=response)
